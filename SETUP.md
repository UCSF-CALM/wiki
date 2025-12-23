# CALM Microscopy Wiki - Setup Guide

This document explains how to deploy your CALM Microscopy Wiki to GitHub Pages.

## Overview

Your wiki has been configured with:
- **82 cleaned markdown pages** from your Confluence export
- **6 main categories** with organized navigation
- **Persistent left sidebar** with category-based navigation
- **Jekyll minimalistic theme** (forked version)
- **GitHub Pages deployment** ready to go

## Directory Structure

```
wiki/
├── _config.yml                   # Main Jekyll configuration
├── _layouts/                     # Page layouts
├── _includes/                    # Reusable components (header, footer, sidebar)
├── _sass/                        # Stylesheets
├── assets/                       # CSS, JS, images
├── pages/                        # All wiki content organized by category
│   ├── microscopes/              # 27 microscope pages
│   ├── data-analysis/            # 18 data analysis pages
│   ├── sample-preparation/       # 16 sample prep pages
│   ├── references-and-education/ # 11 education pages
│   ├── calm-information/         # 4 info pages
│   └── miscellaneous/            # 4 misc pages
├── index.md                      # Home page
└── .github/workflows/            # GitHub Actions for deployment

Categories:
1. **Microscopes** - All microscope-specific pages (CSU-W1, OMX-SR, TIRF, etc.)
2. **Data Analysis** - Analysis tools, workstations, Fiji, Huygens, MATLAB
3. **Sample Preparation** - Dyes, protocols, clearing methods, fixation
4. **References & Education** - Courses, books, presentations, method examples
5. **CALM Information** - User guides, iLab, acknowledgements
6. **Miscellaneous** - PSFs, fabrication resources, equipment
```

## GitHub Pages Deployment

### Option 1: Deploy to Your Own Repository (Recommended)

1. **Create a new GitHub repository**:
   ```bash
   # On GitHub, create a new repository (e.g., "calm-wiki")
   # DO NOT initialize with README, .gitignore, or license
   ```

2. **Initialize and push your wiki**:
   ```bash
   cd wiki
   git init
   git add .
   git commit -m "Initial commit: CALM Microscopy Wiki

   - Imported 82 pages from Confluence
   - Organized into 6 main categories
   - Configured Jekyll minimalistic theme
   - Added persistent sidebar navigation"

   git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
   git branch -M main
   git push -u origin main
   ```

3. **Enable GitHub Pages**:
   - Go to your repository on GitHub
   - Navigate to **Settings** → **Pages**
   - Under "Build and deployment":
     - Source: **GitHub Actions**
   - The site will automatically build and deploy

4. **Access your site**:
   - URL: `https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/`
   - Build status: Check **Actions** tab

### Option 2: Deploy to Organization Account

If deploying under `ucsf` or organization account:

1. Create repo as `ORGANIZATION/calm-wiki`
2. Follow same steps as above
3. URL will be: `https://ORGANIZATION.github.io/calm-wiki/`

### Option 3: Custom Domain

To use a custom domain (e.g., `wiki.calm.ucsf.edu`):

1. Add a `CNAME` file to the `wiki/` directory:
   ```bash
   echo "wiki.calm.ucsf.edu" > CNAME
   git add CNAME
   git commit -m "Add custom domain"
   git push
   ```

2. Configure DNS:
   - Add a CNAME record pointing to `YOUR-USERNAME.github.io`
   - Or A records pointing to GitHub Pages IPs

3. Enable HTTPS in repository settings

## Configuration

### _config.yml

Key settings you may want to customize:

```yaml
title: Center For Advanced Light Microscopy Wiki (CALM) @ UCSF
logo: /assets/img/logo.jpg  # Add your logo to assets/img/
description: Wiki
favicon: true
color-scheme: auto  # Options: auto, light, dark

plugins:
  - jekyll-sitemap
  - jekyll-seo-tag
  - jemoji

platforms:
  - name: GitHub
    icon: <i class="fa-brands fa-github"></i>
    link: YOUR_GITHUB_URL  # Update this

navigation:
  # The 6-level category navigation is already configured
  # Edit to add/remove pages or reorganize structure
```

### Adding a Logo

1. Add your logo image to `wiki/assets/img/logo.jpg`
2. Update `_config.yml` if using a different filename
3. Recommended size: 200x200px or similar

### Updating Navigation

To add a new page to the navigation:

1. Add the page file to the appropriate category folder
2. Edit `_config.yml` navigation section:
   ```yaml
   - name: Category Name
     link: ./pages/category/main-page.html
     sublist:
       - name: New Page
         link: ./pages/category/new-page.html
   ```

## Local Development (Optional)

To test the site locally before pushing:

1. **Install Ruby** (version 3.2 or higher):
   - Windows: Download from https://rubyinstaller.org/
   - macOS: `brew install ruby`
   - Linux: Use package manager

2. **Install dependencies**:
   ```bash
   cd wiki
   bundle install
   ```

3. **Run local server**:
   ```bash
   bundle exec jekyll serve
   ```

4. **View site**:
   - Open http://localhost:4000 in your browser
   - Changes to files will auto-rebuild

## File Organization

### Adding New Pages

1. Create markdown file in appropriate category folder:
   ```markdown
   ---
   layout: default
   title: Your Page Title
   category: microscopes
   author: Your Name
   ---

   # Your Page Title

   Your content here...
   ```

2. Add to navigation in `_config.yml` if needed

### Internal Links

Use relative paths from the root:
```markdown
[Link to another page](./pages/microscopes/OMX-SR_517182062.html)
[Link to home](./index.html)
```

## Content Cleanup

The automated cleanup script removed most Confluence formatting, but some pages may still have:
- Nested brackets `[[text]]` - can be manually cleaned
- Attachment references marked as `(attachment)` - replace with actual files
- Some inline HTML/CSS remnants - can be removed

To further clean a page:
1. Open the markdown file in a text editor
2. Remove any remaining `{...}` attribute blocks
3. Fix any broken links
4. Add actual image files to `assets/img/` if needed

## Maintenance

### Updating Content

1. Edit markdown files directly in the `pages/` folders
2. Commit and push changes:
   ```bash
   git add .
   git commit -m "Update microscope information"
   git push
   ```

3. GitHub Actions will automatically rebuild and deploy

### Adding New Categories

1. Create new folder in `pages/`
2. Add pages to folder
3. Update `_config.yml` navigation
4. Commit and push

## Troubleshooting

### Build Failures

Check the **Actions** tab on GitHub for build logs. Common issues:
- YAML syntax errors in `_config.yml`
- Invalid liquid syntax in markdown files
- Missing dependencies

### Broken Links

- Ensure all internal links use relative paths
- Check that linked files exist in the `pages/` folders
- Verify `.html` extensions in links (Jekyll converts `.md` to `.html`)

### Images Not Showing

- Add images to `wiki/assets/img/`
- Use relative paths: `![Alt text](../assets/img/image.png)`
- Or absolute paths: `![Alt text](/assets/img/image.png)`

## Scripts Created

Two Python scripts were created to help with setup:

### clean_confluence_markdown.py
Cleans Confluence HTML/Pandoc formatting from exported markdown files.
- Removes div/span tags
- Extracts titles and metadata
- Creates Jekyll front matter
- Output: `wiki/pages/*.md`

### organize_by_category.py
Organizes cleaned files into category folders.
- Maps files to 6 main categories
- Creates category directories
- Copies files to appropriate locations
- Reports uncategorized files

## Next Steps

1. ✅ Review the home page (`index.md`) and customize as needed
2. ✅ Add your logo to `assets/img/logo.jpg`
3. ✅ Update the GitHub link in `_config.yml` platforms section
4. ✅ Create GitHub repository and push
5. ✅ Enable GitHub Pages in repository settings
6. ✅ Review built site and fix any broken links
7. ✅ Clean up any remaining Confluence artifacts in individual pages
8. ✅ Add any missing images to assets/img/
9. ✅ Configure custom domain (optional)
10. ✅ Share with team and gather feedback

## Support

For Jekyll/GitHub Pages help:
- Jekyll Documentation: https://jekyllrb.com/docs/
- GitHub Pages Documentation: https://docs.github.com/pages
- Theme Documentation: Check the original theme repository

## Credits

- Jekyll Theme: Minimalistic (forked)
- Content: Migrated from Confluence Wiki
- Migration Date: December 2025
