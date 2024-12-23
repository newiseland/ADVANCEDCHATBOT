FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "telegram_chatgpt_bot.py"]
docker build -t telegram-chatgpt-bot .
docker run -d telegram-chatgpt-bot