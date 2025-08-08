# Simple CRM Setup Guide

## 🚀 Quick Start

### Option 1: Automatic Setup (Windows)
1. Double-click `setup.bat` to run the automatic setup
2. Follow the prompts to install dependencies and initialize the database
3. Run `python app.py` to start the application

### Option 2: Manual Setup

## 📋 Prerequisites

- **Python 3.7 or higher**
- **pip** (Python package installer)
- **Git** (optional, for cloning)

## 🛠️ Installation Steps

### 1. Install Python

**Windows:**
- Download from: https://www.python.org/downloads/
- **Important:** Check "Add Python to PATH" during installation
- Verify installation: `python --version`

**macOS/Linux:**
```bash
# macOS (using Homebrew)
brew install python

# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip
```

### 2. Clone/Download the Project

```bash
# If using Git
git clone <repository-url>
cd Simple-CRM

# Or download and extract the ZIP file
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize Database

```bash
python init_db.py
```

### 5. Run the Application

```bash
python app.py
```

### 6. Access the Application

- Open your web browser
- Navigate to: `http://localhost:5000`
- Login with: `admin` / `admin123`

## 🔧 Troubleshooting

### Python Not Found

**Error:** `Python was not found; run without arguments to install from the Microsoft Store`

**Solutions:**
1. **Install Python properly:**
   - Download from https://www.python.org/downloads/
   - Check "Add Python to PATH" during installation
   - Restart your terminal/command prompt

2. **Use Python launcher:**
   ```bash
   py init_db.py
   py app.py
   ```

3. **Use full path:**
   ```bash
   C:\Python39\python.exe init_db.py
   C:\Python39\python.exe app.py
   ```

### Database Errors

**Error:** `sqlalchemy.exc.OperationalError: no such table: user`

**Solution:**
```bash
# Delete the existing database file
rm crm.db

# Reinitialize the database
python init_db.py
```

### Port Already in Use

**Error:** `Address already in use`

**Solutions:**
1. **Find and kill the process:**
   ```bash
   # Windows
   netstat -ano | findstr :5000
   taskkill /PID <PID> /F

   # macOS/Linux
   lsof -i :5000
   kill -9 <PID>
   ```

2. **Use a different port:**
   ```bash
   python app.py --port 5001
   ```

### Import Errors

**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or install individually
pip install Flask Flask-SQLAlchemy Flask-Login Flask-WTF WTForms Werkzeug email-validator python-dotenv
```

### Permission Errors

**Error:** `Permission denied`

**Solutions:**
1. **Run as administrator (Windows)**
2. **Use virtual environment:**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

## 📁 Project Structure

```
Simple-CRM/
├── app.py                 # Main Flask application
├── init_db.py            # Database initialization script
├── run.py                # Application runner
├── setup.bat             # Windows setup script
├── requirements.txt      # Python dependencies
├── README.md            # Main documentation
├── SETUP_GUIDE.md       # This file
├── templates/           # HTML templates
└── crm.db              # SQLite database (auto-created)
```

## 🔒 Security Notes

- Change the default admin password after first login
- The secret key in `app.py` should be changed for production
- Database file (`crm.db`) contains sensitive data - keep it secure

## 🚀 Production Deployment

For production use:

1. **Set environment variables:**
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-secure-secret-key
   ```

2. **Use a production WSGI server:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. **Set up a reverse proxy (Nginx/Apache)**

4. **Use a production database (PostgreSQL/MySQL)**

## 📞 Support

If you encounter issues:

1. Check this setup guide
2. Review the main README.md
3. Check Python and dependency versions
4. Ensure all files are in the correct locations
5. Try the troubleshooting steps above

## 🎯 Next Steps

After successful setup:

1. **Explore the dashboard** to see sample data
2. **Add your own contacts, accounts, and opportunities**
3. **Create custom objects** for your specific needs
4. **Customize the interface** by modifying templates
5. **Add new features** by extending the Flask routes

---

**Happy CRM-ing! 🎉** 