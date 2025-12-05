import os
import threading
import webbrowser
import time

def start_backend():
    backend_path = os.path.join(os.getcwd(), "backend", "app.py")
    os.system(f'python "{backend_path}"')

threading.Thread(target=start_backend, daemon=True).start()

time.sleep(3)

frontend_path = os.path.join(os.getcwd(), "frontend", "index.html")
webbrowser.open(f'file://{frontend_path}')

print("Chatbot is starting... please wait a few seconds.")
