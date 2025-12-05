📘 Student Information Management System

A secure and encrypted student information management system built using Flask, MySQL, and ECDSA digital signature verification.
The system ensures only authorized users can add or modify student records, and all actions are logged for transparency and auditing.

🚀 Features
🔐 Secure Authentication

Login system with account verification

Session-based user authentication

Prevents unauthorized access

🧾 Student Record Management

Add new student details

Update or delete existing records

Store structured student information in MySQL

🔑 ECDSA Signature Verification

Every modification request is digitally signed

Uses SECP256k1 public/private keys

Ensures only the creator can authorize modifications

Prevents tampering of student data

📊 Audit Logging

Every action (add/modify/delete) is logged

Each action includes a unique transaction ID

Useful for tracking history and debugging

🌐 Web Interface

Built with Flask templates

Clean and simple UI

Easy form submission and data view

🛠️ Tech Stack
Component	Technology
Backend	Flask (Python)
Database	MySQL
Security	ECDSA (SECP256k1), Hashing
Frontend	HTML, CSS, JavaScript
Environment	Python 3.x
📦 Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/your-username/students_info.git
cd students_info

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Configure Database

Create a MySQL database

Update your DB credentials inside the Flask config file

Import the .sql file if provided

4️⃣ Run the Application
python app.py


The system will start running on:

http://127.0.0.1:5000/

📂 Project Structure (example)
students_info/
│── app.py
│── templates/
│── static/
│── database/
│── utils/
│── requirements.txt
└── README.md

🧪 How Verification Works

User submits a request to add/modify data

System generates a hash of the student info

User signs it using their private key

System verifies using the public key

Only if the signature is valid, data is updated

This prevents:

Unauthorized edits

Fake student records

Data tampering

👥 Contributors

Rajeswari Varadarajugari

Joshna Kamsani

Gopi nerella

Youtube Video:

[![Watch the Video: Students Info with ECC Cryptic Verifying Process](https://img.youtube.com/vi/9T-1dFIHJrg/0.jpg)](https://youtu.be/9T-1dFIHJrg)
