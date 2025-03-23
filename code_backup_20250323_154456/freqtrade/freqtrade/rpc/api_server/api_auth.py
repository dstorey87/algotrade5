import logging
import secrets
from datetime import datetime, timedelta, timezone
# REMOVED_UNUSED_CODE: from typing import Any

import jwt
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from fastapi import APIRouter, Depends, HTTPException, Query, WebSocket, status
from fastapi.security import OAuth2PasswordBearer
# REMOVED_UNUSED_CODE: from fastapi.security.http import HTTPBasic, HTTPBasicCredentials

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.rpc.api_server.api_schemas import AccessAndRefreshToken, AccessToken
# REMOVED_UNUSED_CODE: from freqtrade.rpc.api_server.deps import get_api_config


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)

ALGORITHM = "HS256"

# REMOVED_UNUSED_CODE: router_login = APIRouter()


# REMOVED_UNUSED_CODE: def verify_auth(api_config, username: str, password: str):
# REMOVED_UNUSED_CODE:     """Verify username/password"""
# REMOVED_UNUSED_CODE:     return secrets.compare_digest(username, api_config.get("username")) and secrets.compare_digest(
# REMOVED_UNUSED_CODE:         password, api_config.get("password")
# REMOVED_UNUSED_CODE:     )


# REMOVED_UNUSED_CODE: httpbasic = HTTPBasic(auto_error=False)
# REMOVED_UNUSED_CODE: security = HTTPBasic()
# REMOVED_UNUSED_CODE: oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


# REMOVED_UNUSED_CODE: def get_user_from_token(token, secret_key: str, token_type: str = "access") -> str:  # noqa: S107
# REMOVED_UNUSED_CODE:     credentials_exception = HTTPException(
# REMOVED_UNUSED_CODE:         status_code=status.HTTP_401_UNAUTHORIZED,
# REMOVED_UNUSED_CODE:         detail="Could not validate credentials",
# REMOVED_UNUSED_CODE:         headers={"WWW-Authenticate": "Bearer"},
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     try:
# REMOVED_UNUSED_CODE:         payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
# REMOVED_UNUSED_CODE:         username: str = payload.get("identity", {}).get("u")
# REMOVED_UNUSED_CODE:         if username is None:
# REMOVED_UNUSED_CODE:             raise credentials_exception
# REMOVED_UNUSED_CODE:         if payload.get("type") != token_type:
# REMOVED_UNUSED_CODE:             raise credentials_exception
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     except jwt.PyJWTError:
# REMOVED_UNUSED_CODE:         raise credentials_exception
# REMOVED_UNUSED_CODE:     return username


# This should be reimplemented to better realign with the existing tools provided
# by FastAPI regarding API Tokens
# https://github.com/tiangolo/fastapi/blob/master/fastapi/security/api_key.py
# REMOVED_UNUSED_CODE: async def validate_ws_token(
# REMOVED_UNUSED_CODE:     ws: WebSocket,
# REMOVED_UNUSED_CODE:     ws_token: str | None = Query(default=None, alias="token"),
# REMOVED_UNUSED_CODE:     api_config: dict[str, Any] = Depends(get_api_config),
# REMOVED_UNUSED_CODE: ):
# REMOVED_UNUSED_CODE:     secret_ws_token = api_config.get("ws_token", None)
# REMOVED_UNUSED_CODE:     secret_jwt_key = api_config.get("jwt_secret_key", "super-secret")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Check if ws_token is/in secret_ws_token
# REMOVED_UNUSED_CODE:     if ws_token and secret_ws_token:
# REMOVED_UNUSED_CODE:         is_valid_ws_token = False
# REMOVED_UNUSED_CODE:         if isinstance(secret_ws_token, str):
# REMOVED_UNUSED_CODE:             is_valid_ws_token = secrets.compare_digest(secret_ws_token, ws_token)
# REMOVED_UNUSED_CODE:         elif isinstance(secret_ws_token, list):
# REMOVED_UNUSED_CODE:             is_valid_ws_token = any(
# REMOVED_UNUSED_CODE:                 [secrets.compare_digest(potential, ws_token) for potential in secret_ws_token]
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if is_valid_ws_token:
# REMOVED_UNUSED_CODE:             return ws_token
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Check if ws_token is a JWT
# REMOVED_UNUSED_CODE:     try:
# REMOVED_UNUSED_CODE:         user = get_user_from_token(ws_token, secret_jwt_key)
# REMOVED_UNUSED_CODE:         return user
# REMOVED_UNUSED_CODE:     # If the token is a jwt, and it's valid return the user
# REMOVED_UNUSED_CODE:     except HTTPException:
# REMOVED_UNUSED_CODE:         pass
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # If it doesn't match, close the websocket connection
# REMOVED_UNUSED_CODE:     await ws.close(code=status.WS_1008_POLICY_VIOLATION)


# REMOVED_UNUSED_CODE: def create_token(data: dict, secret_key: str, token_type: str = "access") -> str:  # noqa: S107
# REMOVED_UNUSED_CODE:     to_encode = data.copy()
# REMOVED_UNUSED_CODE:     if token_type == "access":  # noqa: S105
# REMOVED_UNUSED_CODE:         expire = datetime.now(timezone.utc) + timedelta(minutes=15)
# REMOVED_UNUSED_CODE:     elif token_type == "refresh":  # noqa: S105
# REMOVED_UNUSED_CODE:         expire = datetime.now(timezone.utc) + timedelta(days=30)
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         raise ValueError()
# REMOVED_UNUSED_CODE:     to_encode.update(
# REMOVED_UNUSED_CODE:         {
# REMOVED_UNUSED_CODE:             "exp": expire,
# REMOVED_UNUSED_CODE:             "iat": datetime.now(timezone.utc),
# REMOVED_UNUSED_CODE:             "type": token_type,
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
# REMOVED_UNUSED_CODE:     return encoded_jwt


# REMOVED_UNUSED_CODE: def http_basic_or_jwt_token(
# REMOVED_UNUSED_CODE:     form_data: HTTPBasicCredentials = Depends(httpbasic),
# REMOVED_UNUSED_CODE:     token: str = Depends(oauth2_scheme),
# REMOVED_UNUSED_CODE:     api_config=Depends(get_api_config),
# REMOVED_UNUSED_CODE: ):
# REMOVED_UNUSED_CODE:     if token:
# REMOVED_UNUSED_CODE:         return get_user_from_token(token, api_config.get("jwt_secret_key", "super-secret"))
# REMOVED_UNUSED_CODE:     elif form_data and verify_auth(api_config, form_data.username, form_data.password):
# REMOVED_UNUSED_CODE:         return form_data.username
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     raise HTTPException(
# REMOVED_UNUSED_CODE:         status_code=status.HTTP_401_UNAUTHORIZED,
# REMOVED_UNUSED_CODE:         detail="Unauthorized",
# REMOVED_UNUSED_CODE:     )


# REMOVED_UNUSED_CODE: @router_login.post("/token/login", response_model=AccessAndRefreshToken)
# REMOVED_UNUSED_CODE: def token_login(
# REMOVED_UNUSED_CODE:     form_data: HTTPBasicCredentials = Depends(security), api_config=Depends(get_api_config)
# REMOVED_UNUSED_CODE: ):
# REMOVED_UNUSED_CODE:     if verify_auth(api_config, form_data.username, form_data.password):
# REMOVED_UNUSED_CODE:         token_data = {"identity": {"u": form_data.username}}
# REMOVED_UNUSED_CODE:         access_token = create_token(
# REMOVED_UNUSED_CODE:             token_data,
# REMOVED_UNUSED_CODE:             api_config.get("jwt_secret_key", "super-secret"),
# REMOVED_UNUSED_CODE:             token_type="access",  # noqa: S106
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         refresh_token = create_token(
# REMOVED_UNUSED_CODE:             token_data,
# REMOVED_UNUSED_CODE:             api_config.get("jwt_secret_key", "super-secret"),
# REMOVED_UNUSED_CODE:             token_type="refresh",  # noqa: S106
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         return {
# REMOVED_UNUSED_CODE:             "access_token": access_token,
# REMOVED_UNUSED_CODE:             "refresh_token": refresh_token,
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         raise HTTPException(
# REMOVED_UNUSED_CODE:             status_code=status.HTTP_401_UNAUTHORIZED,
# REMOVED_UNUSED_CODE:             detail="Incorrect username or password",
# REMOVED_UNUSED_CODE:         )


# REMOVED_UNUSED_CODE: @router_login.post("/token/refresh", response_model=AccessToken)
# REMOVED_UNUSED_CODE: def token_refresh(token: str = Depends(oauth2_scheme), api_config=Depends(get_api_config)):
# REMOVED_UNUSED_CODE:     # Refresh token
# REMOVED_UNUSED_CODE:     u = get_user_from_token(token, api_config.get("jwt_secret_key", "super-secret"), "refresh")
# REMOVED_UNUSED_CODE:     token_data = {"identity": {"u": u}}
# REMOVED_UNUSED_CODE:     access_token = create_token(
# REMOVED_UNUSED_CODE:         token_data,
# REMOVED_UNUSED_CODE:         api_config.get("jwt_secret_key", "super-secret"),
# REMOVED_UNUSED_CODE:         token_type="access",  # noqa: S106
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     return {"access_token": access_token}
