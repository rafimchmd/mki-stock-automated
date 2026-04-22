from ollama import Client, web_fetch, web_search
import json
from datetime import datetime
from constant.app_constant import OLLAMA_KEY, LIST_EXPECTED_SIMILAR_STOCKS_RESPONSE

def get_analysis(request_message: str):

  client = Client(
      host='https://ollama.com',
      headers={'Authorization': 'Bearer ' + OLLAMA_KEY}
  )


  print("[ollama-analyzer] Start analyzing . . .")
  messages = [
    {
      'role': 'user',
      'content': request_message
    },
  ]
  try:
    message = ''
    for part in client.chat('qwen3.5:397b-cloud', messages=messages, stream=True):
      if part.message.content is not None:
        message += part.message.content
    formatted_message = json.loads(message)
    return formatted_message
  except Exception as e:
    print(f"Exception {str(e)}")