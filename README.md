### Create a virtual environment and install the requirements.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Migration and runserver
```bash
python manage.py migrate
python manage.py runserver
```
