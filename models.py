from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Column, VARCHAR # type: ignore

class UserCreate(SQLModel):
    name: str = Field(min_length=3, max_length=50, description = "name of the user", schema_extra={'example': 'A very nice item'}, title= "Name")
    email: EmailStr = Field(sa_column=Column('email', VARCHAR, unique=True, index=True))
    password: str = Field(min_length=8, max_lenth=100, description="Password of user", title='password')
    age: int = Field(min_length=1, max_lenth=3, description="Age of user", title='Age')
    
# Assuming User is a SQLModel class
class User(UserCreate, table=True):
    id: int = Field(default=None, primary_key=True)
   
class UserLogin(SQLModel):
    email: EmailStr = Field(description="Email of the user")
    password: str = Field(min_length=8, max_length=100, description="Password of the user", title="Password")