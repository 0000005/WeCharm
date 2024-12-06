from dataclasses import dataclass
from typing import List


@dataclass
class SuggestedResponse:
    style: str
    text: str


@dataclass
class ReplyResponse:
    suggested_response: List[SuggestedResponse]

    @classmethod
    def from_dict(cls, data: dict) -> "LLMResponse":
        """Convert dictionary to LLMResponse object

        Args:
            data (dict): A dictionary containing 'suggested_response' key with a list of
                        response dictionaries, where each dictionary has a 'text' field

        Returns:
            LLMResponse: A new LLMResponse object with the converted data

        Example:
            data = {
                'suggested_response': [
                    {'style': '正式','text': 'response1'},
                    {'style': '理性','text': 'response2'}
                ]
            }
            response = LLMResponse.from_dict(data)
        """
        responses = [SuggestedResponse(**resp) for resp in data["suggested_response"]]
        return cls(suggested_response=responses)


@dataclass
class IntentItem:
    text: str


@dataclass
class IntentResponse:
    intent_list: List[IntentItem]

    @classmethod
    def from_dict(cls, data: dict) -> "IntentResponse":
        """
        Create an IntentResponse instance from a dictionary.

        Args:
            data: Dictionary containing intent list data

        Returns:
            IntentResponse: Instance created from the dictionary
        """
        intents = [IntentItem(**intent) for intent in data["intent_list"]]
        return cls(intent_list=intents)
