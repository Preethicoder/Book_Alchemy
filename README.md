# Flask ORM Library Management System

## 📌 Overview
This project is a simple **Library Management System** built using **Flask** and **SQLAlchemy ORM**. It allows users to manage authors and books using a database powered by **SQLite**.


## 🛠️ Setup & Installation
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-repo/flask-orm-library.git
cd flask-orm-library
```
### 2️⃣ Create & Activate a Virtual Environment (Recommended)
```bash
python -m venv venv  # Create virtual environment
source venv/bin/activate  # Activate on macOS/Linux
venv\Scripts\activate  # Activate on Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Initialize the Database
```bash
python
>>> from app import db
>>> db.create_all()
>>> exit()
```

### 5️⃣ Run the Flask App
```bash
python app.py
```

The app should now be running on **http://127.0.0.1:5000/** 🎉

## 🔥 Features
✅ **Add, Update, Delete Books**  
✅ **Manage Authors**  
✅ **Use SQLAlchemy ORM for database operations**  
✅ **Flask Flash Messages for User Notifications**  
✅ **SQLite Database for easy local storage**  

## 📝 API Endpoints (Example)
| Method | Endpoint | Description |
|--------|----------|--------------|
| GET | `/books` | Get all books |
| POST | `/books/add` | Add a new book |
| GET | `/authors` | Get all authors |
| POST | `/authors/add` | Add a new author |

## 🚀 Future Improvements
- [ ] Implement a frontend using React or Jinja templates
- [ ] Add user authentication & roles
- [ ] Migrate to PostgreSQL for production
- [ ] API documentation using Swagger/OpenAPI

## 🤝 Contributing
Feel free to fork the repository and submit pull requests. Contributions are welcome! 😊

## 📜 License
This project is licensed under the MIT License. Feel free to use and modify it as needed.

---
**Author:** preethi
**Contact:** preethisivakumar2024@gmail.com

