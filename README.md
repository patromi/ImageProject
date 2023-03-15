# ImageProject

##Fast Setup
You must first copy the repository:

```
git clone https://github.com/patromi/ImageProject.git

```
In the next step, create a ".env" file and specify SECRET_KEY inside. If you do not know how, simply copy from https://djecrety.ir/.


###Docker setup

```
docker build -t imageapi .  

```

and run

```

docker run -p 8000:8000 imageapi

```

### Normal setup
```
cd Imageproject/imageapi 

```

Install Depediences

```
pip install  -r requirements.txt

```
Run server

```
python manage.py runserver 0.0.0.0:8000

```

####Create a superuser
You can create a basic superuser with custom commmand 'initadmin'
```
python manage.py inituser

```
Then the email will be 'admin@gmail.com' and the password = 'admin'. 
Of course, you can change the credentials later in /admin
or create them manually:

```
python manage.py createsuperuser

```
###Tests
The project has 14 different unit tests. To run the tests execute:

```

python manage.py test


```
The project also has a command that runs the tests and the server simultaneously

```
python manage.py run

```







