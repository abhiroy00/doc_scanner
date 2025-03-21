# doc_scanner

This project is an end-to-end solution that creates a pipeline to perform Optical Character Recognition (OCR) on uploaded documents, extracts key information using Large Language Models (LLMs), and provides a chat interface for users to query document content. The solution is deployed on AWS and uses Django for the web framework, HTML/CSS for the frontend, and SQLite for the database.

Architecture Overview

1.Frontend (HTML/CSS): The user interface where users can upload documents and interact with the chat interface.

2. Backend (Django): Handles the business logic, including document upload, OCR processing, and interaction with the LLM.

3.OCR Processing: Utilizes Tesseract OCR to extract text from uploaded documents.

4.LLM Integration: Uses OpenAI's GPT-4 (or another LLM) to extract key information from the OCR-processed text.
5.Chat Interface: A conversational interface where users can query the document content.
6.Database (SQLite): Stores document metadata, OCR text, and extracted information

7.AWS Deployment: The entire solution is deployed on AWS using services like EC2, S3, and RDS.

Prerequisites:

Python 3.8+
Django 4.0+
Tesseract OCR
OpenAI API key
AWS account

Setup Instructions:
1. Clone the Repository
git clone https://github.com/abhiroy00/doc_scanner.git
cd doc_scanner
2. Install Dependencies
pip install -r requirements.txt

4. Configure OpenAI API
Create a .env file in the root directory and add your OpenAI API key:
OPENAI_API_KEY=your_openai_api_key

5. Database Setup
The project uses SQLite by default. To initialize the database, run:

6. Run the Development Server
python manage.py runserver
Visit http://127.0.0.1:8000/ in your browser to access the application.

Deployment on AWS:
1. Create an EC2 Instance
Launch an EC2 instance with Ubuntu 20.04 LTS.

SSH into the instance: or use mobax 

 Install Dependencies on EC2
sudo apt-get update
sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx
pip3 install virtualenv


4. Clone the Repository on EC2
git clone https://github.com/yourusername/document-intelligence-pipeline.git
cd document-intelligence-pipeline
pip install -r requirements.txt

5. Configure Gunicorn and Nginx
Create a Gunicorn systemd service file:
sudo nano /etc/systemd/system/gunicorn.service


Add the following content:
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/document-intelligence-pipeline
ExecStart=/home/ubuntu/myenv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/ubuntu/document-intelligence-pipeline/document_intelligence.sock document_intelligence.wsgi:application

[Install]
WantedBy=multi-user.target

Start and enable Gunicorn:
--sudo systemctl start gunicorn
--sudo systemctl enable gunicorn

Configure Nginx:
sudo nano /etc/nginx/sites-available/doc_scanner

Add the following content:
server {
    listen 80;
    server_name your-ec2-public-ip;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/document-intelligence-pipeline/document_intelligence.sock;
    }
}

Enable the Nginx configuration:
sudo ln -s /etc/nginx/sites-available/document_intelligence /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

6. Configure Security Groups
Ensure that your EC2 instance's security group allows HTTP traffic on port 80.

7. Access the Application
Visit http://your-ec2-public-ip in your browser to access the deployed application.


Usage
1. Upload a Document

* Navigate to the upload page and upload a document (PDF, image, etc.).
* The document will be processed using Tesseract OCR, and the text will be extracted.

2
Query the Document

* Use the chat interface to ask questions about the document content.
* The system will use the LLM to provide answers based on the extracted text.

Documentation

API Endpoints

POST /upload/: Upload a document for processing.
POST /chat/: Send a query to the chat interface.

Database Schema


Document: Stores metadata about uploaded documents.

id: Primary key
file_name: Name of the uploaded file
uploaded_at: Timestamp of upload
ocr_text: Extracted text from OCR
extracted_info:Extracted information from text


ChatHistory: Stores chat interactions.

id: Primary key
document_id: Foreign key to Document
query: User query
response: LLM response
timestamp: Timestamp of interaction


Conclusion

This solution provides a robust pipeline for document intelligence with a conversational interface. It leverages OCR and LLMs to extract and query information from documents, and is deployable on AWS for scalable production use.
For further enhancements, consider integrating additional document types, improving the OCR accuracy, or using a more powerful LLM for better query responses.

GitHub Repository: Doc_scanner
Author: Abhishek kumar



