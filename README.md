# DMC Order Analytics Dashboard

A comprehensive data visualization and analysis tool for DMC (Digital Media Center) order data. This application provides insights into order patterns, revenue, product performance, and more.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [How to Use](#how-to-use)
- [Data Requirements](#data-requirements)
- [Application Modes](#application-modes)
- [Visualizations](#visualizations)
- [Deployment Guide](#deployment-guide)
- [Troubleshooting](#troubleshooting)
- [Support](#support)

---

## Overview

The DMC Order Analytics Dashboard is a Streamlit-based web application designed to help stakeholders visualize and analyze order data efficiently. It supports both single-year analysis and multi-year comparisons, with automatic data cleaning and validation.

### Key Benefits

- **Easy Data Upload**: Simple drag-and-drop interface for CSV files
- **Automatic Validation**: Ensures data quality before processing
- **Comprehensive Analytics**: Multiple visualizations and metrics
- **Data Cleaning**: Removes sensitive/unnecessary columns automatically
- **Multi-Year Support**: Compare trends across different seasons/years
- **Export Capability**: Download cleaned data for further analysis

---

## Features

### Current Features (v1.0)

- ✅ Single Year Analysis with comprehensive visualizations
- ✅ Multi-Year Data Merging with season tracking
- ✅ Automatic data validation and cleaning
- ✅ Smart encoding detection (UTF-8, Latin-1, CP1252)
- ✅ Interactive charts and tables
- ✅ CSV export of cleaned data
- ✅ Responsive design for various screen sizes

### Upcoming Features

- 🔄 Multi-Year Comparison Visualizations
- 🔄 Trend Analysis Charts
- 🔄 Advanced Filtering Options
- 🔄 Custom Report Generation

---

## Requirements

### System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **RAM**: Minimum 4GB (8GB recommended for large datasets)
- **Browser**: Modern web browser (Chrome, Firefox, Safari, Edge)

### Python Dependencies

All required packages are listed in `requirements.txt`:

```
pandas>=1.5.0
matplotlib>=3.5.0
seaborn>=0.12.0
numpy>=1.23.0
openpyxl>=3.0.0
streamlit>=1.28.0
```

---

## Installation

### Step 1: Clone or Download the Repository

```bash
git clone https://github.com/yourusername/DMC_Visualization.git
cd DMC_Visualization
```

Or download and extract the ZIP file.

### Step 2: Create a Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
streamlit --version
```

You should see the Streamlit version number if installation was successful.

---

## How to Use

### Starting the Application

1. **Open Terminal/Command Prompt** in the project directory

2. **Activate Virtual Environment** (if using one)

3. **Run the Application:**
   ```bash
   streamlit run app.py
   ```

4. **Access the Dashboard:**
   - The application will automatically open in your default web browser
   - If not, navigate to: `http://localhost:8501`

### Using the Application

#### Single Year Analysis

1. **Navigate to the "Single Year Analysis" tab**

2. **Upload Your CSV File:**
   - Click "Browse files" or drag & drop your CSV file
   - Supported format: `.csv`

3. **Validation:**
   - The app will automatically validate your file
   - If required columns are missing, you'll see an error message with details
   - Ensure your file contains: `Product name`, `Copies`, `Charged`

4. **View Results:**
   - Preview raw and cleaned data
   - Explore interactive visualizations
   - Review key metrics (total orders, revenue, etc.)

5. **Download Cleaned Data:**
   - Click "Download Cleaned CSV" to save the processed data

#### Multi-Year Comparison

1. **Navigate to the "Multi-Year Comparison" tab**

2. **Upload Multiple CSV Files:**
   - Click "Browse files" and select multiple CSV files
   - Or drag & drop multiple files at once

3. **Season Detection:**
   - The app automatically extracts season information from filenames
   - Example: `Papercut_orders-Fall2023_1sthalf.csv` → "Fall 2023"

4. **Merging Process:**
   - Files are validated individually
   - A "Season" column is added to track data origin
   - All valid files are merged into one dataset

5. **View Results:**
   - See season distribution
   - Preview merged and cleaned data
   - Download merged dataset

---

## Data Requirements

### Required Columns

Your CSV file **must** contain these columns:

- `Product name` - Type of product/service ordered
- `Copies` - Number of copies ordered
- `Charged` - Whether the order was charged (Yes/No)

### Optional Columns (Recommended)

These columns enhance the visualizations:

- `Charged amount` - Dollar amount charged
- `Order status` - Current status of the order
- `Order number` - Unique identifier
- `Date submitted` - When order was placed

### Columns That Will Be Removed

For privacy and clarity, these columns are automatically removed:

- Room name / Title
- Customer / Customer name
- Email
- Last status update
- Charged time / account type / account name
- Filename
- Additional instructions
- Operator names (from Special Information and Print Information)

### File Naming Convention (Multi-Year)

For best results with multi-year analysis, name your files like:

- `Papercut_orders-Fall2023_1sthalf.csv`
- `Papercut_orders-Spring2024_2ndhalf.csv`
- `orders-Fall2025.csv`

The app will extract: **Fall 2023**, **Spring 2024**, **Fall 2025**

---

## Application Modes

### 1. Single Year Analysis

**Purpose:** Analyze data from a single season or year in detail.

**What You Get:**
- Key metrics dashboard (total orders, revenue, copies, charge rate)
- Product summary table with totals
- Charging status distribution (bar and pie charts)
- Copies by product type (horizontal bar chart)
- Revenue by product type (horizontal bar chart)
- Order status distribution (if available)

**Best For:**
- Detailed analysis of a specific period
- Understanding product performance
- Identifying charging patterns
- Quick insights into operations

### 2. Multi-Year Comparison

**Purpose:** Compare data across multiple seasons/years.

**What You Get:**
- Combined dataset with season tracking
- Season distribution visualization
- Merged data preview and download
- Future: Trend analysis and comparison charts

**Best For:**
- Identifying seasonal trends
- Year-over-year comparisons
- Long-term pattern analysis
- Strategic planning

---

## Visualizations

### Key Metrics Dashboard

Four primary metrics displayed at the top:

1. **Total Orders** - Count of all orders
2. **Total Revenue** - Sum of all charged amounts
3. **Total Copies** - Sum of all copies ordered
4. **Charged Orders** - Percentage of orders that were charged

### Charts and Graphs

#### 1. Product Summary Table
- Lists all products with totals
- Columns: Charged Amount, Copies, Order Count
- Sortable and formatted with currency/commas
- Includes grand total row

#### 2. Charging Status Visualizations
- **Bar Chart**: Count of orders by charge status (Yes/No/Unknown)
- **Pie Chart**: Percentage distribution of charge status
- Value labels for easy reading

#### 3. Copies by Product Type
- Horizontal bar chart
- Shows total copies for each product
- Sorted from lowest to highest
- Value labels on bars

#### 4. Revenue by Product Type
- Horizontal bar chart
- Shows total revenue for each product
- Formatted with dollar signs
- Color-coded for clarity

#### 5. Order Status Distribution
- Top 10 order statuses
- Bar chart and data table
- Shows operational workflow patterns

---

## Deployment Guide

### Local Deployment

Follow the [Installation](#installation) and [How to Use](#how-to-use) sections above.

### Cloud Deployment

#### Option 1: Streamlit Community Cloud (Free)

1. **Push Code to GitHub:**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file: `app.py`
   - Click "Deploy"

3. **Access Your App:**
   - You'll get a public URL like: `https://yourapp.streamlit.app`
   - Share this URL with stakeholders

#### Option 2: Heroku

1. **Create `Procfile`:**
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Deploy:**
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

#### Option 3: AWS/Azure/GCP

- Use container services (Docker)
- Deploy as a web service
- Configure appropriate security groups and networking

### Production Considerations

- **Security**: Add authentication if handling sensitive data
- **Scaling**: Use cloud services for high traffic
- **Backup**: Regularly backup uploaded data
- **Monitoring**: Set up logging and error tracking
- **Updates**: Keep dependencies updated for security

---

## Troubleshooting

### Common Issues and Solutions

#### Issue: "Missing columns in CSV"

**Problem:** Your CSV doesn't have required columns.

**Solution:**
- Check the error message for missing column names
- Ensure your CSV has: `Product name`, `Copies`, `Charged`
- Column names must match exactly (case-sensitive)

#### Issue: "File upload fails" or "Encoding error"

**Problem:** File too large, incorrect format, or encoding issues.

**Solution:**
- Ensure file is in CSV format (not Excel .xlsx)
- The app automatically handles different encodings (UTF-8, Latin-1, CP1252)
- Try with a smaller file first
- Check file isn't corrupted
- Use the `data_cleaner.py` script first to clean your data
- If using Excel, try "Save As" → "CSV UTF-8"

#### Issue: "Visualizations not showing"

**Problem:** Data issues or browser compatibility.

**Solution:**
- Check browser console for errors
- Try refreshing the page
- Ensure data has numeric values for Copies and Charged amount
- Try a different browser (Chrome recommended)

#### Issue: "Season not detected properly"

**Problem:** Filename doesn't match expected pattern.

**Solution:**
- Use format: `filename-Fall2023.csv` or `filename-Spring2024.csv`
- Include year and season in filename
- Alternatively, manually add a "Season" column to your CSV

#### Issue: "Application won't start"

**Problem:** Missing dependencies or Python version.

**Solution:**
```bash
# Check Python version (need 3.8+)
python --version

# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Clear Streamlit cache
streamlit cache clear
```

---

## Data Validation Details

The application performs several validation checks:

### 1. Column Validation
- Checks for required columns
- Provides list of missing columns
- Shows available columns in your file

### 2. Data Type Validation
- Converts "Copies" to numeric
- Handles currency formatting in "Charged amount"
- Standardizes "Charged" status (Yes/No/Unknown)

### 3. Data Cleaning
- Removes sensitive columns
- Handles missing values
- Standardizes formats

---

## File Structure

```
DMC_Visualization/
│
├── app.py                  # Main Streamlit application
├── data_cleaner.py         # Standalone data cleaning script
├── requirements.txt        # Python dependencies
├── README.md              # This documentation file
│
├── single.ipynb           # Original analysis notebook (reference)
│
├── orders.csv             # Sample data file (if included)
└── orders_cleaned.csv     # Sample cleaned data (if generated)
```

---

## Best Practices

### For Data Preparation

1. **Standardize Column Names:** Ensure consistent naming across files
2. **Clean Before Upload:** Remove obviously invalid rows
3. **Backup Original Data:** Keep copies of raw data
4. **Document Changes:** Note any manual data modifications

### For Analysis

1. **Start with Single Year:** Understand one period before comparing
2. **Check Data Quality:** Review preview before trusting visualizations
3. **Download Cleaned Data:** Save processed data for records
4. **Regular Updates:** Upload new data regularly for trend analysis

### For Deployment

1. **Test Locally First:** Ensure everything works before deploying
2. **Use Version Control:** Track changes with Git
3. **Monitor Performance:** Watch for slow queries with large datasets
4. **Document Custom Changes:** Note any modifications to the code

---

## Support

### Getting Help

- **Technical Issues:** Check the [Troubleshooting](#troubleshooting) section
- **Feature Requests:** Submit an issue on GitHub
- **Data Questions:** Review [Data Requirements](#data-requirements)

### Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)

---

## Version History

### v1.0 (Current)
- Initial release
- Single year analysis with full visualizations
- Multi-year data merging
- Automatic data cleaning
- CSV export functionality

### Planned Updates
- v1.1: Multi-year comparison visualizations
- v1.2: Trend analysis and forecasting
- v1.3: Advanced filtering and custom reports

---

## License

This project is created for DMC (Digital Media Center) internal use.

---

## Contributing

For internal improvements and suggestions:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request with detailed description

---

## Acknowledgments

- Built with [Streamlit](https://streamlit.io)
- Data processing powered by [Pandas](https://pandas.pydata.org)
- Visualizations created with [Matplotlib](https://matplotlib.org) and [Seaborn](https://seaborn.pydata.org)

---

## Quick Start Checklist

- [ ] Python 3.8+ installed
- [ ] Repository cloned/downloaded
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] CSV data file prepared with required columns
- [ ] Application started (`streamlit run app.py`)
- [ ] Browser opened to `http://localhost:8501`
- [ ] CSV file uploaded successfully
- [ ] Visualizations displayed correctly
- [ ] Cleaned data downloaded (optional)

---

**Last Updated:** December 2025

**Maintained By:** DMC Analytics Team

For questions or support, please contact your system administrator or create an issue in the repository.
