# DDD Workflow System

This directory contains the comprehensive workflow definitions for the Document-Driven Development (DDD) framework, including both core DDD workflows and specialized migration workflows.

## 📁 Files Overview

### **Core DDD Workflows**
| File | Purpose | Target Audience | Format |
|------|---------|-----------------|--------|
| `ddd-workflow.yml` | **Primary workflow definition** | LLMs, Automation | YAML |
| `ddd-workflow-ascii.md` | **ASCII diagram with details** | All users, Documentation | ASCII Art |
| `ddd-workflow.mmd` | **Architecture diagram** | Humans, Documentation | Mermaid Architecture |
| `ddd-workflow-simple.mmd` | **Simple block diagram** | Quick reference | Mermaid Block |
| `ddd-workflow-layered.mmd` | **Layered flowchart** | Complex flows | Mermaid Flowchart |

### **Migration Workflows**
| File | Purpose | Target Audience | Format |
|------|---------|-----------------|--------|
| `test-cases-migration.yml` | **TEST-CASES.md → Features migration** | DDD Projects, LLMs | YAML |
| `legacy-structure-migration.yml` | **Legacy → Modern DDD migration** | Project Teams | YAML |

### **Validation & Tools**
| File | Purpose | Target Audience | Format |
|------|---------|-----------------|--------|
| `validate-sync.py` | **Synchronization validator** | Maintenance, CI/CD | Python |
| `test-mermaid.py` | **Mermaid syntax validator** | Development | Python |
| `README.md` | **Documentation and usage guide** | All users | Markdown |

## 🔄 Synchronization System

The workflow system uses a **dual-format approach** to serve both LLMs and humans effectively:

### **YAML Workflow (Primary)**
- **Machine-readable** format for LLM processing
- **Detailed step definitions** with actions, conditions, and validation
- **Structured data** for automated workflow execution
- **Complete error handling** and recovery procedures

### **ASCII Diagram (Universal - .md format)**
- **Repository-based details** (`ddd-workflow-ascii.md`) - Implementation-specific documentation
- **Pass hooks system** showing auto-running generic hooks (before/after/error/skip)
- **Identifier patterns** and configuration-driven behavior from .agent3d-config.yml
- **Status tracking** and metrics calculation details for DDD-STATUS.md
- **Universal compatibility** - works in any text editor, terminal, or documentation system
- **Comprehensive execution flows** with real implementation details

### **Mermaid Architecture Diagrams (.mmd format)**
- **Architecture diagram** (`ddd-workflow.mmd`) - Detailed service-oriented view with hooks
- **Simple block diagram** (`ddd-workflow-simple.mmd`) - Clean grid layout for quick reference
- **Layered flowchart** (`ddd-workflow-layered.mmd`) - Complex flows with multiple paths
- **Pure Mermaid syntax** for optimal tool support and rendering
- **Interactive diagrams** that render in GitHub, VS Code, and Mermaid tools
- **Visual workflow representation** for training and communication

### **Synchronization Rules**
1. **Content must match** between YAML and Mermaid
2. **Step IDs must correspond** (e.g., `step-0-requirements` ↔ `STEP0`)
3. **Decision logic must align** (conditions and paths)
4. **Deliverables must be consistent**
5. **Versions must be synchronized**

## 🚀 Usage Instructions

### **For LLMs (Automated Processing)**

```python
import yaml

# Load workflow definition
with open('workflows/ddd-workflow.yml', 'r') as f:
    workflow = yaml.safe_load(f)

# Access step definitions
steps = workflow['workflow']['steps']
current_step = steps['step-0-requirements']

# Execute actions
for action in current_step['actions']:
    print(f"Executing: {action}")

# Check success criteria
for criteria in current_step['success_criteria']:
    print(f"Validating: {criteria}")
```

### **For Humans (Visual Reference)**

#### **Option 1: VS Code (Recommended)**
1. Install **Mermaid Preview** extension
2. Open `workflows/ddd-workflow.mmd`
3. Use **Ctrl+Shift+P** → "Mermaid: Preview"

#### **Option 2: GitHub**
1. Navigate to `workflows/ddd-workflow.mmd` on GitHub
2. GitHub automatically renders Mermaid diagrams

#### **Option 3: Mermaid Live Editor**
1. Copy content from `ddd-workflow.mmd`
2. Paste into [Mermaid Live Editor](https://mermaid.live/)

#### **Option 4: Command Line**
```bash
# Install Mermaid CLI
npm install -g @mermaid-js/mermaid-cli

# Generate PNG/SVG
mmdc -i workflows/ddd-workflow.mmd -o workflow-diagram.png
```

### **For Implementation (Development)**

```bash
# Validate synchronization
python workflows/validate-sync.py

# Check workflow structure
python -c "import yaml; print(yaml.safe_load(open('workflows/ddd-workflow.yml'))['metadata'])"

# Preview Mermaid diagram
code workflows/ddd-workflow.mmd  # Opens in VS Code with Mermaid preview
```

## 🔍 Validation and Maintenance

### **Automatic Validation**

Run the synchronization validator:

```bash
cd /path/to/project
python workflows/validate-sync.py
```

**Exit Codes:**
- `0` - Perfect synchronization
- `1` - Synchronization issues found

### **Manual Validation Checklist**

- [ ] All YAML steps have corresponding Mermaid nodes
- [ ] Decision conditions match between formats
- [ ] Action lists are consistent
- [ ] Input/output dependencies align
- [ ] Error handling paths are complete
- [ ] Final deliverables match exactly
- [ ] Version numbers are synchronized
- [ ] Last updated dates match

### **Update Procedures**

#### **When Modifying Workflow:**

1. **Update YAML first** (primary source of truth)
2. **Update corresponding Mermaid nodes**
3. **Verify decision logic alignment**
4. **Update metadata** (version, date) in both files
5. **Run validation script**
6. **Fix any synchronization issues**

#### **Version Control:**

```bash
# Before committing changes
python workflows/validate-sync.py

# Commit both files together
git add workflows/ddd-workflow.yml workflows/ddd-workflow.mmd
git commit -m "Update DDD workflow: [description]"
```

## 📊 Workflow Structure

### **Step Hierarchy**
```
DDD Workflow
├── Step 0: Requirements Pass
├── Step 1: Foundation Pass
├── Step 2: Development Pass
│   ├── Planning Sub-Pass
│   ├── Implementation Sub-Pass
│   └── Testing Sub-Pass
├── Step 3: Synchronization Pass
├── Step 4: Code Review Pass
├── Step 5: Refactoring Pass
└── Step 6: Documentation Pass
```

### **Key Components**

- **Entry Points**: Multiple workflow entry points based on project state
- **Decision Logic**: Conditional branching with clear criteria
- **Error Handling**: Recovery procedures for common failure scenarios
- **Validation**: Success criteria and quality gates
- **Traceability**: Complete REQ → FT → TC → Test chain
- **Deliverables**: Clear outputs for each step

## 🎯 Best Practices

### **For LLM Processing**
- Always reference the YAML file for execution
- Follow decision conditions exactly as specified
- Implement all validation criteria
- Use error handling procedures when issues occur
- Maintain workflow state for recovery

### **For Human Usage**
- Start with the Mermaid flowchart (`.mmd`) for overview
- Reference YAML for detailed implementation
- Use VS Code with Mermaid extension for best experience
- Follow maintenance procedures for updates

### **For System Integration**
- Parse YAML for automated workflow engines
- Use Mermaid for documentation generation
- Implement validation in CI/CD pipelines
- Monitor synchronization in version control

## 🔧 Troubleshooting

### **Common Issues**

1. **Synchronization Errors**
   - Run `validate-sync.py` to identify issues
   - Check step ID mappings
   - Verify decision logic alignment

2. **YAML Parsing Errors**
   - Validate YAML syntax
   - Check indentation and structure
   - Verify required fields are present

3. **Mermaid Rendering Issues**
   - Check Mermaid syntax
   - Verify node connections
   - Ensure proper styling classes

### **Getting Help**

- Check validation script output for specific errors
- Review synchronization rules in flowchart documentation
- Verify against workflow structure examples
- Test with minimal workflow subset

## 📈 Future Enhancements

- **Automated sync validation** in CI/CD
- **Workflow execution engine** based on YAML
- **Interactive workflow navigator**
- **Performance metrics** and optimization
- **Multi-language workflow support**
