## Intro

Web App to help you manage your bill wisely.

## Setup

1. Install Python3 and Git on your local

2. Clone this repository on your local and must rename

``git clone git@github.com:YuanPeihao/bill_mgmt_sys.git bill_management_system``

3. Setup runtime environment, dependencies and DB

```
cd bill_management_system
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
```

4. Start App

``python manage.py runserver``

5. Access the website by typing the below address on your browser

``http://127.0.0.1:8000/bill_collector/``


