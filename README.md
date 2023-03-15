# ImageProject
## Project objective

The purpose of this project is create a API picture hosting based on Django and Django Rest Framework.


## Fast Setup
You must first copy the repository:

```
git clone https://github.com/patromi/ImageProject.git
```
In the next step, create a ".env" file and specify SECRET_KEY inside. If you do not know how, simply copy from https://djecrety.ir/.


### Docker setup

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

### Create a superuser
You can create a basic superuser with custom commmand 'initadmin'
```
python manage.py initadmin
```
Then the email will be 'admin@gmail.com' and the password = 'admin'. 
Of course, you can change the credentials later in /admin
or create them manually:

```
python manage.py createsuperuser
```
### Tests
The project has 14 different unit tests. To run the tests execute:

```
python manage.py test
```
The project also has a command that runs the tests and the server simultaneously

```
python manage.py run
```

## Permissions
## "Basic" plan  
* a link to a thumbnail that's 200px in height
## "Premium" plan  
* a link to a thumbnail that's 200px in height
* a link to a thumbnail that's 400px in height
* a link to the originally uploaded image
## "Enterprise" plan  
* a link to a thumbnail that's 200px in height
* a link to a thumbnail that's 400px in height
* a link to the originally uploaded image
* ability to fetch an expiring link to the image 

### "Admin"
arbitrary thumbnail sizes
presence of the link to the originally uploaded file
ability to generate expiring links



## Endpoints
Public Endpoint is avaibible on /docs/

## Token

To get a token you need to send POST /api/token/

```json
{
    "email": "email",
    "password": "pass"
}
```

Response Code 201:
```json
{
    "refresh": "Refresh Token",
    "access": "Your Token"
}

```
Response Code 401 Unauthorized bad credentials:
```json
{
    "detail": "No active account found with the given credentials"
}

```

## Authorization

For successful authentication, You must send the Authorization header with the value "Bearer {your token}"


## Functionality

### Upload a small image (200x200)
Access : "Basic" and upper

* url: POST /api/upload/small/ 
* title: str max_lenght(20) (required)
* image: Image (required)
* expired_time: int 300-30000 (only for enterprise and root plan)

Response code 201:

```json

{
    "status": "Uploaded"
}

```

Response code 400 bad params:
```json 
{
    "image": [
        "No file was submitted."
    ]
}
```

## Upload a medium image (400x400)

Access : "Premium" and upper

* url: POST /api/upload/medium/ 
* title: str max_lenght(20) (required)
* image: Image (required)
* expired_time: int 300-30000 (only for enterprise and root plan)


Response code 201:

```json

{
    "status": "Uploaded"
}

```

Response code 400 bad params:
```json 
{
    "image": [
        "No file was submitted."
    ]
}
```

## Upload a original image (original resolution)

Access : "Premium" and upper

* url: POST /api/upload/original/ 
* title: str max_lenght(20) (required)
* image: Image (required)
* expired_time: int 300-30000 (only for enterprise and root plan)


Response code 201:

```json

{
    "status": "Uploaded"
}

```

Response code 400 bad params:
```json 
{
    "image": [
        "No file was submitted."
    ]
}
```


## Upload a Custom image (Custom resolution)

Access : "Premium" and upper

* url: POST /api/upload/original/ 
* title: str max_lenght(20) (required)
* image: Image (required)
* height: int (required)
* width: int (required)
* expired_time: int 300-30000 (only for enterprise and root plan)


Response code 201:

```json

{
    "status": "Uploaded"
}

```

Response code 400 bad params:
```json 
{
    "image": [
        "No file was submitted."
    ]
}
```

Response code 403 No permision:

```json
{
    "detail": "You do not have permission to perform this action."
}
```

## Upload a expired_time img

Access : "Enterprise" and upper


* url: POST /api/upload/original/ 
* title: str max_lenght(20) (required)
* image: Image (required)
* expired_time: int 300-30000 

Response code 201:

```json

{
    "status": "Uploaded"
}

```
Response code 400 bad params:
```json 
{
    "image": [
        "No file was submitted."
    ]
}
```

Response code 403 No permision:

```json
{
    "detail": "You do not have permission to perform this action."
}
```


## View your images

* url: GET /api/list/ 

Response code 200

```json
{
    "count": count,
    "next": null,
    "previous": null,
    "results": [
        {
            "title": "title",
            "link": "{host}/api/view/{uuid}/",
            "resolution": "200x200",
            "create_at": "2023-03-15T12:41:30.668695Z",
            "expired_at": "2023-03-15T12:46:56Z"
        },
        {
            "title": "{title}",
            "link": "{host}/api/view/{uuid",
            "resolution": "900x900",
            "create_at": "2023-03-15T12:46:40.459191Z",
            "expired_at": "2023-03-15T12:51:40.054522Z"
        },
    ]
}
```
Response code 403 No permision:

```json
{
    "detail": "You do not have permission to perform this action."
}
```

### View file

* url: GET /api/view/{uuid}

Renspose 200:
```File PNG```

Response 403 Forbidden:
{
    "error": [
        "Sorry, the link is expired"
    ]
}

Disclaimer: The link is only expired if expired_time was specified










