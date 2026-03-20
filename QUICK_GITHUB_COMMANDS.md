# Quick GitHub Push Commands

## If you prefer manual commands, use these:

### Step 1: Initialize Git
```bash
cd c:\Users\KIIT0001\OneDrive\Desktop\tryingit
git init
```

### Step 2: Add Files
```bash
git add .
git status
```

### Step 3: Commit
```bash
git commit -m "Initial commit: India Carbon Emissions Tracker for MoSPI portfolio"
```

### Step 4: Create Repo on GitHub
1. Go to: https://github.com/new
2. Name: `india-carbon-emissions-tracker`
3. Description: `AI-powered dashboard tracking India's state-wise carbon emissions with ML forecasting for MoSPI portfolio`
4. Click "Create repository"

### Step 5: Push to GitHub
Replace `YOUR-USERNAME` with your GitHub username:

```bash
git remote add origin https://github.com/YOUR-USERNAME/india-carbon-emissions-tracker.git
git branch -M main
git push -u origin main
```

### Step 6: Enter Credentials
- **Username**: Your GitHub username
- **Password**: Use a Personal Access Token from https://github.com/settings/tokens

---

## Future Updates

After making changes:

```bash
git add .
git commit -m "Description of what changed"
git push
```

---

## Deploy to Streamlit Cloud (Optional)

1. Go to: https://share.streamlit.io/
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Main file: `app.py`
6. Click "Deploy"

Your app will be live at: `https://YOUR-USERNAME-india-carbon-emissions-tracker.streamlit.app`

---

## That's it! 🚀

Your project is now:
- ✅ Backed up on GitHub
- ✅ Visible to recruiters
- ✅ Ready for deployment
- ✅ Portfolio-ready
