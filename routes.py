from fastapi import APIRouter, HTTPException
# from app import crud, dependencies
from models import User, UserCreate
from database import get_user, register_user
from passlib.context import CryptContext # type: ignore
from sqlmodel import SQLModel, Field, Session, create_engine, select
from fastapi import HTTPException, APIRouter
from passlib.context import CryptContext



# Create a new router
router = APIRouter()

# Create a password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create a database engine
engine = create_engine("sqlite:///database.db")

@router.post("/", response_model=User)
async def create_user(user: UserCreate):
    """Create a new user."""
    with Session(engine) as session:
        # Check if email already exists
        statement = select(User).where(User.email == user.email)
        results = session.exec(statement)
        existing_user = results.first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already exists")
        
        # Hash the user's password
        hashed_password = pwd_context.hash(user.password)
        
        # Create a new user instance
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        
        # Add the new user to the session and commit
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        
        return db_user
