# test-task-kaizen
Install mysql

Run (in backend folder)
pip install -r requirements.txt

Open backend/backend/settings.py and change db settings (DATABASES object)

Run (in backend folder)
python manage.py makemigrations 
python manage.py migrate
python manage.py runserver

Open `http://127.0.0.1:8000/docs/` for swagger docs
Create user api `accounts/register`
Login api `accounts/login`

Login api returns token.
Add token to autherization header
'Authorization: Token <token here>'

To check apis using swaggger
Login using `accounts/login` api in swagger
Click Authorize button in the top-right area
Add "Token <token here>" in the textfield

Testing
Run `python manage.py test`
