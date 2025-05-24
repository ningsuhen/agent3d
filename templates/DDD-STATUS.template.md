# DDD Status

**FORMAT SPECIFICATION:** Tracks DDD pass status, alignment, and project health. Each pass includes status, alignment %, drift level, execution date, priority, and artifacts.

**REQUIRED SECTIONS:** Summary, Pass Status, Individual Passes (Full + 10 numbered), Health Indicators

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

## 📋 Pass Status

**Structure:** Full Pass + 10 numbered passes (Foundation → Documentation → Implementation → Testing → Refactoring → Code Review → Synchronization → Quality → Prune → Reverse)

## 🏥 Health Indicators
- **Critical Issues:** {{critical_count}} 🚨
- **Documentation Gaps:** {{doc_gaps}} 📝
- **Implementation Drift:** {{impl_drift}} ⚠️
- **Quality Score:** {{quality_score}}/100 📊

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

**EXAMPLE:** See the actual DDD-STATUS.md file in the local repository: `~/.agent3d/docs/DDD-STATUS.md`

**VALIDATION CHECKLIST:**
- [ ] All passes have status, alignment, drift, execution date, and priority
- [ ] Alignment percentages match the progress bar representation
- [ ] Drift levels are justified with explanations
- [ ] Artifacts list is complete and up-to-date
- [ ] Summary statistics match individual pass data
- [ ] Health indicators reflect current project state
- [ ] Each pass section follows the same format structure

