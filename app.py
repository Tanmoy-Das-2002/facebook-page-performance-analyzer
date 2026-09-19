import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Facebook Page Performance Analyzer",
    layout="wide"
)

# Dataset selection
st.sidebar.header("Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Upload Facebook CSV",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    DATA_PATH = "data/LumaCraft_Studio_Facebook_Content_2025_SYNTHETIC.csv"
    df = pd.read_csv(DATA_PATH)

required_columns = [
    "Publish time",
    "Post type",
    "Reach",
    "Views",
    "Reactions, comments and shares",
    "Total clicks",
    "Reactions",
    "Comments",
    "Shares",
    "Description",
    "Post ID"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error("The uploaded CSV is missing required columns:")
    st.write(missing_columns)
    st.stop()

numeric_columns = [
    "Reach",
    "Views",
    "Reactions, comments and shares",
    "Total clicks",
    "Reactions",
    "Comments",
    "Shares"
]

invalid_numeric_columns = []
missing_numeric_columns = []

for column in numeric_columns:
    numeric_values = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    invalid_values = (
        numeric_values.isna() &
        df[column].notna()
    )

    missing_values = df[column].isna()

    if invalid_values.any():
        invalid_numeric_columns.append(column)

    if missing_values.any():
        missing_numeric_columns.append(column)

if invalid_numeric_columns:
    st.error("The uploaded CSV contains invalid numeric values in:")
    st.write(invalid_numeric_columns)
    st.stop()

if missing_numeric_columns:
    st.error("The uploaded CSV contains missing values in required numeric columns:")
    st.write(missing_numeric_columns)
    st.stop()

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column])

# Convert publish time to datetime
df["Publish time"] = pd.to_datetime(
    df["Publish time"],
    errors="coerce"
)

if df["Publish time"].isna().any():
    st.error("The uploaded CSV contains invalid date values in 'Publish time'.")
    st.stop()

# Create date/time features
df["Date"] = df["Publish time"].dt.date
df["Month"] = df["Publish time"].dt.month
df["Day of Week"] = df["Publish time"].dt.day_name()
df["Hour"] = df["Publish time"].dt.hour

# Calculate performance metrics
df["Engagement Rate (%)"] = (
    df["Reactions, comments and shares"] / df["Reach"] * 100
)

df["Click Rate (%)"] = (
    df["Total clicks"] / df["Reach"] * 100
)

# Dashboard header
st.title("Facebook Page Performance Analyzer")

if uploaded_file is not None:
    st.caption(
        "Analyzing uploaded Facebook Page CSV data. "
        "Metrics and visualizations update based on the selected filters."
    )
else:
    st.caption(
        "Demo dataset: synthetic data modeled on Meta Business Suite export structure. "
        "Upload your own Facebook Page CSV to analyze real data."
    )

# Dashboard filters
st.sidebar.header("Filters")

post_type_options = ["All"] + sorted(df["Post type"].dropna().unique().tolist())

selected_post_type = st.sidebar.selectbox(
    "Post Type",
    post_type_options
)

min_date = df["Date"].min()
max_date = df["Date"].max()

# Date range filter
start_date = st.sidebar.date_input(
    "Start Date",
    value=min_date,
    min_value=min_date,
    max_value=max_date
)

end_date = st.sidebar.date_input(
    "End Date",
    value=max_date,
    min_value=min_date,
    max_value=max_date
)

# Apply filters
filtered_df = df.copy()

if selected_post_type != "All":
    filtered_df = filtered_df[
        filtered_df["Post type"] == selected_post_type
    ]

if start_date <= end_date:
    filtered_df = filtered_df[
        (filtered_df["Date"] >= start_date) &
        (filtered_df["Date"] <= end_date)
    ]
else:
    st.sidebar.error("End Date must be after Start Date.")

# Use filtered data for the dashboard
df = filtered_df

if df.empty:
    st.warning("No posts match the selected filters. Please adjust the filters.")
    st.stop()

# KPI calculations
total_posts = len(df)
total_reach = df["Reach"].sum()
total_views = df["Views"].sum()
avg_engagement_rate = df["Engagement Rate (%)"].mean()
avg_click_rate = df["Click Rate (%)"].mean()

st.info(
    f"Showing {len(df):,} posts from "
    f"{start_date.strftime('%d %b %Y')} to "
    f"{end_date.strftime('%d %b %Y')} "
    f"({selected_post_type} posts)."
)

# KPI cards
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Posts", f"{total_posts:,}")
col2.metric("Total Reach", f"{total_reach:,}")
col3.metric("Total Views", f"{total_views:,}")
col4.metric("Avg Engagement Rate", f"{avg_engagement_rate:.2f}%")
col5.metric("Avg Click Rate", f"{avg_click_rate:.2f}%")

st.caption(
    "Total Reach and Total Views are sums of post-level metrics across the selected posts; "
    "they do not represent unique people or unique viewers."
)

# Post type performance
st.header("Post Type Performance")

post_type_summary = (
    df.groupby("Post type")
    .agg(
        Average_Reach=("Reach", "mean"),
        Average_Views=("Views", "mean"),
        Average_Engagement_Rate=("Engagement Rate (%)", "mean")
    )
    .reset_index()
)

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Average Reach")

    reach_chart = post_type_summary.set_index("Post type")[
        ["Average_Reach"]
    ]

    st.bar_chart(reach_chart)

with col2:
    st.subheader("Average Views")

    views_chart = post_type_summary.set_index("Post type")[
        ["Average_Views"]
    ]

    st.bar_chart(views_chart)

with col3:
    st.subheader("Average Engagement Rate (%)")

    engagement_chart = post_type_summary.set_index("Post type")[
        ["Average_Engagement_Rate"]
    ]

    st.bar_chart(engagement_chart)

# Monthly performance
st.header("Monthly Performance")

monthly_summary = (
    df.groupby("Month")
    .agg(
        Average_Reach=("Reach", "mean"),
        Average_Engagement_Rate=("Engagement Rate (%)", "mean")
    )
    .reset_index()
)

# Create chronological month labels
month_order = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

monthly_summary["Month"] = pd.to_datetime(
    monthly_summary["Month"],
    format="%m"
).dt.strftime("%b")

monthly_summary["Month"] = pd.Categorical(
    monthly_summary["Month"],
    categories=month_order,
    ordered=True
)

monthly_summary = monthly_summary.sort_values("Month")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Average Reach by Month")

    reach_monthly = monthly_summary.set_index("Month")[
        ["Average_Reach"]
    ]

    st.line_chart(reach_monthly)

with col2:
    st.subheader("Average Engagement Rate by Month (%)")

    engagement_monthly = monthly_summary.set_index("Month")[
        ["Average_Engagement_Rate"]
    ]

    st.line_chart(engagement_monthly)

# Posting time performance
st.header("Posting Time Performance")

df["Time Period"] = pd.cut(
    df["Hour"],
    bins=[5, 11, 17, 23],
    labels=["Morning", "Afternoon", "Evening"]
)

st.caption(
    "Posting periods: Morning (06:00–11:59), "
    "Afternoon (12:00–17:59), Evening (18:00–23:59)."
)

time_summary = (
    df.groupby("Time Period", observed=False)
    .agg(
        Average_Reach=("Reach", "mean"),
        Average_Engagement_Rate=("Engagement Rate (%)", "mean"),
        Post_Count=("Post ID", "count")
    )
    .reset_index()
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Average Reach by Posting Time")

    time_reach = time_summary.set_index("Time Period")[
        ["Average_Reach"]
    ]

    st.bar_chart(time_reach)

with col2:
    st.subheader("Average Engagement Rate by Posting Time (%)")

    time_engagement = time_summary.set_index("Time Period")[
        ["Average_Engagement_Rate"]
    ]

    st.bar_chart(time_engagement)

st.caption(
    "Time periods are based on the post's publish hour. "
    "Results describe patterns in this dataset and do not establish causation."
)

# Engagement composition
st.header("Engagement Composition")

engagement_totals = pd.DataFrame({
    "Engagement Type": [
        "Reactions",
        "Comments",
        "Shares"
    ],
    "Total": [
        df["Reactions"].sum(),
        df["Comments"].sum(),
        df["Shares"].sum()
    ]
})

engagement_chart = engagement_totals.set_index("Engagement Type")

st.bar_chart(engagement_chart)

st.caption(
    "Shows the total number of reactions, comments, and shares across all posts."
)

# Hashtag extraction and performance
st.header("Hashtag Performance")

def extract_hashtags(text):
    if pd.isna(text):
        return []

    return [
        word for word in str(text).split()
        if word.startswith("#")
    ]

# Extract hashtags from the post description
df["Hashtags"] = df["Description"].apply(extract_hashtags)

hashtag_rows = []

for _, row in df.iterrows():
    for hashtag in set(row["Hashtags"]):
        hashtag_rows.append({
            "Hashtag": hashtag,
            "Reach": row["Reach"],
            "Engagement Rate (%)": row["Engagement Rate (%)"]
        })

if hashtag_rows:
    hashtag_df = pd.DataFrame(hashtag_rows)

    hashtag_summary = (
        hashtag_df.groupby("Hashtag")
        .agg(
            Average_Reach=("Reach", "mean"),
            Average_Engagement_Rate=("Engagement Rate (%)", "mean"),
            Post_Count=("Hashtag", "count")
        )
        .reset_index()
        .sort_values("Average_Reach", ascending=False)
    )

    hashtag_display = hashtag_summary.rename(columns={
        "Average_Reach": "Average Reach",
        "Average_Engagement_Rate": "Average Engagement Rate (%)",
        "Post_Count": "Post Count"
    })

    hashtag_display["Average Reach"] = (
        hashtag_display["Average Reach"].round(0).astype(int)
    )

    hashtag_display["Average Engagement Rate (%)"] = (
        hashtag_display["Average Engagement Rate (%)"].round(2)
    )

    hashtag_display["Post Count"] = (
        hashtag_display["Post Count"].astype(int)
    )

    st.dataframe(
        hashtag_display,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("No hashtags were found in the selected posts.")

st.caption(
    "Hashtag metrics describe performance associated with posts using each hashtag. "
    "Posts may contain multiple hashtags, so groups overlap. "
    "These results show association, not the causal impact of individual hashtags."
)

# Top performing posts
st.header("Top Performing Posts")

top_posts = (
    df[
        [
            "Post ID",
            "Post type",
            "Publish time",
            "Reach",
            "Engagement Rate (%)"
        ]
    ]
    .sort_values("Engagement Rate (%)", ascending=False)
    .head(10)
)

top_posts["Engagement Rate (%)"] = top_posts[
    "Engagement Rate (%)"
].round(2)

st.dataframe(
    top_posts,
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Top 10 posts ranked by engagement rate, calculated as "
    "total reactions, comments, and shares divided by reach."
)

