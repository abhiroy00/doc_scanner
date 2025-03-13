from openai import OpenAI
from PIL import Image, UnidentifiedImageError
import pytesseract
import fitz  # PyMuPDF
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def perform_ocr(file_path):
    file_extension = file_path.split('.')[-1].lower()

    if file_extension in ['jpg', 'jpeg', 'png', 'bmp', 'gif']:
        return pytesseract.image_to_string(Image.open(file_path))
    elif file_extension == 'pdf':
        doc = fitz.open(file_path)
        text = ""
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text += page.get_text()
        return text
    else:
        return "Unsupported file type."

def extract_information(text):
    try:
        # Retrieve OpenAI API key from environment variable
        openai_api_key = os.getenv('OPENAI_API_KEY')

        if not openai_api_key:
            raise ValueError("OpenAI API key not found in environment variables.")

        # Initialize the OpenAI client
        client = OpenAI(api_key=openai_api_key)
        
        # Define the prompt for extracting key information
        prompt = f"Extract key information from the following text:\n\n{text}"
        
        # Call the OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # You can change this to "gpt-4" if needed
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts key information from text."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150  # Adjust based on the expected output length
        )
        
        # Extract and return the generated content
        extracted_info = response.choices[0].message.content
        return extracted_info
    except Exception as e:
        raise Exception(f"An error occurred during information extraction: {str(e)}")
