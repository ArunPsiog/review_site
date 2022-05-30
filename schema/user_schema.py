from pydantic import Field, BaseModel
from beanie import Document


class User(Document):

    """
        Schema design for User with attributes
        1. name
        2. email
        3. password
        4. isActive
        5. isSuperUser
    """

    name: str = Field(
        ...,
        title="User name",
        description="Enter your name"
    )
    email:str = Field(
        ...,
        regex=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
        title="Email",
        description="Enter your email id"
    )
    password: str = Field(
        ...,
        regex=r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$",
        title="Password",
        description=" Enter password",
        
    )
    isActive: bool = True
    isSuperUser: bool = False


    class Config:
        schema_extra = {
            "example": {
                "name": "Arun Mukesh",
                "email": "arun.mukesh@dms.in",
                "password": "Sam@123456",
            }
        }


class ResUser(BaseModel):
    """
        ODM model for user's resonse
    """
    name: str
    email:str
    isActive: bool
    isSuperUser: bool