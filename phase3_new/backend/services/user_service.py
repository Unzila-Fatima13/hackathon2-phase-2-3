from sqlmodel import Session, select
from typing import Optional
from models.user import User, UserCreate
from schemas.user import UserPublic
from auth.jwt_handler import hash_password, verify_password
from fastapi import HTTPException, status

class UserService:
    @staticmethod
    def create_user(*, session: Session, user_create: UserCreate) -> User:
        """Create a new user with hashed password"""
        # Check if user with this email already exists
        existing_user = session.exec(select(User).where(User.email == user_create.email)).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists"
            )

        # Hash the password (with automatic truncation if needed)
        hashed_password = hash_password(user_create.password)

        # Create the user
        db_user = User(
            email=user_create.email,
            password_hash=hashed_password
        )

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return db_user

    @staticmethod
    def authenticate_user(*, session: Session, email: str, password: str) -> Optional[User]:
        """Authenticate a user by email and password"""
        user = session.exec(select(User).where(User.email == email)).first()

        if not user or not verify_password(password, user.password_hash):
            return None

        return user

    @staticmethod
    def get_user_by_email(*, session: Session, email: str) -> Optional[User]:
        """Get a user by email"""
        return session.exec(select(User).where(User.email == email)).first()

    @staticmethod
    def get_user_by_id(*, session: Session, user_id: str) -> Optional[User]:
        """Get a user by ID"""
        import uuid
        try:
            # Convert the string ID to UUID format for proper lookup
            user_uuid = uuid.UUID(user_id)
            return session.get(User, user_uuid)
        except ValueError:
            # If conversion fails, try with original string
            return session.get(User, user_id)