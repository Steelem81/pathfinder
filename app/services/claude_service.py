import os
from typing import Optional, Dict, Any
from config.settings import settings
from anthropic import Client, RateLimitError, APIConnectionError, APIError

class ClaudeService:

    def __init__(self, api_key: Optional[str]=None):
        self.api_key = settings.ANTHROPIC_API_KEY
        self.model = settings.ANTHROPIC_MODEL
        self.max_tokens = settings.MAX_TOKENS
        self.temperature = settings.TEMPERATURE

    def generate(
        self,
        prompt:str,
        max_tokens: Optional[int]=None,
        temperature: Optional[float]=None,
        system: Optional[str]=None,
        max_retries: int =3,
    ) -> str:
    
        max_tokens = max_tokens or self.max_tokens
        temperature = temperature or self.temperature

        for attempt in range(max_retries):
            try:
                request_params = {
                    "model": self.model,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "messages": [
                        {"role":"user", "content":prompt}
                    ]
                }
                response = self.client.messages.create(**request_params)

                self.total_input_tokens += response.usage.input_tokens
                self.total_ouput_tokens += response.usage.output_tokens
                self.request_count += 1

                return response.content[0].text
            
            except RateLimitError as e:
                if attempt <= max_retries -1:
                    wait_time = (2 ** attempt)*1
                    print(f"Rate limit hit. Waiting {wait_time} before retry {attempt}/{max_retries}")
                    time.sleep(wait_time)
                else:
                    raise APIError(f"Rate limit exceeded after {max_retries} retries") from e
            
            except APIConnectionError as e:
                if attempt <= max_retries -1:
                    wait_time = (2 ** attempt) * 1
                    print(f"Connection error. Retrying in {wait_time} minutes...attempt {attempt}/{max_retries}")
                    time.sleep(wait_time)
                else:
                    raise APIError(f"Connection failed after {max_retries} attempts") from e
            
            except Exception as e:
                raise APIError(f"Claude API Error: {str(e)}") from e
    # raise APIError("Failed to get response from Claude")

    def generate_json(
        self,
        prompt: str,
        max_tokens: Optional[int]=None,
        max_retries: int=3
        ) -> Dict[str, Any]:

        response_text = self.generate(prompt, max_tokens, max_retries)

        cleaned = response_text.strip()

        # Try to extract JSON from response
        # Sometimes Claude wraps it in markdown code blocks
        cleaned = response_text.strip()
        
        # Remove markdown code blocks if present
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:] 
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]  
        
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3] 
        
        cleaned = cleaned.strip()
        
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON response: {str(e)}\nResponse: {cleaned[:200]}...")


if __name__ == "__main__":
    try:
        claude = ClaudeService()

        print("="*50)
        print("Testing Claude Service")
        
        response = claude.generate(
            prompt="Explain what machine learning is in one sentence",
            max_tokens=100
        )

        print("Response", response)
        print("="*50)
    
    except ValueError as e:
        print(f"Error: {e}")