from pydantic import BaseModel
from typing import Optional

class Friend(BaseModel):
    # Basic Information
    wechatNickname: str
    name: str = ""
    age: Optional[int] = None
    relationship: str = ""
    gender: str = ""
    occupation: str = ""
    additionalInfo: str = ""
    contextSize: int = 5
