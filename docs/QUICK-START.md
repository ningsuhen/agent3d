# Quick Start Guide

Streamlined introduction for Agent3D framework. Minimum steps to begin using Documentation-Driven Development workflow.

## 1. Clone Agent3D
1. Clone Agent3D repository to `~/.agent3d`:
   ```bash
   git clone git@github.com:ningsuhen/agent3d.git ~/.agent3d
   ```
2. Keep repository up to date:
   ```bash
   git -C ~/.agent3d pull origin main
   ```

## 2. Configure Your Project
1. Run Foundation Pass to create `.agent3d-config.yml` in project root.
2. Adjust configuration to match project's language and quality requirements.

## 3. Follow the Core Workflow
Execute DDD workflow for each development task:
1. **Scan** – Identify missing or outdated documentation.
2. **Draft** – Update or create necessary docs.
3. **Ask** – Clarify open questions with stakeholders.
4. **Sync** – Implement code that matches documentation.
5. **Confirm** – **ALWAYS CONFIRM BEFORE COMMITTING** - Get human approval for all commits.

Commit documentation and code together. If commit does not update docs, include `docs-n/a` tag.

## 4. Run Tests and Validate
Use language‑specific tests and linting to verify code matches documented requirements. Testing pass ensures quality and alignment.

## 5. Maintain Synchronization
Regularly pull updates from `~/.agent3d` to keep rules and templates current. Re-run relevant passes when documentation or code drifts.

---

For detailed procedures and advanced configuration, see [Configuration Guide](CONFIGURATION-GUIDE.md) and [Common Procedures](COMMON-PROCEDURES.md).
