# Quick Start Guide - Deploy in 5 Minutes

## Prerequisites
- GitHub account
- Git installed on your computer

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `calm-wiki` (or your preferred name)
3. Description: "CALM Microscopy Wiki"
4. Set to **Public** (required for free GitHub Pages)
5. **DO NOT** check "Initialize with README"
6. Click "Create repository"

## Step 2: Push Your Wiki

Open terminal/command prompt and run:

```bash
cd C:\Users\NIC-ADMIN4\Workspace\wiki

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: CALM Microscopy Wiki with 80 pages"

# Connect to your GitHub repo (REPLACE WITH YOUR URL)
git remote add origin https://github.com/YOUR-USERNAME/calm-wiki.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** (top menu)
3. Click **Pages** (left sidebar)
4. Under "Build and deployment":
   - Source: Select **GitHub Actions**
5. Click **Save**

## Step 4: Wait for Build

1. Go to **Actions** tab in your repository
2. You should see "Deploy Jekyll with GitHub Pages" workflow running
3. Wait 2-3 minutes for it to complete (green checkmark)

## Step 5: View Your Site

Your site will be live at:
```
https://YOUR-USERNAME.github.io/calm-wiki/
```

## That's It!

Your wiki is now live with:
- ✅ 80 organized pages across 6 categories
- ✅ Persistent left sidebar navigation
- ✅ Clean, professional theme
- ✅ Mobile responsive design
- ✅ Automatic HTTPS
- ✅ Free hosting

## Next Steps

1. **Add a logo**: Place `logo.jpg` in `assets/img/` folder
2. **Update links**: Edit `_config.yml` to add your GitHub/contact links
3. **Review content**: Check pages for any remaining formatting issues
4. **Share**: Send the URL to your team

## Making Updates

After making changes to any files:

```bash
cd C:\Users\NIC-ADMIN4\Workspace\wiki
git add .
git commit -m "Description of changes"
git push
```

The site will automatically rebuild in 2-3 minutes.

## Need Help?

- See `SETUP.md` for detailed documentation
- GitHub Pages: https://docs.github.com/pages
- Jekyll: https://jekyllrb.com/docs/
