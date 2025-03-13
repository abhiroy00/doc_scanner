from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .forms import DocumentForm
from .models import Document
from .utils import perform_ocr, extract_information
from PIL import UnidentifiedImageError
import os

def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)  # Don't save to DB yet
            file = document.file

            try:
                # Save the document to DB first to ensure the file is stored
                document.save()

                # Check file extension to decide which processing method to use
                file_extension = os.path.splitext(file.name)[1].lower()

                if file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.tiff', '.bmp']:
                    # If it's an image, process with OCR
                    ocr_text = perform_ocr(file.path)
                elif file_extension == '.pdf':
                    # If it's a PDF, process with PDF extraction
                    ocr_text = perform_ocr(file.path)
                elif file_extension in ['.docx', '.doc']:
                    # If it's a Word document, process with Word extraction
                    ocr_text = perform_ocr(file.path)
                else:
                    # For unsupported file types
                    return render(request, 'upload_document.html', {
                        'form': form,
                        'error': "Unsupported file type. Please upload a valid document (PDF, DOCX, JPG, PNG, etc.)."
                    })

                # Extract information using the LLM
                document.ocr_text = ocr_text
                llm_response = extract_information(ocr_text)  # Get LLM response
                document.extracted_info = llm_response  # Save LLM response to the model
                
                # Save the document after processing
                document.save()
                
                # Redirect to the document detail page
                return redirect('document_detail', document.id)

            except UnidentifiedImageError:
                return render(request, 'upload_document.html', {
                    'form': form,
                    'error': "The uploaded file is not a valid image or is corrupted."
                })
            except Exception as e:
                return render(request, 'upload_document.html', {
                    'form': form,
                    'error': f"An error occurred during processing: {str(e)}"
                })
    else:
        form = DocumentForm()
    return render(request, 'upload_document.html', {'form': form})
