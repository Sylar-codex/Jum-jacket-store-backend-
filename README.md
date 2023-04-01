## Jum-Jacket store(frontend)

An ecommerce api which allows authentication of users, which also integrates payment using paystack.
using serializers to convert python objects to json and xml and also deserializing json and xml back to python objects.
usuage of cloudinary for image optimization in database.

updating the database soon...

## Tools and language

<table>
	 <tbody>
  <tr>
   <td align="Center" width="25%"> 
 <a href="https://www.python.org/" target="_blank" rel="noreferrer"><img src="https://img.icons8.com/fluency/48/000000/python.png" width="36" height="36" alt="Python" /></a>
    <br>Python
    </td>   
   
   <td align="Center" width="25%">
        <a href="https://www.djangoproject.com/" target="_blank" rel="noreferrer"><img src="https://img.icons8.com/external-tal-revivo-filled-tal-revivo/24/000000/external-django-a-high-level-python-web-framework-that-encourages-rapid-development-logo-filled-tal-revivo.png" width="36" height="36" alt="Django" /></a>
	<br>Django
    </td>   
	  </tr>
</tbody>
  </table>
	
<br>

## Prerequisites

Before installation, please make sure you have already installed the following tools:

- [Git](https://git-scm.com/downloads)
- [Python](https://www.python.org/downloads/)

## 🛠️ Installation Steps

1. clone app

2. while in root folder create a virtual environment

create a folder named (venv)

3. Run the following cmd

```bash
python3 -m venv root-venvFolder-path/venv
```

5. Activate virtual environment

```bash
source venv/bin/activate
```

6. cd into app dir where you can find requirements.txt to Install all packages using the following cmd

```bash
pip install -r requirements.txt
```

7. makemigrations and migrate

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

8. Run project

```bash
python manage.py runserver
```
