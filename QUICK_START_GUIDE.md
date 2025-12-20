# Quick Start Guide - DMC Order Analytics Dashboard

A simple guide to get you started with the DMC Order Analytics Dashboard in under 5 minutes.

## What You Need

- Python 3.8 or higher installed
- Your order data in CSV format
- 5 minutes of your time

## Installation (One-Time Setup)

### Step 1: Download the Project

Download and extract the project files to your computer.

### Step 2: Open Terminal/Command Prompt

Navigate to the project folder:
```bash
cd path/to/DMC_Visualization
```

### Step 3: Install Requirements

Run this command:
```bash
pip install -r requirements.txt
```

Wait for all packages to install (takes 1-2 minutes).

## Running the Application

### Start the App

In your terminal, run:
```bash
streamlit run app.py
```

Your browser will automatically open to the dashboard. If not, go to: `http://localhost:8501`

## Using the Dashboard

### For Single Year Analysis

1. Click the **"Single Year Analysis"** tab
2. Click **"Browse files"** and select your CSV file
3. Wait for validation (you'll see a green checkmark if successful)
4. Scroll down to view:
   - Key metrics (Total Orders, Revenue, etc.)
   - Product summary table
   - Charts and graphs
5. Download cleaned data if needed

### For Multi-Year Comparison

1. Click the **"Multi-Year Comparison"** tab
2. Click **"Browse files"** and select **multiple** CSV files
3. The app will automatically:
   - Detect seasons from filenames
   - Merge the files
   - Add a "Season" column
4. View the merged data and download if needed

## Your CSV File Must Have These Columns

✅ Required:
- `Product name`
- `Copies`
- `Charged`

✅ Recommended (for better insights):
- `Charged amount`
- `Order status`

If your file is missing required columns, you'll see a helpful error message telling you what's missing.

## File Naming Tips (Multi-Year)

For automatic season detection, name your files like:
- `Papercut_orders-Fall2023.csv` → "Fall 2023"
- `orders-Spring2024.csv` → "Spring 2024"
- `DMC-Fall2025_1sthalf.csv` → "Fall 2025"

## Common Issues

### "Missing columns" Error
**Fix:** Make sure your CSV has `Product name`, `Copies`, and `Charged` columns.

### Can't Upload File
**Fix:** Ensure your file is saved as `.csv` (not `.xlsx`). Use Excel's "Save As" → "CSV" if needed.

### Charts Not Showing
**Fix:** Refresh the page and re-upload your file.

## What Happens to Your Data

The app automatically:
1. ✅ Validates your columns
2. ✅ Removes sensitive info (emails, customer names, etc.)
3. ✅ Cleans data formats
4. ✅ Creates visualizations
5. ✅ Lets you download the cleaned version

Your original file is **never modified**.

## Getting Help

- Read the full [README.md](README.md) for detailed documentation
- Check column names match exactly (case-sensitive)
- Try with a smaller file first if you have issues

## Quick Tips

- Always preview your data before trusting the visualizations
- Download cleaned data for your records
- Start with single year analysis before multi-year comparison
- Keep your CSV files organized with clear naming

## That's It!

You're ready to analyze your DMC order data. Upload your first file and explore the insights!

---

**Need More Help?** See the full [README.md](README.md) documentation.
