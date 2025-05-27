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
1. **Scan:** `gh pr status`, apply language rules, identify issues, verify coverage
2. **Draft:** Generate review comments, include solutions, note documentation updates
3. **Ask:** Submit pending PR comments, verify requirements, challenge decisions
4. **Sync:** Submit automated comments, request changes, hand off to human

**Note:** During execution, mark completed steps with ✅ to track progress.

## Expected Outcomes
- Automated PR comments in pending mode
- Actionable feedback with solutions
- Human-agent collaborative workflow
- Strict standards enforcement
- Language-specific compliance

## Language-Specific Review Criteria

**CRITICAL:** Always consult and strictly enforce the language-specific rules from `~/.agent3d/rules/[language].md` (includes both development rules and review standards).

### Supported Languages
- **Markdown:** `~/.agent3d/rules/markdown.md`
- **Python:** `~/.agent3d/rules/python.md`
- **JavaScript:** `~/.agent3d/rules/javascript.md`
- **Java:** `~/.agent3d/rules/java.md`
- **Go:** `~/.agent3d/rules/go.md`



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

## GitHub CLI Integration

**For detailed GitHub CLI integration instructions, see [GitHub CLI Integration Guide](../../docs/GITHUB-CLI-INTEGRATION.md).**

### PR-Aware Review Process

When the local project is on a PR branch:

1. **Automatic PR Detection** - Uses GitHub CLI to detect if current branch is associated with a PR
2. **Automated Comment Submission** - Submits review comments in **pending mode** for human completion
3. **Human Review Completion** - Human reviewer completes the review process with final approval/rejection

### Key Benefits

- **Automated Analysis** - Agent performs detailed code analysis using language-specific rules
- **Pending Mode Comments** - Comments submitted but review not finalized until human approval
- **Human Control** - Human maintains final decision authority over PR approval/rejection
- **Fallback Support** - Works with or without GitHub CLI availability

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
**Reference:** ~/.agent3d/rules/[language].md - [specific section]
**Severity:** [Critical/High/Medium/Low]
```

## Integration with CI/CD
See [Common Procedures](../docs/COMMON-PROCEDURES.md#quality--github) for CI/CD integration patterns.

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
**Language-Specific:** Rules from `~/.agent3d/rules/[language].md` and `[language]-review-guidelines.md`
**Universal:** Quality standards from [Common Procedures](../../docs/COMMON-PROCEDURES.md#quality-standards)
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
