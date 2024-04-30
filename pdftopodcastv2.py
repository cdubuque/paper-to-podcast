from pathlib import Path
from openai import OpenAI
from PyPDF2 import PdfReader
import os
import requests
import json
import re
import pytz
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, generate_blob_sas, BlobSasPermissions,ContentSettings
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
pdf_directory = Path(os.getenv('PDF_DIRECTORY'))

pdf_file_path = next(pdf_directory.glob('*.pdf'))
print(pdf_file_path)
pdf_text = ''
# Print (os.path.getsize(pdf_file_path))
# Check if the file exists and is not empty
if os.path.exists(pdf_file_path) and os.path.getsize(pdf_file_path) > 0:
    pdf_reader = PdfReader(pdf_file_path)
    
    for page in pdf_reader.pages:
        pdf_text += page.extract_text()
else:
    print(f"The file {pdf_file_path} does not exist or is empty.")

completion = client.chat.completions.create(
  model="gpt-4-turbo-2024-04-09",
  messages=[
    {"role": "system", "content": os.getenv('SCRIPT_PROMPT')},
    {"role": "user", "content": pdf_text}
  ]
)

# Get the message content
message_content = completion.choices[0].message.content


# Write the GPT-4 response to the script file
with open('output.txt', 'w') as f:
    f.write(message_content)

print ("Script file updated.")
# Create a summary for the episode description field

completion = client.chat.completions.create(
  model="gpt-4-turbo-2024-04-09",
  messages=[
    {"role": "system", "content": "Now generate an episode description for the following podcast script."},
    {"role": "user", "content": message_content}
  ]
)

paper_overview = completion.choices[0].message.content

with open('summary.txt', 'w') as g:
    g.write(paper_overview)

print ("Summary created")

# Create a title for the episode

completion = client.chat.completions.create(
  model="gpt-4-turbo-2024-04-09",
  messages=[
    {"role": "system", "content": "Now generate an episode title for the following podcast script."},
    {"role": "user", "content": message_content}
  ]
)

episode_title = completion.choices[0].message.content

with open('title.txt', 'w') as h:
    h.write(episode_title)

print ("Title created")


# PDF TO PODCAST AUDIO FILE

speech_file_path = Path(os.getenv('SPEECH_FILE_PATH'))
script_file_path = Path(os.getenv('SCRIPT_FILE_PATH'))

# Read the text from the script file
with open(script_file_path, 'r') as f:
    script_text = f.read()

response = client.audio.speech.create(
  model="tts-1-hd",
  voice="alloy",
  input=script_text  # Use the text from the script file
)

# Save the response to a file
with open(speech_file_path, 'wb') as f:
    for data in response.iter_bytes():
        f.write(data)

print ("Audio file created")

# Create a BlobServiceClient object
connection_string = os.getenv('AZURE_CONNECTION_STRING')
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Get a reference to the blob container
container_name = os.getenv('CONTAINER_NAME')  # replace with your container name
container_client = blob_service_client.get_container_client(container_name)

# Upload the file
blob_name = re.sub('[^A-Za-z]', '', str(episode_title))
blob_client = container_client.get_blob_client(blob_name)
with open(speech_file_path, "rb") as data:
    blob_client.upload_blob(data, blob_type="BlockBlob", content_settings=ContentSettings(content_type='audio/mpeg', content_disposition='attachment'))
print(episode_title + "uploaded successfully.")

# Generate SAS token
sas_token = generate_blob_sas(
    blob_service_client.account_name,
    container_name,
    blob_name,
    account_key=blob_service_client.credential.account_key,
    permission=BlobSasPermissions(read=True),
    expiry=datetime.now(timezone.utc) + timedelta(hours=1)  # Token valid for 1 hours
)

# Create a secure URL for the blob
blob_url_with_sas = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"

print (blob_url_with_sas)

# Shorten long URL with SAS

bitly_url = 'https://api-ssl.bitly.com/v4/shorten'
bitly_headers = {
    'Authorization': os.getenv('BITLY_KEY'),
    'Content-Type': 'application/json',
}

# Data for the Bitly API request
bitly_data = {
    'group_guid': os.getenv('BITLY_GUID'),
    'domain': 'bit.ly',
    'long_url': blob_url_with_sas,
}

# Make the request to the Bitly API
bitly_response = requests.post(bitly_url, headers=bitly_headers, data=json.dumps(bitly_data))


# Get the short URL from the response
short_url = bitly_response.json().get('link')

print (short_url)


# UPLOAD TO BUZZSPROUT API

publishtime = datetime.now(pytz.timezone('US/Pacific')) + timedelta(minutes=15)

url = os.getenv('BUZZSPROUT_URL')
headers = {
    'Authorization': os.getenv('BUZZSPROUT_KEY'),
}
data = {
    'title': episode_title,
    'description': paper_overview,
    'audio_url': short_url,
    'private': False,
    'published_at': publishtime
}

# NEED TO FIGURE OUT HOW TO GET THIS TO AUTOPUBLISH THE EPISODE
response = requests.post(url, headers=headers, data=data)

print(response.status_code)
print(response.text)