# 🚀 VS Code + Git + GitHub + Railway Deployment Guide

## 📋 Prerequisites

1. **VS Code** - Download from https://code.visualstudio.com
2. **Git** - Download from https://git-scm.com/download/win
3. **GitHub Account** - Sign up at https://github.com

## 🔧 Step-by-Step VS Code Deployment

### Step 1: Open Project in VS Code

1. **Open VS Code**
2. **File → Open Folder**
3. **Navigate to your project folder:**
   ```
   C:\Users\2052443\OneDrive - Cognizant\Desktop\My Personal Project AI\Simple CRM
   ```
4. **Click "Select Folder"**

### Step 2: Initialize Git Repository

1. **Press `Ctrl+Shift+P`** to open Command Palette
2. **Type:** `Git: Initialize Repository`
3. **Press Enter**
4. **Select your project folder**

### Step 3: Create GitHub Repository

1. **Go to GitHub:** https://github.com
2. **Click "+" → "New repository"**
3. **Fill in details:**
   - Repository name: `simple-crm`
   - Description: `Simple CRM with user management and permission sets`
   - **Make it Public** ✅
   - **Don't check** any initialization options
4. **Click "Create repository"**
5. **Copy the repository URL**

### Step 4: Connect to GitHub

1. **In VS Code**, press `Ctrl+Shift+P`
2. **Type:** `Git: Add Remote`
3. **Press Enter**
4. **Remote name:** `origin`
5. **Remote URL:** `https://github.com/YOUR_USERNAME/simple-crm.git`

### Step 5: Stage Files

1. **Click Source Control icon** in left sidebar (branch icon)
2. **You'll see all files listed**
3. **Click "+" next to each file** to stage them
4. **Or click "Stage All Changes"** to stage everything

### Step 6: Commit Files

1. **Enter commit message:** `Initial commit - Simple CRM`
2. **Click checkmark (✓)** to commit

### Step 7: Push to GitHub

1. **Click "..." menu** in Source Control panel
2. **Select "Push"**
3. **Sign in to GitHub** if prompted
4. **Authorize VS Code** to access GitHub
5. **Code will be pushed to GitHub!**

## 🚀 Deploy to Railway

### Step 1: Deploy from GitHub

1. **Go to Railway:** https://railway.app
2. **Click "Start a New Project"**
3. **Click "Deploy from GitHub repo"**
4. **Sign in with GitHub**
5. **Select your `simple-crm` repository**
6. **Click "Deploy"**

### Step 2: Configure Environment Variables

1. **Click on your project** in Railway dashboard
2. **Click "Variables" tab**
3. **Add variable:**
   - Key: `SECRET_KEY`
   - Value: `your-super-secret-key-here`
4. **Click "Add"**

### Step 3: Add Database

1. **Click "New" → "Database"**
2. **Choose "PostgreSQL"**
3. **Railway will auto-set DATABASE_URL**

### Step 4: Initialize Database

1. **Go to "Deployments" tab**
2. **Click on latest deployment**
3. **Click "View Logs"**
4. **Add command:**
   ```bash
   python -c "from app import init_app; init_app()"
   ```

### Step 5: Access Your App

1. **Click on your service**
2. **Click "Generate Domain"**
3. **Your CRM is live!**

## 🎯 VS Code Git Commands

### Essential Commands

| Action | Command Palette | Description |
|--------|----------------|-------------|
| Initialize Git | `Git: Initialize Repository` | Start Git in project |
| Add Remote | `Git: Add Remote` | Connect to GitHub |
| Stage All | `Git: Stage All Changes` | Stage all files |
| Commit | `Git: Commit` | Commit staged files |
| Push | `Git: Push` | Push to GitHub |
| Pull | `Git: Pull` | Pull from GitHub |

### Keyboard Shortcuts

| Action | Shortcut | Description |
|--------|----------|-------------|
| Command Palette | `Ctrl+Shift+P` | Open command palette |
| Source Control | `Ctrl+Shift+G` | Open Git panel |
| Quick Open | `Ctrl+P` | Quick file search |
| Terminal | `Ctrl+`` | Open terminal |

## 🛠️ Troubleshooting

### Git Not Found
1. **Install Git:** https://git-scm.com/download/win
2. **Restart VS Code**
3. **Check Git installation:** `git --version`

### GitHub Authentication
1. **Use GitHub CLI:** Install from https://cli.github.com
2. **Or use Personal Access Token:**
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - Generate new token
   - Use token as password

### Push Fails
1. **Check remote URL:** `git remote -v`
2. **Check authentication**
3. **Try:** `git push -u origin main`

### Railway Deployment Fails
1. **Check logs** in Railway dashboard
2. **Verify all files** are in GitHub
3. **Check environment variables**

## 📊 VS Code Extensions (Recommended)

1. **GitLens** - Enhanced Git capabilities
2. **GitHub Pull Requests** - Manage PRs in VS Code
3. **Python** - Python language support
4. **Auto Rename Tag** - HTML tag renaming
5. **Bracket Pair Colorizer** - Color-coded brackets

## 🎉 Success Checklist

- ✅ Project opened in VS Code
- ✅ Git repository initialized
- ✅ GitHub repository created
- ✅ Remote added to VS Code
- ✅ Files staged and committed
- ✅ Code pushed to GitHub
- ✅ Railway deployment started
- ✅ Environment variables set
- ✅ Database added
- ✅ Database initialized
- ✅ App accessible via URL

## 🔐 Login Credentials
- **Username:** `admin`
- **Password:** `admin123`

## 📞 Need Help?

- **VS Code docs:** https://code.visualstudio.com/docs
- **Git docs:** https://git-scm.com/doc
- **Railway docs:** https://docs.railway.app
- **Check logs:** Always check logs first!

---

**Happy Coding with VS Code! 🚀** 