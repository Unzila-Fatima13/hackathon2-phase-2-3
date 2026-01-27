from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Any
from database.database import get_session
from models.user import UserCreate
from services.user_service import UserService
from schemas.user import UserPublic, UserLogin, Token
from auth.jwt_handler import create_access_token, create_refresh_token
from auth.middleware import get_current_user_id
from datetime import timedelta

router = APIRouter()

@router.post("/register", response_model=UserPublic)
def register_user(user: UserCreate, session: Session = Depends(get_session)) -> Any:
    """Register a new user"""
    try:
        db_user = UserService.create_user(session=session, user_create=user)
        return db_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the user: {str(e)}"
        )


@router.post("/login", response_model=Token)
def login_user(user_login: UserLogin, session: Session = Depends(get_session)) -> Any:
    """Authenticate user and return JWT tokens"""
    user = UserService.authenticate_user(
        session=session,
        email=user_login.email,
        password=user_login.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    # Create refresh token
    refresh_token_expires = timedelta(days=30)
    refresh_token = create_refresh_token(
        data={"sub": str(user.id)}, expires_delta=refresh_token_expires
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/logout")
def logout_user() -> Any:
    """Logout user (client-side token invalidation)"""
    # In a real implementation, you might want to add tokens to a blacklist
    # For now, we just return a success message
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserPublic)
def get_current_user(
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> Any:
    """Get current authenticated user's information"""
    user = UserService.get_user_by_id(session=session, user_id=current_user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


from pydantic import BaseModel

class TokenRefreshRequest(BaseModel):
    refresh_token: str

@router.post("/refresh", response_model=Token)
def refresh_token(request: TokenRefreshRequest) -> Any:
    """Refresh the access token using a refresh token"""
    from auth.jwt_handler import verify_token

    try:
        # Extract refresh token from the request body
        refresh_token_str = request.refresh_token
        if not refresh_token_str:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Refresh token is required"
            )

        # Verify the refresh token
        payload = verify_token(refresh_token_str, "refresh")
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        # Create new access token
        from datetime import timedelta
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": user_id}, expires_delta=access_token_expires
        )

        # Create new refresh token (optional: rotate refresh tokens)
        refresh_token_expires = timedelta(days=30)
        new_refresh_token = create_refresh_token(
            data={"sub": user_id}, expires_delta=refresh_token_expires
        )

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not refresh token"
        )