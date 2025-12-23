# Deployment Checklist

Use this checklist to ensure smooth deployment of your CALM Microscopy Wiki.

## Pre-Deployment

- [ ] Review `QUICK_START.md` for deployment steps
- [ ] Review `SETUP.md` for detailed configuration options
- [ ] Read `MIGRATION_SUMMARY.md` to understand what was done
- [ ] Have GitHub account ready
- [ ] Have Git installed and configured

## Deployment Steps

- [ ] **Create GitHub repository**
  - Name: `calm-wiki` (or your choice)
  - Visibility: Public (required for free GitHub Pages)
  - Do NOT initialize with README

- [ ] **Push to GitHub**
  ```bash
  cd C:\Users\NIC-ADMIN4\Workspace\wiki
  git init
  git add .
  git commit -m "Initial commit: CALM Microscopy Wiki"
  git remote add origin https://github.com/YOUR-USERNAME/calm-wiki.git
  git branch -M main
  git push -u origin main
  ```

- [ ] **Enable GitHub Pages**
  - Go to repository Settings → Pages
  - Source: GitHub Actions
  - Save

- [ ] **Wait for deployment**
  - Check Actions tab
  - Wait for green checkmark (2-3 minutes)

- [ ] **Verify site is live**
  - Visit: `https://YOUR-USERNAME.github.io/calm-wiki/`
  - Check home page loads
  - Test sidebar navigation
  - Click through a few pages

## Post-Deployment Configuration

- [ ] **Add logo** (optional)
  - Place logo file in `assets/img/logo.jpg`
  - Commit and push
  - Verify it appears in sidebar

- [ ] **Update _config.yml** (optional)
  - Update GitHub link in platforms section
  - Add any additional social links
  - Customize description if needed
  - Commit and push

- [ ] **Test navigation**
  - Click through all main navigation items
  - Test sublist items
  - Verify all links work
  - Note any broken links for fixing

- [ ] **Review home page**
  - Check index.md content is appropriate
  - Update welcome message if needed
  - Verify quick links work

## Content Review

- [ ] **Check key pages**
  - Main category pages (6 total)
  - Most important microscope pages
  - Frequently accessed protocols
  - User guides

- [ ] **Fix formatting issues**
  - Look for remaining `[[brackets]]`
  - Remove any stray HTML/CSS
  - Fix broken internal links
  - Add missing images

- [ ] **Verify attachments**
  - Note pages marked with "(attachment)"
  - Upload actual attachment files to `assets/`
  - Update markdown links

## Optional Enhancements

- [ ] **Custom domain** (if desired)
  - Add CNAME file with your domain
  - Configure DNS settings
  - Update in GitHub Pages settings
  - Verify HTTPS works

- [ ] **Analytics** (if desired)
  - Add Google Analytics tracking ID
  - Update `_includes/head-custom.html`
  - Verify tracking works

- [ ] **Search functionality** (if desired)
  - Consider adding lunr.js or similar
  - Requires custom implementation

- [ ] **Comments** (if desired)
  - Consider Disqus or utterances
  - Add to layout template

## Team Onboarding

- [ ] **Create team documentation**
  - How to request page updates
  - How to submit new content
  - Style guide for consistency

- [ ] **Train content editors**
  - How to edit markdown files
  - How to commit and push changes
  - How to check build status

- [ ] **Set up workflows**
  - Content review process
  - Update approval process
  - Maintenance schedule

## Maintenance Plan

- [ ] **Regular reviews**
  - Schedule quarterly content review
  - Update outdated information
  - Archive deprecated pages

- [ ] **Monitor**
  - Check Actions for failed builds
  - Review broken link reports
  - Update dependencies periodically

- [ ] **Backup**
  - Repository is auto-backed up on GitHub
  - Consider local backup of source files
  - Document any custom changes

## Launch

- [ ] **Announce to team**
  - Email with site URL
  - Quick tour of navigation
  - How to request updates

- [ ] **Update old wiki**
  - Add redirect or notice on Confluence
  - Point users to new site
  - Set timeline for Confluence shutdown

- [ ] **Collect feedback**
  - Create feedback mechanism
  - Track common questions
  - Plan improvements

## Success Metrics

After launch, track:
- [ ] Page views (if analytics enabled)
- [ ] User feedback
- [ ] Number of content updates
- [ ] Broken link reports
- [ ] Team satisfaction

## Troubleshooting

If deployment fails:
1. Check Actions tab for error logs
2. Verify _config.yml syntax
3. Ensure all files are committed
4. Check GitHub Pages settings
5. Review `SETUP.md` troubleshooting section

## Completed!

Date deployed: _______________
Deployed by: _______________
Site URL: _______________
Repository: _______________

Notes:
_________________________________
_________________________________
_________________________________
