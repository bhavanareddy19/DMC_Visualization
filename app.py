import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import re
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="DMC Order Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(120deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .category-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin: 2rem 0;
        padding: 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        border-bottom: 3px solid #667eea;
    }
    .filter-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 5px solid #1f77b4;
    }
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Helper functions
def extract_season_from_filename(filename):
    """Extract season information from filename"""
    name = filename.replace('.csv', '').replace('.CSV', '')
    match = re.search(r'(Fall|Spring|Summer|Winter)\s*(\d{4})', name, re.IGNORECASE)
    if match:
        return f"{match.group(1).capitalize()} {match.group(2)}"
    match = re.search(r'(\d{4})', name)
    if match:
        return match.group(1)
    return name

def validate_columns(df, required_columns):
    """Validate required columns"""
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        message = f"❌ **Validation Failed**: Missing columns:\n\n"
        for col in missing:
            message += f"- `{col}`\n"
        return False, missing, message
    return True, [], "✅ All required columns present!"

def clean_currency(series):
    """Convert currency strings to numeric"""
    if series.dtype == "O":
        series = series.astype(str).str.replace("$", "", regex=False).str.replace(",", "", regex=False).str.strip()
    return pd.to_numeric(series, errors="coerce")

def clean_data(df):
    """Clean and prepare dataframe"""
    columns_to_remove = [
        'room name', 'Room name', 'title', 'Title', 'customer', 'Customer name',
        'email', 'Email', 'last status update', 'Last status update',
        'Charged time', 'Charged account type', 'Charged account name',
        'Filename', 'Additional instructions',
        'Special Information (Operator Only) Operator name',
        'Print Information (DMC staff only) Operator name'
    ]

    columns_found = [col for col in columns_to_remove if col in df.columns]
    if columns_found:
        df = df.drop(columns=columns_found)

    if "Copies" in df.columns:
        df["Copies"] = pd.to_numeric(df["Copies"], errors="coerce").fillna(0)
    if "Charged" in df.columns:
        df["Charged"] = df["Charged"].astype(str).str.strip().str.title()
        df.loc[~df["Charged"].isin(["Yes", "No"]), "Charged"] = "Unknown"
    if "Charged amount" in df.columns:
        df["Charged amount"] = clean_currency(df["Charged amount"])
    if "Date submitted" in df.columns:
        df["Date submitted"] = pd.to_datetime(df["Date submitted"], errors='coerce')

    return df

def apply_filters(df, filters):
    """Apply interactive filters to dataframe"""
    filtered_df = df.copy()

    for col, values in filters.items():
        if col in filtered_df.columns and values:
            filtered_df = filtered_df[filtered_df[col].isin(values)]

    return filtered_df

def create_interactive_table(df, columns, title):
    """Create interactive sortable table"""
    if len(df) == 0:
        return None

    display_df = df[columns].copy()

    # Format numeric columns
    for col in display_df.columns:
        if display_df[col].dtype in ['float64', 'int64']:
            if 'amount' in col.lower() or 'revenue' in col.lower():
                display_df[col] = display_df[col].apply(lambda x: f'${x:,.2f}')
            else:
                display_df[col] = display_df[col].apply(lambda x: f'{int(x):,}')

    return display_df

# ==================== ENHANCED SINGLE YEAR VISUALIZATIONS ====================

def create_overall_visualizations(df):
    """Enhanced overall category visualizations with interactivity"""
    st.markdown('<p class="category-header">📊 OVERALL ANALYSIS</p>', unsafe_allow_html=True)

    # Interactive Filters
    with st.expander("🔍 Interactive Filters", expanded=False):
        col1, col2, col3 = st.columns(3)

        filters = {}
        with col1:
            if "Order status" in df.columns:
                status_options = df["Order status"].dropna().unique().tolist()
                selected_status = st.multiselect("Order Status", status_options, default=status_options, key="overall_status")
                if selected_status:
                    filters["Order status"] = selected_status

        with col2:
            if "Charged" in df.columns:
                charged_options = df["Charged"].unique().tolist()
                selected_charged = st.multiselect("Charged", charged_options, default=charged_options, key="overall_charged")
                if selected_charged:
                    filters["Charged"] = selected_charged

        with col3:
            if "Product name" in df.columns:
                product_options = df["Product name"].dropna().unique().tolist()
                selected_products = st.multiselect("Products", product_options, default=product_options, key="overall_products")
                if selected_products:
                    filters["Product name"] = selected_products

    # Apply filters
    df_filtered = apply_filters(df, filters)

    # Dynamic KPIs with animated delta
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📦 Total Orders", f"{len(df_filtered):,}",
                 delta=f"{len(df_filtered) - len(df)}" if len(df_filtered) != len(df) else None)
    with col2:
        if "Charged amount" in df_filtered.columns:
            total_revenue = df_filtered["Charged amount"].sum()
            original_revenue = df["Charged amount"].sum()
            st.metric("💰 Total Revenue", f"${total_revenue:,.2f}",
                     delta=f"${total_revenue - original_revenue:,.2f}" if total_revenue != original_revenue else None)
    with col3:
        if "Copies" in df_filtered.columns:
            total_copies = df_filtered["Copies"].sum()
            original_copies = df["Copies"].sum()
            st.metric("📄 Total Copies", f"{int(total_copies):,}",
                     delta=f"{int(total_copies - original_copies):,}" if total_copies != original_copies else None)
    with col4:
        if "Charged" in df_filtered.columns and len(df_filtered) > 0:
            charged_pct = (df_filtered["Charged"] == "Yes").sum() / len(df_filtered) * 100
            st.metric("✅ Charged Rate", f"{charged_pct:.1f}%")

    st.markdown("---")

    # Interactive Product Summary with drill-down
    if "Product name" in df_filtered.columns:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("#### 📋 Interactive Product Summary")

            product_summary = df_filtered.groupby("Product name").agg({
                "Charged amount": "sum",
                "Copies": "sum",
                "Product name": "count"
            }).rename(columns={"Product name": "Order Count"}).sort_values("Charged amount", ascending=False)

            # Interactive bar chart with click details
            fig = go.Figure()

            fig.add_trace(go.Bar(
                name='Revenue',
                x=product_summary.index,
                y=product_summary['Charged amount'],
                marker_color='#2ca02c',
                hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.2f}<br><extra></extra>',
                text=[f'${x:,.0f}' for x in product_summary['Charged amount']],
                textposition='outside'
            ))

            fig.update_layout(
                title="Revenue by Product (Click to see details)",
                xaxis_title="Product",
                yaxis_title="Revenue ($)",
                height=400,
                hovermode='x unified',
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_tickangle=-45
            )

            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### 📊 Top Products")
            st.dataframe(
                product_summary.style.format({
                    "Charged amount": "${:,.2f}",
                    "Copies": "{:,.0f}",
                    "Order Count": "{:,.0f}"
                }),
                height=400
            )

    # Interactive Sunburst Chart
    if "Product name" in df_filtered.columns and "Order status" in df_filtered.columns:
        st.markdown("#### 🌟 Order Distribution (Interactive Sunburst)")

        # Create hierarchical data
        sunburst_data = df_filtered.groupby(["Product name", "Order status"]).size().reset_index(name='Count')

        fig = px.sunburst(
            sunburst_data,
            path=['Product name', 'Order status'],
            values='Count',
            color='Count',
            color_continuous_scale='Blues',
            title="Click to drill down: Product → Status"
        )

        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

    # Charging Analysis with Animation
    if "Charged" in df_filtered.columns:
        st.markdown("#### 💰 Interactive Charging Analysis")

        col1, col2 = st.columns(2)

        count_charged = df_filtered["Charged"].value_counts()

        with col1:
            # Animated bar chart
            fig = go.Figure(data=[
                go.Bar(
                    x=count_charged.index,
                    y=count_charged.values,
                    marker_color=['#2ca02c' if x == 'Yes' else '#d62728' if x == 'No' else '#ff7f0e'
                                 for x in count_charged.index],
                    text=[f'{x:,}<br>({x/count_charged.sum()*100:.1f}%)' for x in count_charged.values],
                    textposition='outside',
                    hovertemplate='<b>%{x}</b><br>Count: %{y:,}<br><extra></extra>'
                )
            ])

            fig.update_layout(
                title="Charging Status Distribution",
                xaxis_title="Status",
                yaxis_title="Count",
                height=400,
                showlegend=False
            )

            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Interactive donut with custom hover
            fig = go.Figure(data=[go.Pie(
                labels=count_charged.index,
                values=count_charged.values,
                hole=0.5,
                marker_colors=['#2ca02c', '#d62728', '#ff7f0e'],
                textinfo='label+percent',
                hovertemplate='<b>%{label}</b><br>Count: %{value:,}<br>Percentage: %{percent}<extra></extra>',
                pull=[0.1 if x == count_charged.max() else 0 for x in count_charged.values]
            )])

            fig.update_layout(
                title="Charging Distribution",
                height=400,
                annotations=[dict(text=f'{count_charged.sum():,}<br>Total', x=0.5, y=0.5,
                                font_size=20, showarrow=False)]
            )

            st.plotly_chart(fig, use_container_width=True)

    # Timeline Analysis (if date available)
    if "Date submitted" in df_filtered.columns:
        st.markdown("#### 📅 Interactive Timeline")

        df_timeline = df_filtered[df_filtered["Date submitted"].notna()].copy()

        if len(df_timeline) > 0:
            timeline_data = df_timeline.groupby(df_timeline["Date submitted"].dt.date).agg({
                "Copies": "sum",
                "Charged amount": "sum"
            }).reset_index()

            # Create subplot with shared x-axis
            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                subplot_titles=("Orders Over Time", "Revenue Over Time"),
                vertical_spacing=0.1
            )

            fig.add_trace(
                go.Scatter(
                    x=timeline_data["Date submitted"],
                    y=timeline_data["Copies"],
                    mode='lines+markers',
                    name='Copies',
                    fill='tozeroy',
                    line=dict(color='#1f77b4', width=3),
                    marker=dict(size=8),
                    hovertemplate='<b>%{x}</b><br>Copies: %{y:,}<extra></extra>'
                ),
                row=1, col=1
            )

            fig.add_trace(
                go.Scatter(
                    x=timeline_data["Date submitted"],
                    y=timeline_data["Charged amount"],
                    mode='lines+markers',
                    name='Revenue',
                    fill='tozeroy',
                    line=dict(color='#2ca02c', width=3),
                    marker=dict(size=8),
                    hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.2f}<extra></extra>'
                ),
                row=2, col=1
            )

            fig.update_layout(
                height=600,
                hovermode='x unified',
                showlegend=True
            )

            fig.update_xaxes(title_text="Date", row=2, col=1)
            fig.update_yaxes(title_text="Copies", row=1, col=1)
            fig.update_yaxes(title_text="Revenue ($)", row=2, col=1)

            st.plotly_chart(fig, use_container_width=True)

def create_3d_print_visualizations(df):
    """Enhanced 3D Print visualizations"""
    st.markdown('<p class="category-header">🖨️ 3D PRINT ANALYSIS</p>', unsafe_allow_html=True)

    df3d = df[df["Product name"].str.strip() == "3D Print"].copy()

    if len(df3d) == 0:
        st.warning("No 3D Print data found")
        return

    # Interactive Filters
    with st.expander("🔍 3D Print Filters", expanded=False):
        col1, col2, col3 = st.columns(3)

        filters = {}
        with col1:
            if "Material name" in df3d.columns:
                materials = df3d["Material name"].dropna().unique().tolist()
                selected_materials = st.multiselect("Materials", materials, default=materials, key="3d_materials")
                if selected_materials:
                    filters["Material name"] = selected_materials

        with col2:
            if "Special Information (Operator Only) Machine" in df3d.columns:
                machines = df3d["Special Information (Operator Only) Machine"].dropna().unique().tolist()
                selected_machines = st.multiselect("Machines", machines, default=machines, key="3d_machines")
                if selected_machines:
                    filters["Special Information (Operator Only) Machine"] = selected_machines

        with col3:
            if "Special Information (Operator Only) Job difficulty" in df3d.columns:
                difficulties = df3d["Special Information (Operator Only) Job difficulty"].dropna().unique().tolist()
                selected_diff = st.multiselect("Job Difficulty", difficulties, default=difficulties, key="3d_diff")
                if selected_diff:
                    filters["Special Information (Operator Only) Job difficulty"] = selected_diff

    df3d_filtered = apply_filters(df3d, filters)

    # KPIs
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📦 3D Print Orders", f"{len(df3d_filtered):,}")
    with col2:
        st.metric("📄 Total Copies", f"{int(df3d_filtered['Copies'].sum()):,}")
    with col3:
        if "Charged amount" in df3d_filtered.columns:
            st.metric("💰 Revenue", f"${df3d_filtered['Charged amount'].sum():,.2f}")

    # Material Analysis with 3D effect
    if "Material name" in df3d_filtered.columns:
        st.markdown("#### 🧱 Material Usage Analysis")

        material_data = df3d_filtered.groupby("Material name").agg({
            "Copies": "sum",
            "Charged amount": "sum",
            "Material name": "count"
        }).rename(columns={"Material name": "Orders"}).sort_values("Copies", ascending=False)

        col1, col2 = st.columns([2, 1])

        with col1:
            # 3D bar chart
            fig = go.Figure(data=[
                go.Bar(
                    x=material_data.index,
                    y=material_data['Copies'],
                    marker=dict(
                        color=material_data['Copies'],
                        colorscale='Viridis',
                        showscale=True,
                        colorbar=dict(title="Copies")
                    ),
                    text=[f'{int(x):,}' for x in material_data['Copies']],
                    textposition='outside',
                    hovertemplate='<b>%{x}</b><br>Copies: %{y:,}<br>Revenue: $%{customdata:,.2f}<extra></extra>',
                    customdata=material_data['Charged amount']
                )
            ])

            fig.update_layout(
                title="Copies by Material (Hover for details)",
                xaxis_title="Material",
                yaxis_title="Copies",
                height=400,
                hovermode='x'
            )

            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("**Material Statistics**")
            st.dataframe(
                material_data.style.format({
                    "Copies": "{:,.0f}",
                    "Charged amount": "${:,.2f}",
                    "Orders": "{:,.0f}"
                }),
                height=400
            )

    # Job Difficulty - Funnel Chart
    if "Special Information (Operator Only) Job difficulty" in df3d_filtered.columns:
        st.markdown("#### ⚙️ Job Difficulty Analysis")

        job_col = "Special Information (Operator Only) Job difficulty"
        job_data = df3d_filtered[df3d_filtered[job_col].notna()].groupby(job_col)["Copies"].sum().sort_values(ascending=False)

        # Create funnel chart
        fig = go.Figure(go.Funnel(
            y=job_data.index,
            x=job_data.values,
            textinfo="value+percent initial",
            marker=dict(color=px.colors.sequential.Blues[::-1]),
            hovertemplate='<b>%{y}</b><br>Copies: %{x:,}<extra></extra>'
        ))

        fig.update_layout(
            title="Job Difficulty Distribution (Funnel View)",
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

    # Machine Usage - Treemap
    if "Special Information (Operator Only) Machine" in df3d_filtered.columns:
        st.markdown("#### 🤖 Machine Usage (Interactive Treemap)")

        machine_data = df3d_filtered[df3d_filtered["Special Information (Operator Only) Machine"].notna()].groupby(
            "Special Information (Operator Only) Machine"
        ).agg({
            "Copies": "sum",
            "Charged amount": "sum"
        }).reset_index()

        fig = px.treemap(
            machine_data,
            path=['Special Information (Operator Only) Machine'],
            values='Copies',
            color='Charged amount',
            color_continuous_scale='Reds',
            title="Click to see machine details",
            hover_data={'Copies': ':,', 'Charged amount': ':$,.2f'}
        )

        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

def create_document_visualizations(df):
    """Enhanced Document visualizations"""
    st.markdown('<p class="category-header">📄 DOCUMENT ANALYSIS</p>', unsafe_allow_html=True)

    df_doc = df[df["Product name"].str.strip() == "Document"].copy()

    if len(df_doc) == 0:
        st.warning("No Document data found")
        return

    # Interactive Filters
    with st.expander("🔍 Document Filters", expanded=False):
        col1, col2, col3 = st.columns(3)

        filters = {}
        with col1:
            if "Paper type" in df_doc.columns:
                paper_types = df_doc["Paper type"].dropna().unique().tolist()
                selected_types = st.multiselect("Paper Type", paper_types, default=paper_types, key="doc_paper_type")
                if selected_types:
                    filters["Paper type"] = selected_types

        with col2:
            if "Paper size" in df_doc.columns:
                sizes = df_doc["Paper size"].dropna().unique().tolist()
                selected_sizes = st.multiselect("Paper Size", sizes, default=sizes, key="doc_size")
                if selected_sizes:
                    filters["Paper size"] = selected_sizes

        with col3:
            if "Single or double sided" in df_doc.columns:
                sided = df_doc["Single or double sided"].dropna().unique().tolist()
                selected_sided = st.multiselect("Sides", sided, default=sided, key="doc_sided")
                if selected_sided:
                    filters["Single or double sided"] = selected_sided

    df_doc_filtered = apply_filters(df_doc, filters)

    # KPIs
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📦 Document Orders", f"{len(df_doc_filtered):,}")
    with col2:
        st.metric("📄 Total Copies", f"{int(df_doc_filtered['Copies'].sum()):,}")
    with col3:
        if "Charged amount" in df_doc_filtered.columns:
            st.metric("💰 Revenue", f"${df_doc_filtered['Charged amount'].sum():,.2f}")

    # Paper Analysis - Grouped Bar
    if "Paper type" in df_doc_filtered.columns and "Paper size" in df_doc_filtered.columns:
        st.markdown("#### 📋 Paper Type & Size Matrix")

        paper_matrix = df_doc_filtered.pivot_table(
            values="Copies",
            index="Paper type",
            columns="Paper size",
            aggfunc="sum",
            fill_value=0
        )

        fig = go.Figure()

        for col in paper_matrix.columns:
            fig.add_trace(go.Bar(
                name=str(col),
                x=paper_matrix.index,
                y=paper_matrix[col],
                text=[f'{int(x):,}' if x > 0 else '' for x in paper_matrix[col]],
                textposition='auto',
                hovertemplate='<b>%{x}</b><br>Size: ' + str(col) + '<br>Copies: %{y:,}<extra></extra>'
            ))

        fig.update_layout(
            barmode='group',
            title="Paper Type vs Size Distribution",
            xaxis_title="Paper Type",
            yaxis_title="Copies",
            height=450,
            hovermode='x unified',
            legend_title="Paper Size"
        )

        st.plotly_chart(fig, use_container_width=True)

    # Single/Double Sided - Animated Pie
    if "Single or double sided" in df_doc_filtered.columns:
        st.markdown("#### 🔄 Single vs Double Sided Analysis")

        col1, col2 = st.columns([1, 1])

        sided_data = df_doc_filtered.groupby("Single or double sided").agg({
            "Copies": "sum",
            "Charged amount": "sum"
        })

        with col1:
            fig = go.Figure(data=[go.Pie(
                labels=sided_data.index,
                values=sided_data['Copies'],
                hole=0.4,
                marker_colors=['#1f77b4', '#ff7f0e'],
                textinfo='label+percent+value',
                hovertemplate='<b>%{label}</b><br>Copies: %{value:,}<br>Percentage: %{percent}<extra></extra>',
                pull=[0.1, 0]
            )])

            fig.update_layout(
                title="Copies Distribution",
                height=400,
                annotations=[dict(text=f'{sided_data["Copies"].sum():,.0f}<br>Total',
                                x=0.5, y=0.5, font_size=16, showarrow=False)]
            )

            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = go.Figure(data=[go.Pie(
                labels=sided_data.index,
                values=sided_data['Charged amount'],
                hole=0.4,
                marker_colors=['#2ca02c', '#d62728'],
                textinfo='label+percent',
                hovertemplate='<b>%{label}</b><br>Revenue: $%{value:,.2f}<br>Percentage: %{percent}<extra></extra>',
                pull=[0.1, 0]
            )])

            fig.update_layout(
                title="Revenue Distribution",
                height=400,
                annotations=[dict(text=f'${sided_data["Charged amount"].sum():,.0f}<br>Total',
                                x=0.5, y=0.5, font_size=16, showarrow=False)]
            )

            st.plotly_chart(fig, use_container_width=True)

def create_poster_visualizations(df):
    """Enhanced Poster visualizations"""
    st.markdown('<p class="category-header">🖼️ LARGE FORMAT POSTER ANALYSIS</p>', unsafe_allow_html=True)

    df_poster = df[df["Product name"].str.strip() == "Large-Format Poster"].copy()

    if len(df_poster) == 0:
        st.warning("No Large-Format Poster data found")
        return

    # Interactive Filters
    with st.expander("🔍 Poster Filters", expanded=False):
        col1, col2 = st.columns(2)

        filters = {}
        with col1:
            if "Paper size" in df_poster.columns:
                sizes = df_poster["Paper size"].dropna().unique().tolist()
                selected_sizes = st.multiselect("Poster Size", sizes, default=sizes, key="poster_size")
                if selected_sizes:
                    filters["Paper size"] = selected_sizes

        with col2:
            if "Paper color" in df_poster.columns:
                colors = df_poster["Paper color"].dropna().unique().tolist()
                selected_colors = st.multiselect("Paper Color", colors, default=colors, key="poster_color")
                if selected_colors:
                    filters["Paper color"] = selected_colors

    df_poster_filtered = apply_filters(df_poster, filters)

    # KPIs
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📦 Poster Orders", f"{len(df_poster_filtered):,}")
    with col2:
        st.metric("📄 Total Copies", f"{int(df_poster_filtered['Copies'].sum()):,}")
    with col3:
        if "Charged amount" in df_poster_filtered.columns:
            st.metric("💰 Revenue", f"${df_poster_filtered['Charged amount'].sum():,.2f}")

    # Poster Size Analysis - Stacked Bar
    if "Paper size" in df_poster_filtered.columns and "Paper color" in df_poster_filtered.columns:
        st.markdown("#### 📏 Size & Color Matrix")

        size_color_data = df_poster_filtered.pivot_table(
            values="Copies",
            index="Paper size",
            columns="Paper color",
            aggfunc="sum",
            fill_value=0
        )

        fig = go.Figure()

        for col in size_color_data.columns:
            fig.add_trace(go.Bar(
                name=str(col),
                x=size_color_data.index,
                y=size_color_data[col],
                text=[f'{int(x):,}' if x > 0 else '' for x in size_color_data[col]],
                textposition='auto',
                hovertemplate='<b>%{x}</b><br>' + str(col) + '<br>Copies: %{y:,}<extra></extra>'
            ))

        fig.update_layout(
            barmode='stack',
            title="Poster Size vs Paper Color (Stacked)",
            xaxis_title="Poster Size",
            yaxis_title="Copies",
            height=450,
            xaxis_tickangle=-45,
            hovermode='x unified'
        )

        st.plotly_chart(fig, use_container_width=True)

    # Revenue heatmap
    if "Paper size" in df_poster_filtered.columns and "Charged amount" in df_poster_filtered.columns:
        st.markdown("#### 💰 Revenue Heatmap by Size")

        revenue_by_size = df_poster_filtered.groupby("Paper size")["Charged amount"].sum().sort_values(ascending=False)

        fig = go.Figure(data=go.Bar(
            y=revenue_by_size.index,
            x=revenue_by_size.values,
            orientation='h',
            marker=dict(
                color=revenue_by_size.values,
                colorscale='Greens',
                showscale=True,
                colorbar=dict(title="Revenue ($)")
            ),
            text=[f'${x:,.0f}' for x in revenue_by_size.values],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Revenue: $%{x:,.2f}<extra></extra>'
        ))

        fig.update_layout(
            title="Revenue by Poster Size (Interactive)",
            xaxis_title="Revenue ($)",
            yaxis_title="Poster Size",
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

# ==================== ENHANCED COMPARISON VISUALIZATIONS ====================

def create_overall_comparison(df):
    """Enhanced overall comparison with interactivity"""
    st.markdown('<p class="category-header">📊 OVERALL COMPARISON</p>', unsafe_allow_html=True)

    if "Season" not in df.columns:
        st.error("Season column not found")
        return

    # Interactive Season Selector
    with st.expander("🔍 Select Seasons to Compare", expanded=True):
        seasons = df["Season"].unique().tolist()
        selected_seasons = st.multiselect(
            "Choose Seasons",
            seasons,
            default=seasons,
            key="comp_seasons"
        )

    if not selected_seasons:
        st.warning("Please select at least one season")
        return

    df_filtered = df[df["Season"].isin(selected_seasons)]

    # Animated Revenue Comparison
    st.markdown("#### 💰 Revenue Comparison Across Seasons")

    revenue_by_season = df_filtered.groupby("Season")["Charged amount"].sum()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=revenue_by_season.index,
        y=revenue_by_season.values,
        marker=dict(
            color=revenue_by_season.values,
            colorscale='Blues',
            showscale=True,
            colorbar=dict(title="Revenue ($)")
        ),
        text=[f'${x:,.0f}' for x in revenue_by_season.values],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.2f}<extra></extra>'
    ))

    fig.update_layout(
        xaxis_title="Season",
        yaxis_title="Revenue ($)",
        height=450,
        hovermode='x',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Product Comparison - Grouped & Stacked toggle
    if "Product name" in df_filtered.columns:
        st.markdown("#### 📊 Product Performance Across Seasons")

        col1, col2 = st.columns([1, 4])

        with col1:
            chart_type = st.radio("Chart Type", ["Grouped", "Stacked"], key="product_chart_type")

        with col2:
            pivot_data = df_filtered.pivot_table(
                values="Copies",
                index="Season",
                columns="Product name",
                aggfunc="sum",
                fill_value=0
            )

            fig = go.Figure()

            for product in pivot_data.columns:
                fig.add_trace(go.Bar(
                    name=product,
                    x=pivot_data.index,
                    y=pivot_data[product],
                    text=[f'{int(x):,}' if x > 0 else '' for x in pivot_data[product]],
                    textposition='auto',
                    hovertemplate=f'<b>{product}</b><br>Season: %{{x}}<br>Copies: %{{y:,}}<extra></extra>'
                ))

            fig.update_layout(
                barmode='group' if chart_type == "Grouped" else 'stack',
                xaxis_title="Season",
                yaxis_title="Copies",
                height=450,
                hovermode='x unified',
                legend_title="Product"
            )

            st.plotly_chart(fig, use_container_width=True)

    # Season Distribution - Enhanced Pie
    st.markdown("#### 📈 Copies Distribution by Season")

    copies_by_season = df_filtered.groupby("Season")["Copies"].sum()

    fig = go.Figure(data=[go.Pie(
        labels=copies_by_season.index,
        values=copies_by_season.values,
        hole=0.4,
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>Copies: %{value:,}<br>Percentage: %{percent}<extra></extra>',
        marker=dict(
            colors=px.colors.qualitative.Set3,
            line=dict(color='white', width=2)
        ),
        pull=[0.1 if x == copies_by_season.max() else 0 for x in copies_by_season.values]
    )])

    fig.update_layout(
        height=500,
        annotations=[dict(
            text=f'{copies_by_season.sum():,.0f}<br>Total<br>Copies',
            x=0.5, y=0.5, font_size=18, showarrow=False
        )]
    )

    st.plotly_chart(fig, use_container_width=True)

def create_3d_print_comparison(df):
    """Enhanced 3D Print comparison"""
    st.markdown('<p class="category-header">🖨️ 3D PRINT COMPARISON</p>', unsafe_allow_html=True)

    df3d = df[df["Product name"].str.strip() == "3D Print"].copy()

    if len(df3d) == 0:
        st.warning("No 3D Print data found")
        return

    # Dual axis chart - Copies and Revenue
    st.markdown("#### 📊 Copies & Revenue Trend")

    season_data = df3d.groupby("Season").agg({
        "Copies": "sum",
        "Charged amount": "sum"
    })

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            name="Copies",
            x=season_data.index,
            y=season_data["Copies"],
            marker_color='#9467bd',
            text=[f'{int(x):,}' for x in season_data["Copies"]],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Copies: %{y:,}<extra></extra>'
        ),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(
            name="Revenue",
            x=season_data.index,
            y=season_data["Charged amount"],
            mode='lines+markers',
            line=dict(color='#e377c2', width=3),
            marker=dict(size=10),
            hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.2f}<extra></extra>'
        ),
        secondary_y=True
    )

    fig.update_xaxes(title_text="Season")
    fig.update_yaxes(title_text="Copies", secondary_y=False)
    fig.update_yaxes(title_text="Revenue ($)", secondary_y=True)

    fig.update_layout(
        height=450,
        hovermode='x unified',
        title="Copies (Bars) vs Revenue (Line)"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Material comparison across seasons
    if "Material name" in df3d.columns:
        st.markdown("#### 🧱 Material Usage Evolution")

        material_pivot = df3d.pivot_table(
            values="Copies",
            index="Season",
            columns="Material name",
            aggfunc="sum",
            fill_value=0
        )

        fig = go.Figure()

        for material in material_pivot.columns:
            fig.add_trace(go.Scatter(
                name=str(material),
                x=material_pivot.index,
                y=material_pivot[material],
                mode='lines+markers',
                line=dict(width=3),
                marker=dict(size=10),
                stackgroup='one',
                hovertemplate=f'<b>{material}</b><br>Season: %{{x}}<br>Copies: %{{y:,}}<extra></extra>'
            ))

        fig.update_layout(
            title="Material Usage Over Time (Stacked Area)",
            xaxis_title="Season",
            yaxis_title="Copies",
            height=450,
            hovermode='x unified'
        )

        st.plotly_chart(fig, use_container_width=True)

def create_document_comparison(df):
    """Enhanced Document comparison"""
    st.markdown('<p class="category-header">📄 DOCUMENT COMPARISON</p>', unsafe_allow_html=True)

    df_doc = df[df["Product name"].str.strip() == "Document"].copy()

    if len(df_doc) == 0:
        st.warning("No Document data found")
        return

    col1, col2 = st.columns(2)

    # Copies trend
    with col1:
        st.markdown("#### 📄 Copies Trend")

        copies_by_season = df_doc.groupby("Season")["Copies"].sum()

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=copies_by_season.index,
            y=copies_by_season.values,
            mode='lines+markers',
            fill='tozeroy',
            line=dict(color='#ff7f0e', width=4),
            marker=dict(size=12, symbol='diamond'),
            text=[f'{int(x):,}' for x in copies_by_season.values],
            textposition='top center',
            hovertemplate='<b>%{x}</b><br>Copies: %{y:,}<extra></extra>'
        ))

        fig.update_layout(height=400, hovermode='x')
        st.plotly_chart(fig, use_container_width=True)

    # Revenue trend
    with col2:
        st.markdown("#### 💰 Revenue Trend")

        revenue_by_season = df_doc.groupby("Season")["Charged amount"].sum()

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=revenue_by_season.index,
            y=revenue_by_season.values,
            mode='lines+markers',
            fill='tozeroy',
            line=dict(color='#2ca02c', width=4),
            marker=dict(size=12, symbol='diamond'),
            text=[f'${x:,.0f}' for x in revenue_by_season.values],
            textposition='top center',
            hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.2f}<extra></extra>'
        ))

        fig.update_layout(height=400, hovermode='x')
        st.plotly_chart(fig, use_container_width=True)

    # Paper type evolution
    if "Paper type" in df_doc.columns:
        st.markdown("#### 📋 Paper Type Evolution")

        paper_pivot = df_doc.pivot_table(
            values="Copies",
            index="Season",
            columns="Paper type",
            aggfunc="sum",
            fill_value=0
        )

        fig = go.Figure()

        for paper in paper_pivot.columns:
            fig.add_trace(go.Bar(
                name=str(paper),
                x=paper_pivot.index,
                y=paper_pivot[paper],
                text=[f'{int(x):,}' if x > 0 else '' for x in paper_pivot[paper]],
                textposition='auto',
                hovertemplate=f'<b>{paper}</b><br>Season: %{{x}}<br>Copies: %{{y:,}}<extra></extra>'
            ))

        fig.update_layout(
            barmode='group',
            height=400,
            hovermode='x unified',
            xaxis_title="Season",
            yaxis_title="Copies"
        )

        st.plotly_chart(fig, use_container_width=True)

def create_poster_comparison(df):
    """Enhanced Poster comparison"""
    st.markdown('<p class="category-header">🖼️ LARGE FORMAT POSTER COMPARISON</p>', unsafe_allow_html=True)

    df_poster = df[df["Product name"].str.strip() == "Large-Format Poster"].copy()

    if len(df_poster) == 0:
        st.warning("No Large-Format Poster data found")
        return

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📄 Copies by Season")

        copies_by_season = df_poster.groupby("Season")["Copies"].sum()

        fig = go.Figure(data=[go.Bar(
            x=copies_by_season.index,
            y=copies_by_season.values,
            marker=dict(
                color=copies_by_season.values,
                colorscale='Reds',
                showscale=True
            ),
            text=[f'{int(x):,}' for x in copies_by_season.values],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Copies: %{y:,}<extra></extra>'
        )])

        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 💰 Revenue by Season")

        revenue_by_season = df_poster.groupby("Season")["Charged amount"].sum()

        fig = go.Figure(data=[go.Bar(
            x=revenue_by_season.index,
            y=revenue_by_season.values,
            marker=dict(
                color=revenue_by_season.values,
                colorscale='Purples',
                showscale=True
            ),
            text=[f'${x:,.0f}' for x in revenue_by_season.values],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.2f}<extra></extra>'
        )])

        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Poster size comparison
    if "Paper size" in df_poster.columns:
        st.markdown("#### 📏 Poster Size Distribution Across Seasons")

        size_pivot = df_poster.pivot_table(
            values="Copies",
            index="Season",
            columns="Paper size",
            aggfunc="sum",
            fill_value=0
        )

        fig = go.Figure()

        for size in size_pivot.columns:
            fig.add_trace(go.Bar(
                name=str(size),
                x=size_pivot.index,
                y=size_pivot[size],
                hovertemplate=f'<b>{size}</b><br>Season: %{{x}}<br>Copies: %{{y:,}}<extra></extra>'
            ))

        fig.update_layout(
            barmode='stack',
            height=450,
            hovermode='x unified',
            xaxis_title="Season",
            yaxis_title="Copies",
            legend_title="Poster Size"
        )

        st.plotly_chart(fig, use_container_width=True)

# ==================== MAIN APP ====================

def main():
    st.markdown('<p class="main-header">📊 DMC Order Analytics Dashboard</p>', unsafe_allow_html=True)

    # Enhanced Sidebar
    with st.sidebar:
        st.markdown("## 📊 DMC Analytics")
        st.markdown("---")

        st.markdown("### 🎯 Interactive Features")
        st.markdown("""
        ✨ **Multi-Select Filters**
        🔍 **Drill-Down Charts**
        📊 **Dynamic Comparisons**
        🎨 **Color-Coded Insights**
        💾 **Export Capabilities**
        """)

        st.markdown("---")
        st.markdown("### 💡 Tips")
        st.info("💡 Click on legends to show/hide data  \n🖱️ Hover over charts for details  \n🔍 Use filters for focused analysis")

    # Main tabs
    tab1, tab2 = st.tabs(["📈 Single Year Analysis", "📊 Multi-Year Comparison"])

    # ==================== SINGLE YEAR TAB ====================
    with tab1:
        st.markdown("### 📤 Upload Single Year Data")

        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=['csv'],
            key='single_year',
            help="Upload your order data for single year analysis"
        )

        if uploaded_file:
            try:
                # Read CSV with encoding handling
                try:
                    df = pd.read_csv(uploaded_file, encoding='utf-8')
                except:
                    uploaded_file.seek(0)
                    try:
                        df = pd.read_csv(uploaded_file, encoding='latin-1')
                    except:
                        uploaded_file.seek(0)
                        df = pd.read_csv(uploaded_file, encoding='cp1252')

                st.success(f"✅ Loaded {len(df):,} rows and {len(df.columns)} columns")

                # Validate
                required = ["Product name", "Copies", "Charged"]
                is_valid, missing, msg = validate_columns(df, required)

                if not is_valid:
                    st.error(msg)
                else:
                    df_cleaned = clean_data(df.copy())

                    # Category tabs with icons
                    cat_tabs = st.tabs([
                        "📊 Overall",
                        "🖨️ 3D Print",
                        "📄 Document",
                        "🖼️ Large Format Poster"
                    ])

                    with cat_tabs[0]:
                        create_overall_visualizations(df_cleaned)

                    with cat_tabs[1]:
                        create_3d_print_visualizations(df_cleaned)

                    with cat_tabs[2]:
                        create_document_visualizations(df_cleaned)

                    with cat_tabs[3]:
                        create_poster_visualizations(df_cleaned)

                    # Download section
                    st.markdown("---")
                    st.markdown("### 💾 Export Data")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.download_button(
                            "📥 Download Cleaned CSV",
                            df_cleaned.to_csv(index=False),
                            f"cleaned_{uploaded_file.name}",
                            "text/csv",
                            use_container_width=True
                        )

                    with col2:
                        # Download filtered data
                        st.info("💡 Use filters in each category to export specific data")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                with st.expander("Show Error Details"):
                    st.exception(e)

    # ==================== MULTI-YEAR TAB ====================
    with tab2:
        st.markdown("### 📤 Upload Multiple Years")

        uploaded_files = st.file_uploader(
            "Choose CSV files",
            type=['csv'],
            accept_multiple_files=True,
            key='multi_year',
            help="Upload multiple files for year-over-year comparison"
        )

        if uploaded_files:
            try:
                st.success(f"✅ Uploaded {len(uploaded_files)} file(s)")

                dfs = []
                file_info = []

                for file in uploaded_files:
                    try:
                        df = pd.read_csv(file, encoding='utf-8')
                    except:
                        file.seek(0)
                        try:
                            df = pd.read_csv(file, encoding='latin-1')
                        except:
                            file.seek(0)
                            df = pd.read_csv(file, encoding='cp1252')

                    season = extract_season_from_filename(file.name)
                    df['Season'] = season
                    dfs.append(df)
                    file_info.append({
                        'Filename': file.name,
                        'Season': season,
                        'Rows': len(df)
                    })

                # Show file info
                with st.expander("📋 File Summary", expanded=True):
                    st.dataframe(pd.DataFrame(file_info), use_container_width=True)

                merged_df = pd.concat(dfs, ignore_index=True)
                merged_cleaned = clean_data(merged_df.copy())

                st.success(f"✅ Merged {len(merged_df):,} total rows from {len(uploaded_files)} files")

                # Comparison category tabs
                comp_tabs = st.tabs([
                    "📊 Overall",
                    "🖨️ 3D Print",
                    "📄 Document",
                    "🖼️ Large Format Poster"
                ])

                with comp_tabs[0]:
                    create_overall_comparison(merged_cleaned)

                with comp_tabs[1]:
                    create_3d_print_comparison(merged_cleaned)

                with comp_tabs[2]:
                    create_document_comparison(merged_cleaned)

                with comp_tabs[3]:
                    create_poster_comparison(merged_cleaned)

                # Download
                st.markdown("---")
                st.markdown("### 💾 Export Merged Data")

                st.download_button(
                    "📥 Download Merged & Cleaned CSV",
                    merged_cleaned.to_csv(index=False),
                    "merged_cleaned.csv",
                    "text/csv",
                    use_container_width=True
                )

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                with st.expander("Show Error Details"):
                    st.exception(e)

    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666; padding: 2rem;'>
            <p><b>DMC Order Analytics Dashboard</b> | Powered by Streamlit & Plotly</p>
            <p>📧 For support, contact your administrator</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
