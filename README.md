# 🚀 Simple CRM System

A comprehensive Customer Relationship Management (CRM) system built with Python Flask, featuring advanced user management, permission sets, and custom objects.

## ✨ Features

- 🔐 **User Management**: Create and manage users with roles and permissions
- 🛡️ **Permission Sets**: Reusable permission collections for efficient user management
- 📊 **Standard Objects**: Contacts, Accounts, Opportunities, and Leads
- ⚙️ **Custom Objects**: Create custom objects with dynamic fields
- 🎨 **Modern UI**: Bootstrap 5 and Font Awesome icons
- 📱 **Responsive Design**: Works on desktop and mobile devices

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/simple-crm.git
   cd simple-crm
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Open your browser and go to `http://localhost:5000`
   - Login with: `admin` / `admin123`

### Cloud Deployment

#### Railway (Recommended - Free)
1. **Fork this repository** to your GitHub account
2. **Go to Railway:** https://railway.app
3. **Click "Start a New Project"**
4. **Choose "Deploy from GitHub repo"**
5. **Select your repository**
6. **Click "Deploy"**

See [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) for detailed instructions.

### 🔧 Troubleshooting

If you encounter issues:

- **Python not found:** Install Python from https://www.python.org/downloads/ and check "Add Python to PATH"
- **Database errors:** Run `python init_db.py` to reinitialize the database
- **Import errors:** Reinstall dependencies with `pip install -r requirements.txt`
- **Port conflicts:** Use a different port or kill existing processes
- **Template errors:** The application includes custom Jinja2 filters for JSON handling

For detailed troubleshooting, see [SETUP_GUIDE.md](SETUP_GUIDE.md).

## 📋 Default Login Credentials

- **Username**: admin
- **Password**: admin123

## 🏗️ Project Structure

```
Simple-CRM/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── dashboard.html    # Main dashboard
│   ├── contacts.html     # Contacts list
│   ├── contact_form.html # Contact add/edit form
│   ├── accounts.html     # Accounts list
│   ├── account_form.html # Account add/edit form
│   ├── opportunities.html # Opportunities list
│   ├── opportunity_form.html # Opportunity add/edit form
│   ├── leads.html        # Leads list
│   ├── lead_form.html    # Lead add/edit form
│   ├── custom_objects.html # Custom objects management
│   ├── custom_object_form.html # Custom object creation
│   ├── custom_records.html # Custom records list
│   └── custom_record_form.html # Custom record creation
└── crm.db               # SQLite database (created automatically)
```

## 🎯 Usage Guide

### Getting Started

1. **Login**: Use the default admin credentials to access the system
2. **Dashboard**: View overview statistics and recent activities
3. **Navigation**: Use the sidebar to access different modules

### Managing Standard Objects

#### Contacts
- Add new contacts with personal and company information
- Edit existing contact details
- View contact list with search and filter capabilities

#### Accounts
- Create company/organization records
- Track industry, revenue, and employee information
- Link accounts to opportunities and contacts

#### Opportunities
- Track sales opportunities through different stages
- Set amounts, probabilities, and close dates
- Link to accounts and contacts

#### Leads
- Manage potential customer leads
- Track lead sources and status
- Convert leads to opportunities

### Custom Objects

#### Creating Custom Objects
1. Navigate to "Custom Objects" in the sidebar
2. Click "New Custom Object"
3. Define object name, label, and description
4. Add custom fields with appropriate types
5. Save the custom object

#### Managing Custom Records
1. Select a custom object from the list
2. View existing records or add new ones
3. Use the dynamic forms to enter data

## 🔧 Configuration

### Database
- The application uses SQLite by default
- Database file (`crm.db`) is created automatically
- No additional database setup required

### Security
- Change the default admin password after first login
- The secret key can be modified in `app.py`
- Password hashing uses Werkzeug's security functions

## 🎨 Customization

### Styling
- Modify CSS variables in `templates/base.html` for theme colors
- Customize Bootstrap classes for layout changes
- Add custom CSS for specific styling needs

### Adding Features
- Extend the Flask routes in `app.py`
- Add new templates in the `templates/` directory
- Modify database models for additional fields

## 🔒 Security Features

- Password hashing with Werkzeug
- Session management with Flask-Login
- CSRF protection with Flask-WTF
- Input validation and sanitization
- SQL injection protection with SQLAlchemy

## 📱 Responsive Design

- Mobile-friendly interface
- Responsive tables and forms
- Touch-friendly navigation
- Optimized for all screen sizes

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
1. Set `debug=False` in `app.py`
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Configure a reverse proxy (Nginx, Apache)
4. Set up environment variables for security

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the documentation
2. Review existing issues
3. Create a new issue with detailed information

## 🔄 Updates

- Regular updates and improvements
- New features and bug fixes
- Security patches and enhancements

---

**Simple CRM** - A powerful, flexible CRM solution for modern businesses. 