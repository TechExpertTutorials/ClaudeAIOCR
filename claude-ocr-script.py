import base64
import os
from anthropic import Anthropic

def encode_image(image_path):
    """
    Encode an image file to base64 for API transmission.
    
    :param image_path: Path to the image file
    :return: Base64 encoded string of the image
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def extract_text_from_image(api_key, image_path):
    """
    Use Claude Haiku to extract text from an image.
    
    :param api_key: Your Anthropic API key
    :param image_path: Path to the image file
    :return: Extracted text from the image
    """
    # Initialize the Anthropic client
    client = Anthropic(api_key=api_key)
    
    try:
        # Encode the image
        base64_image = encode_image(image_path)
        
        # Send request to Claude Haiku
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",  # or image/png, adjust as needed
                                "data": base64_image
                            }
                        },
                        {
                            "type": "text",
                            "text": "Please extract all the text from this image. If there are multiple text regions, list them clearly."
                        }
                    ]
                }
            ]
        )
        
        # Return the extracted text
        return response.content[0].text
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def main():
    # Replace with your actual Anthropic API key
    API_KEY = os.getenv('ANTHROPIC_API_KEY')
    
    if not API_KEY:
        print("Please set the ANTHROPIC_API_KEY environment variable.")
        return
    
    # Path to your image file
    IMAGE_PATH = r'D:\Documents\Projects\OCR\content\dl1.jpg'
    
    # Extract text from the image
    extracted_text = extract_text_from_image(API_KEY, IMAGE_PATH)
    
    if extracted_text:
        print("Extracted Text:")
        print(extracted_text)
    else:
        print("Failed to extract text from the image.")

if __name__ == '__main__':
    main()
