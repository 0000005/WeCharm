from langchain_openai import ChatOpenAI
from config.settings import DEEPSEEK_API_KEY, DEEPSEEK_MODEL, DEEPSEEK_BASE_URL
from config.prompts import get_prompt
from models.llm_response import LLMResponse
import json


class LLMUtils:
    @staticmethod
    def get_llm_response(
        prompt_type: str, user_intent: str, chat_history: str, relationship: str
    ) -> LLMResponse:
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
        prompt = get_prompt(prompt_type)
        # 使用 user_input 替换 {USER_INTENT}
        prompt = prompt.replace("{USER_INTENT}", user_intent)
        # 使用 chat_history 替换 {CHAT_HISTORY}
        prompt = prompt.replace("{CHAT_HISTORY}", chat_history)
        # 根据relationship是否为空来决定是否添加关系信息
        relationship_text = f"对方的是我的{relationship}。" if relationship else ""
        prompt = prompt.replace("{RELATIONSHIP_TEXT}", relationship_text)

        llm = ChatOpenAI(
            model=DEEPSEEK_MODEL,
            openai_api_key=DEEPSEEK_API_KEY,
            openai_api_base=DEEPSEEK_BASE_URL,
            max_tokens=4024,
            temperature=1.5,
            response_format={"type": "json_object"},
        )
        print(f"prompt: {prompt}")
        response = llm.invoke(prompt)
        # Parse the JSON string into a dictionary
        content_dict = json.loads(response.content)
        return LLMResponse.from_dict(content_dict)
