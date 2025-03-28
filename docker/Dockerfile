FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    python -m nltk.downloader -d /usr/share/nltk_data stopwords

ENV NLTK_DATA=/usr/share/nltk_data

CMD ["python", "main.py"]