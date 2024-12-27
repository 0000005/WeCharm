from dataclasses import dataclass
from .llm_response_model import ReplyLlmResponse, ReplyListItem
from typing import List

@dataclass
class ReplyModel:
    wechatNickname: str
    replyList: List[ReplyListItem]
    contextNum: int
    lastMessage: str
