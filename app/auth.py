"""CP3 — Xác thực bằng API key.

Public URL = ai cũng gọi được. Không có lớp này, hóa đơn LLM của bạn do
người lạ quyết định.
"""

from __future__ import annotations

import secrets

from fastapi import Header, HTTPException, status

from .config import get_settings

ANONYMOUS_USER = "anonymous"


def verify_api_key(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    x_user_id: str | None = Header(default=None, alias="X-User-Id"),
) -> str:
    """Kiểm tra header ``X-API-Key``; trả về user_id nếu hợp lệ.

    So sánh bằng ``secrets.compare_digest`` để không rò rỉ thông tin khóa
    qua thời gian phản hồi. Request hợp lệ được gắn với user id hoặc
    ``ANONYMOUS_USER`` nếu header user id không được gửi.
    """
    expected = get_settings().agent_api_key
    if x_api_key is None or not secrets.compare_digest(x_api_key, expected):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid or missing API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    return x_user_id or ANONYMOUS_USER
