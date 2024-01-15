import openai
import os # for getting API token from env variable OPENAI_API_KEY
import tiktoken
import aiohttp
import asyncio
from typing import List, Dict, Tuple, Any

openai_client = openai.OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))

def num_tokens(text: str, model = "gpt-4") -> int:
    """
        Return the number of tokens in a string.
    """
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def sync_chat_completion(**kwargs):
    """
        Synchronous chat completion
    """
    return openai_client.chat.completions.create(**kwargs)

def chat_completion(messages_list: List[Dict[str,str]], model: str, temperature: float) -> List[Tuple[Any, str]]:
    """
        Perform chat completion on a messages_list. Use asynchronous calls for batch speed-up for GPT-3.5
    """
    if model == "gpt-4": # async API calls throw lots of errors for GPT-4
        assert len(messages_list) == 1
        return [(messages_list[0][0],sync_chat_completion(messages=messages_list[0][1], model=model, temperature=temperature).choices[0].message.content)]
    else: 
        results = asyncio.run(batch_openai_api(messages_list, model, temperature))
        return [(idx,x['choices'][0]['message']['content']) for (idx, _), x in results]


def single_chat_completion(prompt, model, temperature):
    messages = [{"role":"user", "content":prompt}]
    messages_list = [ (0, messages) ] 
    return chat_completion(messages_list, model, temperature)[0][1]


# asynchronous Open API call code taken from https://blog.finxter.com/how-to-request-openais-api-asynchronously-in-python/
openai.api_key = os.environ.get("OPENAI_API_KEY")

async def async_openai_request(messages, model, temperature):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            return await response.json()


async def batch_openai_api(messages_list, model, temperature):
    # Gather results from all asynchronous tasks
    results = await asyncio.gather(*(async_openai_request(messages, model,temperature) for _,messages in messages_list))
    return zip(messages_list, results)
