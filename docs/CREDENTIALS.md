# Credentials & MCP Setup

How to run the RM skills stack without the Claude.ai desktop app, with your own API keys, and switch between agents or models.

---

## 1. Install Claude Code CLI

```bash
npm install -g @anthropic-ai/claude-code
```

Then authenticate:
```bash
claude auth login
# Or set directly:
export ANTHROPIC_API_KEY=sk-ant-...
```

To use a specific model:
```bash
claude --model claude-opus-4-7   # Opus (most capable)
claude --model claude-sonnet-4-6  # Sonnet (default, balanced)
claude --model claude-haiku-4-5-20251001  # Haiku (fastest)
```

---

## 2. Set up your credentials

```bash
cp .env.example .env
# Edit .env with your values — never commit it
```

Required credentials:

| Service | Where to get it |
|---|---|
| `ANTHROPIC_API_KEY` | console.anthropic.com → API Keys |
| `GITHUB_TOKEN` | github.com/settings/tokens (scopes: `repo`, `read:org`, `workflow`) — or just run `gh auth login` |
| `JIRA_TRUTHLY_API_TOKEN` | truthly-ai.atlassian.net → Profile → Security → API tokens |
| `JIRA_MOZART_API_TOKEN` | ryan-miranda.atlassian.net → Profile → Security → API tokens |
| `SLACK_BOT_TOKEN` | api.slack.com/apps — create app with read scopes, install to workspace |
| `SLACK_TEAM_ID` | Your Slack workspace URL: `https://<team>.slack.com` → Settings → About |
| `GOOGLE_*` | console.cloud.google.com → OAuth credentials (Gmail + Drive scopes) |
| `FIGMA_ACCESS_TOKEN` | figma.com/settings → Personal access tokens |

Slack scopes needed: `channels:read channels:history groups:read groups:history im:read im:history mpim:read mpim:history search:read users:read files:read`

---

## 3. Configure MCP servers

MCP servers replace the Claude.ai desktop app's built-in integrations. Copy the example config:

```bash
cp mcp.json.example .mcp.json
```

`.mcp.json` in your project root is picked up automatically by Claude Code. To install globally (applies to all projects):

```bash
cp mcp.json.example ~/.claude/mcp.json
```

Load your `.env` before starting a session:

```bash
source .env && claude
```

Or add to your shell profile (`~/.zshrc` / `~/.bashrc`):
```bash
export ANTHROPIC_API_KEY=sk-ant-...
# etc.
```

---

## 4. Install the skills

```bash
git clone https://github.com/ryan-miranda-partners/ryan-miranda.git ~/Documents/ryan-miranda
cd ~/Documents/ryan-miranda && ./setup
```

Then start Claude Code from your working repo:
```bash
cd ~/Documents/<your-project>
source ~/Documents/ryan-miranda/.env   # if you stored creds there
claude
```

---

## 5. Switch agents / models mid-session

In any Claude Code session:
```
/model claude-opus-4-7        # switch to Opus
/model claude-sonnet-4-6      # switch to Sonnet
```

Or set a default in `~/.claude/settings.json`:
```json
{
  "model": "claude-sonnet-4-6"
}
```

---

## 6. Verify everything is working

```bash
# Check Claude Code
claude --version

# Check GitHub
gh auth status

# Check Jira (replace with your email + base URL)
curl -u "$JIRA_TRUTHLY_EMAIL:$JIRA_TRUTHLY_API_TOKEN" \
  "$JIRA_TRUTHLY_BASE_URL/rest/api/3/myself" | jq .displayName

# Check Slack
curl -s -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  https://slack.com/api/auth.test | jq .ok
```

---

## Troubleshooting

**MCP server not found:** Make sure `.mcp.json` is in your working directory or `~/.claude/`. Run `claude mcp list` to see what's loaded.

**Jira auth fails:** API tokens are per-user. Each teammate needs their own token from their Atlassian profile, not a shared one.

**Slack search returns nothing:** Confirm your app is installed to the workspace and has `search:read` scope.

**Model not available:** Check your Anthropic account tier — Opus requires an API plan with access.
