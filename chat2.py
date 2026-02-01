from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI()

system_message = """ 

You are an AI assistant who is an expert in breaking down complex 
problems and then solving them.

For the given user input , you breakdown the problem step by step
The steps are you get a user input ,  You analyse, you think , you again think
for several times and then you validate the calculated answer before concluding it as the final answer.

Follow the steps in sequence that is "Analyse" -> "Think" -> "Output" -> "Validate" -> "Final Answer"

Rules:
1. You must follow the steps in the exact order as mentioned below.
2. You must follow the exact format as mentioned below that is JSON format.
3. You must not skip any step.
4. Always perform one step at a time , and wait for the next input.

Example:
Input: What is 2+2 
Output: {{step: "Analyse" , content: "So, the user is asking for a simple addition of two numbers 2 and 2."}}
Output: {{step: "Think" , content: To Perform this addition , I'll add the numbers from left to right." }}
Output: {{step: "Output" , content: "4" }}
Output: {{step: "Validate" , content: "I have rechecked the addition and the answer is indeed 4." }}
Output: {{step: "Final Answer" , content: "2+2 is 4" }}

"""
messages = [
    {"role": "system", "content": system_message},
]

query = input("> ")
messages.append({"role": "user", "content": query})

while(True):
    
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=messages
    )
    
    parsed_response = json.loads(response.choices[0].message.content)
    messages.append({"role": "assistant", "content": json.dumps(parsed_response)})
    
    if(parsed_response.get("step") != "Final Answer"):
        print(">> " , parsed_response.get("content"))
        continue
    
    print(">>> ", parsed_response.get("content"))
    break
