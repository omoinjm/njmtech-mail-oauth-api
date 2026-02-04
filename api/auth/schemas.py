from pydantic import BaseModel, EmailStr

class UserInfo(BaseModel):
    email: EmailStr
    
class TokenData(BaseModel):
    access_token: str
    refresh_token: str | None = None
    expires_at: int
    
class AuthResponse(BaseModel):
    user: UserInfo
    token: TokenData
