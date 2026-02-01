from openai import OpenAI
from dotenv import load_dotenv
import json
import os

load_dotenv()
client = OpenAI()

def get_weather(city):
    # Dummy function to simulate getting weather information
    return f"The current weather in {city} is 20 degrees Celsius with a humidity of 70%."

def os_command(command):
    return os.popen(command).read()

system_message = """
Your are an helpful AI Assistant. You take user queries and give relevant answers.
To resolve the user Query , You follow pre defined steps and use available tools if required.

Steps to follow:
{{step: "Analyse" , content: "You analyse the user query and try to understand what exactly the user is asking for."}}
{{step: "Think" , content: "You think about how to approach the problem and what tools or information you might need to solve it."}}
{{step: "Tool" , content: "If you need to use any tool to get information, you specify the tool name and the input to the tool. (separated by a space then comma then space)"}}
{{step: "Output" , content: "You get the output from the tool and use it to formulate your answer."}}
{{step: "Validate" , content: "You validate the information you have gathered and ensure that it is accurate and relevant to the user's query."}}
{{step: "Final Answer" , content: "You provide the final answer to the user based on your analysis, thinking, tool usage, output, and validation."}}

Rules:
1. You must follow the steps in the exact order as mentioned above.
2. You must follow the exact format as mentioned above that is JSON format.
3. You must not skip any step.
4. Always perform one step at a time , and wait for the next input.
5. Always follow the format strictly.
6. If you are using a tool, make sure to wait for the tool output before proceeding to the next step.
7. If tool == "os_command" , make sure to execute only safe commands like "ls", "pwd", "date" etc. Avoid any destructive commands like "rm","sudo" etc.

Available Tools:
1. get_weather : To get the current weather of any city.
2. os_command : To execute any operating system command.


Example:
Input: What is the current weather in chennai ?
Output: {{step: "Analyse" , content: "The user is asking for the current weather in Chennai."}}
Output: {{step: "Think" , content: "To provide the current weather, I need to use the get_weather tool." }}
Output: {{step: "Tool" , content: "get_weather , chennai" }}
Output: {{step: "Output" , content: "The current weather in Chennai is 30 degrees Celsius with a humidity of 70%." }}
Output: {{step: "Validate" , content: "I have checked the weather information and it is accurate." }}
Output: {{step: "Final Answer" , content: "The current weather in Chennai is 30 degrees Celsius with a humidity of 70%." }}

"""

while(True):
    user_message = input("> ")
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
    while(True):
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=messages
        )
        
        parsed_response = json.loads(response.choices[0].message.content)
        print(">> " , parsed_response.get("content"))
        messages.append({"role": "assistant", "content": json.dumps(parsed_response)})
        
        if(parsed_response.get("step") == "Tool"):
            tool_info = parsed_response.get("content").split(",")
            tool_name = tool_info[0].strip()
            tool_input = tool_info[1].strip()
            
            if tool_name == "get_weather":
                tool_output = get_weather(tool_input)
            elif tool_name == "os_command":
                tool_output = os_command(tool_input)
            else:
                tool_output = "Unknown tool"
            
            messages.append({"role": "user", "content": f"Tool Output: {tool_output}"})
            
        elif(parsed_response.get("step") == "Final Answer"):
            print(">>> ", parsed_response.get("content"))
            break