"""
conda create -n claude-ocr -c conda-forge
conda activate claude-ocr
conda install python anthropic pillow -c conda-forge

setup ANTHROPIC_API_KEY env var

Key Improvements in this Updated Script:
Model Update
Switched to Claude 3.5 Sonnet (most advanced for text extraction)
Increased max_tokens to 4096 for more comprehensive text capture
Image Preprocessing
Added image validation and size optimization
Automatically resizes large images
Converts images to PNG for consistent handling
Enhanced Text Extraction Prompt
More detailed instructions for comprehensive text extraction
Requests preservation of formatting and layout
Asks for notes on text clarity and formatting
Error Handling
Improved error handling at multiple stages
Validates image files before processing
Provides informative error messages
Flexible Output
Optional text file saving
Interactive command-line interface
Allows multiple image processing in one session
Prerequisites:
Install required libraries:
pip install anthropic Pillow
Set Anthropic API key as an environment variable
Usage Tips:
Best for clear, high-quality images
Works with various document types, screenshots, etc.
Handles mixed content (text with graphics)
Limitations:
Relies on AI interpretation, not traditional OCR
Performance varies with image complexity
Requires Anthropic API access
"""

import base64
import os
from pathlib import Path
from typing import Optional, List
from anthropic import Anthropic
from PIL import Image
import io

def validate_and_preprocess_image(image_path: str) -> Optional[str]:
    """
    Validate and preprocess the image before OCR.
    
    :param image_path: Path to the image file
    :return: Base64 encoded image or None if invalid
    """
    try:
        # Open and validate image
        with Image.open(image_path) as img:
            # Check image size and convert to optimal format
            max_size = 5 * 1024 * 1024  # 5MB max
            
            # Resize if image is too large
            if os.path.getsize(image_path) > max_size:
                img.thumbnail((2048, 2048), Image.LANCZOS)
                
                # Save to a bytes buffer
                buffer = io.BytesIO()
                img.save(buffer, format='PNG')
                image_data = buffer.getvalue()
            else:
                with open(image_path, "rb") as image_file:
                    image_data = image_file.read()
            
            # Encode to base64
            return base64.b64encode(image_data).decode('utf-8')
    
    except Exception as e:
        print(f"Image preprocessing error: {e}")
        return None

def extract_text_from_image(api_key: str, image_path: str) -> Optional[str]:
    """
    Extract text from an image using Claude 3.5 Sonnet.
    
    :param api_key: Anthropic API key
    :param image_path: Path to the image file
    :return: Extracted text or None if extraction fails
    """
    # Initialize the Anthropic client
    client = Anthropic(api_key=api_key)
    
    # Preprocess the image
    base64_image = validate_and_preprocess_image(image_path)
    
    if not base64_image:
        print("Image preprocessing failed.")
        return None
    
    try:
        # Send request to Claude 3.5 Sonnet
        response = client.messages.create(
            #model="claude-3-5-sonnet-20240611",
            model="claude-3-haiku-20240307",
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": base64_image
                            }
                        },
                        {
                            "type": "text",
                            "text": (
                                "Please perform a comprehensive text extraction from this image. "
                                "I want you to:\n"
                                "1. Extract ALL visible text, including headers, captions, labels\n"
                                "2. Preserve the original formatting and layout as much as possible\n"
                                "3. If text is in multiple columns or sections, clearly indicate this\n"
                                "4. Note any special formatting like bold, italics, or different font sizes\n"
                                "5. If some text is unclear, mention 'Partially legible' or 'Text partially obscured'"
                            )
                        }
                    ]
                }
            ]
        )
        
        # Return the extracted text
        return response.content[0].text
    
    except Exception as e:
        print(f"Text extraction error: {e}")
        return None

def save_extracted_text(text: str, output_path: Optional[str] = None) -> None:
    """
    Save extracted text to a file or print to console.
    
    :param text: Extracted text
    :param output_path: Optional path to save the text file
    """
    if output_path:
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"Text saved to {output_path}")
        except Exception as e:
            print(f"Error saving text file: {e}")
    else:
        print("Extracted Text:\n", text)

def main():
    # Get API key from environment variable
    API_KEY = os.getenv('ANTHROPIC_API_KEY')
    
    if not API_KEY:
        print("Please set the ANTHROPIC_API_KEY environment variable.")
        return
    
    # Prompt for image path
    while True:
        IMAGE_PATH = r'D:\Documents\Projects\OCR\content\dl1.jpg'

        if IMAGE_PATH.lower() == 'quit':
            break
        
        # Validate file exists
        if not os.path.exists(IMAGE_PATH):
            print("File does not exist. Please check the path.")
            continue
        
        # Extract text
        extracted_text = extract_text_from_image(API_KEY, IMAGE_PATH)
        
        if extracted_text:
            print("Extracted Text:")
            print(extracted_text)
        else:
            print("Failed to extract text from the image.")

if __name__ == '__main__':
    main()
