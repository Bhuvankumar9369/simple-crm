# 🚀 Heroku Deployment Guide for Simple CRM

This guide will help you deploy your Simple CRM application to Heroku.

## 📋 Prerequisites

1. **Heroku Account** - Sign up at [heroku.com](https://heroku.com)
2. **Heroku CLI** - Install from [devcenter.heroku.com](https://devcenter.heroku.com/articles/heroku-cli)
3. **Git** - Make sure your project is in a Git repository

## 🔧 Step-by-Step Deployment

### 1. **Prepare Your Project**

Make sure you have all the required files:
- ✅ `app.py` - Main application file
- ✅ `requirements.txt` - Python dependencies
- ✅ `Procfile` - Tells Heroku how to run your app
- ✅ `runtime.txt` - Python version specification
- ✅ `templates/` - All HTML templates
- ✅ `.gitignore` - Git ignore file

### 2. **Initialize Git (if not already done)**

```bash
git init
git add .
git commit -m "Initial commit for Heroku deployment"
```

### 3. **Login to Heroku**

```bash
heroku login
```

### 4. **Create Heroku App**

```bash
heroku create your-crm-app-name
```

Replace `your-crm-app-name` with your desired app name (must be unique).

### 5. **Add PostgreSQL Database**

```bash
heroku addons:create heroku-postgresql:mini
```

### 6. **Set Environment Variables**

```bash
heroku config:set SECRET_KEY="your-super-secret-key-here"
```

Generate a strong secret key:
```python
import secrets
print(secrets.token_hex(32))
```

### 7. **Deploy to Heroku**

```bash
git push heroku main
```

If your branch is called `master` instead of `main`:
```bash
git push heroku master
```

### 8. **Run Database Migrations**

```bash
heroku run python -c "from app import init_app; init_app()"
```

### 9. **Open Your App**

```bash
heroku open
```

## 🔐 **Default Login Credentials**

After deployment, you can login with:
- **Username:** `admin`
- **Password:** `admin123`

## 🛠️ **Troubleshooting**

### **Common Issues:**

#### **1. Build Failed**
```bash
# Check build logs
heroku logs --tail
```

#### **2. Database Connection Issues**
```bash
# Check database status
heroku pg:info
```

#### **3. App Crashes**
```bash
# Check application logs
heroku logs --tail
```

#### **4. Database Not Initialized**
```bash
# Manually initialize database
heroku run python -c "from app import db, User; db.create_all()"
heroku run python -c "from app import initialize_database; initialize_database()"
```

## 📊 **Monitoring Your App**

### **View Logs**
```bash
heroku logs --tail
```

### **Check App Status**
```bash
heroku ps
```

### **Restart App**
```bash
heroku restart
```

## 🔄 **Updating Your App**

When you make changes:

```bash
git add .
git commit -m "Update description"
git push heroku main
```

## 💰 **Cost Considerations**

- **Free Tier**: No longer available on Heroku
- **Basic Dyno**: ~$7/month
- **PostgreSQL Mini**: ~$5/month
- **Total**: ~$12/month

## 🚀 **Alternative Free Hosting**

If you want free hosting, consider:
- **Railway** - Free tier available
- **Render** - Free tier available
- **PythonAnywhere** - Free tier available

## 📝 **Environment Variables**

Your app uses these environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | `your-secret-key-here` |
| `DATABASE_URL` | Database connection | Auto-set by Heroku |

## 🔒 **Security Notes**

1. **Change Default Password** - Change admin password after first login
2. **Use Strong Secret Key** - Generate a strong SECRET_KEY
3. **Enable HTTPS** - Heroku provides SSL automatically
4. **Regular Updates** - Keep dependencies updated

## 📞 **Support**

If you encounter issues:
1. Check Heroku logs: `heroku logs --tail`
2. Verify all files are committed
3. Ensure database is properly initialized
4. Check environment variables are set

## 🎉 **Success!**

Once deployed, your Simple CRM will be available at:
`https://your-crm-app-name.herokuapp.com`

---

**Happy Deploying! 🚀** 