Paper-to-Podcast
This project automates the process of converting research papers in PDF format into podcast episodes. It uses the OpenAI API to generate a script from the PDF, creates an audio file from the script, and uploads the audio file to Azure Blob Storage.

Setup
1. Clone this repository to your local machine.

2. Install the required Python packages using pip:

    pip install -r requirements.txt

3. Set up your environment variables in a .env file in the root directory of the project. The following variables are required:
    OPENAI_API_KEY="your_openai_api_key"
    PDF_DIRECTORY="your_pdf_directory"
    SPEECH_FILE_PATH="your_speech_file_path"
    SCRIPT_FILE_PATH="your_script_file_path"
    AZURE_CONNECTION_STRING="your_azure_connection_string"
    CONTAINER_NAME="your_container_name"
    SCRIPT_PROMPT="your_script_prompt"
    BITLY_KEY='your_bitly_key'
    BITLY_GUID='your_bitly_guid'
    BUZZSPROUT_URL='your_buzzsprout_url'
    BUZZSPROUT_KEY='your_buzzsprout_key'
    
4. Add your .env file to your .gitignore file to prevent it from being committed to your Git repository.

Usage

Run the pdftopodcastv2.py script to convert a PDF into a podcast episode:
    python pdftopodcastv2.py

The script will generate a script from the PDF using the OpenAI API, create an audio file from the script, and upload the audio file to Azure Blob Storage.

Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.