import os
import openai
import json
import pdfplumber

# Retrieve OpenAI API key on first run
if not os.path.exists("config.json"):
    openai_key = input("Please enter your OpenAI API key: ")
    with open("config.json", "w") as f:
        json.dump({"openai_key": openai_key}, f)
else:
    with open("config.json", "r") as f:
        openai_key = json.load(f)["openai_key"]

# Set up OpenAI client
openai.api_key = openai_key

def summarize(text):
    response = openai.ChatCompletion.create(
      model="GPT-3.5-turbo",  # Use the correct model name based on availability
      messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Summarize the following text.",
            },
            {
                "role": "user",
                "content": text,
            }
        ],
      max_tokens=3000
    )

    return response['choices'][0]['message']['content']

def scan_and_summarize(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    summary = summarize(text)
    return summary

while True:
    doc_to_scan = input("Enter the path of the PDF document you want to scan and summarize: ")
    summary = scan_and_summarize(doc_to_scan)
    print(f"Summary:\n{summary}")
  
