# 🚀 GitHub + Railway Deployment Guide

## 📋 Step-by-Step Instructions

### Step 1: Create GitHub Account
1. **Go to:** https://github.com
2. **Click "Sign up"**
3. **Enter your details:**
   - Email address
   - Password
   - Username (choose carefully - this will be your GitHub username)
4. **Verify your email** (check your inbox)

### Step 2: Create GitHub Repository
1. **Go to GitHub** (after signing up)
2. **Click the "+" icon** in the top right corner
3. **Select "New repository"**
4. **Fill in the details:**
   - Repository name: `simple-crm`
   - Description: `Simple CRM with user management and permission sets`
   - **Make it Public** ✅
   - **Don't check** "Add a README file"
   - **Don't check** "Add .gitignore"
   - **Don't check** "Choose a license"
5. **Click "Create repository"**

### Step 3: Upload Your Files
1. **In your new repository**, you'll see a page with upload options
2. **Click "uploading an existing file"**
3. **Drag and drop these files:**
   - `app.py`
   - `requirements.txt`
   - `Procfile`
   - `runtime.txt`
   - `railway.json`
   - `render.yaml`
   - `fly.toml`
   - `vercel.json`
   - `HEROKU_DEPLOYMENT.md`
   - `RAILWAY_DEPLOYMENT.md`
   - `README.md`
   - `.gitignore`
   - **Entire `templates/` folder** (drag the whole folder)
4. **Add a commit message:** `Initial commit - Simple CRM`
5. **Click "Commit changes"**

### Step 4: Deploy to Railway
1. **Go to Railway:** https://railway.app
2. **Click "Start a New Project"**
3. **Click "Deploy from GitHub repo"**
4. **Sign in with GitHub** (click "Continue with GitHub")
5. **Authorize Railway** to access your GitHub
6. **Select your repository** (`simple-crm`)
7. **Click "Deploy"**
8. **Wait for deployment** (2-3 minutes)

### Step 5: Configure Environment Variables
1. **In Railway dashboard**, click on your project
2. **Click "Variables" tab**
3. **Add this variable:**
   - Key: `SECRET_KEY`
   - Value: `your-super-secret-key-here`
4. **Click "Add"**

**Generate a secret key:**
- Go to: https://www.python.org/shell/
- Run this code:
```python
import secrets
print(secrets.token_hex(32))
```
- Copy the output and use it as your SECRET_KEY

### Step 6: Add Database
1. **Click "New" → "Database"**
2. **Choose "PostgreSQL"**
3. **Railway will automatically set DATABASE_URL**

### Step 7: Initialize Database
1. **Go to "Deployments" tab**
2. **Click on your latest deployment**
3. **Click "View Logs"**
4. **Add this command:**
```bash
python -c "from app import init_app; init_app()"
```

### Step 8: Access Your App
1. **Click on your service**
2. **Click "Generate Domain"**
3. **Your CRM is live!**

## 🔐 Login Credentials
- **Username:** `admin`
- **Password:** `admin123`

## 🎉 Success!
Your Simple CRM will be available at:
`https://your-app-name.railway.app`

## 🛠️ Troubleshooting

### If deployment fails:
1. **Check logs** in Railway dashboard
2. **Verify all files** are uploaded to GitHub
3. **Check environment variables** are set correctly

### If database doesn't work:
1. **Add PostgreSQL** from Railway dashboard
2. **Check DATABASE_URL** is set
3. **Initialize database** manually

### If app doesn't start:
1. **Check Procfile** is correct
2. **Verify gunicorn** is in requirements.txt
3. **Check logs** for error messages

## 📞 Need Help?
- **Railway docs:** https://docs.railway.app
- **GitHub docs:** https://docs.github.com
- **Check logs:** Always check the logs first!

---

**Happy Deploying! 🚀** 