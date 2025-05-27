# GitHub CLI Integration

## PR Detection & Review

```bash
# PR Detection
CURRENT_BRANCH=$(git branch --show-current)
PR_NUMBER=$(gh pr list --head "$CURRENT_BRANCH" --json number --jq '.[0].number')

# PR Operations
gh pr list; gh pr view [PR_NUMBER]; gh pr diff [PR_NUMBER]; gh pr checks [PR_NUMBER]
```

## Review Workflow

```bash
# PR Detection
detect_pr_context() {
  local current_branch=$(git branch --show-current)
  local pr_number=$(gh pr list --head "$current_branch" --json number --jq '.[0].number' 2>/dev/null)
  if [ -n "$pr_number" ] && [ "$pr_number" != "null" ]; then
    echo "PR_DETECTED=true"; echo "PR_NUMBER=$pr_number"; echo "BRANCH=$current_branch"; return 0
  else
    echo "PR_DETECTED=false"; return 1
  fi
}

# Review Submission
gh pr review "$PR_NUMBER" --comment -b "$(cat review_summary.md)"
gh pr review "$PR_NUMBER" --comment -f "src/auth.py:15:Use specific exception types"
while IFS= read -r comment; do gh pr review "$PR_NUMBER" --comment -f "$comment"; done < file_comments.txt
```

## Review Completion

```bash
# Human Review Completion
gh pr view "$PR_NUMBER"
gh pr review "$PR_NUMBER" --approve -b "LGTM after addressing automated comments"
gh pr review "$PR_NUMBER" --request-changes -b "Please address the issues noted in comments"

# Review Status
gh pr view "$PR_NUMBER" --json reviews
gh api repos/:owner/:repo/pulls/$PR_NUMBER/reviews
gh pr view "$PR_NUMBER" --json mergeable,mergeStateStatus
```

## Fallback: No GitHub CLI

```bash
# Generate Review Report
cat > code_review_report.md << 'EOF'
# Code Review Report - PR #{{PR_NUMBER}}
## Summary: {{OVERALL_ASSESSMENT}}
## Critical Issues: {{CRITICAL_ISSUES}}
## File Comments: {{FILE_PATH}} Line {{LINE_NUMBER}}: {{COMMENT}}
## Decision: [ ] Approve [ ] Request Changes [ ] Comment Only
EOF
```

## Troubleshooting & Integration

```bash
# Troubleshooting
gh auth status
gh auth refresh
gh api repos/:owner/:repo --jq '.permissions'
export GH_DEBUG=1; gh api user; gh api rate_limit
```

## DDD Pass Integration

Code Review Pass: Detects PR context → Generates review comments → Submits pending review → Human completion

```bash
# Pass Integration Examples
if detect_pr_context; then
  gh pr comment "$PR_NUMBER" --body "Foundation changes detected."
  gh pr comment "$PR_NUMBER" --body "$(cat test_results.md)"
fi
```

## Guidelines

- **Comments**: Include file paths and line numbers, provide context, suggest solutions
- **Automation**: Always use pending mode, require human oversight, handle CLI unavailability

---

**Usage**: Reference from DDD passes needing GitHub CLI integration.
