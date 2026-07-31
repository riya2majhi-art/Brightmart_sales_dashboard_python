import streamlit as st
import pandas as pd
import plotly.express as px

from data_loader import load_data

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="BrightMart Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# MODERN DARK DASHBOARD THEME
# =====================================================

st.markdown(
    """
    <style>

    /* Main App Background & Typography */
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Container Spacing */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
    }

    /* Typography Hierarchy */
    h1 {
        color: #F8FAFC !important;
        font-size: 32px !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }

    h2, h3, h4 {
        color: #E2E8F0 !important;
        font-weight: 600 !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #1E293B !important;
        border-right: 1px solid #334155;
    }

    section[data-testid="stSidebar"] * {
        color: #CBD5E1 !important;
    }

    /* Sidebar Labels - Made Compact & Smaller */
    section[data-testid="stSidebar"] label p {
        font-size: 13px !important;
        font-weight: 500 !important;
        color: #94A3B8 !important;
        margin-bottom: 2px !important;
    }

    /* Sidebar Dropdowns & Multi-Select Boxes */
    div[data-baseweb="select"] > div {
        background-color: #0F172A !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        min-height: 38px !important;
    }

    /* Tab Styling - High Visibility Active Highlights */
    button[data-baseweb="tab"] {
        background-color: #1E293B !important;
        color: #94A3B8 !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        padding: 8px 18px !important;
        margin-right: 8px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease;
    }

    button[data-baseweb="tab"]:hover {
        border-color: #38BDF8 !important;
        color: #F8FAFC !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #0284C7 !important;
        color: #FFFFFF !important;
        border-color: #38BDF8 !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.35);
    }

    /* Dataframe Styling */
    div[data-testid="stDataFrame"] {
        background-color: #1E293B;
        border-radius: 12px;
        border: 1px solid #334155;
        padding: 4px;
    }

    /* Horizontal Rules */
    hr {
        border-color: #334155 !important;
        margin: 1.5rem 0 !important;
    }

    /* Alert Boxes Overrides */
    .stAlert {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        color: #38BDF8 !important;
        border-radius: 10px !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# TITLE
# =====================================================

st.title("📊 BrightMart Sales Dashboard")
st.caption("Interactive Dashboard for Sales & Operations Analysis")

st.markdown("---")

# =====================================================
# LOAD DATA
# =====================================================

df_master, active_orders, cancelled_orders = load_data()

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.markdown(
    """
    <div style="
        background: #0F172A;
        padding: 12px 16px;
        border-radius: 12px;
        border: 1px solid #334155;
        text-align: center;
        margin-bottom: 20px;
    ">
        <p style="color:#94A3B8; font-size:11px; margin:0; text-transform:uppercase; letter-spacing:0.5px;">Developed By</p>
        <h4 style="color:#38BDF8; margin:4px 0 0 0; font-size:16px;">Riya Majhi</h4>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("<h3 style='font-size:16px; color:#F8FAFC; margin-bottom:12px;'>Dashboard Filters</h3>", unsafe_allow_html=True)

region = st.sidebar.multiselect(
    "🌍 Region",
    sorted(active_orders["region"].unique()),
    default=sorted(active_orders["region"].unique())
)

category = st.sidebar.multiselect(
    "📦 Category",
    sorted(active_orders["category"].unique()),
    default=sorted(active_orders["category"].unique())
)

segment = st.sidebar.multiselect(
    "👥 Segment",
    sorted(active_orders["segment"].unique()),
    default=sorted(active_orders["segment"].unique())
)

date_range = st.sidebar.date_input(
    "📅 Order Date",
    value=(
        active_orders["order_date"].min(),
        active_orders["order_date"].max()
    )
)

# =====================================================
# FILTER DATA
# =====================================================

filtered_df = active_orders[
    (active_orders["region"].isin(region)) &
    (active_orders["category"].isin(category)) &
    (active_orders["segment"].isin(segment))
]

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df["order_date"] >= pd.to_datetime(start_date)) &
        (filtered_df["order_date"] <= pd.to_datetime(end_date))
    ]

# =====================================================
# NO DATA MESSAGE
# =====================================================

if filtered_df.empty:
    st.warning("⚠️ No data available for the selected filter combination.")
    st.stop()

# =====================================================
# KPI CALCULATIONS
# =====================================================

total_revenue = filtered_df["line_revenue"].sum()
total_orders = filtered_df["order_id"].nunique()
avg_order_value = (
    filtered_df.groupby("order_id")["line_revenue"]
    .sum()
    .mean()
)
unique_customers = filtered_df["customer_id"].nunique()
cancelled_count = cancelled_orders["order_id"].nunique()

# =====================================================
# KPI CARD FUNCTION
# =====================================================

def kpi_card(title, value, color="#38BDF8"):
    st.markdown(
        f"""
        <div style="
            background: #1E293B;
            padding: 16px;
            border-radius: 12px;
            border: 1px solid #334155;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
            margin-bottom: 10px;
        ">
            <p style="
                font-size: 12px;
                color: #94A3B8;
                font-weight: 500;
                margin: 0 0 6px 0;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            ">{title}</p>
            <h3 style="
                color: {color} !important;
                font-size: 24px !important;
                font-weight: 700 !important;
                margin: 0;
            ">{value}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📋 Executive Overview",
        "📦 Sales & Orders",
        "🌍 Location Analysis",
        "👥 Customer Insights",
        "💡 Business Insights"
    ]
)

# Plotly Theme Helper
PLOTLY_TEMPLATE = "plotly_dark"
COLOR_SEQUENCE = ["#38BDF8", "#818CF8", "#F43F5E", "#34D399", "#FBBF24"]

# =====================================================
# TAB 1 : EXECUTIVE OVERVIEW
# =====================================================

with tab1:
    st.subheader("Executive Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        kpi_card("Total Revenue", f"₹ {total_revenue:,.0f}", "#38BDF8")

    with col2:
        kpi_card("Total Orders", f"{total_orders:,}", "#34D399")

    with col3:
        kpi_card("Avg Order Value", f"₹ {avg_order_value:,.0f}", "#A855F7")

    with col4:
        kpi_card("Customers", f"{unique_customers:,}", "#F97316")

    st.markdown("---")

    # Monthly Revenue Trend
    monthly_sales = (
        filtered_df
        .groupby(filtered_df["order_date"].dt.to_period("M"))["line_revenue"]
        .sum()
        .reset_index()
    )
    monthly_sales["order_date"] = monthly_sales["order_date"].astype(str)

    fig = px.line(
        monthly_sales,
        x="order_date",
        y="line_revenue",
        markers=True,
        title="Monthly Revenue Trend",
        template=PLOTLY_TEMPLATE
    )
    fig.update_traces(line_color="#38BDF8", line_width=3, marker_size=8)
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# TAB 2 : SALES & ORDERS
# =====================================================

with tab2:
    st.subheader("Sales & Order Analysis")

    col1, col2 = st.columns(2)

    with col1:
        category_sales = (
            filtered_df
            .groupby("category")["line_revenue"]
            .sum()
            .reset_index()
            .sort_values("line_revenue", ascending=False)
        )

        fig = px.bar(
            category_sales,
            x="category",
            y="line_revenue",
            title="Revenue by Category",
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=["#38BDF8"]
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        segment_sales = (
            filtered_df
            .groupby("segment")["line_revenue"]
            .sum()
            .reset_index()
        )

        fig = px.pie(
            segment_sales,
            names="segment",
            values="line_revenue",
            title="Sales Contribution by Segment",
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=COLOR_SEQUENCE
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top Products")

    top_products = (
        filtered_df
        .groupby("product_name")["line_revenue"]
        .sum()
        .reset_index()
        .sort_values("line_revenue", ascending=False)
        .head(10)
    )

    st.dataframe(top_products, use_container_width=True)

# =====================================================
# TAB 3 : LOCATION ANALYSIS
# =====================================================

with tab3:
    st.subheader("Location Performance Analysis")

    col1, col2 = st.columns(2)

    with col1:
        region_sales = (
            filtered_df
            .groupby("region")["line_revenue"]
            .sum()
            .reset_index()
            .sort_values("line_revenue", ascending=False)
        )

        fig = px.bar(
            region_sales,
            x="region",
            y="line_revenue",
            title="Revenue by Region",
            text_auto=".2s",
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=["#818CF8"]
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        state_sales = (
            filtered_df
            .groupby("state")["line_revenue"]
            .sum()
            .reset_index()
            .sort_values("line_revenue", ascending=False)
            .head(10)
        )

        fig = px.bar(
            state_sales,
            x="state",
            y="line_revenue",
            title="Top 10 States by Revenue",
            text_auto=".2s",
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=["#34D399"]
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.subheader("City-wise Performance")

    city_sales = (
        filtered_df
        .groupby("city")
        .agg(
            Revenue=("line_revenue", "sum"),
            Orders=("order_id", "nunique"),
            Customers=("customer_id", "nunique")
        )
        .reset_index()
        .sort_values("Revenue", ascending=False)
    )

    st.dataframe(city_sales.head(20), use_container_width=True)

# =====================================================
# TAB 4 : CUSTOMER INSIGHTS
# =====================================================

with tab4:
    st.subheader("Customer Behaviour Analysis")

    col1, col2 = st.columns(2)

    with col1:
        customer_segment = (
            filtered_df
            .groupby("segment")
            .agg(
                Customers=("customer_id", "nunique"),
                Revenue=("line_revenue", "sum")
            )
            .reset_index()
        )

        fig = px.pie(
            customer_segment,
            names="segment",
            values="Customers",
            title="Customer Distribution by Segment",
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=COLOR_SEQUENCE
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        top_customers = (
            filtered_df
            .groupby("customer_id")["line_revenue"]
            .sum()
            .reset_index()
            .sort_values("line_revenue", ascending=False)
            .head(10)
        )

        fig = px.bar(
            top_customers,
            x="customer_id",
            y="line_revenue",
            title="Top 10 Customers",
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=["#F43F5E"]
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.subheader("Customer Revenue Details")

    customer_table = (
        filtered_df
        .groupby(["customer_id", "segment"])
        .agg(
            Total_Revenue=("line_revenue", "sum"),
            Total_Orders=("order_id", "nunique")
        )
        .reset_index()
        .sort_values("Total_Revenue", ascending=False)
    )

    st.dataframe(customer_table.head(20), use_container_width=True)

# =====================================================
# TAB 5 : BUSINESS INSIGHTS
# =====================================================

with tab5:
    st.subheader("Business Insights")

    cancellation_rate = (
        cancelled_count / (cancelled_count + total_orders)
    ) * 100 if (cancelled_count + total_orders) > 0 else 0

    col1, col2 = st.columns(2)

    with col1:
        kpi_card("Cancellation Rate", f"{cancellation_rate:.2f}%", "#EF4444")

    with col2:
        kpi_card("Cancelled Orders", f"{cancelled_count:,}", "#F97316")

    st.markdown("---")

    st.subheader("Key Findings")

    highest_category = (
        filtered_df
        .groupby("category")["line_revenue"]
        .sum()
        .idxmax()
    ) if not filtered_df.empty else "N/A"

    highest_region = (
        filtered_df
        .groupby("region")["line_revenue"]
        .sum()
        .idxmax()
    ) if not filtered_df.empty else "N/A"

    highest_customer = (
        filtered_df
        .groupby("customer_id")["line_revenue"]
        .sum()
        .idxmax()
    ) if not filtered_df.empty else "N/A"

    st.info(
        f"""
        * **Highest Performing Category:** {highest_category}
        * **Top Revenue Region:** {highest_region}
        * **Top Spending Customer:** {highest_customer}
        """
    )

    st.markdown("---")

    st.subheader("Export Data")

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Filtered Sales CSV",
        data=csv,
        file_name="BrightMart_Filtered_Sales.csv",
        mime="text/csv"
    )