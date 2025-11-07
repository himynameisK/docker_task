import os
import time
from flask import Flask
from datetime import datetime

app = Flask(__name__)

message = os.getenv('MESSAGE', 'NO ENV SUPPLIED')

# Путь для логов - используем домашнюю директорию или /tmp
LOG_DIR = os.getenv('LOG_DIR', '/tmp/logs')
LOG_FILE = os.path.join(LOG_DIR, 'app.log')


def log_message(msg):
    """Запись логов в файл"""
    try:
        # Создаем директорию если не существует
        os.makedirs(LOG_DIR, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {msg}\n"

        # Записываем в лог-файл
        with open(LOG_FILE, 'a') as f:
            f.write(log_entry)

        print(log_entry.strip())
    except Exception as e:
        print(f"Error writing log: {e}")


@app.route('/')
def hello():
    log_message(f"Received request for root path. Message: {message}")
    return f"<h1>{message}</h1><p>This is our Dockerized application!</p>"


@app.route('/health')
def health():
    log_message("Health check requested")
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.route('/logs')
def show_logs():
    """Эндпоинт для просмотра логов"""
    try:
        with open(LOG_FILE, 'r') as f:
            logs = f.read()
        return f"<pre>{logs}</pre>"
    except FileNotFoundError:
        return "Logs not found yet"
    except Exception as e:
        return f"Error reading logs: {e}"


if __name__ == '__main__':
    log_message("Application started successfully!")
    app.run(host='0.0.0.0', port=8888, debug=False)