import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

key = os.getenv("OPENAI_API_KEY")
assist_id = os.getenv("ASSISTANT_ID")
vect_id = os.getenv("VECTOR_ID")

client = OpenAI(api_key=key)

#Update the assistant with a vector store
assistant = client.beta.assistants.update(
    assistant_id=assist_id,
    tool_resources={"file_search": {"vector_store_ids": [vect_id]}},
)

print("Assistant updated with vector store!")

# Create a thread
thread = client.beta.threads.create()
print(f"Your thread id is - {thread.id}\n\n")

# Run a loop where user can ask questions
while True:
    text = input("Mau nanya apa bro?\n")

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=text,
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id, assistant_id=assistant.id
    )

    messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
    message_content = messages[0].content[0].text
    print("Response: \n")
    print(f"{message_content.value}\n")