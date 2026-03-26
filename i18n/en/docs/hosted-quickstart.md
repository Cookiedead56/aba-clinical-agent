# Hosted Quick Start Guide

No installation required. Run ABA Clinical Agent directly in your browser using GitHub Codespaces.

## What You Need

1. A **GitHub account** (free): [github.com/signup](https://github.com/signup)
2. An **Anthropic API key**: [console.anthropic.com](https://console.anthropic.com/)
   - Sign up, go to API Keys, create a new key
   - Expected cost: $5-20/month depending on usage

## Step 1: Set Your API Key

Before opening a Codespace, add your API key as a secret:

1. Go to [github.com/settings/codespaces](https://github.com/settings/codespaces)
2. Under "Codespaces secrets", click **New secret**
3. Name: `ANTHROPIC_API_KEY`
4. Value: paste your API key (starts with `sk-ant-...`)
5. Repository access: select `open-behavior-analysis/aba-clinical-agent`
6. Click **Add secret**

## Step 2: Open in Codespace

1. Go to [github.com/open-behavior-analysis/aba-clinical-agent](https://github.com/open-behavior-analysis/aba-clinical-agent)
2. Click the green **Code** button
3. Select the **Codespaces** tab
4. Click **Create codespace on main**
5. Wait 2-3 minutes for the environment to build

When ready, you will see a VS Code editor in your browser with a terminal at the bottom showing a welcome message.

## Step 3: Start Using

In the terminal, type:

```bash
bash scripts/start.sh
```

Or simply:

```bash
claude
```

Then enter your first command:

```
Please read CLAUDE.md and enter the clinical supervisor role.
I have a new case named "Alex" - please run intake-interview and tell me what information you need.
```

## Saving Your Work

Your clinical data is stored in the `Obsidian-Vault/` directory. To save your work:

```bash
git add Obsidian-Vault/
git commit -m "save clinical data"
git push
```

We recommend forking the repository first (click "Fork" on the repo page) so your data goes to your private copy.

## Switching Languages

The system supports English and Chinese:

```bash
# Switch to Chinese
python scripts/setup.py --lang zh-CN

# Switch back to English
python scripts/setup.py --lang en
```

## Free Tier Limits

GitHub Free accounts include **60 hours/month** of Codespace usage. This is enough for most individual BCBAs. If you need more:

- GitHub Pro ($4/month): 120 hours/month
- You can stop your Codespace when not in use to save hours

## FAQ

**Q: Is my clinical data safe?**
A: Your data stays in your Codespace (or your forked repo). It is not shared with anyone. We recommend using a private fork for real clinical data.

**Q: What happens if my Codespace is deleted?**
A: Codespaces are deleted after 30 days of inactivity. Always commit and push your work to keep it safe.

**Q: Can I use this offline?**
A: The hosted version requires internet. For offline use, clone the repo and set up locally (see the main README).

**Q: How much does the API cost?**
A: Anthropic charges based on usage. Typical BCBA usage is $5-20/month. You can set spending limits in the Anthropic console.
