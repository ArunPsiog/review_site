from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config.utils import decodeJWT

# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# def decodeJWT(token: str) -> dict:
#     try:
#         decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         print(decoded_token)
#         return decoded_token if decoded_token["exp"] >= int(datetime.utcnow().timestamp()) else None
#     except Exception as e:
#         print(f"exception in decode jwt = {e}")

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            # if not self.verify_jwt(credentials.credentials):
            #     raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            #return credentials.credentials
            return self.verify_jwt(credentials.credentials)
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        #isTokenValid: bool = False

        try:
            payload = decodeJWT(token=jwtoken)
        except Exception as e:
            print(f'exception:  verify_jwt = {e}')
            payload = None
        # if payload:
        #     isTokenValid = True
        return payload