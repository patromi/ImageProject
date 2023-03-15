FROM python:3.10-slim-buster
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y git
ENV PYTHONUNBUFFERED=1
#RUN git clone https://github.com/patromi/ImageProject /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py makemigrations core
RUN python manage.py makemigrations users

RUN python manage.py migrate
RUN python manage.py migrate core
RUN python manage.py migrate users
RUN python manage.py initadmin
RUN python manage.py test

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
