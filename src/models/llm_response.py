from dataclasses import dataclass
from typing import List

@dataclass
class SuggestedResponse:
    text: str

@dataclass
class LLMResponse:
    suggested_response: List[SuggestedResponse]

    @classmethod
    def from_dict(cls, data: dict) -> 'LLMResponse':
        """Convert dictionary to LLMResponse object
        
        Args:
            data (dict): A dictionary containing 'suggested_response' key with a list of 
                        response dictionaries, where each dictionary has a 'text' field
        
        Returns:
            LLMResponse: A new LLMResponse object with the converted data
            
        Example:
            data = {
                'suggested_response': [
                    {'text': 'response1'},
                    {'text': 'response2'}
                ]
            }
            response = LLMResponse.from_dict(data)
        """
        responses = [SuggestedResponse(**resp) for resp in data['suggested_response']]
        return cls(suggested_response=responses)
