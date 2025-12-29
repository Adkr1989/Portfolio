# GitHub Portfolio Repository - Setup Instructions

## Step 1: Prepare Your Files

All files are ready in: `c:\Users\Arikl\claude-agent-sdk-intro\docs\portfolio\github-repo\`

### Current Structure:
```
github-repo/
├── README.md                          ✅ Created
├── .gitignore                         ✅ Created
├── docs/
│   ├── resume.html                    📝 Copy from parent folder
│   └── cv.html                        📝 Copy from parent folder
├── projects/
│   ├── evlv-grant-platform/
│   │   └── README.md                  ✅ Created
│   └── adev-dashboard/
│       └── README.md                  ✅ Created
└── code-samples/
    ├── claude-agent-sdk/
    │   └── multi_agent_orchestration.py  ✅ Created
    └── fastapi-patterns/
        └── websocket_streaming.py     ✅ Created
```

## Step 2: Copy Resume and CV

```bash
# Copy your resume and CV to the docs folder
cp c:/Users/Arikl/claude-agent-sdk-intro/docs/portfolio/resume.html c:/Users/Arikl/claude-agent-sdk-intro/docs/portfolio/github-repo/docs/
cp c:/Users/Arikl/claude-agent-sdk-intro/docs/portfolio/cv.html c:/Users/Arikl/claude-agent-sdk-intro/docs/portfolio/github-repo/docs/
```

## Step 3: Review and Sanitize Content

### Pre-Commit Security Checklist

Before initializing Git, verify NO sensitive data:

- [ ] No API keys in any files
- [ ] No client names (if sensitive)
- [ ] No database credentials
- [ ] No proprietary algorithms
- [ ] No real user data
- [ ] No internal URLs
- [ ] No .env files (use .env.example only)
- [ ] GitHub usernames/links updated in README.md

### Update Placeholders

Edit these files to add your real information:

**README.md:**
- Line 3: Update LinkedIn URL
- Line 4: Update email (already correct)
- Line 256: Update GitHub username
- Line 257: Update LinkedIn URL

**Resume.html & CV.html:**
- Line 286 (resume) / Line 286 (cv): Update GitHub URL
- Line 256 (resume) / Line 286 (cv): Update LinkedIn URL

## Step 4: Create GitHub Repository

### Option A: Using GitHub CLI (Recommended)

```bash
# Navigate to the portfolio folder
cd c:/Users/Arikl/claude-agent-sdk-intro/docs/portfolio/github-repo

# Initialize Git
git init

# Add all files
git add .

# Review what you're about to commit
git status
git diff --cached

# IMPORTANT: Check for secrets one more time
git diff --cached | grep -i "api_key\|password\|secret\|token"

# Create initial commit
git commit -m "Initial commit: AI Agent Developer Portfolio

- Add professional resume and CV
- Add 4 project showcases (EV_LV, ADEV, Consumer SaaS, Maine Scientific)
- Add sanitized code examples (multi-agent orchestration, WebSocket streaming)
- Include comprehensive .gitignore for security
- Add architecture documentation

🤖 Generated with Claude Code
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# Create GitHub repository
gh repo create ari-klopfer-portfolio --public --source=. --description "Professional portfolio showcasing AI Agent development, Claude SDK expertise, and production systems with measurable business impact" --push
```

### Option B: Using GitHub Web Interface

1. Go to https://github.com/new
2. Repository name: `ari-klopfer-portfolio`
3. Description: "Professional portfolio showcasing AI Agent development, Claude SDK expertise, and production systems"
4. Public repository
5. **DO NOT** initialize with README, .gitignore, or license (we have our own)
6. Click "Create repository"

Then push your local code:

```bash
cd c:/Users/Arikl/claude-agent-sdk-intro/docs/portfolio/github-repo

git init
git add .
git commit -m "Initial commit: AI Agent Developer Portfolio"

# Use the URL from the GitHub page
git remote add origin https://github.com/YOUR-USERNAME/ari-klopfer-portfolio.git
git branch -M main
git push -u origin main
```

## Step 5: Enable GitHub Pages

### Via GitHub Web Interface:

1. Go to repository Settings → Pages
2. Source: Deploy from a branch
3. Branch: `main` → folder: `/docs`
4. Click Save

Your portfolio will be available at:
`https://YOUR-USERNAME.github.io/ari-klopfer-portfolio/`

### Via GitHub CLI:

```bash
gh repo edit --enable-pages --pages-branch main --pages-path /docs
```

## Step 6: Add Topics to Repository

Make your repo discoverable:

```bash
gh repo edit --add-topic ai-agents
gh repo edit --add-topic claude-sdk
gh repo edit --add-topic portfolio
gh repo edit --add-topic python
gh repo edit --add-topic typescript
gh repo edit --add-topic fastapi
gh repo edit --add-topic anthropic
```

Or via web interface:
Settings → About → Topics → Add:
- `ai-agents`
- `claude-sdk`
- `portfolio`
- `python`
- `typescript`
- `fastapi`
- `anthropic`
- `mcp-servers`

## Step 7: Create Repository Social Card

1. Go to Settings → About
2. Click "Edit"
3. Add a description:
   > "AI Agent Developer portfolio: Claude SDK, multi-agent orchestration, production systems. 75K+ lines of code, $500/mo MRR. Real projects, sanitized examples."

4. Add website: Your LinkedIn or personal site
5. Add topics (see Step 6)

## Step 8: Add README Badges (Optional)

Add these to your README.md for a professional look:

```markdown
[![GitHub Stars](https://img.shields.io/github/stars/YOUR-USERNAME/ari-klopfer-portfolio?style=social)](https://github.com/YOUR-USERNAME/ari-klopfer-portfolio)
[![Portfolio](https://img.shields.io/badge/Portfolio-Live-success)](https://YOUR-USERNAME.github.io/ari-klopfer-portfolio/)
```

## Step 9: Test Your Portfolio

### Local Testing:

```bash
# Serve locally to test
cd c:/Users/Arikl/claude-agent-sdk-intro/docs/portfolio/github-repo/docs
python -m http.server 8000

# Open http://localhost:8000 in browser
```

### Live Testing:

1. Wait 2-5 minutes for GitHub Pages to deploy
2. Visit `https://YOUR-USERNAME.github.io/ari-klopfer-portfolio/`
3. Check all links work
4. Verify no sensitive data visible
5. Test on mobile

## Step 10: Share Your Portfolio

### Add to Your Resume/CV:

Update the "Portfolio" link at the bottom of resume.html and cv.html:

```html
<footer>
    <p>
        References available upon request |
        Portfolio: <a href="https://YOUR-USERNAME.github.io/ari-klopfer-portfolio/">
            View Live Portfolio
        </a> |
        Last updated: December 2025
    </p>
</footer>
```

### Add to LinkedIn:

1. Edit Profile → Featured → Add link
2. Title: "AI Agent Developer Portfolio"
3. URL: `https://github.com/YOUR-USERNAME/ari-klopfer-portfolio`

### Add to Email Signature:

```
Ari Klopfer | AI Agent Developer
Portfolio: github.com/YOUR-USERNAME/ari-klopfer-portfolio
```

## Security Reminders

### NEVER Commit:
- `.env` files (use `.env.example`)
- API keys or secrets
- Client data or PII
- Production database credentials
- Internal documentation

### Before Every Commit:

```bash
# Always review changes
git diff

# Check for secrets
git diff | grep -i "api_key\|password\|secret\|token\|credential"

# Review staged files
git status
```

### If You Accidentally Commit Secrets:

```bash
# DO NOT just delete and recommit
# The secret is still in Git history!

# Instead:
# 1. Revoke/regenerate the secret immediately
# 2. Use git-filter-repo or BFG Repo-Cleaner to remove from history
# 3. Force push the cleaned history
# 4. Rotate all potentially exposed credentials
```

## Ongoing Maintenance

### Update Portfolio Regularly:

```bash
# Make changes
vim README.md

# Commit with descriptive message
git add .
git commit -m "Update: Add new project showcase for XYZ"
git push
```

### Track Analytics:

- Monitor repository traffic (Insights → Traffic)
- Track visitors to GitHub Pages
- Monitor which projects get the most attention

### Respond to Issues/PRs:

If someone opens an issue or PR:
- Respond professionally
- Shows you're active and engaged
- Good for networking

## Troubleshooting

### GitHub Pages not showing:

```bash
# Check GitHub Pages status
gh repo view --web
# Go to Settings → Pages → Check for errors

# Force rebuild
git commit --allow-empty -m "Trigger Pages rebuild"
git push
```

### Permission errors:

```bash
# Check SSH keys
ssh -T git@github.com

# Or use HTTPS with personal access token
gh auth login
```

### Large files blocked:

```bash
# Check file sizes
find . -type f -size +50M

# GitHub has 100MB file size limit
# Use Git LFS for large files
```

## Next Steps

1. ✅ Complete the setup above
2. 📧 Include portfolio link in your GenAI Labs email
3. 📱 Add to LinkedIn Featured section
4. 🎯 Monitor who views your profile
5. 🔄 Update monthly with new projects

---

**Need Help?**

If you encounter issues:
1. Check the troubleshooting section above
2. Review GitHub documentation: https://docs.github.com/
3. Ask in the GitHub community: https://github.community/

**Ready to push to GitHub? Let's do it!**
