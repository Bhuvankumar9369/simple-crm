@echo off
echo 🚀 Simple CRM - GitHub Deployment Helper
echo ========================================

echo.
echo 📋 Step 1: Initialize Git Repository
echo ------------------------------------
git init
git add .
git commit -m "Initial commit - Simple CRM with user management"

echo.
echo 📋 Step 2: GitHub Repository Setup
echo -----------------------------------
echo Please follow these steps:
echo 1. Go to https://github.com
echo 2. Click "+" and select "New repository"
echo 3. Name it: simple-crm
echo 4. Make it Public
echo 5. Don't initialize with README
echo 6. Click "Create repository"
echo.
echo After creating the repository, copy the repository URL
echo and run the next command with your repository URL.

echo.
echo 📋 Step 3: Connect to GitHub (Run this after creating repo)
echo -----------------------------------------------------------
echo git remote add origin https://github.com/YOUR_USERNAME/simple-crm.git
echo git push -u origin main

echo.
echo 📋 Step 4: Deploy to Railway
echo -----------------------------
echo 1. Go to https://railway.app
echo 2. Click "Start a New Project"
echo 3. Choose "Deploy from GitHub repo"
echo 4. Select your simple-crm repository
echo 5. Click "Deploy"

echo.
echo 🎉 Your Simple CRM will be live soon!
pause 