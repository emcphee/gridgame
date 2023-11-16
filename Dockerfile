FROM python:latest

WORKDIR /home

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001
CMD ["python", "./app.py"]