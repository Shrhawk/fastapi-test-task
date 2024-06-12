from pydantic import BaseModel, EmailStr, SecretStr, field_validator


class UserRequestSchema(BaseModel):
    email: EmailStr
    password: SecretStr

    @field_validator('password')
    def password_length(cls, user_pass: SecretStr) -> SecretStr:
        password = user_pass.get_secret_value()
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(char.isalpha() for char in password) or not any(char.isdigit() for char in password):
            raise ValueError('Password must contain both letters and numbers')
        return user_pass


class UserRequestLoginSchema(UserRequestSchema):
    pass
