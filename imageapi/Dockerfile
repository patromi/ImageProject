FROM python:3.10-slim-buster
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y git

#RUN git clone https://github.com/patromi/ImageProject /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "inituser"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
