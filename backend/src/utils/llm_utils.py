from langchain_openai import ChatOpenAI
from config.prompts import get_prompt
from models.llm_response_model import ReplyResponse, IntentResponse
from models.friend_model import Friend
from models.setting_model import Settings
from utils.time_utils import get_current_time
import json
import logging

logger = logging.getLogger("wecharm")


class LLMUtils:

    @staticmethod
    def _build_info_text(info_parts: list) -> str:
        """Build a text string from a list of info parts."""
        return "，".join(filter(None, info_parts)) + "。" if info_parts else ""

    @staticmethod
    def _build_personal_info(settings: Settings) -> str:
        """Build personal info text from settings."""
        info_parts = []
        if settings.name:
            info_parts.append(f"我的名字是{settings.name}")
        if settings.age:
            info_parts.append(f"今年{settings.age}岁")
        if settings.gender:
            info_parts.append(f"性别是{settings.gender}")
        if settings.occupation:
            info_parts.append(f"职业是{settings.occupation}")
        if settings.otherInfo:
            info_parts.append(settings.otherInfo)
        # 如果 info_parts 不为空，则在数组第一个元素中添加“- ”字符
        if info_parts:
            info_parts[0] = f"- {info_parts[0]}"
        return LLMUtils._build_info_text(info_parts)

    @staticmethod
    def _build_friend_info(friend: Friend) -> str:
        """Build friend info text from friend model."""
        info_parts = []
        if friend.relationship:
            info_parts.append(f"对方是我的{friend.relationship}")
        if friend.name:
            info_parts.append(f"名字是{friend.name}")
        if friend.age:
            info_parts.append(f"今年{friend.age}岁")
        if friend.gender:
            info_parts.append(f"性别是{friend.gender}")
        if friend.occupation:
            info_parts.append(f"职业是{friend.occupation}")
        if friend.additionalInfo:
            info_parts.append(friend.additionalInfo)
        # 如果 info_parts 不为空，则在数组第一个元素中添加“- ”字符
        if info_parts:
            info_parts[0] = f"- {info_parts[0]}"
        return LLMUtils._build_info_text(info_parts)

    @staticmethod
    def _create_llm_instance(settings: Settings) -> ChatOpenAI:
        """Create and return a ChatOpenAI instance with the given settings."""
        return ChatOpenAI(
            model=settings.model,
            openai_api_key=settings.apiKey,
            openai_api_base=settings.baseUrl,
            max_tokens=4024,
            temperature=1.5,
            response_format={"type": "json_object"},
        )

    @staticmethod
    def _log_messages(messages: list):
        """Log the messages being sent to LLM."""
        logger.debug("LLM请求内容：")
        for msg in messages:
            logger.debug(f"{msg['role']}：{msg['content']}")

    @staticmethod
    def get_llm_response(
        prompt_type: str, chat_history: str, friend: Friend, settings: Settings
    ) -> IntentResponse:
        """
        Get LLM response using the specified prompt type in JSON mode.

        Args:
            prompt_type: Type of prompt to use
            chat_history: Previous chat history
            friend: Friend model containing relationship info
            settings: Settings model containing API configuration

        Returns:
            IntentResponse: Model containing different response styles
        """
        sys_prompt = get_prompt(prompt_type)

        # Process chat history
        chat_context = get_prompt("聊天上下文").replace("{CHAT_HISTORY}", chat_history)

        # Add additional info
        additional_info = """# 补充信息"""
        additional_info += f"\n- 当前时间：{get_current_time()}"
        sys_prompt = sys_prompt.replace("{ADDITIONAL_INFO}", additional_info)
        # Replace placeholders with personal and friend info
        sys_prompt = sys_prompt.replace(
            "{MINE_INFO}", LLMUtils._build_personal_info(settings)
        )
        sys_prompt = sys_prompt.replace(
            "{FRIEND_INFO}", LLMUtils._build_friend_info(friend)
        )

        # Create messages and get response
        messages = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": chat_context},
        ]

        LLMUtils._log_messages(messages)
        llm = LLMUtils._create_llm_instance(settings)
        response = llm.invoke(messages)

        return IntentResponse.from_dict(json.loads(response.content))

    @staticmethod
    def get_llm_response_with_intent(
        prompt_type: str,
        user_intent: str,
        chat_history: str,
        friend: Friend,
        settings: Settings,
    ) -> ReplyResponse:
        """
        Get LLM response using the specified prompt type in JSON mode.

        Args:
            prompt_type: Type of prompt to use
            user_intent: User's input text
            chat_history: Previous chat history
            friend: Friend model containing relationship info
            settings: Settings model containing API configuration

        Returns:
            ReplyResponse: Model containing different response styles
        """
        sys_prompt = get_prompt(prompt_type)
        sys_prompt = sys_prompt.replace("{CHAT_HISTORY}", chat_history)

        # Replace placeholders with personal and friend info
        sys_prompt = sys_prompt.replace(
            "{MINE_INFO}", LLMUtils._build_personal_info(settings)
        )
        sys_prompt = sys_prompt.replace(
            "{FRIEND_INFO}", LLMUtils._build_friend_info(friend)
        )

        # Process user intent
        user_intent_prompt = get_prompt("用户意图").replace(
            "{USER_INTENT}", user_intent
        )

        # Create messages and get response
        messages = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_intent_prompt},
        ]

        LLMUtils._log_messages(messages)
        llm = LLMUtils._create_llm_instance(settings)
        response = llm.invoke(messages)

        return ReplyResponse.from_dict(json.loads(response.content))
