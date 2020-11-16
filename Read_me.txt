--for development mode--

_____________Enable Virtual environment______________________

# ..\scripts\activate 

_____________run api______________________
run

# flask run

_____________run jobs(not available)_____________________

# celery worker --app=tasks.worker.app --pool=eventlet --loglevel=info --pid=
# celery beat --app=tasks.worker.app --loglevel=info --pid=