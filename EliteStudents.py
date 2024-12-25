import os
import google.generativeai as genai

# Directly set the API key in the environment for this session
os.environ["GOOGLE_API_KEY"] = "AIzaSyAHFEbcjuns24NyttqyFrkPV9021a4YJnM"

def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini.

    See https://ai.google.dev/gemini-api/docs/prompting_with_media
    """
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return None
    
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

# Example file path (you should replace this with the actual file path you want to upload)
file_path = "D:/Elite Students'bot/EliteStudents.py"  # Replace with your actual file path

# Check if the file exists and proceed with the upload
files = []
if os.path.exists(file_path):
    files = [upload_to_gemini(file_path, mime_type="text/plain")]
else:
    print(f"File not found: {file_path}")

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                "Hi",
            ],
        },
        {
            "role": "model",
            "parts": [
                "Hi there! I am Sooma ,an AI made by Assem, How can I help you",
            ],
        },
        {
            "role": "user",
            "parts": [
                "who are you?",
            ],
        },
        {
            "role": "model",
            "parts": [
                "I am Sooma, a large language model, trained by Assem.",
            ],
        },
        {
            "role": "user",
            "parts": [
                "من أنت ؟",
            ],
        },
        {
            "role": "model",
            "parts": [
                "أنا نموذج لغوي كبير، تم تدريبي بواسطة عاصم. اسمي صوما",
            ],
        },
        {
            "role": "user",
            "parts": [
                "انت مين؟",
            ],
        },
        {
            "role": "model",
            "parts": [
                files[0] if files else "",
                "أنا نموذج لغوي كبير، اسمي صوما، تم تدريبي بواسطة عاصم.\n",
            ],
        },
    ]
)

response = chat_session.send_message("كيف حالك؟")

print(response.text)
