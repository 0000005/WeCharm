from langchain_openai import ChatOpenAI
from config.settings import DEEPSEEK_API_KEY, DEEPSEEK_MODEL, DEEPSEEK_BASE_URL
from config.prompts import get_prompt
from models.llm_response import ReplyResponse, IntentResponse
from utils.time_utils import get_current_time
import json


class LLMUtils:

    @staticmethod
    def get_llm_response_no_intent(
        prompt_type: str, chat_history: str, relationship: str
    ) -> IntentResponse:
        """
        Get LLM response using the specified prompt type in JSON mode.

        Args:
            prompt_type: Type of prompt to use ('general', 'code', 'writing')
            chat_history: Previous chat history
            relationship: Relationship context

        Returns:
            LLMResponse: Model containing different response styles
        """
        sys_prompt = get_prompt(prompt_type)
        # 根据relationship是否为空来决定是否添加关系信息
        relationship_text = f"对方的是我的{relationship}。" if relationship else ""
        sys_prompt = sys_prompt.replace("{RELATIONSHIP_TEXT}", relationship_text)

        chat_context = get_prompt("聊天上下文")
        # 使用 chat_history 替换 {CHAT_HISTORY}
        chat_context = chat_context.replace("{CHAT_HISTORY}", chat_history)

        # 补充额外信息
        addtional_info = """# 补充信息"""
        # 如果 relationship 不为空，添加关系信息 到 addtional_info
        if relationship:
            addtional_info += f"\n- 对方的是我的{relationship}。"
        # 新增当前时间 到 addtional_info
        addtional_info += f"\n- 当前时间：{get_current_time()}"
        # 将 addtional_info 添加到 sys_prompt
        sys_prompt = sys_prompt.replace("{ADDITIONAL_INFO}", addtional_info)

        llm = ChatOpenAI(
            model=DEEPSEEK_MODEL,
            openai_api_key=DEEPSEEK_API_KEY,
            openai_api_base=DEEPSEEK_BASE_URL,
            max_tokens=4024,
            temperature=1.5,
            response_format={"type": "json_object"},
        )
        messages = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": chat_context},
        ]

        # 打印日志
        print("LLM请求内容：")
        for msg in messages:
            print(f"{msg['role']}：{msg['content']}")

        response = llm.invoke(messages)
        # Parse the JSON string into a dictionary
        content_dict = json.loads(response.content)
        return IntentResponse.from_dict(content_dict)

    @staticmethod
    def get_llm_response(
        prompt_type: str, user_intent: str, chat_history: str, relationship: str
    ) -> ReplyResponse:
        """
        Get LLM response using the specified prompt type in JSON mode.

        Args:
            prompt_type: Type of prompt to use ('general', 'code', 'writing')
            user_intent: User's input text
            chat_history: Previous chat history
            relationship: Relationship context

        Returns:
            LLMResponse: Model containing different response styles
        """
        sys_prompt = get_prompt(prompt_type)
        # 使用 chat_history 替换 {CHAT_HISTORY}
        sys_prompt = sys_prompt.replace("{CHAT_HISTORY}", chat_history)
        # 根据relationship是否为空来决定是否添加关系信息
        relationship_text = f"对方的是我的{relationship}。" if relationship else ""
        sys_prompt = sys_prompt.replace("{RELATIONSHIP_TEXT}", relationship_text)

        user_intent_prompt = get_prompt("用户意图")
        # 使用 user_input 替换 {USER_INTENT}
        user_intent_prompt = user_intent_prompt.replace("{USER_INTENT}", user_intent)

        llm = ChatOpenAI(
            model=DEEPSEEK_MODEL,
            openai_api_key=DEEPSEEK_API_KEY,
            openai_api_base=DEEPSEEK_BASE_URL,
            max_tokens=4024,
            temperature=1.5,
            response_format={"type": "json_object"},
        )
        messages = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_intent_prompt},
        ]

        # 打印日志
        print("LLM请求内容：")
        for msg in messages:
            print(f"{msg['role']}：{msg['content']}")

        response = llm.invoke(messages)
        # Parse the JSON string into a dictionary
        content_dict = json.loads(response.content)
        return ReplyResponse.from_dict(content_dict)
