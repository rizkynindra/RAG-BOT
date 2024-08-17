import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")

client = OpenAI(api_key=key)

#create vector store
vector_store = client.beta.vector_stores.create(name="qnatk")
print(f"Vector Store Id - {vector_store.id}")

#upload files
file_paths = ["doc/FAQ_2023.pdf"]
file_streams = [open(path, "rb") for path in file_paths]

#add files to vector store
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id= vector_store.id,
    files = file_streams
)

#check the status of files
print(f"File status {file_batch.status}")

#Update the assistant with a vector store
assistant = client.beta.assistants.update(
    assistant_id=assistant_id,
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
)

print("Assistant updated with vector store!")

# Create a thread
thread = client.beta.threads.create()
print(f"Your thread id is - {thread.id}\n\n")

# Run a loop where user can ask questions
while True:
    text = input("Halo ada yang bisa dibantu?\n")

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