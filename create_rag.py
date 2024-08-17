import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=key)

description = """
    Kamu adalah seorang customer service BPJS Ketenagakerjaan yang ramah.
    Jawablah pertanyaan - pertanyaan seputar yang ada di dokumen.
    Jika ada pertanyaan diluar dokumen silakan jawab 'maaf saya tidak mengerti, 
    saya hanya bisa memberikan informasi seputar BPJS Ketenagakerjaan'
"""

instructions = """
    Jika ada pertanyaan diluar dokumen yang sudah kamu pelajari silakan jawab dengan:
    'Maaf, saya hanya bisa memberikan informasi seputar BPJS Ketenagakerjaan'
"""

assistant = client.beta.assistants.create(
    name="BPJSTK Assistant",
    description=description,
    instructions=instructions,
    model="gpt-3.5-turbo",
    tools=[{"type": "file_search"}],
)

print(assistant)