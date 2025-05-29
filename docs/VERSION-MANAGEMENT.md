# Version Management System

The Agent3D framework includes automatic version management for templates and framework YAML files to ensure proper tracking and template management.

## 🎯 Overview

The version management system automatically increments versions when writing template files or framework YAML files, ensuring:
- **Proper version tracking** for all templates and framework files
- **Template management** with version-based rewrite detection
- **Consistent versioning** across all Agent3D projects
- **Automated updates** without manual intervention

## 📁 Files Covered

### **Template Files**
- `templates/*.template.yml` - All YAML template files
- `templates/*.template.md` - All Markdown template files  
- `templates/index.yml` - Template system index

### **Framework YAML Files**
- `procedures.yml/*.yml` - All procedure files
- `passes.yml/*.yml` - All pass definition files
- `rules.yml/*.yml` - All language rule files
- `.agent3d-config.yml` - Main configuration file
- `AGENT-GUIDELINES.yml` - Framework guidelines

## 🔧 How It Works

### **Automatic Detection**
The system automatically detects when files matching the patterns above are being written and:
1. **Reads current version** from file metadata
2. **Determines change type** (patch, minor, major)
3. **Calculates new version** using semantic versioning
4. **Updates version metadata** in the file
5. **Updates timestamp** to current date

### **Version Format**
Uses semantic versioning: `MAJOR.MINOR.PATCH`
- **Patch** (default): Content updates, bug fixes, minor changes
- **Minor**: New features, structure changes, significant updates  
- **Major**: Breaking changes, complete rewrites, API changes

### **Version Location**
- **YAML files**: `version` or `metadata.version` field
- **Markdown files**: `<!-- Template Version: X.X.X -->` comment and YAML frontmatter

## 🛠 Tools

### **Version Manager Tool**
`tools/version_manager.py` - Core version management functionality

**Usage:**
```bash
# Update version automatically (patch increment)
python3 tools/version_manager.py <file_path>

# Specify change type
python3 tools/version_manager.py <file_path> patch|minor|major
```

**Examples:**
```bash
# Patch update for template
python3 tools/version_manager.py templates/agent3d-config.template.yml

# Minor update for procedure
python3 tools/version_manager.py procedures.yml/core-patterns.yml minor

# Major update for guidelines
python3 tools/version_manager.py AGENT-GUIDELINES.yml major
```

## 📋 Integration Points

### **DDD Passes**
Version management is integrated into all DDD passes:

#### **Foundation Pass**
- Updates config template version before copying
- Updates generated config version after creation

#### **Development Pass**  
- Updates template versions when modifying templates
- Tracks template usage in execution plans

#### **All Passes**
- Automatic version updates for any template or framework file modifications
- Version tracking in execution plans and status files

### **Core Patterns**
File operations include version management:
```yaml
file_operations:
  before_write:
    - "validate_file_path"
    - "check_file_permissions" 
    - "backup_if_exists"
    - "validate_content_format"
    - "update_version_if_template_or_framework_file"
```

### **Agent Guidelines**
Version management requirements are built into agent guidelines:
```yaml
version_management:
  requirement: "ALWAYS update versions when writing template or framework YAML files"
  process: "See procedures.yml/version-management.yml for complete workflow"
  tool: "tools/version_manager.py"
```

## 🎯 Benefits

### **Template Management**
- **Version-based rewrite detection** - Templates can check if they need updating
- **Template consistency** - All templates maintain proper version tracking
- **Migration support** - Version tracking enables proper migration workflows

### **Framework Consistency**
- **Automatic updates** - No manual version management required
- **Consistent tracking** - All framework files use same versioning approach
- **Change tracking** - Version history provides change audit trail

### **Developer Experience**
- **Transparent operation** - Version updates happen automatically
- **Clear versioning** - Semantic versioning provides clear change indication
- **Tool integration** - Works seamlessly with existing DDD workflows

## 📊 Version Update Rules

### **Change Type Detection**
The system determines change types based on modification patterns:

#### **Patch Changes (X.X.+1)**
- Typo fixes and formatting improvements
- Minor content updates and comment additions
- Small corrections and clarifications

#### **Minor Changes (X.+1.0)**
- New sections or fields added
- Structure enhancements and feature additions
- Significant content updates

#### **Major Changes (+1.0.0)**
- Breaking format changes and complete restructuring
- API breaking changes and major workflow changes
- Complete rewrites or fundamental changes

### **Default Behavior**
- **Default increment**: Patch (safest option)
- **Automatic detection**: Based on file modification patterns
- **Manual override**: Can specify change type explicitly

## 🔍 Monitoring

### **Version Change Tracking**
All version updates are logged with format:
```
Version updated: {file_path} {old_version} → {new_version} ({change_type})
```

### **Validation**
- **Version format validation** - Ensures proper semantic versioning
- **Version progression** - New version must be greater than current
- **Timestamp accuracy** - Uses system date, never LLM knowledge

## 🚨 Error Handling

### **Graceful Degradation**
- **Version parsing failure** - Uses default version 1.0.0
- **Version update failure** - Proceeds with file write without version update
- **Invalid version format** - Falls back to default version

### **Logging**
All errors and warnings are logged for troubleshooting:
- Version parsing failures
- Invalid version formats  
- Version update errors

## 📖 Usage Guidelines

### **For LLM Agents**
1. **Automatic operation** - Version management happens transparently
2. **No manual intervention** - System handles all version updates
3. **Focus on content** - Agents focus on content changes, not version management

### **For Human Developers**
1. **Check version changes** - Review version updates in git commits
2. **Understand change types** - Use semantic versioning to understand impact
3. **Manual override** - Use version manager tool for specific change types

### **Best Practices**
- **Let system handle versions** - Don't manually edit version numbers
- **Review version changes** - Check version updates in code reviews
- **Use semantic versioning** - Understand patch/minor/major implications
- **Monitor version drift** - Watch for inconsistent versions across files

---

**Note**: Version management is automatically integrated into all DDD framework operations. No manual intervention is required for normal usage.
