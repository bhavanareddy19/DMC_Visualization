"""
DMC Order Analytics - Poster Generator
Creates a comprehensive 3D-style poster with all visualizations
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle
import seaborn as sns
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


def clean_currency(series):
    """Convert currency strings to numeric values"""
    if series.dtype == "O":
        series = (
            series.astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.strip()
        )
    return pd.to_numeric(series, errors="coerce")


def add_3d_shadow(ax, alpha=0.3):
    """Add 3D shadow effect to plot"""
    ax.patch.set_edgecolor('black')
    ax.patch.set_linewidth(2)
    ax.patch.set_alpha(0.1)

    # Add shadow
    shadow = Rectangle((0.02, -0.02), 0.98, 0.98,
                       transform=ax.transAxes,
                       color='gray', alpha=alpha, zorder=-1)
    ax.add_patch(shadow)


def add_gradient_background(ax, color1='#ffffff', color2='#f0f0f0'):
    """Add gradient background to axis"""
    gradient = np.linspace(0, 1, 256).reshape(256, 1)
    extent = [ax.get_xlim()[0], ax.get_xlim()[1],
              ax.get_ylim()[0], ax.get_ylim()[1]]
    ax.imshow(gradient, extent=extent, aspect='auto',
              cmap=plt.cm.colors.ListedColormap([color1, color2]),
              alpha=0.3, zorder=-10)


def create_title_section(fig, title, subtitle, gs_row):
    """Create a fancy title section with 3D effect"""
    ax = fig.add_subplot(gs_row)
    ax.axis('off')

    # Main title with border
    ax.text(0.5, 0.7, title,
            fontsize=48, fontweight='bold',
            ha='center', va='center',
            color='#1f77b4',
            transform=ax.transAxes,
            bbox=dict(boxstyle='round,pad=1', facecolor='white',
                     edgecolor='#1f77b4', linewidth=3, alpha=0.9))

    # Subtitle
    ax.text(0.5, 0.3, subtitle,
            fontsize=20, ha='center', va='center',
            color='#555', style='italic',
            transform=ax.transAxes)

    # Date
    ax.text(0.5, 0.1, f"Generated: {datetime.now().strftime('%B %d, %Y')}",
            fontsize=12, ha='center', va='center',
            color='#888',
            transform=ax.transAxes)


def create_kpi_section(fig, df, gs_row):
    """Create KPI cards with 3D effect"""
    ax = fig.add_subplot(gs_row)
    ax.axis('off')

    # Calculate KPIs
    total_orders = len(df)
    total_revenue = df["Charged amount"].sum() if "Charged amount" in df.columns else 0
    total_copies = df["Copies"].sum() if "Copies" in df.columns else 0
    charged_pct = (df["Charged"] == "Yes").sum() / len(df) * 100 if "Charged" in df.columns else 0

    kpis = [
        ("📦 Total Orders", f"{total_orders:,}", "#3498db"),
        ("💰 Total Revenue", f"${total_revenue:,.2f}", "#2ecc71"),
        ("📄 Total Copies", f"{int(total_copies):,}", "#e74c3c"),
        ("✅ Charged Rate", f"{charged_pct:.1f}%", "#f39c12")
    ]

    card_width = 0.22
    card_height = 0.6
    start_x = 0.05

    for i, (label, value, color) in enumerate(kpis):
        x = start_x + i * 0.24

        # Shadow
        shadow = FancyBboxPatch((x + 0.01, 0.15), card_width, card_height,
                               boxstyle="round,pad=0.02",
                               transform=ax.transAxes,
                               facecolor='gray', alpha=0.3, zorder=1)
        ax.add_patch(shadow)

        # Card
        card = FancyBboxPatch((x, 0.17), card_width, card_height,
                             boxstyle="round,pad=0.02",
                             transform=ax.transAxes,
                             facecolor=color, edgecolor='white',
                             linewidth=2, alpha=0.9, zorder=2)
        ax.add_patch(card)

        # Label
        ax.text(x + card_width/2, 0.65, label,
               fontsize=11, ha='center', va='center',
               color='white', fontweight='bold',
               transform=ax.transAxes, zorder=3)

        # Value
        ax.text(x + card_width/2, 0.35, value,
               fontsize=18, ha='center', va='center',
               color='white', fontweight='bold',
               transform=ax.transAxes, zorder=3)


def create_product_table(ax, df):
    """Create product summary table"""
    product_summary = (
        df.groupby("Product name", dropna=False)
          .agg(**{
              "Revenue": ("Charged amount", "sum"),
              "Copies": ("Copies", "sum"),
              "Orders": ("Product name", "count")
          })
          .sort_values("Revenue", ascending=False)
          .head(10)
    )

    ax.axis('off')

    # Create table
    table_data = []
    table_data.append(['Product Name', 'Revenue ($)', 'Copies', 'Orders'])

    for idx, row in product_summary.iterrows():
        table_data.append([
            idx[:30] + '...' if len(str(idx)) > 30 else idx,
            f'${row["Revenue"]:,.2f}',
            f'{int(row["Copies"]):,}',
            f'{int(row["Orders"]):,}'
        ])

    table = ax.table(cellText=table_data, cellLoc='left',
                    bbox=[0.05, 0.1, 0.9, 0.8],
                    colWidths=[0.5, 0.2, 0.15, 0.15])

    table.auto_set_font_size(False)
    table.set_fontsize(9)

    # Style header
    for i in range(4):
        cell = table[(0, i)]
        cell.set_facecolor('#1f77b4')
        cell.set_text_props(weight='bold', color='white', size=10)
        cell.set_height(0.08)

    # Style rows
    for i in range(1, len(table_data)):
        for j in range(4):
            cell = table[(i, j)]
            if i % 2 == 0:
                cell.set_facecolor('#f0f0f0')
            else:
                cell.set_facecolor('white')
            cell.set_edgecolor('#cccccc')

    ax.text(0.5, 0.95, '📋 Top 10 Products by Revenue',
           fontsize=14, fontweight='bold', ha='center',
           transform=ax.transAxes)


def create_charging_analysis(ax1, ax2, df):
    """Create charging status visualizations"""
    count_charged = df["Charged"].value_counts().reindex(["Yes", "No", "Unknown"], fill_value=0)

    # Bar chart
    colors = ['#2ecc71', '#e74c3c', '#95a5a6']
    bars = ax1.bar(count_charged.index, count_charged.values, color=colors,
                   edgecolor='white', linewidth=2, alpha=0.8)

    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}\n({height/count_charged.sum()*100:.1f}%)',
                ha='center', va='bottom', fontweight='bold', fontsize=10)

    ax1.set_title('💰 Orders by Charging Status', fontsize=14, fontweight='bold', pad=20)
    ax1.set_xlabel('Charging Status', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Number of Orders', fontsize=11, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    ax1.set_axisbelow(True)
    add_3d_shadow(ax1)

    # Pie chart
    wedges, texts, autotexts = ax2.pie(count_charged.values, labels=count_charged.index,
                                        autopct='%1.1f%%', colors=colors,
                                        startangle=90, explode=(0.05, 0.05, 0.05),
                                        shadow=True, textprops={'fontsize': 10, 'fontweight': 'bold'})

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(11)
        autotext.set_fontweight('bold')

    ax2.set_title('📊 Charging Distribution', fontsize=14, fontweight='bold', pad=20)


def create_copies_chart(ax, df):
    """Create copies by product chart"""
    copies_by_product = df.groupby("Product name")["Copies"].sum().sort_values(ascending=True).tail(15)

    # Create gradient colors
    colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(copies_by_product)))

    bars = ax.barh(range(len(copies_by_product)), copies_by_product.values,
                   color=colors, edgecolor='white', linewidth=1.5, alpha=0.9)

    ax.set_yticks(range(len(copies_by_product)))
    ax.set_yticklabels([label[:35] + '...' if len(label) > 35 else label
                        for label in copies_by_product.index], fontsize=9)

    # Add value labels
    for i, (bar, value) in enumerate(zip(bars, copies_by_product.values)):
        ax.text(value, bar.get_y() + bar.get_height()/2.,
               f' {int(value):,}',
               va='center', fontweight='bold', fontsize=9)

    ax.set_title('📄 Top 15 Products by Copy Volume', fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Total Copies', fontsize=11, fontweight='bold')
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    add_3d_shadow(ax)


def create_revenue_chart(ax, df):
    """Create revenue by product chart"""
    if df["Charged amount"].notna().sum() == 0:
        ax.text(0.5, 0.5, 'No Revenue Data Available',
               ha='center', va='center', fontsize=16, transform=ax.transAxes)
        ax.axis('off')
        return

    amt_by_product = df.groupby("Product name")["Charged amount"].sum().sort_values(ascending=True).tail(15)

    # Create gradient colors
    colors = plt.cm.Greens(np.linspace(0.4, 0.9, len(amt_by_product)))

    bars = ax.barh(range(len(amt_by_product)), amt_by_product.values,
                   color=colors, edgecolor='white', linewidth=1.5, alpha=0.9)

    ax.set_yticks(range(len(amt_by_product)))
    ax.set_yticklabels([label[:35] + '...' if len(label) > 35 else label
                        for label in amt_by_product.index], fontsize=9)

    # Add value labels
    for i, (bar, value) in enumerate(zip(bars, amt_by_product.values)):
        ax.text(value, bar.get_y() + bar.get_height()/2.,
               f' ${value:,.2f}',
               va='center', fontweight='bold', fontsize=9)

    ax.set_title('💵 Top 15 Products by Revenue', fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Revenue ($)', fontsize=11, fontweight='bold')
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    add_3d_shadow(ax)


def create_status_chart(ax, df):
    """Create order status distribution chart"""
    if "Order status" not in df.columns:
        ax.text(0.5, 0.5, 'No Order Status Data Available',
               ha='center', va='center', fontsize=16, transform=ax.transAxes)
        ax.axis('off')
        return

    status_counts = df["Order status"].value_counts().head(12)

    # Create gradient colors
    colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(status_counts)))

    bars = ax.barh(range(len(status_counts)), status_counts.values,
                   color=colors, edgecolor='white', linewidth=1.5, alpha=0.9)

    ax.set_yticks(range(len(status_counts)))
    ax.set_yticklabels([label[:40] + '...' if len(label) > 40 else label
                        for label in status_counts.index], fontsize=9)

    # Add value labels
    for i, (bar, value) in enumerate(zip(bars, status_counts.values)):
        pct = value / len(df) * 100
        ax.text(value, bar.get_y() + bar.get_height()/2.,
               f' {int(value):,} ({pct:.1f}%)',
               va='center', fontweight='bold', fontsize=9)

    ax.set_title('📊 Top 12 Order Statuses', fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Number of Orders', fontsize=11, fontweight='bold')
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    add_3d_shadow(ax)


def create_timeline_chart(ax, df):
    """Create timeline if date column exists"""
    if "Date submitted" not in df.columns:
        ax.text(0.5, 0.5, 'No Date Information Available',
               ha='center', va='center', fontsize=16, transform=ax.transAxes)
        ax.axis('off')
        return

    try:
        df_temp = df.copy()
        df_temp["Date submitted"] = pd.to_datetime(df_temp["Date submitted"], errors='coerce')
        df_temp = df_temp.dropna(subset=["Date submitted"])

        if len(df_temp) == 0:
            raise ValueError("No valid dates")

        timeline = df_temp.groupby(df_temp["Date submitted"].dt.date).size()

        ax.plot(timeline.index, timeline.values, linewidth=3, color='#1f77b4',
               marker='o', markersize=6, markerfacecolor='#ff7f0e',
               markeredgecolor='white', markeredgewidth=2, alpha=0.8)
        ax.fill_between(timeline.index, timeline.values, alpha=0.3, color='#1f77b4')

        ax.set_title('📅 Order Timeline', fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Date', fontsize=11, fontweight='bold')
        ax.set_ylabel('Number of Orders', fontsize=11, fontweight='bold')
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        add_3d_shadow(ax)

    except:
        ax.text(0.5, 0.5, 'Unable to parse date information',
               ha='center', va='center', fontsize=14, transform=ax.transAxes)
        ax.axis('off')


def generate_poster(csv_file, output_file='DMC_Analytics_Poster.png'):
    """Generate complete analytics poster"""

    print(f"[INFO] Reading data from {csv_file}...")

    # Read and clean data
    try:
        df = pd.read_csv(csv_file, encoding='utf-8')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(csv_file, encoding='latin-1')
        except:
            df = pd.read_csv(csv_file, encoding='cp1252')

    print(f"[SUCCESS] Loaded {len(df):,} rows")

    # Clean data
    if "Copies" in df.columns:
        df["Copies"] = pd.to_numeric(df["Copies"], errors="coerce").fillna(0)

    if "Charged" in df.columns:
        df["Charged"] = df["Charged"].astype(str).str.strip().str.title()
        df.loc[~df["Charged"].isin(["Yes", "No"]), "Charged"] = "Unknown"

    if "Charged amount" in df.columns:
        df["Charged amount"] = clean_currency(df["Charged amount"])

    print("[INFO] Creating poster...")

    # Create figure - A3 size poster (11.7 x 16.5 inches)
    fig = plt.figure(figsize=(11.7, 24), facecolor='white')

    # Use GridSpec for layout
    import matplotlib.gridspec as gridspec
    gs = gridspec.GridSpec(12, 2, figure=fig,
                          height_ratios=[1.2, 1, 2, 2, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 0.5],
                          hspace=0.4, wspace=0.3,
                          left=0.08, right=0.95, top=0.97, bottom=0.03)

    # Title Section
    create_title_section(fig, 'DMC Order Analytics',
                        'Comprehensive Data Visualization Report', gs[0, :])

    # KPI Section
    create_kpi_section(fig, df, gs[1, :])

    # Product Table
    ax_table = fig.add_subplot(gs[2, :])
    create_product_table(ax_table, df)

    # Charging Analysis (2 columns)
    ax_charge_bar = fig.add_subplot(gs[3, 0])
    ax_charge_pie = fig.add_subplot(gs[3, 1])
    create_charging_analysis(ax_charge_bar, ax_charge_pie, df)

    # Copies Chart
    ax_copies = fig.add_subplot(gs[4, :])
    create_copies_chart(ax_copies, df)

    # Revenue Chart
    ax_revenue = fig.add_subplot(gs[5, :])
    create_revenue_chart(ax_revenue, df)

    # Status Chart
    ax_status = fig.add_subplot(gs[6, :])
    create_status_chart(ax_status, df)

    # Timeline
    ax_timeline = fig.add_subplot(gs[7, :])
    create_timeline_chart(ax_timeline, df)

    # Additional analysis charts if space allows
    if "Paper size" in df.columns:
        ax_paper = fig.add_subplot(gs[8, :])
        paper_counts = df["Paper size"].value_counts().head(10)
        if len(paper_counts) > 0:
            colors = plt.cm.Set3(np.linspace(0, 1, len(paper_counts)))
            bars = ax_paper.bar(range(len(paper_counts)), paper_counts.values,
                               color=colors, edgecolor='white', linewidth=1.5, alpha=0.9)
            ax_paper.set_xticks(range(len(paper_counts)))
            ax_paper.set_xticklabels(paper_counts.index, rotation=45, ha='right')
            ax_paper.set_title('📏 Top 10 Paper Sizes', fontsize=14, fontweight='bold', pad=20)
            ax_paper.set_ylabel('Number of Orders', fontsize=11, fontweight='bold')
            ax_paper.grid(axis='y', alpha=0.3, linestyle='--')
            ax_paper.set_axisbelow(True)
            add_3d_shadow(ax_paper)

            for bar in bars:
                height = bar.get_height()
                ax_paper.text(bar.get_x() + bar.get_width()/2., height,
                            f'{int(height):,}',
                            ha='center', va='bottom', fontweight='bold', fontsize=9)

    if "Print color" in df.columns:
        ax_color = fig.add_subplot(gs[9, :])
        color_counts = df["Print color"].value_counts()
        if len(color_counts) > 0:
            colors_map = {'Color': '#e74c3c', 'Black and white': '#34495e',
                         'Grayscale': '#95a5a6'}
            colors = [colors_map.get(x, '#3498db') for x in color_counts.index]

            bars = ax_color.bar(range(len(color_counts)), color_counts.values,
                               color=colors, edgecolor='white', linewidth=1.5, alpha=0.9)
            ax_color.set_xticks(range(len(color_counts)))
            ax_color.set_xticklabels(color_counts.index, rotation=45, ha='right')
            ax_color.set_title('🎨 Print Color Distribution', fontsize=14, fontweight='bold', pad=20)
            ax_color.set_ylabel('Number of Orders', fontsize=11, fontweight='bold')
            ax_color.grid(axis='y', alpha=0.3, linestyle='--')
            ax_color.set_axisbelow(True)
            add_3d_shadow(ax_color)

            for bar in bars:
                height = bar.get_height()
                ax_color.text(bar.get_x() + bar.get_width()/2., height,
                            f'{int(height):,}',
                            ha='center', va='bottom', fontweight='bold', fontsize=9)

    # Footer
    ax_footer = fig.add_subplot(gs[11, :])
    ax_footer.axis('off')
    ax_footer.text(0.5, 0.5, '© DMC Order Analytics Dashboard | Generated with Python, Matplotlib & Seaborn',
                  ha='center', va='center', fontsize=10, color='#888',
                  transform=ax_footer.transAxes)

    # Save poster
    print(f"[INFO] Saving poster to {output_file}...")
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"[SUCCESS] Poster saved successfully!")
    print(f"[INFO] Image size: ~{11.7*300}x{24*300} pixels at 300 DPI")

    # Also save as PDF
    pdf_file = output_file.replace('.png', '.pdf')
    print(f"[INFO] Saving PDF version to {pdf_file}...")
    plt.savefig(pdf_file, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"[SUCCESS] PDF saved successfully!")

    plt.close()

    return output_file, pdf_file


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python generate_poster.py <csv_file> [output_file]")
        print("\nExample:")
        print("  python generate_poster.py orders.csv")
        print("  python generate_poster.py orders.csv my_poster.png")
        sys.exit(1)

    csv_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'DMC_Analytics_Poster.png'

    png_file, pdf_file = generate_poster(csv_file, output_file)

    print("\n" + "="*60)
    print("POSTER GENERATION COMPLETE!")
    print("="*60)
    print(f"\nFiles created:")
    print(f"  - PNG: {png_file}")
    print(f"  - PDF: {pdf_file}")
    print("\nYou can now:")
    print("  - Open the PNG in any image viewer")
    print("  - Print the PDF for a physical poster")
    print("  - Share with stakeholders")
    print("\n")
