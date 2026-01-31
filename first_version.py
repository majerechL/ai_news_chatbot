import os
from dotenv import load_dotenv
import openai

load_dotenv() 

api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI()

model = "gpt-4.1-mini"

assistant = client.beta.assistants.create(
    name="Osobný tréner", model=model,
    instructions="Tvojou úlohou je odporúčiť cviky a stravu pre zdravý životný štýl pre 25-ročného.")
print(assistant.id)

thread = client.beta.threads.create()
print(thread.id)

message = "Čo by som mal jesť ráno ?"
created_message = client.beta.threads.messages.create(thread.id, content=message, role="user")

run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)

while True:
    run_info = client.beta.threads.runs.retrieve(run_id=run.id, thread_id=thread.id)
    if run_info.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        last_message = messages.data[0].content[0].text.value
        print(last_message)
        break