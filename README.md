# URL Screenshot Tracker API

This project is a simple asynchronous API that accepts a URL and returns a simulated screenshot via webhook and API.

---

## Features

- Submit a URL to queue a screenshot job
- Simulates screenshot with a placeholder image
- Asynchronous background processing (non-blocking)
- Notifies client via webhook when job completes
- Retrieve job status and screenshot image
- SQLite for job storage

---

## Language and Framework use

- Python 3
- Flask
- SQLite
- Requests (for webhook)
- threading (for async job simulation)

---

## Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/Vidit-Shah17/assignment_Skima
cd assignment_Skima
```

2. **Create virtual env**
```bash
python -m venv venv
# Activating the venv
linux: source venv/bin/activate   
Windows: venv\Scripts\activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Adding image as name placeholder.png**
```bash
Place a PNG file named placeholder.png in the project root. \n
i have used
![placeholder](https://github.com/user-attachments/assets/3ab257a4-602c-4f06-a864-7f1eac285634)
this as png file
```

6. **Run the server**
```bash
python app.py

'''
You will get this output:

 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
'''
```

7. **Submit URL for Screenshot (POST /screenshots)**
```bash
# Open new terminal and write
curl -X POST http://localhost:5000/screenshots -H "Content-Type: application/json" -d "{\"url\":\"https://example.com\",\"webhook_url\":\"https://webhook.site/e71f9397-89d5-40f7-b44a-c85944f71a17\"}"
'''
Here,
"https://webhook.site/e71f9397-89d5-40f7-b44a-c85944f71a17" this is my workbook id link you can replace with yours.
```

8. 
