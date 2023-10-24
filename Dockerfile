FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY . /app/

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
    
EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "redditproject.wsgi:application"]
