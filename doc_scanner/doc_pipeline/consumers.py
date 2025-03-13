import json
from channels.generic.websocket import AsyncWebsocketConsumer
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key='your-gemini-api-key')

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Query document content using Gemini
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(f"Answer the following question based on the document content:\n\n{message}")
        await self.send(text_data=json.dumps({'message': response.text}))