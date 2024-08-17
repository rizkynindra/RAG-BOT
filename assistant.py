from openai import OpenAI
import config
import os
from dotenv import load_dotenv
load_dotenv()



def createAssistant(file_ids, title):
    #Create the OpenAI Client Instance
    key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=key)

    #GET Instructions saved in the Settings.py File (We save the instructions there for easy access when modifying)
    instructions = """
    Kamu adalah seorang customer service BPJS Ketenagakerjaan yang ramah.
    Jawablah pertanyaan - pertanyaan seputar yang ada di dokumen.
    Jika ada pertanyaan diluar dokumen silakan jawab 'maaf saya tidak mengerti, 
    saya hanya bisa memberikan informasi seputar BPJS Ketenagakerjaan'. 
    """

    #The GPT Model for the Assistant (This can also be updated in the settings )
    model = "gpt-3.5-turbo"

    #Only Retireval Tool is relevant for our use case
    tools = [{"type": "file_search"}]

    ##CREATE VECTOR STORE
    # vector_store = client.beta.vector_stores.create(name=title,file_ids=file_ids)
    vector_store_id = os.getenv("VECTOR_STORE_ID")
    tool_resources = {"file_search": {"vector_store_ids": [vector_store_id]}}

    #Create the Assistant
    assistant = client.beta.assistants.create(
    name=title,
    instructions=instructions,
    model=model,
    tools=tools,
    tool_resources=tool_resources
    )

    #Return the Assistant ID
    return assistant.id,vector_store_id




# def saveFileOpenAI(location):
#     #Create OpenAI Client
#     key = os.getenv("OPENAI_API_KEY")
#     client = OpenAI(api_key=key)
#
#     #Send File to OpenAI
#     file = client.files.create(file=open(location, "rb"),purpose='assistants')
#
#     # Delete the temporary file
#     os.remove(location)
#
#     #Return FileID
#     return file.id



def startAssistantThread(prompt,vector_id):
    #Initiate Messages
    messages = [{"role": "user", "content": prompt}]
    #Create the OpenAI Client
    key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=key)
    #Create the Thread
    tool_resources = {"file_search": {"vector_store_ids": [vector_id]}}
    thread = client.beta.threads.create(messages=messages,tool_resources=tool_resources)

    return thread.id



def runAssistant(thread_id, assistant_id):
    #Create the OpenAI Client
    key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=key)
    # client = OpenAI(api_key=config.API_KEY)
    run = client.beta.threads.runs.create(thread_id=thread_id,assistant_id=assistant_id)
    return run.id



def checkRunStatus(thread_id, run_id):
    key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=key)
    # client = OpenAI(api_key=config.API_KEY)
    run = client.beta.threads.runs.retrieve(thread_id=thread_id,run_id=run_id)
    return run.status



def retrieveThread(thread_id):
    key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=key)
    # client = OpenAI(api_key=config.API_KEY)
    thread_messages = client.beta.threads.messages.list(thread_id)
    list_messages = thread_messages.data
    thread_messages = []
    for message in list_messages:
        obj = {}
        obj['content'] = message.content[0].text.value
        obj['role'] = message.role
        thread_messages.append(obj)
    return thread_messages[::-1]



def addMessageToThread(thread_id, prompt):
    key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=key)
    # client = OpenAI(api_key=config.API_KEY)
    thread_message = client.beta.threads.messages.create(thread_id,role="user",content=prompt)