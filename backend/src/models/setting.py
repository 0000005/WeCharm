from pydantic import BaseModel
from typing import Optional


class Settings(BaseModel):
    # AI Settings
    baseUrl: str = ""
    model: str = ""
    apiKey: str = ""
    # Personal Information
    name: str = ""
    age: int = ""
    gender: str = ""
    occupation: str = ""
    otherInfo: str = ""
