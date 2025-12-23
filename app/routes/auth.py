from typing import Optional

from urllib.parse import urlparse

from fastapi import APIRouter, Depends, Query, Request, HTTPException
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session

from app.core.auth import oauth
from app.core.security import create_guest_token
from app.database import get_db
from app.models.users import Guest

router = APIRouter(prefix='/auth/google', tags=['Google OAuth'])

# Login to redirect user
@router.get('/login')
async def google_login(
    request: Request,
     redirect: Optional[str] = Query(
        default=None,
        description="Frontend URL to redirect to after successful login",
        example="http://127.0.0.1:5173/dashboard",
    ),
    ):
    callback_url = request.url_for('google_callback')

    return await oauth.google.authorize_redirect(
        request,
        callback_url,
        state=redirect,
    )


# callback from google
@router.get("/callback",  response_class=RedirectResponse,)
async def google_callback(
    request: Request,
    db: Session = Depends(get_db)
):

    # Fetch token from Google
    response_token = await oauth.google.authorize_access_token(request)

    # Get user info
    user_info = response_token.get("userinfo")
    if user_info is None:
        raise HTTPException(
            status_code=400, detail="Unable to get user info"
        )

    google_id = user_info['sub']
    email = user_info.get('email')
    full_name = user_info.get('name')
    avatar_url = user_info.get('picture')

    guest = db.query(Guest).filter(Guest.google_id == google_id).first()

    if not guest:
        guest = Guest(
            google_id=google_id,
            email=email,
            full_name=full_name,
            avater_url=avatar_url,
        )
        db.add(guest)
        db.commit()
        db.refresh(guest)

    access_token = create_guest_token(guest)

    state = request.query_params.get("state")

    # Default fallback (safety)
    frontend_redirect = "http://127.0.0.1:5173"

    if state:
        parsed = urlparse(state)

        # Whitelist allowed redirect hosts
        if (
            parsed.scheme in ("http", "https")
            and parsed.hostname in {
                "localhost",
                "127.0.0.1",
            }
        ):
            frontend_redirect = state

    response = RedirectResponse(url=frontend_redirect)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 24,  # 1 day
    )

    return response