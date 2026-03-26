---
name: aba-fusion-compare
description: ABA inclusion data comparison and IEP goal attainment skill. When the supervisor uploads inclusion daily feedback form PDFs and/or IEP documents, automatically extract inclusion intervention data (peer-mediated intervention, mainstreaming, group instruction attention rate, group instruction compliance, USOPAC, etc.), perform multi-day trend analysis, and compare against IEP goals for attainment determination. Supports weekly/daily mode (focused on current data trends) and monthly mode (global scan + kindergarten assessment dimension prompts). Applicable when uploading inclusion feedback forms for data analysis, comparing IEP goal achievement, or reviewing social/group/self-care dimension progress. Even if the user simply says "check the inclusion data" or "compare with IEP" or "how's inclusion this week," this skill should be triggered. Note: This skill has companion Python scripts - always use the scripts rather than writing your own parsing logic.
---

# ABA Inclusion Data Comparison and IEP Goal Attainment

## Overview

This skill extracts all inclusion intervention data from inclusion daily feedback form PDFs, performs trend analysis, and optionally compares with IEP goals for attainment determination.

## Prerequisites

```bash
sudo apt-get install -y poppler-utils
pip install openpyxl
```

## Two Operating Modes

### Mode A: Daily/Weekly Mode (Default)
Input: Inclusion feedback form PDFs x N days
Output: Inclusion data trend tables + text summary
Focuses on current intervention program data trajectories.

### Mode B: Monthly Global Mode
Input: Inclusion feedback form PDFs x N days + IEP document (optional)
Output: Trend tables + IEP attainment assessment + kindergarten assessment dimension global scan checklist
Use at month-end or for monthly summaries; provides comprehensive dimension review.

Usage:
```bash
# Mode A (daily)
python3 <skill_dir>/scripts/fusion_analyze.py \
  --files fusion1.pdf fusion2.pdf ... \
  --output report.xlsx

# Mode B (monthly global + IEP comparison)
python3 <skill_dir>/scripts/fusion_analyze.py \
  --files fusion1.pdf fusion2.pdf ... \
  --iep iep_document.docx \
  --mode monthly \
  --output report.xlsx
```

## Data Dimensions Extracted from Inclusion Feedback Forms

### Page 1 Data (Shared with session data skill)
- **Session programs**: Multi-trial programs (program name, percentage, mastery status)
- **Fluency programs**: e.g., clothespin squeezing (specific programs vary by student)

### Page 1 End - Inclusion Intervention Data
**Peer-Mediated Intervention Programs**:
- Game initiation: Independent count, prompted count, percentage
- Game response: Independent count, prompted count, percentage
- Specific peer intervention game programs (vary by student, e.g., imitation games, rule-based games): Independent count, prompted count, percentage

Note: Specific peer intervention game programs vary by student's intervention plan. The script extracts all data within the peer intervention section by row position, not by fixed program names.

### Page 2 Data
**Mainstreaming** (7 sub-items):
- Indoor activity prompt level (full physical / partial physical / minimal / independent)
- Outdoor activity prompt level
- Group instruction attention rate: total duration, attention duration, percentage
- Group instruction - individual instruction compliance: total attempts, responses, percentage
- Transition - outdoor following: total attempts, responses, percentage
- Group instruction compliance: total attempts, responses, percentage
- Requesting from teacher or peers: total attempts, independent attempts, percentage

**USOPAC Social Observation**:
- Target child row: U(Unoccupied), S(Solitary), O(Onlooker), P(Parallel), A(Associative), C(Cooperative), Independent initiation, Independent response
- Peer row: Same categories (for comparison)
- Note: USOPAC is not recorded daily; typically once per week, timing varies by classroom schedule

**Self-Care Skills**:
- Sleep: Bedtime, fall-asleep time, wake time
- Eating: Description per meal
- Toileting: Records

**Behavior Records**: Antecedent, teacher strategy, function, duration, frequency

**Daily Highlights + Daily Summary**: Text content (used in monthly mode to infer kindergarten assessment dimensions)

## IEP Goal Attainment Logic

When an IEP document is provided, the script will:
1. Extract all short-term goals and their expected criteria from the IEP
2. Compare current inclusion data against each goal
3. Output attainment status: Met / Approaching / Not Met / Insufficient Data

IEP goals typically involve these inclusion dimensions:
- Social domain: Peer initiation %, peer response %, USOPAC play types, requesting from teacher accuracy, number of recognized classmates, variety of social games, independent leisure time
- Group domain: Group instruction attention rate, individual instruction compliance rate, group instruction compliance rate, outdoor activity prompt level
- Self-care domain: Dressing, handwashing, eating independence

## Monthly Global Scan Checklist

Output additionally in monthly mode, based on 55 dimensions from the kindergarten assessment form:

### Part 1: IEP Goal Attainment Status
Current data, attainment determination, and trend direction for each IEP goal.

### Part 2: Skill Advancement Prompts
For mastered skills, suggest possible next steps:
- Example: "Independent peer response stable at 80% -> Consider adjusting prompt level for 'responding to peer invitations'"
- Example: "Individual instruction compliance exceeds target at 75% -> Next phase: focus on 'responding to group classroom instructions'"

### Part 3: Dimensions Requiring Attention
Filter from kindergarten assessment dimensions: items where feedback data suggests changes or need attention.

### Part 4: Supervisor Observation Prompts
List the 18 kindergarten assessment dimensions that cannot be automatically extracted from feedback forms, reminding the supervisor to observe during this month.

See `references/assessment_mapping.md` for detailed kindergarten assessment dimension mapping.

## Technical Notes

- Inclusion feedback form PDFs are 3 pages, far more complex than session feedback forms
- After pdftotext extraction, table columns are split into non-contiguous lines
- The script uses specialized parsers for each section, not a generic state machine
- "N/A" in peer intervention data means the activity was not conducted that day (not 0 times)
- Specific peer intervention game programs vary by student; the script extracts by position rather than hard-coded name matching
- USOPAC data is not recorded daily; recording frequency varies by classroom schedule; unrecorded days show "N/A"
- Group instruction attention duration format is "Xmin Ysec" and needs conversion to seconds for percentage calculation
- Some days may not have group instruction (e.g., outdoor activity days); empty attention rate is normal
- IEP documents are in docx format; pandoc converts to markdown before parsing
- IEP formats vary by BCBA; parsing logic uses semantic matching rather than hard-coded format
