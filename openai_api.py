import openai
import os # for getting API token from env variable OPENAI_API_KEY
openai_client = openai.OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))

def chat_completion(**kwargs):
    return openai_client.chat.completions.create(**kwargs)
