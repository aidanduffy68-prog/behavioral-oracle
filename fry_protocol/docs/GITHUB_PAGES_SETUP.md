# GitHub Pages Setup - 2 Minute Guide

## Enable GitHub Pages

1. Go to your repo: https://github.com/aidanduffy68-prog/USD_FRY
2. Click **Settings** (top right)
3. Scroll down to **Pages** (left sidebar)
4. Under "Build and deployment":
   - **Source**: Deploy from a branch
   - **Branch**: main
   - **Folder**: /docs
5. Click **Save**

## Wait 2-3 minutes

GitHub will build and deploy. You'll see a green checkmark and URL:
```
✅ Your site is live at https://aidanduffy68-prog.github.io/USD_FRY/
```

## Update README Links

Once live, update README.md to use the live URL instead of relative path:

**Change from:**
```markdown
📊 **[View Live Dashboard](docs/retention-dashboard.html)**
```

**Change to:**
```markdown
📊 **[View Live Dashboard](https://aidanduffy68-prog.github.io/USD_FRY/retention-dashboard.html)**
```

## Test

Visit: https://aidanduffy68-prog.github.io/USD_FRY/retention-dashboard.html

Should see the beautiful rendered dashboard with:
- Purple gradient background
- Metric cards
- Wallet list
- Charts

## Auto-Deploy

Every time you push to main, GitHub Pages auto-updates. So when you run:
```bash
python core/oracle/generate_public_metrics.py
git add docs/retention-dashboard.html
git commit -m "Update retention metrics"
git push
```

The live dashboard updates automatically within 1-2 minutes.

## Bonus: Custom Domain (Optional)

If you want `retention.greenhouse.co` or similar:
1. Add CNAME file to /docs with your domain
2. Update DNS settings
3. Enable HTTPS in GitHub Pages settings

But the github.io URL works great for now.
