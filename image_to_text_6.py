from transformers import BlipProcessor, BlipForConditionalGeneration, pipeline
from PIL import Image
import torch
import itertools
 
def image_to_detailed_description(image_path):
    try:
        # Load the processor and model
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
        # Open the image
        img = Image.open(image_path)
        # Preprocess the image for the model
        inputs = processor(images=img, return_tensors="pt")
        # Generate detailed description using the model
        with torch.no_grad():
            outputs = model.generate(**inputs, max_length=10000)  # Adjust max_length for more detailed text
        # Convert the output tokens to text (detailed description)
        description = processor.decode(outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
        return description
    except Exception as e:
        print(f"Error in image_to_detailed_description: {e}")
        return "Failed to extract description."
 
def main(image_path):
    # Extract detailed description from image
    description = image_to_detailed_description(image_path)
    return description











# from transformers import BlipProcessor, BlipForConditionalGeneration, pipeline
# from PIL import Image
# from chromadb import Client
# import torch
# import uuid  # To generate unique IDs
# import itertools  # For flattening the list
 
# def image_to_detailed_description(image_path):
#     try:
#         # Load the processor and model
#         processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
#         model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
#         # Open the image
#         img = Image.open(image_path)
#         # Preprocess the image for the model
#         inputs = processor(images=img, return_tensors="pt")
#         # Generate detailed description using the model
#         with torch.no_grad():
#             outputs = model.generate(**inputs, max_length=50)  # Adjust max_length for more detailed text
#         # Convert the output tokens to text (detailed description)
#         description = processor.decode(outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
#         return description
#     except Exception as e:
#         print(f"Error in image_to_detailed_description: {e}")
#         return None
 
# def get_embeddings(text):
#     try:
#         # Check if GPU is available
#         device = 0 if torch.cuda.is_available() else -1
#         # Load Hugging Face model to convert text to embeddings on the appropriate device
#         model = pipeline('feature-extraction', model="sentence-transformers/paraphrase-MiniLM-L6-v2", device=device, clean_up_tokenization_spaces=True)
#         embeddings = model(text)
#         # Flatten the embeddings (a list of lists) to a single list
#         flattened_embeddings = list(itertools.chain.from_iterable(embeddings[0]))
#         return flattened_embeddings
#     except Exception as e:
#         print(f"Error in get_embeddings: {e}")
#         return None
 
# def store_in_vector_db(text, embeddings):
#     try:
#         client = Client()
#         collection = client.create_collection("image_text_collection")
#         # Generate a unique ID for the document
#         unique_id = str(uuid.uuid4())
#         # Store the text, its embeddings, and the unique ID in the vector database
#         collection.add(
#             ids=[unique_id],           # Unique ID for this document
#             embeddings=[embeddings],   # Flattened embeddings for the text
#             documents=[text]           # Original text
#         )
#         print("Text and embeddings stored in the vector database.")
#     except Exception as e:
#         print(f"Error in store_in_vector_db: {e}")
 
# def main(image_path):
#     # Step 1: Extract detailed description from image
#     description = image_to_detailed_description(image_path)
#     if description:
#         print(f"Extracted detailed description from image: {description}")
#         # Step 2: Convert text (description) to embeddings
#         embeddings = get_embeddings(description)
#         if embeddings:
#             # Step 3: Store text and embeddings in vector database
#             store_in_vector_db(description, embeddings)
#     else:
#         print("Failed to extract description.")
 
# if __name__ == "__main__":
#     # Path to the image file
#     image_path = 'img.jpg'
#     main(image_path)