# HARD CHAT web form
Create using Flask

- Settings
1. Environment variables 
``` [export | set ] FLASK_APP=run.py ```
2. flask run --host 0.0.0.0

- Database migration:
1. Create Migration State
``` flask db migrate -m "Whate new for migration" ```
2. Updgrade or Downgrade
``` flask db [ upgrade | downgrade ] ```

- For Test:
1. shell with flask
``` flask shell ```

2. Test mail server
``` python -m smtpd -n -c DebuggingServer localhost:8025 ```
