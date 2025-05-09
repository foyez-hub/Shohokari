from llm import generate_gemini_response 
from read_email import gmail_authenticate, get_latest_message_id, read_message
import time

def main():
    service = gmail_authenticate()
    last_id = get_latest_message_id(service)
    print("✅ Watching for new emails...")

    while True:
        time.sleep(10)  # Check every 10 seconds
        new_id = get_latest_message_id(service)
        if new_id != last_id:
            subject , body=read_message(service, new_id)
            # Generate a response using the LLM
            response = generate_gemini_response(f"Classify the following email based on its content. Categories: Higher Studies, Office, Job, Other.\n\nEmail Body:\n{subject}")
            last_id = new_id
            print(f"LLM Response: {response}")

if __name__ == '__main__':
    main()
