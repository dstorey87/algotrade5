import logging
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from fastapi import APIRouter, Depends, HTTPException, Query, WebSocket, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.http import HTTPBasic, HTTPBasicCredentials

from freqtrade.rpc.api_server.api_schemas import AccessAndRefreshToken, AccessToken
from freqtrade.rpc.api_server.deps import get_api_config


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)

ALGORITHM = "HS256"

router_login = APIRouter()


def verify_auth(api_config, username: str, password: str):
    """Verify username/password"""
    return secrets.compare_digest(username, api_config.get("username")) and secrets.compare_digest(
        password, api_config.get("password")
    )


httpbasic = HTTPBasic(auto_error=False)
security = HTTPBasic()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


def get_user_from_token(token, secret_key: str, token_type: str = "access") -> str:  # noqa: S107
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        username: str = payload.get("identity", {}).get("u")
        if username is None:
            raise credentials_exception
        if payload.get("type") != token_type:
            raise credentials_exception

    except jwt.PyJWTError:
        raise credentials_exception
    return username


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


def create_token(data: dict, secret_key: str, token_type: str = "access") -> str:  # noqa: S107
    to_encode = data.copy()
    if token_type == "access":  # noqa: S105
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    elif token_type == "refresh":  # noqa: S105
        expire = datetime.now(timezone.utc) + timedelta(days=30)
    else:
        raise ValueError()
    to_encode.update(
        {
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            "type": token_type,
        }
    )
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt


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
def token_login(
    form_data: HTTPBasicCredentials = Depends(security), api_config=Depends(get_api_config)
):
    if verify_auth(api_config, form_data.username, form_data.password):
        token_data = {"identity": {"u": form_data.username}}
        access_token = create_token(
            token_data,
            api_config.get("jwt_secret_key", "super-secret"),
            token_type="access",  # noqa: S106
        )
        refresh_token = create_token(
            token_data,
            api_config.get("jwt_secret_key", "super-secret"),
            token_type="refresh",  # noqa: S106
        )
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )


# REMOVED_UNUSED_CODE: @router_login.post("/token/refresh", response_model=AccessToken)
def token_refresh(token: str = Depends(oauth2_scheme), api_config=Depends(get_api_config)):
    # Refresh token
    u = get_user_from_token(token, api_config.get("jwt_secret_key", "super-secret"), "refresh")
    token_data = {"identity": {"u": u}}
    access_token = create_token(
        token_data,
        api_config.get("jwt_secret_key", "super-secret"),
        token_type="access",  # noqa: S106
    )
    return {"access_token": access_token}
