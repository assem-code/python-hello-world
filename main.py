# import os
# from dotenv import load_dotenv
# import google.generativeai as genai
# import telebot

# load_dotenv()

# google_api_key = os.getenv("GOOGLE_API_KEY")

# if not google_api_key:
#     raise ValueError("Google API key is missing. Please ensure the .env file is configured correctly.")

# genai.configure(api_key=google_api_key)

# bot = telebot.TeleBot("8002800371:AAG7wnOpTpAcLsDRUmGwpGBl_GRIjSMS1jA", parse_mode=None)

# def upload_to_gemini(path, mime_type=None):
#     """Uploads the given file to Gemini."""
#     if not os.path.exists(path):
#         print(f"File not found: {path}")
#         return None
    
#     file = genai.upload_file(path, mime_type=mime_type)
#     print(f"Uploaded file '{file.display_name}' as: {file.uri}")
#     return file

# file_path = "D:/Elite Students'bot/main.py"  

# files = []
# if os.path.exists(file_path):
#     files = [upload_to_gemini(file_path, mime_type="text/plain")]
# else:
#     print(f"File not found: {file_path}")

# generation_config = {
#     "temperature": 1,
#     "top_p": 0.95,
#     "top_k": 40,
#     "max_output_tokens": 8192,
#     "response_mime_type": "text/plain",
# }

# model = genai.GenerativeModel(
#     model_name="gemini-2.0-flash-exp",
#     generation_config=generation_config,
# )

# chat_session = model.start_chat(
#     history=[
#         {"role": "user", "parts": ["Hi"]},
#         {"role": "model", "parts": ["Hi there! I am Sooma, an AI made by Assem. How can I help you?"]},
#         {"role": "user", "parts": ["who are you?"]},
#         {"role": "model", "parts": ["I am Sooma, a large language model, trained by Assem."]},
#         {"role": "user", "parts": ["من أنت ؟"]},
#         {"role": "model", "parts": ["أنا نموذج لغوي كبير، تم تدريبي بواسطة عاصم. اسمي صوما"]},
#         {"role": "user", "parts": ["انت مين؟"]},
#         {"role": "model", "parts": [
#             files[0] if files else "",
#             "أنا نموذج لغوي كبير، اسمي صوما، تم تدريبي بواسطة عاصم.\n",
#         ]},
#     ]
# )

# @bot.message_handler(func=lambda m: True)
# def echo_all(message):
#     response = chat_session.send_message(message.text)
#     print(response.text)
#     bot.reply_to(message, response.text)

# bot.infinity_polling()
















import os
from dotenv import load_dotenv
import google.generativeai as genai
import telebot
import PyPDF2  # مكتبة لتحليل ملفات PDF

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    raise ValueError("Google API key is missing. Please ensure the .env file is configured correctly.")

genai.configure(api_key=google_api_key)

bot = telebot.TeleBot("8002800371:AAG7wnOpTpAcLsDRUmGwpGBl_GRIjSMS1jA", parse_mode=None)

def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini."""
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return None
    
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

# استخراج النص من ملف PDF
def extract_text_from_pdf(pdf_path):
    """استخراج النص من ملف PDF."""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return ""

# معالجة ملف PDF المرفق من المستخدم
@bot.message_handler(content_types=["document"])
def handle_pdf(message):
    if message.document.mime_type == 'application/pdf':
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # حفظ الملف مؤقتًا لاستخراج النص
        file_path = "temp.pdf"
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        # استخراج النص من PDF
        pdf_text = extract_text_from_pdf(file_path)
        
        # إرسال النص المستخرج إلى النموذج لفهمه
        if pdf_text:
            response = chat_session.send_message(pdf_text)
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "Failed to extract text from the PDF.")

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
        {"role": "user", "parts": ["Hi"]},
        {"role": "model", "parts": ["Hi there! I am Sooma, an AI made by Assem. How can I help you?"]},
    ]
)

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    response = chat_session.send_message(message.text)
    bot.reply_to(message, response.text)

bot.infinity_polling()



