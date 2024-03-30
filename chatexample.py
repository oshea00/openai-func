import os
from dotenv import load_dotenv
load_dotenv()
import json
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored  
import requests
import sys

GPT_MODEL = "gpt-4"
client = OpenAI()

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e

def pretty_print_conversation(messages):
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "function": "magenta",
    }
    
    for message in messages:
        if message["role"] == "system":
            print(colored(f"system: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "user":
            print(colored(f"user: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "assistant" and message.get("function_call"):
            print(colored(f"assistant: {message['function_call']}\n", role_to_color[message["role"]]))
        elif message["role"] == "assistant" and not message.get("function_call"):
            print(colored(f"assistant: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "function":
            print(colored(f"function ({message['name']}): {message['content']}\n", role_to_color[message["role"]]))

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA or a zip code, e.g. 94107, or a lat,long pair, e.g. 37.7749,-122.4194",
                    }
                },
                "required": ["location"],
            },
        }
    }
]

def get_current_weather(location):
    weather_api_key = os.getenv("WEATHER_API_KEY")
    url = f"https://api.weatherapi.com/v1/current.json?q={location}&alerts=yes&key={weather_api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: Unable to fetch weather data for {location}"

def execute_function_call(message):
    if message.tool_calls[0].function.name == "get_current_weather":
        location = json.loads(message.tool_calls[0].function.arguments)["location"]
        results = get_current_weather(location)
    else:
        results = f"Error: function {message.tool_calls[0].function.name} does not exist"
    return results

messages = []
messages.append({"role": "system", "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."})
location = sys.argv[1] if len(sys.argv) > 1 else "Seattle"
messages.append({"role": "user", "content": f"What's the weather like today in {location}"})
chat_response = chat_completion_request(messages, tools=tools)

assistant_message = chat_response.choices[0].message

# If the assistant made a function call, execute the function and return the results
# otherwise print the assistant's response - which is usually for clarification.
# This interchange would typically be part of a loop in a real application.

if assistant_message.tool_calls:
    call_id = assistant_message.tool_calls[0].id
    function_name = assistant_message.tool_calls[0].function.name
    results = execute_function_call(assistant_message)
    response_message = {"role": "function", "tool_call_id": call_id, "name": function_name, "content": results} 
    messages.append(response_message)
else:
    messages.append({"role": "assistant", "content": assistant_message.content})

pretty_print_conversation(messages)


