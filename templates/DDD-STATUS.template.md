# DDD Status

**FORMAT SPECIFICATION:** This document must track the status and alignment of each DDD pass with drift indicators. Each pass entry must include:
- Status: Completed ✅, In Progress ⏸️, Pending ⏸️, Not Applicable 🚫, Ready ⏸️
- Alignment: Percentage with progress bar (e.g., 85% ████████░░)
- Drift: None 🟢, Low 🟡, Medium 🟠, High 🔴 with explanation
- Last Execution: Date when pass was last run
- Priority: High, Medium, Low based on current needs
- Notes: Brief explanation of current state
- Artifacts: List of deliverables with status indicators

**REQUIRED SECTIONS:**
1. Summary - Overall statistics
2. Pass Status Sections - Explanation of the repeating structure
3. Individual pass entries (Full Pass + 10 numbered passes)
4. Drift Indicators section
5. Metrics section

**PASS STRUCTURE:** Each DDD pass gets its own section following the same format. The document includes:
- Full Pass (comprehensive pass)
- 10 numbered passes (Foundation through Reverse)
- Each pass section repeats the same status tracking format

**METRICS CALCULATION:**

### Drift Calculation
**Drift** measures how much the current state deviates from the ideal state for a specific pass:
- **None (🟢):** 0-10% deviation - Current state matches pass objectives
- **Low (🟡):** 11-30% deviation - Minor gaps or inconsistencies
- **Medium (🟠):** 31-60% deviation - Significant gaps requiring attention
- **High (🔴):** 61-100% deviation - Major misalignment, pass needs re-execution

### Alignment Calculation
**Alignment** measures completion within the pass's specific scope:
- **100%:** All pass objectives fully achieved
- **80-99%:** Most objectives complete, minor items pending
- **60-79%:** Core objectives complete, some secondary items pending
- **40-59%:** Basic objectives complete, significant work remaining
- **0-39%:** Major objectives incomplete, pass needs substantial work

**TEMPLATE:**
<code>
# DDD Status

## 📊 Summary
- **Total Passes:** {{total_passes}}
- **Completed:** {{completed_count}} ✅
- **Pending:** {{pending_count}} ⏸️
- **Skipped:** {{skipped_count}} ⏭️
- **Documentation Drift:** {{overall_drift}} {{drift_icon}}
- **Last Full Pass:** {{last_full_pass_date}}
- **Last Sync Check:** {{last_sync_date}}

## � Pass Status Sections

**NOTE:** The following sections repeat for each DDD pass (Full Pass + 10 numbered passes). Each pass has its own dedicated section with status tracking, progress indicators, drift measurements, and execution artifacts.

**Pass Structure:**
- **🔄 Full Pass** - Comprehensive pass encompassing all aspects
- **1️⃣ Foundation Pass** - Creating foundational documentation and architecture
- **2️⃣ Documentation Pass** - Documenting features, requirements, and priorities
- **3️⃣ Implementation Pass** - Implementing features with basic test coverage
- **4️⃣ Testing Pass** - Adding comprehensive tests and verifying edge cases
- **5️⃣ Refactoring Pass** - Cleaning up code without changing functionality
- **6️⃣ Code Review Pass** - Reviewing PR changes and providing feedback
- **7️⃣ Synchronization Pass** - Aligning documentation with code at any scale
- **8️⃣ Quality Pass** - Verifying and improving documentation quality
- **9️⃣ Prune Pass** - Removing outdated or redundant content
- **🔟 Reverse Pass** - Detecting and addressing reverse drift (implementation without documentation)

---

## 🔄 Full Pass
- **Status:** {{status}} {{status_icon}}
- **Alignment:** {{alignment_percentage}}% {{progress_bar}} ({{alignment_description}})
- **Drift:** {{drift_level}} {{drift_icon}} ({{drift_explanation}})
- **Last Execution:** {{execution_date}}
- **Priority:** {{priority_level}}
- **Notes:** {{status_notes}}

*Note: Following section will repeat for each pass included in the DDD.*

## {{Pass Number Icon}} {{Pass Name}}
- **Status:** {{status}} {{status_icon}}
- **Alignment:** {{alignment_percentage}}% {{progress_bar}} ({{alignment_description}})
- **Drift:** {{drift_level}} {{drift_icon}} ({{drift_explanation}})
- **Last Execution:** {{execution_date}}
- **Priority:** {{priority_level}}
- **Notes:** {{status_notes}}
- **Artifacts:**
  - {{artifact_status}} {{artifact_name}} - {{artifact_description}}
  - {{artifact_status}} {{artifact_name}} - {{artifact_description}}
</template>

**EXAMPLE:** See the actual DDD-STATUS.md file in this project: [docs/DDD-STATUS.md]({{DDD_REMOTE_BASE}}/docs/DDD-STATUS.md)

**VALIDATION CHECKLIST:**
- [ ] All passes have status, alignment, drift, execution date, and priority
- [ ] Alignment percentages match the progress bar representation
- [ ] Drift levels are justified with explanations
- [ ] Artifacts list is complete and up-to-date
- [ ] Summary statistics match individual pass data

