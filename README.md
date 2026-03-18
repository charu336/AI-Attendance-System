# Virtual Attendance System (Face Recognition + GPS)

A smart attendance system that uses face recognition and GPS validation to automate attendance and prevent proxy entries.

---

## Features

- Face recognition-based attendance using OpenCV  
- GPS-based location verification  
- Role-based access (Admin, Teacher, Student)  
- Attendance tracking and report generation  
- Real-time identity verification  

---

## Tech Stack

- Backend: Python  
- Computer Vision: OpenCV  
- Database: MongoDB  
- Frontend: HTML/CSS/JavaScript (or React if used)  
- Other: GPS Integration  

---

## How It Works

1. User logs in (Student/Teacher/Admin)  
2. Face is captured and matched with stored data  
3. GPS location is verified  
4. If both match, attendance is marked  
5. Data is stored in MongoDB  

---

## How to Run

### Backend
```bash
pip install -r requirements.txt
python attendance.py
