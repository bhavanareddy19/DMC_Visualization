# DMC Analytics Poster Generator Guide

## Overview

The Poster Generator creates a comprehensive, print-ready visualization document with all your analytics in a beautiful 3D-styled layout. Perfect for presentations, reports, and stakeholder meetings!

## Features

### 📊 What's Included

1. **Title Section** - Professional header with your report title
2. **KPI Cards** - 4 colorful metric cards with 3D shadow effects
3. **Product Summary Table** - Top 10 products with revenue, copies, and order count
4. **Charging Analysis** - Bar chart + Pie chart showing charge distribution
5. **Copy Volume Chart** - Top 15 products by copies (with gradient colors)
6. **Revenue Chart** - Top 15 products by revenue (green gradient)
7. **Order Status** - Top 12 order statuses distribution
8. **Timeline** - Orders over time (if date column available)
9. **Paper Sizes** - Top 10 paper sizes used
10. **Print Colors** - Color vs Black & White distribution

### 🎨 Design Features

- **3D Shadow Effects** - All charts have subtle shadow for depth
- **Gradient Colors** - Beautiful color gradients (Blues, Greens, Viridis)
- **Professional Layout** - A3 poster size (11.7" x 24")
- **High Resolution** - 300 DPI for crisp printing
- **Dual Format** - Both PNG and PDF output

## How to Use

### Basic Usage

```bash
python generate_poster.py orders.csv
```

This creates:
- `DMC_Analytics_Poster.png` (3510 x 7200 pixels)
- `DMC_Analytics_Poster.pdf` (Vector format, perfect for printing)

### Custom Output Name

```bash
python generate_poster.py orders.csv MyReport.png
```

This creates:
- `MyReport.png`
- `MyReport.pdf`

### From Python Code

```python
from generate_poster import generate_poster

png_file, pdf_file = generate_poster('orders.csv', 'output.png')
print(f"Created: {png_file} and {pdf_file}")
```

## Poster Specifications

### Size & Resolution

- **Dimensions**: 11.7" x 24" (A3 width, extended length)
- **Resolution**: 300 DPI (print quality)
- **Pixel Size**: ~3510 x 7200 pixels
- **File Formats**: PNG (raster) + PDF (vector)

### Layout Structure

```
┌─────────────────────────────────────┐
│  TITLE SECTION (with date)          │
├─────────────────────────────────────┤
│  KPI CARDS (4 metrics)              │
├─────────────────────────────────────┤
│  PRODUCT SUMMARY TABLE              │
├───────────────────┬─────────────────┤
│ CHARGING BAR      │ CHARGING PIE    │
├───────────────────┴─────────────────┤
│  COPY VOLUME CHART (Top 15)         │
├─────────────────────────────────────┤
│  REVENUE CHART (Top 15)             │
├─────────────────────────────────────┤
│  ORDER STATUS (Top 12)              │
├─────────────────────────────────────┤
│  TIMELINE (if available)            │
├─────────────────────────────────────┤
│  PAPER SIZES (if available)         │
├─────────────────────────────────────┤
│  PRINT COLORS (if available)        │
├─────────────────────────────────────┤
│  FOOTER (copyright/credits)         │
└─────────────────────────────────────┘
```

## Chart Descriptions

### 1. KPI Cards (Top Section)
- **Total Orders**: Count of all orders
- **Total Revenue**: Sum of charged amounts
- **Total Copies**: Sum of all copies
- **Charged Rate**: Percentage of charged orders

**Colors**: Blue, Green, Red, Orange (3D shadow effect)

### 2. Product Summary Table
- Columns: Product Name, Revenue, Copies, Orders
- Shows top 10 products by revenue
- Alternating row colors for readability

### 3. Charging Analysis
- **Left**: Bar chart with percentages
- **Right**: Donut pie chart
- **Colors**: Green (Yes), Red (No), Gray (Unknown)

### 4. Copy Volume Chart
- Horizontal bar chart
- Top 15 products
- **Color**: Blue gradient (darker = more copies)

### 5. Revenue Chart
- Horizontal bar chart
- Top 15 products
- **Color**: Green gradient (darker = higher revenue)

### 6. Order Status
- Horizontal bar chart
- Top 12 statuses
- **Color**: Viridis gradient (purple to yellow)

### 7. Timeline (Optional)
- Line chart with area fill
- Orders per day
- **Color**: Blue line with orange markers

### 8. Paper Sizes (Optional)
- Bar chart showing top 10 sizes
- **Color**: Colorful Set3 palette

### 9. Print Colors (Optional)
- Bar chart
- **Colors**: Red (Color), Dark (B&W), Gray (Grayscale)

## Printing Guide

### For Home/Office Printers

1. **Open the PDF** in Adobe Reader or similar
2. **Print Settings:**
   - Paper Size: A3 or 11x17"
   - Scale: "Fit to printable area"
   - Quality: Best/Highest

### For Professional Printing

1. **Use the PDF file** (vector format scales perfectly)
2. **Recommended Services:**
   - FedEx Office / Kinkos
   - Local print shops
   - Online: VistaPrint, PrintPlace

3. **Specifications to Request:**
   - Size: 11.7" x 24" (or A3 extended)
   - Paper: Glossy photo paper or matte poster paper
   - Resolution: 300 DPI (already included)

### For Digital Display

1. **Use the PNG file** for:
   - Email attachments
   - Website display
   - Digital presentations
   - Slack/Teams sharing

2. **Recommended viewers:**
   - Windows: Photos app, IrfanView
   - Mac: Preview
   - Cross-platform: GIMP, Photoshop

## Customization Tips

### Modify Colors

Edit the color schemes in `generate_poster.py`:

```python
# Line ~190 for charging colors
colors = ['#2ecc71', '#e74c3c', '#95a5a6']  # Green, Red, Gray

# Line ~223 for copies chart
colors = plt.cm.Blues(...)  # Change to .Greens, .Reds, etc.

# Line ~251 for revenue chart
colors = plt.cm.Greens(...)  # Change color scheme
```

### Adjust Chart Sizes

Modify the GridSpec ratios in `generate_poster.py` around line 395:

```python
gs = gridspec.GridSpec(12, 2,
    height_ratios=[1.2, 1, 2, 2, 2.5, 2.5, ...],
    # Larger number = taller section
    ...
)
```

### Change Poster Size

Modify line 391:

```python
fig = plt.figure(figsize=(11.7, 24))  # (width, height) in inches
# For A4: (8.27, 11.69)
# For Letter: (8.5, 11)
# For Tabloid: (11, 17)
```

## Troubleshooting

### Issue: "Missing column" errors

**Solution**: Some charts are optional and will show "N/A" if columns missing. Required columns:
- Product name
- Copies
- Charged
- Charged amount (for revenue)

### Issue: Charts look squished

**Solution**: Increase poster height in line 391:
```python
fig = plt.figure(figsize=(11.7, 30))  # Taller
```

### Issue: Text too small

**Solution**: Increase font sizes in individual chart functions (search for `fontsize=` in the code)

### Issue: PDF is huge file size

**Solution**: Use PNG for digital sharing. PDF contains vector data which is larger but scales better.

### Issue: Colors print wrong

**Solution**:
- Use PDF for printing (better color accuracy)
- Check printer color calibration
- Try "Print in Color" vs "High Quality Color"

## Best Practices

### 1. **Data Preparation**
- Clean your CSV before generating
- Ensure all required columns are present
- Remove or fix invalid data

### 2. **File Management**
- Name your output files clearly (e.g., `Q4_2024_Report.png`)
- Keep both PNG and PDF versions
- Archive posters by date/quarter

### 3. **Sharing**
- **Email**: Use PNG (smaller file size)
- **Print**: Use PDF (vector quality)
- **Presentations**: Use PNG in PowerPoint/Google Slides
- **Web**: Resize PNG for faster loading

### 4. **Regular Updates**
- Generate posters weekly/monthly
- Compare side-by-side for trends
- Share with stakeholders regularly

## Integration with Streamlit App

The poster generator works independently but complements the Streamlit app:

1. **App**: Interactive exploration
2. **Poster**: Static snapshot for sharing

### Workflow:

```
1. Upload data to Streamlit app
2. Explore interactively
3. Download cleaned CSV
4. Generate poster from cleaned CSV
5. Share poster with stakeholders
```

## Examples

### Example 1: Monthly Report

```bash
python generate_poster.py orders_november.csv November_2024_Report.png
```

### Example 2: Quarterly Analysis

```bash
python generate_poster.py Q4_2024_orders.csv Q4_2024_Analytics.png
```

### Example 3: Year-End Summary

```bash
python generate_poster.py orders_2024_full.csv Year_End_2024.png
```

## Advanced: Batch Processing

Create posters for multiple files:

```bash
# Windows
for %f in (*.csv) do python generate_poster.py %f %~nf_poster.png

# Mac/Linux
for file in *.csv; do python generate_poster.py "$file" "${file%.csv}_poster.png"; done
```

## Support

### Common Questions

**Q: Can I change the title?**
A: Yes! Edit line 401 in `generate_poster.py`:
```python
create_title_section(fig, 'YOUR TITLE HERE', 'Your subtitle', ...)
```

**Q: Can I add my logo?**
A: Yes! Add after line 391:
```python
from matplotlib import image
logo = image.imread('logo.png')
fig.figimage(logo, xo=50, yo=50, alpha=0.8)
```

**Q: Can I export to PowerPoint?**
A: Save as PNG, then insert into PowerPoint normally.

**Q: How do I automate this?**
A: Schedule a script that runs `generate_poster.py` with new data daily/weekly.

---

**Last Updated**: December 2025
**Version**: 1.0
**Maintained By**: DMC Analytics Team

For questions or issues, contact your system administrator or create an issue in the repository.
