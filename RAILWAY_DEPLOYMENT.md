# 🚀 Railway Deployment Guide for Simple CRM

Railway is the easiest alternative to Heroku with a generous free tier!

## 📋 Prerequisites

1. **GitHub Account** - Sign up at [github.com](https://github.com)
2. **Railway Account** - Sign up at [railway.app](https://railway.app)

## 🔧 Step-by-Step Deployment

### 1. **Prepare Your Project**

Make sure your project is in a GitHub repository:

```bash
# Initialize Git (if not already done)
git init
git add .
git commit -m "Initial commit"

# Create GitHub repository and push
# Go to github.com and create a new repository
git remote add origin https://github.com/yourusername/your-repo-name.git
git push -u origin main
```

### 2. **Sign Up for Railway**

1. **Visit Railway:** https://railway.app
2. **Click "Start a New Project"**
3. **Sign up with GitHub** (recommended)
4. **Authorize Railway** to access your GitHub

### 3. **Deploy Your App**

1. **Click "Deploy from GitHub repo"**
2. **Select your repository**
3. **Railway will automatically detect Python**
4. **Click "Deploy"**

### 4. **Configure Environment Variables**

1. **Go to your project dashboard**
2. **Click "Variables" tab**
3. **Add these variables:**

```
SECRET_KEY=your-super-secret-key-here
```

Generate a secret key:
```python
import secrets
print(secrets.token_hex(32))
```

### 5. **Add Database (Optional)**

1. **Click "New" → "Database"**
2. **Choose "PostgreSQL"**
3. **Railway will automatically set DATABASE_URL**

### 6. **Initialize Database**

1. **Go to "Deployments" tab**
2. **Click on your latest deployment**
3. **Click "View Logs"**
4. **Add this command to initialize database:**

```bash
python -c "from app import init_app; init_app()"
```

### 7. **Access Your App**

1. **Click on your service**
2. **Click "Generate Domain"**
3. **Your app is live!**

## 🔐 **Default Login Credentials**

After deployment, login with:
- **Username:** `admin`
- **Password:** `admin123`

## 🆓 **Railway Free Tier**

- **$5 credit monthly**
- **Enough for small apps**
- **No credit card required**
- **Automatic deployments**

## 🛠️ **Troubleshooting**

### **Build Failed**
1. **Check logs** in Railway dashboard
2. **Verify requirements.txt** is correct
3. **Check Python version** in runtime.txt

### **Database Issues**
1. **Add PostgreSQL** from Railway dashboard
2. **Check DATABASE_URL** environment variable
3. **Initialize database** manually

### **App Not Starting**
1. **Check Procfile** is correct
2. **Verify gunicorn** is in requirements.txt
3. **Check logs** for error messages

## 📊 **Monitoring**

### **View Logs**
- Go to your service dashboard
- Click "Deployments" tab
- Click on any deployment to view logs

### **Check Status**
- Green dot = Running
- Red dot = Failed
- Yellow dot = Building

## 🔄 **Updating Your App**

1. **Make changes** to your code
2. **Commit and push** to GitHub
3. **Railway automatically deploys** new version

## 💰 **Cost**

- **Free tier:** $5 credit monthly
- **Small app:** Usually free
- **Upgrade:** Only if needed

## 🎉 **Success!**

Your Simple CRM will be available at:
`https://your-app-name.railway.app`

---

**Happy Deploying on Railway! 🚀** 