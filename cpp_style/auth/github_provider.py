"""
GitHub OAuth 代理提供者

将 MCP OAuth 流程代理到 GitHub，实现 GitHub 账号登录授权。
流程：MCP 客户端 → /authorize → GitHub → /oauth/callback → MCP 客户端
"""

import secrets
import time
from urllib.parse import urlencode

import httpx

from mcp.server.auth.provider import (
    AccessToken,
    AuthorizationCode,
    AuthorizationParams,
    RefreshToken,
    construct_redirect_uri,
)
from mcp.shared.auth import OAuthClientInformationFull, OAuthToken


class GitHubOAuthProvider:
    """GitHub OAuth 代理提供者，将 MCP 授权请求转发到 GitHub"""

    GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
    GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"

    def __init__(self, github_client_id: str, github_client_secret: str, mcp_server_url: str):
        self.github_client_id = github_client_id
        self.github_client_secret = github_client_secret
        self.mcp_server_url = mcp_server_url.rstrip("/")

        # 内存存储（服务重启后失效，如需持久化请换用数据库）
        self._clients: dict[str, OAuthClientInformationFull] = {}
        self._pending_auths: dict[str, dict] = {}  # github_state -> 待处理认证数据
        self._auth_codes: dict[str, AuthorizationCode] = {}
        self._access_tokens: dict[str, AccessToken] = {}
        self._refresh_tokens: dict[str, RefreshToken] = {}

    # ---------- 客户端注册 ----------

    async def get_client(self, client_id: str) -> OAuthClientInformationFull | None:
        return self._clients.get(client_id)

    async def register_client(self, client_info: OAuthClientInformationFull) -> None:
        self._clients[client_info.client_id] = client_info

    # ---------- 授权流程 ----------

    async def authorize(self, client: OAuthClientInformationFull, params: AuthorizationParams) -> str:
        """重定向到 GitHub OAuth 授权页面"""
        github_state = secrets.token_urlsafe(32)

        # 保存 MCP 请求的上下文，等 GitHub 回调时恢复
        self._pending_auths[github_state] = {
            "client_id": client.client_id,
            "redirect_uri": str(params.redirect_uri),
            "code_challenge": params.code_challenge,
            "scopes": params.scopes or [],
            "mcp_state": params.state,
            "redirect_uri_provided_explicitly": params.redirect_uri_provided_explicitly,
        }

        github_params = {
            "client_id": self.github_client_id,
            "redirect_uri": f"{self.mcp_server_url}/oauth/callback",
            "scope": "read:user",
            "state": github_state,
        }
        return f"{self.GITHUB_AUTHORIZE_URL}?{urlencode(github_params)}"

    async def handle_github_callback(self, code: str, state: str) -> str:
        """
        处理 GitHub 回调，生成 MCP 授权码，返回重定向到 MCP 客户端的 URL
        由 /oauth/callback 路由调用
        """
        pending = self._pending_auths.pop(state, None)
        if not pending:
            raise ValueError("无效或已过期的 state 参数")

        # 向 GitHub 换取 access token
        async with httpx.AsyncClient() as http:
            resp = await http.post(
                self.GITHUB_TOKEN_URL,
                data={
                    "client_id": self.github_client_id,
                    "client_secret": self.github_client_secret,
                    "code": code,
                    "redirect_uri": f"{self.mcp_server_url}/oauth/callback",
                },
                headers={"Accept": "application/json"},
            )
            token_data = resp.json()

        if "error" in token_data:
            raise ValueError(
                f"GitHub OAuth 错误: {token_data.get('error_description', token_data['error'])}"
            )

        # 生成 MCP 授权码（至少 128 bits 熵，符合 RFC 6749 §10.10）
        auth_code = secrets.token_urlsafe(32)
        self._auth_codes[auth_code] = AuthorizationCode(
            code=auth_code,
            client_id=pending["client_id"],
            scopes=pending["scopes"],
            code_challenge=pending["code_challenge"],
            redirect_uri=pending["redirect_uri"],  # type: ignore[arg-type]
            redirect_uri_provided_explicitly=pending["redirect_uri_provided_explicitly"],
            expires_at=time.time() + 300,  # 5 分钟有效期
        )

        # 重定向回 MCP 客户端
        return construct_redirect_uri(
            pending["redirect_uri"],
            code=auth_code,
            state=pending["mcp_state"],
        )

    # ---------- 授权码换 Token ----------

    async def load_authorization_code(
        self, client: OAuthClientInformationFull, authorization_code: str
    ) -> AuthorizationCode | None:
        code = self._auth_codes.get(authorization_code)
        if code and code.expires_at > time.time():
            return code
        return None

    async def exchange_authorization_code(
        self, client: OAuthClientInformationFull, authorization_code: AuthorizationCode
    ) -> OAuthToken:
        self._auth_codes.pop(authorization_code.code, None)

        access_token = secrets.token_urlsafe(32)
        refresh_token_str = secrets.token_urlsafe(32)
        expires_at = int(time.time()) + 3600  # 1 小时

        self._access_tokens[access_token] = AccessToken(
            token=access_token,
            client_id=client.client_id,
            scopes=authorization_code.scopes,
            expires_at=expires_at,
        )
        self._refresh_tokens[refresh_token_str] = RefreshToken(
            token=refresh_token_str,
            client_id=client.client_id,
            scopes=authorization_code.scopes,
        )

        return OAuthToken(
            access_token=access_token,
            token_type="bearer",
            expires_in=3600,
            refresh_token=refresh_token_str,
            scope=" ".join(authorization_code.scopes),
        )

    # ---------- Refresh Token ----------

    async def load_refresh_token(
        self, client: OAuthClientInformationFull, refresh_token: str
    ) -> RefreshToken | None:
        token = self._refresh_tokens.get(refresh_token)
        if token and token.client_id == client.client_id:
            return token
        return None

    async def exchange_refresh_token(
        self,
        client: OAuthClientInformationFull,
        refresh_token: RefreshToken,
        scopes: list[str],
    ) -> OAuthToken:
        self._refresh_tokens.pop(refresh_token.token, None)

        # 吊销该客户端的旧 access token
        for t in list(self._access_tokens.values()):
            if t.client_id == client.client_id:
                del self._access_tokens[t.token]

        use_scopes = scopes or refresh_token.scopes
        access_token = secrets.token_urlsafe(32)
        new_refresh_str = secrets.token_urlsafe(32)
        expires_at = int(time.time()) + 3600

        self._access_tokens[access_token] = AccessToken(
            token=access_token,
            client_id=client.client_id,
            scopes=use_scopes,
            expires_at=expires_at,
        )
        self._refresh_tokens[new_refresh_str] = RefreshToken(
            token=new_refresh_str,
            client_id=client.client_id,
            scopes=use_scopes,
        )

        return OAuthToken(
            access_token=access_token,
            token_type="bearer",
            expires_in=3600,
            refresh_token=new_refresh_str,
            scope=" ".join(use_scopes),
        )

    # ---------- Token 验证与吊销 ----------

    async def load_access_token(self, token: str) -> AccessToken | None:
        at = self._access_tokens.get(token)
        if at and (at.expires_at is None or at.expires_at > time.time()):
            return at
        return None

    async def revoke_token(self, token: AccessToken | RefreshToken) -> None:
        if isinstance(token, AccessToken):
            self._access_tokens.pop(token.token, None)
        else:
            self._refresh_tokens.pop(token.token, None)
