# Code Review Pass

**Purpose:** Reviewing code changes between the base branch and a pull request, providing feedback through comments on the PR, and setting the review status to "Pending" until all issues are addressed.

## When to Use
- When a pull request has been submitted
- Before merging code changes into the main branch
- As part of the continuous integration process
- When conducting peer reviews of code changes
- For quality assurance of feature implementations
- When validating that code changes align with documentation

## Process
1. **Scan:** 
   - Examine the diff between the base branch and the PR
   - Identify potential issues, bugs, or code quality concerns
   - Check for alignment with documentation and requirements
   - Verify test coverage for the changes
   - Look for security vulnerabilities or performance issues

2. **Draft:** 
   - Prepare detailed review comments for each issue
   - Document suggestions for improvements
   - Note any documentation updates needed
   - Prepare summary of overall review findings

3. **Ask:** 
   - Seek clarification on implementation decisions if needed
   - Discuss alternative approaches for complex issues
   - Verify requirements understanding with stakeholders
   - Confirm security or performance considerations

4. **Sync:** 
   - Submit review comments on the GitHub PR
   - Set PR review status to "Pending" until issues are addressed
   - Follow up on comment resolutions
   - Approve PR once all issues are resolved

## Expected Outcomes
- Detailed review comments on the GitHub PR
- PR review status set to "Pending" until issues are resolved
- Improved code quality through feedback
- Verification that code changes align with documentation
- Identification of potential bugs or issues before they reach production
- Knowledge sharing and mentoring through the review process

## Example Commit Message
`DDD: Code Review Pass - Reviewed authentication feature PR with security recommendations`

## Review Focus Areas
- **Code Quality**
  - Adherence to coding standards and best practices
  - Proper error handling
  - Appropriate logging
  - Clean, readable, and maintainable code

- **Functionality**
  - Correct implementation of requirements
  - Edge case handling
  - Error conditions and recovery
  - Integration with existing systems

- **Testing**
  - Adequate test coverage
  - Test quality and comprehensiveness
  - Edge case testing
  - Performance testing where applicable

- **Security**
  - Input validation
  - Authentication and authorization
  - Data protection
  - Secure coding practices

- **Performance**
  - Algorithmic efficiency
  - Resource usage
  - Scalability considerations
  - Potential bottlenecks

- **Documentation**
  - Code comments and documentation
  - API documentation
  - Updated requirements or specifications
  - Release notes or changelog updates

## Using GitHub CLI

The Code Review Pass can utilize the GitHub CLI (`gh`) to interact with pull requests:

```bash
# List open pull requests
gh pr list

# View a specific pull request
gh pr view [PR_NUMBER]

# Check out a pull request locally
gh pr checkout [PR_NUMBER]

# View changes in a pull request
gh pr diff [PR_NUMBER]

# Add a review comment to a pull request
gh pr review [PR_NUMBER] --comment -b "Your comment here"

# Request changes on a pull request
gh pr review [PR_NUMBER] --request-changes -b "Changes needed: ..."

# Approve a pull request
gh pr review [PR_NUMBER] --approve -b "LGTM!"
```

## Review Comment Guidelines
- Be specific and clear about the issue
- Provide constructive feedback
- Suggest solutions when possible
- Use a respectful and professional tone
- Reference documentation or best practices
- Distinguish between required changes and suggestions
- Focus on the code, not the author
- Acknowledge good practices and improvements

## Integration with CI/CD
- The Code Review Pass can be integrated with CI/CD pipelines
- Automated checks can supplement manual review
- Code quality tools can be run automatically
- Test coverage reports can inform the review
- Security scanning tools can identify vulnerabilities
