import openai
import os # for getting API token from env variable OPENAI_API_KEY
import tiktoken

openai_client = openai.OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))

def chat_completion(**kwargs):
    return openai_client.chat.completions.create(**kwargs)

def num_tokens(text: str, model = "gpt-4") -> int:
    """Return the number of tokens in a string."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))
