# GitHub CLI Integration for DDD Passes

GitHub CLI integration for automated PR review workflows.

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- Repository access with PR permissions
- Git branch associated with open PR

### Setup

Install GitHub CLI and authenticate: `gh auth login`

## PR Detection and Context

### Check PR Status

```bash
# Detect PR context
gh pr status
CURRENT_BRANCH=$(git branch --show-current)
PR_NUMBER=$(gh pr list --head "$CURRENT_BRANCH" --json number --jq '.[0].number')
```

### PR Operations

```bash
gh pr list                    # List PRs
gh pr view [PR_NUMBER]        # View PR details
gh pr diff [PR_NUMBER]        # Get diff
gh pr checks [PR_NUMBER]      # Check status
```

## Automated Review Workflow

### 1. PR Branch Detection Script

```bash
#!/bin/bash
# detect_pr_context.sh

detect_pr_context() {
  local current_branch=$(git branch --show-current)
  local pr_number=$(gh pr list --head "$current_branch" --json number --jq '.[0].number' 2>/dev/null)

  if [ -n "$pr_number" ] && [ "$pr_number" != "null" ]; then
    echo "PR_DETECTED=true"
    echo "PR_NUMBER=$pr_number"
    echo "BRANCH=$current_branch"
    return 0
  else
    echo "PR_DETECTED=false"
    return 1
  fi
}

# Usage
detect_pr_context
```

### 2. Review Comment Submission

```bash
# Submit review summary in pending mode
gh pr review "$PR_NUMBER" --comment -b "$(cat review_summary.md)"

# Add file-specific comments with line numbers
gh pr review "$PR_NUMBER" --comment -f "src/auth.py:15:Use specific exception types instead of bare except"
gh pr review "$PR_NUMBER" --comment -f "src/utils.py:28:Consider using list comprehension for better performance"

# Submit multiple file comments from file
while IFS= read -r comment; do
  gh pr review "$PR_NUMBER" --comment -f "$comment"
done < file_comments.txt
```

### 3. Review Comment Format

File comments should follow this format:
```
path/to/file.py:line_number:Comment text here
```

Example file_comments.txt:
```
src/auth.py:15:Use specific exception types instead of bare except
src/auth.py:42:This function needs proper error handling
src/utils.py:28:Consider using list comprehension for better performance
tests/test_auth.py:10:Add test case for invalid input handling
```

## Review Completion Workflow

### Human Review Completion

After automated comments are submitted in pending mode:

```bash
# View pending review
gh pr view "$PR_NUMBER"

# Complete review with approval
gh pr review "$PR_NUMBER" --approve -b "LGTM after addressing automated comments"

# Complete review with changes requested
gh pr review "$PR_NUMBER" --request-changes -b "Please address the issues noted in comments"

# Add additional comments during review
gh pr review "$PR_NUMBER" --comment -b "Additional feedback after manual review"
```

### Review Status Management

```bash
# Check review status
gh pr view "$PR_NUMBER" --json reviews

# List all reviews for a PR
gh api repos/:owner/:repo/pulls/$PR_NUMBER/reviews

# Check if PR is ready for merge
gh pr view "$PR_NUMBER" --json mergeable,mergeStateStatus
```

## Fallback: No GitHub CLI Available

When GitHub CLI is not available or not authenticated:

### 1. Generate Review Report

```bash
# Create review report template
cat > code_review_report.md << 'EOF'
# Code Review Report - PR #{{PR_NUMBER}}

## Summary
{{OVERALL_ASSESSMENT}}

## Critical Issues (Must Fix)
{{CRITICAL_ISSUES}}

## High Priority Issues (Should Fix)
{{HIGH_PRIORITY_ISSUES}}

## File-Specific Comments

### {{FILE_PATH}}
- Line {{LINE_NUMBER}}: {{COMMENT}}

## Recommendations
{{RECOMMENDATIONS}}

## Review Decision
[ ] Approve
[ ] Request Changes
[ ] Comment Only

## Next Steps
{{NEXT_STEPS}}
EOF
```

### 2. Manual Review Process

1. **Generate Report**: Create detailed review report using template above
2. **Copy Comments**: Manually copy comments to GitHub PR interface
3. **Submit Review**: Use GitHub web interface to submit review decision

## Error Handling and Troubleshooting

### Common Issues

```bash
# Check GitHub CLI authentication
gh auth status

# Re-authenticate if needed
gh auth refresh

# Check repository permissions
gh api repos/:owner/:repo --jq '.permissions'

# Verify PR exists and is accessible
gh pr view "$PR_NUMBER" || echo "PR not found or not accessible"
```

### Debugging Commands

```bash
# Enable debug mode
export GH_DEBUG=1

# Test API connectivity
gh api user

# Check rate limits
gh api rate_limit
```

## Integration with DDD Passes

### Code Review Pass Integration

The Code Review Pass automatically:

1. **Detects PR context** using the detection script
2. **Generates review comments** based on language-specific rules
3. **Submits pending review** with structured comments
4. **Hands off to human** for final review completion

### Other Pass Integration

Other DDD passes can use similar patterns:

```bash
# Foundation Pass: Check if setup changes affect PR
if detect_pr_context; then
  gh pr comment "$PR_NUMBER" --body "Foundation changes detected. Please review setup modifications."
fi

# Testing Pass: Report test results to PR
if detect_pr_context; then
  gh pr comment "$PR_NUMBER" --body "$(cat test_results.md)"
fi
```

## Best Practices

### Review Comment Guidelines

- **Be Specific**: Include file paths and line numbers
- **Provide Context**: Explain why the change is needed
- **Suggest Solutions**: Don't just identify problems, suggest fixes
- **Reference Standards**: Link to relevant coding standards or guidelines
- **Use Consistent Format**: Follow established comment structure

### Automation Guidelines

- **Pending Mode**: Always submit automated reviews in pending mode
- **Human Oversight**: Require human completion of all reviews
- **Error Handling**: Gracefully handle CLI unavailability
- **Permissions**: Verify appropriate access before attempting operations
- **Rate Limiting**: Be mindful of GitHub API rate limits

---

**Usage**: Reference this document from DDD passes that need GitHub CLI integration for PR operations.
