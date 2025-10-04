Team name - MARKS 
Team id - T086

Members - Radhika Gosain (UI/UX and Backend)
Kashish Verma (AI Integration)
Manpreet Kaur (Attendance system development)
Abhirupa Banerji (Attendance system development)
Sneha Kumari (Presentation)

Problem Statement - Automated Student Attendance Monitoring and Analytics System for Colleges

Enhanced Student-Teacher Portal:
An advanced student–teacher management platform that integrates AI and facial recognition for modern educational institutions.
Built with Django, OpenCV, DeepFace, and Groq API, this portal enhances classroom management, learning accessibility, and interactive assessments.

 Features
 Teacher Module:

Upload notes, study materials, and video lectures.

Take AI-powered attendance using facial recognition.

Organize quizzes with difficulty levels (Easy, Medium, Hard).

 Student Module:

Access uploaded notes and lectures anytime.

Attempt AI-generated quizzes with difficulty options.

Interact with an AI-powered chatbot for learning support.

 AI/ML Integrations:

Facial Recognition: Implemented using OpenCV and DeepFace for secure and accurate attendance tracking.

AI Chatbot: Integrated via Groq API for smart student interactions.

AI Quiz Generator: Automatically generates quizzes with graded levels of difficulty.

Tech Stack:
Frontend:
HTML, CSS, JavaScript

Backend:
Django (Python Framework)

AI & ML:
OpenCV (Face Detection/Recognition)
DeepFace (Facial Recognition Model)
Groq API (Chatbot & AI Quiz Generation)

Database:
SQLite

WORKING:
project-root/
│── backend/ # Django backend code
│── frontend/ # HTML, CSS, JS frontend
│── media/ # Uploaded lectures/notes
│── static/ # Static files (CSS, JS, images)
│── requirements.txt # Python dependencies
│── manage.py # Django project entry
│── README.md # Documentation

Follow these steps to set up and run the project locally:  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/your-username/enhanced-student-teacher-portal.git
cd enhanced-student-teacher-portal

python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt

SECRET_KEY=your-django-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3   # or your PostgreSQL URL
GROQ_API_KEY=your-groq-api-key

python manage.py makemigrations
python manage.py migrate


python manage.py createsuperuser

python manage.py collectstatic

python manage.py runserver

Now visit http://127.0.0.1:8000/
