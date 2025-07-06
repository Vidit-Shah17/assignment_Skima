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

2. **Create virtual env**
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

3. **Install dependencies**
pip install -r requirements.txt

4. **Adding image as name placeholder.png**
Place a PNG file named placeholder.png in the project root. 
i have used
![placeholder](https://github.com/user-attachments/assets/3ab257a4-602c-4f06-a864-7f1eac285634)
this as png file

5. **Run the server**
python app.py
