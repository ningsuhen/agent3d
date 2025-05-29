# DDD Migration System

This directory contains migration workflows for transitioning between different DDD framework versions and structures.

## 📁 Migration Directory Structure

```
docs/migrations/
├── README.md                           # This file - migration system overview
├── migration-tracker.yml              # Tracks completed migrations
├── test-cases-to-features.yml         # TEST-CASES.md → docs/features/ migration
├── legacy-structure-migration.yml     # Legacy → Modern DDD migration
└── templates/
    └── migration.template.yml          # Template for new migrations
```

## 🎯 Migration Tracking System

### **Migration Status Tracking**

All migrations are tracked in `migration-tracker.yml` to prevent duplicate execution:

```yaml
migrations:
  test-cases-to-features:
    status: "completed"
    executed_at: "2025-01-27T10:30:00Z"
    version: "1.0.0"
    checksum: "abc123..."
  legacy-structure:
    status: "pending"
    version: "1.0.0"
```

### **Migration States**

- **`pending`** - Migration available but not executed
- **`running`** - Migration currently in progress
- **`completed`** - Migration successfully completed
- **`failed`** - Migration failed and needs attention
- **`skipped`** - Migration manually skipped (not applicable)

## 🚀 Usage Instructions

### **For LLMs/Agents**

```python
# Check migration status before execution
import yaml

with open('docs/migrations/migration-tracker.yml', 'r') as f:
    tracker = yaml.safe_load(f)

migration_id = "test-cases-to-features"
if tracker['migrations'][migration_id]['status'] == 'completed':
    print(f"Migration {migration_id} already completed - skipping")
else:
    # Execute migration workflow
    execute_migration(migration_id)
```

### **For Manual Execution**

```bash
# Check migration status
python tools/migration_manager.py status

# Execute specific migration
python tools/migration_manager.py run test-cases-to-features

# Mark migration as completed manually
python tools/migration_manager.py complete test-cases-to-features
```

## 📋 Available Migrations

### **1. TEST-CASES.md → Features Migration**
- **File:** `test-cases-to-features.yml`
- **Purpose:** Migrate from separate TEST-CASES.md to merged FT-TC structure
- **Target:** Projects using legacy TEST-CASES.md structure
- **Impact:** High - Changes core documentation structure

### **2. Legacy Structure Migration**
- **File:** `legacy-structure-migration.yml`
- **Purpose:** Migrate from old DDD structure to modern framework
- **Target:** Projects using pre-2025 DDD structure
- **Impact:** High - Updates entire project structure

## 🔧 Migration Workflow Format

Each migration follows this YAML structure:

```yaml
metadata:
  id: "migration-identifier"
  name: "Human Readable Name"
  version: "1.0.0"
  description: "What this migration does"
  
prerequisites:
  - "Condition that must be met"
  - "Another prerequisite"
  
steps:
  - id: "step-1"
    name: "Step Name"
    actions:
      - "Action to perform"
    validation:
      - "How to verify success"
      
rollback:
  - "How to undo this migration"
```

## 🛡️ Safety Features

### **Pre-Migration Checks**
- Verify prerequisites are met
- Check for conflicting changes
- Validate project structure
- Create backup points

### **Rollback Support**
- Each migration includes rollback procedures
- Automatic backup creation before execution
- Step-by-step rollback instructions
- Validation of rollback success

### **Idempotency**
- Migrations can be run multiple times safely
- Status tracking prevents duplicate execution
- Partial completion detection and recovery

## 🔍 Best Practices

### **For Migration Authors**
1. **Always include prerequisites** - Check what must exist before migration
2. **Provide clear rollback** - Every step should be reversible
3. **Validate thoroughly** - Include comprehensive success criteria
4. **Test extensively** - Verify on multiple project types
5. **Document impact** - Clearly state what changes

### **For Migration Users**
1. **Backup first** - Always backup before running migrations
2. **Read documentation** - Understand what the migration does
3. **Check prerequisites** - Ensure your project meets requirements
4. **Validate results** - Verify migration completed successfully
5. **Test thoroughly** - Ensure your project still works

## 📊 Migration History

Track all migrations in your project:

```bash
# View migration history
python tools/migration_manager.py history

# Export migration report
python tools/migration_manager.py report --format yaml
```

## 🚨 Troubleshooting

### **Common Issues**

1. **Migration Already Completed**
   - Check `migration-tracker.yml` status
   - Use `--force` flag to re-run if needed

2. **Prerequisites Not Met**
   - Review prerequisite list in migration file
   - Ensure project structure matches requirements

3. **Partial Migration Failure**
   - Check migration logs for specific step failure
   - Use rollback procedures to restore previous state
   - Fix issues and retry migration

### **Getting Help**

- Review migration-specific documentation
- Check prerequisite requirements
- Examine validation criteria
- Test rollback procedures in safe environment

## 🔮 Future Enhancements

- **Automated migration detection** - Scan project and suggest applicable migrations
- **Migration dependencies** - Support for migration chains and dependencies
- **Interactive migration** - Step-by-step guided migration process
- **Migration templates** - Standardized templates for common migration patterns
- **CI/CD integration** - Automated migration execution in pipelines
