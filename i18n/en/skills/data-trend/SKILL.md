---
name: aba-data-trend
description: ABA session data trend analysis skill. When the supervisor uploads recent daily feedback forms (PDF format), automatically extract session program data, analyze percentage trends, mastery status, and learning velocity for each program, generating structured comparison tables and text summaries. Applicable when uploading multiple days of feedback forms for trend analysis, comparing recent program progress, checking which programs are approaching mastery criteria, or which are stalled and need adjustment. Even if the user simply says "check the recent data" or "analyze these feedback forms," this skill should be triggered. Note: This skill has companion Python scripts - always use the scripts rather than writing your own parsing logic.
---

# ABA Session Data Trend Analysis

## Overview

This skill extracts **session program** data from daily feedback form PDFs, performs multi-day trend analysis, and outputs structured Excel reports and text summaries.

## Prerequisites

Ensure the following are installed before running:
```bash
# PDF text extraction tool (required)
sudo apt-get install -y poppler-utils
# Python dependency (required)
pip install openpyxl
```

## Usage

**Step 1**: User uploads 1-10 daily feedback form PDF files.

**Step 2**: After confirming file paths, call the script in this skill's directory:

```bash
python3 <skill_dir>/scripts/analyze.py \
  --files <pdf1> <pdf2> <pdf3> ... \
  --output <output_dir>/session_data_trend_analysis.xlsx
```

Parameters:
- `--files`: One or more PDF file paths, space-separated
- `--output`: Output Excel file path (defaults to `session_data_trend_analysis.xlsx` in current directory)
- `--student`: Student name (optional, script auto-extracts from PDF)

**Step 3**: The script automatically:
1. Extracts PDF text using `pdftotext` (more reliable than direct PDF reading)
2. Parses session program data (program name, percentage, mastery status)
3. Sorts by date, builds a program x date data matrix
4. Calculates trend direction, mean, and mastery status for each program
5. Generates an Excel report (data table sheet + text summary sheet)
6. Outputs text summary to terminal

**Step 4**: Send the generated Excel file to the user and present key findings from the text summary in the conversation.

## Supported Feedback Form Formats

### Session Feedback Form (1-page PDF)
- Filename example: `BR-EY-MRFK-LQL20260316session_daily_feedback.pdf`
- Contains: Multi-trial program table (program name, percentage, mastery status), fluency programs, negative behaviors, daily highlights

### Inclusion Feedback Form (3-page PDF)
- Filename example: `BR-EY-MRFK-LQL20260316inclusion_daily_feedback.pdf`
- Page 1 contains session programs (this skill extracts this part); remaining pages have inclusion data

Both formats are correctly parsed; the script auto-detects the format.

## Data Parsing Rules

### Multi-Trial Programs
- **Percentage data**: 0%-100%, where 0% is valid data
- **"N/A" marker**: Indicates the program was not run that day, excluded from mean calculation
- **Mastery criterion**: Extracted from header ("3 consecutive days at 80%" or "3 consecutive days at 90%")
- **Mastery status**: Yes/No

### Program Name Matching
The same program may have name variants across days; the script performs standardized matching:
- `Social Story-Sharing-Answering` matches `Social Story "Sharing"-Answering`
- But `Social Game-Freeze Tag (Full Game)` does not match `Social Game-Freeze Tag (Phase: Tagger)` (different teaching phases)

### Date Extraction
Dates are extracted from filenames first, falling back to date fields within the PDF content.

## Trend Assessment Criteria

| Trend Marker | Assessment Rule |
|---------|--------|
| Star - Stable High | All data points >= 80% |
| Up Arrow - Rising | Second half mean is 15+ percentage points higher than first half |
| Down Arrow - Declining | Second half mean is 15+ percentage points lower than first half |
| Wave - Fluctuating | Changes present but doesn't meet rising/declining criteria |
| Down Triangle - Persistent Low | All data points <= 20% |
| Insufficient Data | Fewer than 2 valid data points |

## Output Description

### Excel Report (Two Sheets)

**Sheet 1: Session Data Trends**
- Grouped by domain (Language/Cognitive, Listening Comprehension, Social, Cognitive/Conversation, Fine Motor/Fluency)
- One row per program, showing daily percentages, mean, trend, mastery status
- Color coding: Green = >= 80%, Red = <= 20%

**Sheet 2: Text Summary**
- Ready to copy-paste into monthly reports
- Contains: Mastered programs, near-mastery programs, rising trends, declining trends, persistent low programs, data overview

## Important Notes

- **Always use the script**: Do not write your own PDF parsing logic. The script's state machine parser has been thoroughly tested against the feedback form format.
- **Program name variants**: If the script identifies the same program as two different programs (due to naming differences), alert the user in the output.
- **Mastery criterion changes**: Some data may use 90% criterion while later data uses 80%; the script handles each according to its respective criterion.
