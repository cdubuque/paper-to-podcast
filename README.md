# Paper-to-Podcast

This project automates the process of converting research papers in PDF format into podcast episodes. It utilizes the OpenAI API to generate a script from the PDF, creates an audio file from the script, and uploads the audio file to Azure Blob Storage.

## Setup

1. **Clone the Repository**
   Clone this repository to your local machine.

   git clone [repository-url]

2. **Install Python Packages**
   Use pip to install the required packages from the provided requirements file.

   pip install -r requirements.txt

3. **Environment Setup**
   Set up your environment variables in a .env file in the root directory of the project. Ensure you include all necessary keys:

   OPENAI_API_KEY="your_openai_api_key"
   PDF_DIRECTORY="your_pdf_directory"
   SPEECH_FILE_PATH="your_speech_file_path"
   SCRIPT_FILE_PATH="your_script_file_path"
   AZURE_CONNECTION_STRING="your_azure_connection_string"
   CONTAINER_NAME="your_container_name"
   SCRIPT_PROMPT="your_script_prompt"
   BITLY_KEY="your_bitly_key"
   BITLY_GUID="your_bitly_guid"
   BUZZSPROUT_URL="your_buzzsprout_url"
   BUZZSPROUT_KEY="your_buzzsprout_key"

4. **Secure the Environment File**
   Add the .env file to your .gitignore to prevent it from being committed:

   echo ".env" >> .gitignore

## Usage

To convert a PDF into a podcast episode, run the pdftopodcastv2.py script:

python pdftopodcastv2.py

The script will:
- Generate a script from the PDF using the OpenAI API.
- Create an audio file from the script.
- Upload the audio file to Azure Blob Storage.
- Upload the audio file and corresponding podcast details to Buzzsprout podcast hosting

## Contributing

Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.
