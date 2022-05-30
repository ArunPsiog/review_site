from datetime import timedelta
from typing import Dict, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


from schema.user_schema import User, ResUser
from config.utils import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES,ALGORITHM, verify_password,get_password_hash,\
                        decode_hash,create_access_token, decodeJWT, create_token

from config.auth_bearer import JWTBearer
from beanie.operators import Set

routes:APIRouter = APIRouter()
oauth2_scheme:OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")


# def create_token(user: User) -> Dict:
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.name}, expires_delta=access_token_expi
#     )
#     return {"access_token": access_token, "token_type": "bearer"}

@routes.post('/signup', response_model= Dict)
async def create(user:User) -> Dict:
    """
        Create new user 
    """
    user.password = get_password_hash(password=user.password)
    new_user: User = await user.create()
    return create_token(user= new_user)


@routes.get('/all_users',response_model=List[User],)
async def get_all_users(payload: Dict = Depends(JWTBearer())) -> List[ResUser]:
    """
        Get all users
    """
    user = await User.find_one({'name': payload['sub']})
    if user.isSuperUser:
        return await User.find_all().to_list()
    raise HTTPException(status_code=403, detail={"error":"Only super user can view all users"})


@routes.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Dict:
    """
        Generate token for exisiting User using Oauth2
    """
    try:
        user = await User.find_one(User.name == form_data.username)
        return create_token(user= user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")


@routes.post('/update', )
async def update(
    payload: Dict = Depends(JWTBearer()),
    updated_data: User = Body(...,)
) :
    """
        Generate token for exisiting User using Oauth2
    """
    try:
        await User.find_one(User.name == payload['sub']).update(Set(
            {
                User.email: updated_data.email, 
                User.password: "sam"
            })
        )
        return await User.find_one(User.name == payload['sub'])
        
    except Exception as e:
        raise HTTPException(status_code=402, detail=f"{e}")
    
