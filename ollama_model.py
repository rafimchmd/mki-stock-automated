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

  message = ''
  for part in client.chat('qwen3.5:397b-cloud', messages=messages, stream=True):
    if part.message.content is not None:
      message += part.message.content
  formatted_message = json.loads(message)
  return formatted_message
  available_tools = {'web_search': web_search, 'web_fetch': web_fetch}
  client = Client(
      host='https://ollama.com',
      headers={'Authorization': 'Bearer ' + OLLAMA_KEY}
  )
  messages = [{'role': 'user', 'content': request}]
  while True:
    response = client.chat(
      model='deepseek-v3.1:671b-cloud',
      messages=messages,
      tools=[web_search, web_fetch],
      think=True
      )
    if response.message.thinking:
      print('Thinking: ', response.message.thinking)
    if response.message.content:
      print('Content: ', response.message.content)
    messages.append(response.message)
    if response.message.tool_calls:
      print('Tool calls: ', response.message.tool_calls)
      for tool_call in response.message.tool_calls:
        function_to_call = available_tools.get(tool_call.function.name)
        if function_to_call:
          args = tool_call.function.arguments
          result = function_to_call(**args)
          print('Result: ', str(result)[:200]+'...')
          # Result is truncated for limited context lengths
          messages.append({'role': 'tool', 'content': str(result)[:2000 * 4], 'tool_name': tool_call.function.name})
        else:
          messages.append({'role': 'tool', 'content': f'Tool {tool_call.function.name} not found', 'tool_name': tool_call.function.name})
    else:
      break