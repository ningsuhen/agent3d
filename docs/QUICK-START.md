# Quick Start Guide

This guide provides a streamlined introduction for new users of the Agent3D framework. It summarizes the minimum steps required to begin using the Documentation-Driven Development workflow.

## 1. Clone Agent3D
1. Clone the Agent3D repository to `~/.agent3d`:
   ```bash
   git clone git@github.com:ningsuhen/agent3d.git ~/.agent3d
   ```
2. Keep the repository up to date:
   ```bash
   git -C ~/.agent3d pull origin main
   ```

## 2. Configure Your Project
1. Run the Foundation Pass to create `.agent3d-config.yml` in your project root.
2. Adjust the configuration to match your project's language and quality requirements.

## 3. Follow the Core Workflow
Execute the simplified DDD workflow for each development task:
1. **Scan** – Identify missing or outdated documentation.
2. **Draft** – Update or create the necessary docs.
3. **Ask** – Clarify open questions with stakeholders.
4. **Sync** – Implement code that matches the documentation.

Commit documentation and code together. If a commit does not update docs, include the `docs-n/a` tag in the commit message.

## 4. Run Tests and Validate
Use language‑specific tests and linting to verify that code matches documented requirements. The testing pass ensures quality and alignment.

## 5. Maintain Synchronization
Regularly pull updates from `~/.agent3d` to keep rules and templates current. Re-run relevant passes whenever documentation or code drifts out of sync.

---

For more detailed procedures and advanced configuration options, see the [Configuration Guide](CONFIGURATION-GUIDE.md) and [Common Procedures](COMMON-PROCEDURES.md).
