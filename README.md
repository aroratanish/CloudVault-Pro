
# CloudVault-Pro
CloudVault Pro is a full-stack cloud storage and file management platform developed to provide users with a secure, organized, and intuitive way to manage digital files. Inspired by modern cloud storage solutions, the application combines secure authentication, file organization, sharing capabilities, recovery mechanisms, and real-time analytics within a clean and responsive user interface.

The project was built using Flask and SQLAlchemy to explore real-world software engineering concepts such as authentication systems, database design, file handling, access control, and full-stack web application development. Beyond basic file storage, CloudVault Pro focuses on delivering a seamless user experience through folder organization, search functionality, dashboard insights, and secure file sharing.

🚀 Features 🔐 Secure Authentication User registration and login system Password hashing using Flask-Bcrypt Secure session management with Flask-Login Email-based password reset functionality Account profile management 📂 File Management Upload and store files securely Download files on demand Track file metadata including upload date and size Permanent file deletion Storage usage monitoring 📁 Folder Organization Create and manage custom folders Organize files into structured categories Improve accessibility and file discoverability 🔗 File Sharing Generate unique shareable links Public access to shared files Simple and secure file distribution 🗑️ Trash & Recovery System Soft-delete functionality Restore accidentally deleted files Permanent deletion option for complete removal 🔍 Search Functionality Search files instantly by filename Quick access to stored resources Enhanced user productivity and navigation 📊 Analytics Dashboard Total files overview Folder statistics Shared file metrics Storage usage tracking Recent uploads activity 🏗️ Project Motivation
🚀 Features
🔐 Secure Authentication
User registration and login system
Password hashing using Flask-Bcrypt
Secure session management with Flask-Login
Email-based password reset functionality
Account profile management
📂 File Management
Upload and store files securely
Download files on demand
Track file metadata including upload date and size
Permanent file deletion
Storage usage monitoring
📁 Folder Organization
Create and manage custom folders
Organize files into structured categories
Improve accessibility and file discoverability
🔗 File Sharing
Generate unique shareable links
Public access to shared files
Simple and secure file distribution
🗑️ Trash & Recovery System
Soft-delete functionality
Restore accidentally deleted files
Permanent deletion option for complete removal
🔍 Search Functionality
Search files instantly by filename
Quick access to stored resources
Enhanced user productivity and navigation
📊 Analytics Dashboard
Total files overview
Folder statistics
Shared file metrics
Storage usage tracking
Recent uploads activity
🏗️ Project Motivation

Managing digital files efficiently is an essential requirement for both individuals and organizations. Traditional file systems often become cluttered and difficult to navigate as the amount of stored data grows.

CloudVault Pro was developed to address this challenge by providing a centralized platform where users can securely store files, organize them into folders, share them with others, recover deleted content, and monitor storage activity through an interactive dashboard.

The project also served as an opportunity to gain hands-on experience in designing scalable web applications and implementing industry-relevant backend systems.

🛠️ Technology Stack Backend Python Flask SQLAlchemy ORM Flask-Login Flask-Bcrypt Flask-Mail Frontend HTML5 CSS3 Bootstrap Jinja2 Templates Database SQLite Development Tools Visual Studio Code Git GitHub 📸 Application Preview Home Page

🛠️ Technology Stack
Backend
Python
Flask
SQLAlchemy ORM
Flask-Login
Flask-Bcrypt
Flask-Mail
Frontend
HTML5
CSS3
Bootstrap
Jinja2 Templates
Database
SQLite
Development Tools
Visual Studio Code
Git
GitHub
📸 Application Preview
Home Page

Dashboard

File Management

Trash Recovery

About Page

🗄️ Database Design

The application is built around four primary entities:

User

Stores user account information, authentication credentials, profile details, and relationships with files and folders.

File

Stores file metadata including:

File name File size Upload timestamp Folder association Ownership information Trash status Folder

Maintains user-created folders used to organize uploaded content.

Project Structure: CloudVault-Pro │ ├── flashblog/ │ ├── static/ │ │ ├── main.css │ │ └── profile_pics/ │ │ │ ├── templates/ │ │ ├── home.html │ │ ├── dashboard.html │ │ ├── files.html │ │ ├── folders.html │ │ ├── trash.html │ │ └── ... │ │ │ ├── forms.py │ ├── models.py │ └── routes.py │ ├── screenshots/ ├── instance/ ├── uploads/ ├── run.py ├── requirements.txt ├── README.md └── .gitignore SharedFile

File name
File size
Upload timestamp
Folder association
Ownership information
Trash status
Folder

Maintains user-created folders used to organize uploaded content.

Project Structure:
CloudVault-Pro
│
├── flashblog/
│   ├── static/
│   │   ├── main.css
│   │   └── profile_pics/
│   │
│   ├── templates/
│   │   ├── home.html
│   │   ├── dashboard.html
│   │   ├── files.html
│   │   ├── folders.html
│   │   ├── trash.html
│   │   └── ...
│   │
│   ├── forms.py
│   ├── models.py
│   └── routes.py
│
├── screenshots/
├── instance/
├── uploads/
├── run.py
├── requirements.txt
├── README.md
└── .gitignore
SharedFile

Stores unique sharing tokens that enable public access to files through generated links.

🎯 Key Learning Outcomes

Through the development of CloudVault Pro, the following concepts were explored and implemented:

Full-stack web application development Database modeling and relational design Authentication and authorization workflows Secure password management File handling and storage systems Search implementation User experience and responsive UI design Project organization using Flask architecture Version control and collaborative development using Git

👨‍💻 Developer

Tanish Arora Electronics & Computer Engineering Student Thapar Institute of Engineering & Technology

LinkedIn: www.linkedin.com/in/tanish-arora-7bb792323

⭐ If you found this project interesting, consider giving the repository a star. It helps

Full-stack web application development
Database modeling and relational design
Authentication and authorization workflows
Secure password management
File handling and storage systems
Search implementation
User experience and responsive UI design
Project organization using Flask architecture
Version control and collaborative development using Git

👨‍💻 Developer

Tanish Arora
Electronics & Computer Engineering Student
Thapar Institute of Engineering & Technology

LinkedIn: www.linkedin.com/in/tanish-arora-7bb792323

⭐ If you found this project interesting, consider giving the repository a star. It helps support the project and encourages further development.
