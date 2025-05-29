# DDD Workflow - Layered ASCII Diagram with Pass Hooks & Individual Steps

**Version:** 1.0.0
**Last Updated:** 2024-12-19
**Sync with:** workflows/ddd-workflow.yml

**Architecture:**
- **Top Layer:** Generic Pass Hooks (Before & Skip) - Auto-run before any pass
- **Middle Layer:** DDD Passes with Individual Steps (Scan→Draft→Ask→Sync)
- **Bottom Layer:** Generic Pass Hooks (After & Error) - Auto-run after any pass

```
🚀 DDD WORKFLOW - LAYERED PASSES WITH HOOKS & INDIVIDUAL STEPS

┌─────────────────────────────────────────────────────────────────────────────┐
│                              🚀 DDD START                                  │
│                           [Project State?]                                 │
│                                                                             │
│  Entry Points Based on .agent3d-config.yml:                               │
│  • New Project      → Requirements Pass (Step 0)                          │
│  • Existing+Changes → Synchronization Pass (Step 3)                       │
│  • Code Review Only → Code Review Pass (Step 4)                           │
│  • Quick Sync       → Synchronization Pass (Step 3)                       │
│  • Documentation    → Documentation Pass (Step 6)                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│              🔧 GENERIC PASS HOOKS - BEFORE & SKIP (Top Layer)             │
│                                                                             │
│  🚀 pass.before (Auto-runs before ANY pass):                              │
│     • Check .agent3d-config.yml configuration                             │
│     • Validate enabled_passes list                                        │
│     • Setup workspace and environment                                     │
│     • Initialize DDD-STATUS.md tracking                                   │
│     • Create execution plan branch (exec-plan/{pass-name})                │
│     • Log start time and pass metadata                                    │
│                                                                             │
│  ⏭️ pass.skip (Auto-runs when ANY pass is skipped):                       │
│     • Log skip reason and context                                         │
│     • Update DDD-STATUS.md with skipped status                           │
│     • Maintain workflow state consistency                                 │
│     • Notify stakeholders of skip decision                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    🎯 DDD PASSES LAYER WITH INDIVIDUAL STEPS               │
│                     (Based on enabled_passes in config)                    │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                     📋 REQUIREMENTS PASS (Step 0)                      │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │ │
│  │  │    SCAN     │ │    DRAFT    │ │     ASK     │ │    SYNC     │      │ │
│  │  │ • Review    │ │ • Create    │ │ • Validate  │ │ • Finalize  │      │ │
│  │  │   existing  │ │   REQUIRE-  │ │   with      │ │   REQ-NNNN  │      │ │
│  │  │   docs      │ │   MENTS.md  │ │   stake-    │ │   IDs       │      │ │
│  │  │ • Identify  │ │ • Assign    │ │   holders   │ │ • Get       │      │ │
│  │  │   gaps      │ │   REQ-NNNN  │ │ • Clarify   │ │   approval  │      │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘      │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                     🏗️ FOUNDATION PASS (Step 1)                       │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │ │
│  │  │    SCAN     │ │    DRAFT    │ │     ASK     │ │    SYNC     │      │ │
│  │  │ • Check     │ │ • Create    │ │ • Configure │ │ • Save      │      │ │
│  │  │   require-  │ │   .agent3d- │ │   project   │ │   config    │      │ │
│  │  │   ments     │ │   config    │ │   settings  │ │ • Create    │      │ │
│  │  │ • Review    │ │ • Setup     │ │ • Select    │ │   structure │      │ │
│  │  │   project   │ │   templates │ │   passes    │ │ • Initialize│      │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘      │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                     🔨 DEVELOPMENT PASS (Step 2)                       │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │ │
│  │  │  PLANNING   │ │IMPLEMENTAT'N│ │   TESTING   │ │    SYNC     │      │ │
│  │  │ • Create    │ │ • Implement │ │ • Execute   │ │ • Validate  │      │ │
│  │  │   FEATURES  │ │   features  │ │   all tests │ │   FT→TC     │      │ │
│  │  │ • FT-NNNN   │ │ • Add FT    │ │ • Check     │ │   links     │      │ │
│  │  │   IDs       │ │   comments  │ │   coverage  │ │ • Update    │      │ │
│  │  │ • TC-NNNN   │ │ • Create    │ │ • Quality   │ │   matrix    │      │ │
│  │  │   test cases│ │   tests     │ │   validation│ │             │      │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘      │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                     🔄 SYNCHRONIZATION PASS (Step 3)                   │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │ │
│  │  │    SCAN     │ │    DRAFT    │ │     ASK     │ │    SYNC     │      │ │
│  │  │ • Scan all  │ │ • Generate  │ │ • Review    │ │ • Fix       │      │ │
│  │  │   files for │ │   drift     │ │   drift     │ │   issues    │      │ │
│  │  │   IDs       │ │   report    │ │   issues    │ │ • Update    │      │ │
│  │  │ • Extract   │ │ • Create    │ │ • Validate  │ │   trace-    │      │ │
│  │  │   patterns  │ │   matrix    │ │   fixes     │ │   ability   │      │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘      │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                     👁️ CODE REVIEW PASS (Step 4)                       │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │ │
│  │  │    SCAN     │ │    DRAFT    │ │     ASK     │ │    SYNC     │      │ │
│  │  │ • Review    │ │ • Generate  │ │ • Review    │ │ • Apply     │      │ │
│  │  │   code      │ │   review    │ │   findings  │ │   fixes     │      │ │
│  │  │ • Check     │ │   reports   │ │ • Validate  │ │ • Update    │      │ │
│  │  │   standards │ │ • Language  │ │   fixes     │ │   standards │      │ │
│  │  │ • Test      │ │   specific  │ │ • Approve   │ │ • Generate  │      │ │
│  │  │   quality   │ │   checks    │ │   changes   │ │   reports   │      │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘      │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                     ♻️ REFACTORING PASS (Step 5)                       │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │ │
│  │  │    SCAN     │ │    DRAFT    │ │     ASK     │ │    SYNC     │      │ │
│  │  │ • Analyze   │ │ • Apply DRY │ │ • Review    │ │ • Verify    │      │ │
│  │  │   code      │ │   principles│ │   changes   │ │   tests     │      │ │
│  │  │ • Identify  │ │ • Horizontal│ │ • Validate  │ │ • Update    │      │ │
│  │  │   duplicat'n│ │   merging   │ │   quality   │ │   docs      │      │ │
│  │  │ • Plan      │ │ • Improve   │ │ • Test      │ │ • Maintain  │      │ │
│  │  │   improve-  │ │   structure │ │   coverage  │ │   ID links  │      │ │
│  │  │   ments     │ │             │ │             │ │             │      │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘      │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                     📚 DOCUMENTATION PASS (Step 6)                     │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │ │
│  │  │    SCAN     │ │    DRAFT    │ │     ASK     │ │    SYNC     │      │ │
│  │  │ • Review    │ │ • Compress  │ │ • Validate  │ │ • Finalize  │      │ │
│  │  │   all docs  │ │   content   │ │   changes   │ │   docs      │      │ │
│  │  │ • Identify  │ │ • Remove    │ │ • Check     │ │ • Generate  │      │ │
│  │  │   redundancy│ │   redundant │ │   cross-    │ │   index     │      │ │
│  │  │ • Plan      │ │   content   │ │   refs      │ │ • Validate  │      │ │
│  │  │   compress'n│ │ • Update    │ │ • Test      │ │   rendering │      │ │
│  │  │             │ │   links     │ │   markdown  │ │             │      │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘      │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│              🔧 GENERIC PASS HOOKS - AFTER & ERROR (Bottom Layer)          │
│                                                                             │
│  ✅ pass.after (Auto-runs after ANY pass completes):                      │
│     • Run drift scanner for validation                                    │
│     • Update DDD-STATUS.md with completion metrics                        │
│     • Calculate alignment percentage (0-100%)                             │
│     • Determine drift level (none/low/medium/high)                        │
│     • Generate pass-specific reports and artifacts                        │
│     • Auto-commit progress to exec-plan branch                            │
│     • Tag checkpoints and milestones                                      │
│                                                                             │
│  ❌ pass.error (Auto-runs when ANY pass fails):                           │
│     • Log detailed error information                                      │
│     • Update DDD-STATUS.md with error status                             │
│     • Cleanup partial work and temporary files                           │
│     • Send notifications (if configured)                                  │
│     • Prepare retry with error context                                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         📦 DELIVERABLES & ARTIFACTS                        │
│                                                                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │REQUIREMENTS │ │ FEATURES.md │ │TEST-CASES.md│ │    CODE     │          │
│  │    .md      │ │ FT-NNNN IDs │ │ TC-NNNN IDs │ │IMPLEMENTATION│          │
│  │ REQ-NNNN    │ │ Linked to   │ │ Linked to   │ │   & TESTS   │          │
│  │ Identifiers │ │ REQ-NNNN    │ │ FT-NNNN     │ │ With TC-IDs │          │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘          │
│                                                                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │   DRIFT     │ │ DDD-STATUS  │ │ EXECUTION   │ │ TRACEABILITY│          │
│  │  REPORTS    │ │    .md      │ │   PLANS     │ │   MATRIX    │          │
│  │ Multi-mode  │ │ Pass status │ │ docs/runs/  │ │ REQ↔FT↔TC   │          │
│  │ Detection   │ │ Alignment % │ │ Checkpoints │ │ Validation  │          │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘          │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
                              🎉 DDD COMPLETE

DETAILED HOOK EXECUTION FLOWS:

🔄 STANDARD PASS EXECUTION (Scan → Draft → Ask → Sync):

   1. pass.before hook auto-runs:
      • Load .agent3d-config.yml configuration
      • Check enabled_passes list for current pass
      • Validate pass dependencies and prerequisites
      • Create exec-plan/{pass-name} branch
      • Initialize DDD-STATUS.md entry for this pass
      • Setup workspace and required tools

   2. PASS EXECUTES (4-phase workflow):
      • SCAN: Review current state, identify gaps
      • DRAFT: Create/update documentation and artifacts
      • ASK: Interactive validation and clarification
      • SYNC: Finalize changes and update relationships

   3. pass.after hook auto-runs:
      • Run drift scanner for validation
      • Update DDD-STATUS.md with completion metrics
      • Calculate alignment percentage (0-100%)
      • Determine drift level (none/low/medium/high)
      • Generate pass-specific reports
      • Auto-commit progress to exec-plan branch
      • Tag checkpoints and milestones

🔀 IDENTIFIER PATTERN FLOWS:

   Foundation Pass → Setup patterns in .agent3d-config.yml:
   • REQ-[A-Z]+-\d+(-[a-z])? for requirements
   • FT-[A-Z]+-\d+(-[a-z])? for features
   • TC-[A-Z]+-\d+(-[a-z])? for test cases

   Development Pass → Create and link identifiers:
   • Planning: FT-NNNN ← REQ-NNNN mapping
   • Implementation: Code with FT-NNNN comments
   • Testing: TC-NNNN ← FT-NNNN mapping

   Synchronization Pass → Validate relationships:
   • Scan all files for identifier patterns
   • Validate REQ ↔ FT ↔ TC traceability chains
   • Generate drift reports for broken links
   • Update traceability matrix

📊 STATUS TRACKING & METRICS:

   DDD-STATUS.md tracks for each pass:
   • Status: pending/scanning/drafting/asking/syncing/complete/failed
   • Alignment: 0-100% completion percentage
   • Drift: none/low/medium/high deviation level
   • Last Execution: timestamp of last run
   • Priority: critical/high/medium/low
   • Artifacts: list of generated deliverables

   Health Indicators:
   • Critical Issues count
   • Documentation Gaps count
   • Implementation Drift level
   • Quality Score (0-100)

⚡ CONFIGURATION-DRIVEN BEHAVIOR:

   From .agent3d-config.yml:
   • enabled_passes: Controls which passes are active
   • pass_config: Pass-specific settings and thresholds
   • git_workflow: Auto-commit and branching behavior
   • quality_level: comprehensive/strict/balanced/relaxed
   • execution_mode: comprehensive_full_pass/selective

   Hooks adapt behavior based on configuration:
   • Auto-commit frequency (checkpoint_frequency: 3)
   • Branch naming (exec-plan/{pass-name})
   • Quality thresholds and validation rules
   • Drift detection sensitivity levels
```
