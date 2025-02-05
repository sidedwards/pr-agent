from os import environ
from openai import OpenAI, APIError, RateLimitError, Timeout
from retry import retry

from pr_agent.algo.ai_handlers.base_ai_handler import BaseAiHandler
from pr_agent.config_loader import get_settings
from pr_agent.log import get_logger

OPENROUTER_RETRIES = 5

class OpenRouterHandler(BaseAiHandler):
    def __init__(self):
        try:
            super().__init__()
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=get_settings().openrouter.key
            )
            self.site_url = get_settings().get("OPENROUTER.SITE_URL", "")
            self.site_name = get_settings().get("OPENROUTER.SITE_NAME", "")
        except AttributeError as e:
            raise ValueError("OpenRouter key is required") from e

    @property
    def deployment_id(self):
        """
        Returns the deployment ID (not used for OpenRouter).
        """
        return None

    @retry(exceptions=(APIError, Timeout, AttributeError, RateLimitError),
           tries=OPENROUTER_RETRIES, delay=2, backoff=2, jitter=(1, 3))
    async def chat_completion(self, model: str, system: str, user: str, temperature: float = 0.2):
        try:
            get_logger().info("System: ", system)
            get_logger().info("User: ", user)
            
            messages = [
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ]
            
            extra_headers = {}
            if self.site_url:
                extra_headers["HTTP-Referer"] = self.site_url
            if self.site_name:
                extra_headers["X-Title"] = self.site_name

            chat_completion = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                extra_headers=extra_headers
            )

            resp = chat_completion.choices[0].message.content
            finish_reason = chat_completion.choices[0].finish_reason
            usage = chat_completion.usage
            
            get_logger().info("AI response", response=resp, messages=messages, 
                            finish_reason=finish_reason, model=model, usage=usage)
            return resp, finish_reason
            
        except (APIError, Timeout) as e:
            get_logger().error("Error during OpenRouter inference: ", e)
            raise
        except RateLimitError as e:
            get_logger().error("Rate limit error during OpenRouter inference: ", e)
            raise
        except Exception as e:
            get_logger().error("Unknown error during OpenRouter inference: ", e)
            raise
