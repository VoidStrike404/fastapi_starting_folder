from pydantic import BaseModel

class UserSchema(BaseModel):
    username: str = 'John Doe'
    password: str = 'my_password'



