from pydantic import BaseModel, EmailStr


class Email(BaseModel):
    email: EmailStr
    is_main: bool
    is_checked: bool
