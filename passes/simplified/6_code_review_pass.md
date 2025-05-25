# Code Review Pass

**Purpose:** Reviewing code changes between the base branch and a pull request, providing feedback through comments on the PR, and setting the review status to "Pending" until all issues are addressed.

**Reviewer Role:** Assume the role of a **very strict Senior Software Engineer** with deep expertise in the target programming language. Apply rigorous software engineering standards and language-specific best practices. Be thorough, uncompromising on quality, and focused on long-term maintainability.

## When to Use
- When a pull request has been submitted
- Before merging code changes into the main branch
- As part of the continuous integration process
- When conducting peer reviews of code changes
- For quality assurance of feature implementations
- When validating that code changes align with documentation

## Process
1. **Scan:**
   - **Rigorously examine** the diff between the base branch and the PR
   - Apply **language-specific rules** from `~/.agent3d/rules/[language].md`
   - Identify potential issues, bugs, or code quality concerns with **zero tolerance**
   - Check for strict alignment with documentation and requirements
   - Verify comprehensive test coverage for the changes
   - Look for security vulnerabilities, performance issues, and maintainability concerns
   - **Scrutinize** adherence to language idioms and best practices

2. **Draft:**
   - Prepare **detailed, specific review comments** for each issue found
   - **Demand explanations** for any deviations from best practices
   - Document concrete suggestions for improvements with examples
   - Note any documentation updates needed
   - Prepare comprehensive summary of overall review findings
   - **Be uncompromising** on code quality standards

3. **Ask:**
   - **Challenge implementation decisions** that don't follow best practices
   - Discuss alternative approaches for complex issues with language-specific solutions
   - Verify requirements understanding with stakeholders
   - Confirm security, performance, and maintainability considerations
   - **Question any shortcuts** or technical debt introduced

4. **Sync:**
   - Submit **thorough review comments** on the GitHub PR
   - Set PR review status to **"Request Changes"** for any quality issues
   - **Do not approve** until ALL issues are resolved to high standards
   - Follow up persistently on comment resolutions
   - Approve PR only when code meets **strict quality criteria**

**Note:** During execution, mark completed steps with ✅ to track progress.

## Expected Outcomes
- **Comprehensive review comments** on the GitHub PR with specific, actionable feedback
- PR review status set to **"Request Changes"** until ALL issues are resolved to high standards
- **Significantly improved code quality** through rigorous feedback
- **Strict verification** that code changes align with documentation and language best practices
- **Proactive identification** of potential bugs, security issues, and maintainability problems
- **Uncompromising enforcement** of software engineering standards
- Knowledge transfer of language-specific best practices and patterns

## Language-Specific Review Criteria

**CRITICAL:** Always consult and strictly enforce the language-specific rules from:
- **Development Rules:** `~/.agent3d/rules/[language].md`
- **Review Guidelines:** `~/.agent3d/rules/[language]-review-guidelines.md`



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

### Strict Review Standards
- **Be uncompromisingly specific** about every issue found
- **Demand explanations** for any deviations from language best practices
- **Provide concrete solutions** with code examples, not just suggestions
- **Reference specific rules** from `~/.agent3d/rules/[language].md`
- **Distinguish between critical issues** (must fix) and improvements (should fix)
- **Focus on long-term maintainability** over short-term convenience
- **Acknowledge good practices** but don't lower standards for other areas

### Comment Structure
```markdown
**Issue:** [Specific problem with the code]
**Why:** [Explanation of why this violates best practices]
**Fix:** [Concrete solution with code example]
**Reference:** ~/.agent3d/rules/[language]-review-guidelines.md - [specific section]
**Severity:** [Critical/High/Medium/Low]
```



## Integration with CI/CD
- The Code Review Pass can be integrated with CI/CD pipelines
- Automated checks can supplement manual review
- Code quality tools can be run automatically
- Test coverage reports can inform the review
- Security scanning tools can identify vulnerabilities

## Automated Review Checklist
- [ ] **Code Quality:** Linting and style checks pass
- [ ] **Test Coverage:** Minimum coverage thresholds met
- [ ] **Security:** No high-severity vulnerabilities detected
- [ ] **Performance:** No significant performance regressions
- [ ] **Documentation:** Code changes include documentation updates
- [ ] **Dependencies:** No vulnerable or outdated dependencies introduced
- [ ] **Breaking Changes:** Breaking changes are documented and justified

## Review Templates

### Strict Review Template
```markdown
## Code Review Summary - STRICT STANDARDS APPLIED
- **Overall Assessment:** [Request Changes/Approve] - NO COMPROMISES ON QUALITY
- **Language Rules Applied:** [Reference to ~/.agent3d/rules/[language].md and [language]-review-guidelines.md]
- **Critical Issues:** [Must fix before approval - list with severity]
- **High Priority Issues:** [Should fix for maintainability]
- **Best Practice Violations:** [Language-specific concerns]
- **Documentation Gaps:** [Required documentation updates]

## Detailed Comments by Category

### Code Quality Issues
[Specific violations of language best practices with examples]

### Security Concerns
[Any security vulnerabilities or unsafe patterns]

### Performance Issues
[Inefficient algorithms, memory usage, or scalability concerns]

### Maintainability Problems
[Code that will be difficult to maintain or extend]

## Required Actions Before Approval
- [ ] Fix all Critical and High severity issues
- [ ] Address best practice violations
- [ ] Update documentation as specified
- [ ] Add/improve test coverage
- [ ] Resolve all security concerns

## Standards Enforced
- Language-specific rules from ~/.agent3d/rules/[language].md
- Zero tolerance for technical debt introduction
- Comprehensive test coverage required
- Documentation must be updated with code changes
```

### Language-Specific Review Template
```markdown
## [LANGUAGE] Code Review - EXPERT LEVEL STANDARDS

### Language-Specific Compliance
- **Type Safety:** [Assessment against language standards]
- **Idiom Usage:** [Proper use of language patterns]
- **Performance:** [Efficient use of language features]
- **Error Handling:** [Language-appropriate error patterns]
- **Testing:** [Framework and pattern compliance]

### Critical Language Violations
[List any violations of language-specific best practices]

### Recommendations for Language Excellence
[Specific improvements to achieve language mastery]

### References
- Language Rules: ~/.agent3d/rules/[language].md
- Review Guidelines: ~/.agent3d/rules/[language]-review-guidelines.md
- Best Practices Documentation: [relevant links]
```

### Security Review Template
```markdown
## Security Review - ZERO TOLERANCE FOR VULNERABILITIES
- **Authentication:** [Rigorous assessment]
- **Authorization:** [Comprehensive evaluation]
- **Input Validation:** [Thorough validation check]
- **Data Protection:** [Privacy and security assessment]
- **Vulnerabilities:** [Complete vulnerability analysis]
- **Secure Coding:** [Language-specific security patterns]

## Security Requirements
[Mandatory security improvements - no exceptions]

## Security Standards Applied
[Reference to security guidelines and language-specific security rules]
```
