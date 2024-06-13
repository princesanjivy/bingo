FROM python:3.10.12

WORKDIR /app

# copy all files to /app working dir
COPY server/main.py /app/main.py
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# start the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
