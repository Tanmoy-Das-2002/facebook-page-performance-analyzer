# Facebook Page Performance Analyzer

A reusable Streamlit dashboard for analyzing Facebook Page content performance from CSV exports.

The application analyzes post reach, views, engagement, clicks, posting-time patterns, hashtag-associated performance, and top-performing posts.

The included demo dataset is synthetic data modeled on the structure of a Meta Business Suite Facebook Page export. It is intended for demonstration and portfolio purposes and does not represent real Facebook Page data.

---

## Features

- Upload and analyze Facebook Page CSV data
- Validate required columns, numeric values, missing values, and dates
- Filter analysis by post type and date range
- Track total posts, reach, views, engagement rate, and click rate
- Compare performance across post types
- Analyze monthly reach and engagement trends
- Analyze performance by posting time
- Examine engagement composition across reactions, comments, and shares
- Analyze hashtag-associated reach and engagement
- Identify top-performing posts by engagement rate
- Display results interactively through a Streamlit dashboard

---

## Dashboard Analysis

### 1. KPI Overview

The dashboard provides:

- Total Posts
- Total Reach
- Total Views
- Average Engagement Rate
- Average Click Rate

Total Reach and Total Views are calculated as sums of post-level metrics across the selected posts. They do not represent unique people or unique viewers.

### 2. Post Type Performance

Compares content performance across available post types using:

- Average Reach
- Average Views
- Average Engagement Rate

### 3. Monthly Performance

Analyzes:

- Average Reach by Month
- Average Engagement Rate by Month

The analysis uses the post's publish timestamp to derive the month.

### 4. Posting Time Performance

Posts are grouped into three time periods:

- Morning: 06:00–11:59
- Afternoon: 12:00–17:59
- Evening: 18:00–23:59

The dashboard compares:

- Average Reach
- Average Engagement Rate
- Number of Posts

These results describe patterns in the dataset and do not establish that posting time causes differences in performance.

### 5. Engagement Composition

Shows the total number of:

- Reactions
- Comments
- Shares

This provides a breakdown of the types of engagement generated across the selected posts.

### 6. Hashtag Performance

Extracts hashtags from post descriptions and calculates:

- Average Reach
- Average Engagement Rate
- Post Count

Posts can contain multiple hashtags, so hashtag groups overlap.

Hashtag metrics describe performance associated with posts using each hashtag. They do not establish the causal impact of individual hashtags.

### 7. Top Performing Posts

Displays the top 10 posts ranked by engagement rate.

Engagement rate is calculated as:

(Reactions + Comments + Shares) / Reach × 100

---

## Key Metrics

### Engagement Rate

Measures engagement relative to the post's reach.

```text
(Reactions + Comments + Shares) / Reach × 100
```

### Click Rate

Measures total clicks relative to the post's reach.

```text
Total Clicks / Reach × 100
```

### Average Metrics

Average Reach, Average Views, Average Engagement Rate, and Average Click Rate are calculated at the post level and then averaged across the selected posts.

---

## Data

The included dataset is:

```text
data/LumaCraft_Studio_Facebook_Content_2025_SYNTHETIC.csv
```

It contains 600 synthetic Facebook Page posts across 2025 and follows the structure of a Meta Business Suite export.

The dataset includes fields related to:

- Post information
- Publish timestamps
- Post type
- Views
- Reach
- Reactions
- Comments
- Shares
- Total clicks
- Video metrics
- Monetization-related fields
- Post descriptions and hashtags

### Important Data Note

The included data is **synthetic**.

It was created to model the structure and type of data available in a Facebook Page export and should not be interpreted as real performance data from LumaCraft Studio or any real Facebook Page.

The application is designed so that users can upload their own compatible Facebook CSV export through the Streamlit interface.

---

## Data Validation

The application validates uploaded CSV files before performing analysis.

It checks for:

- Missing required columns
- Invalid numeric values
- Missing values in required numeric columns
- Invalid publish dates
- Invalid date ranges
- Empty results after filtering

This prevents invalid input from reaching the dashboard calculations and producing misleading results or application errors.

---

## Project Structure

```text
facebook_page_analysis/
│
├── data/
│   └── LumaCraft_Studio_Facebook_Content_2025_SYNTHETIC.csv
│
├── notebooks/
│   └── facebook_analysis.ipynb
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Technology Stack

- Python
- Pandas
- Streamlit
- Matplotlib
- Jupyter Notebook

---

## Analysis Workflow

The project follows this general workflow:

```text
Facebook Page CSV
       ↓
Data Validation
       ↓
Date & Time Processing
       ↓
Metric Calculation
       ↓
Filtering
       ↓
Performance Analysis
       ↓
Interactive Streamlit Dashboard
```

The analysis notebook is used for exploratory analysis and validation, while `app.py` contains the interactive dashboard application.

---

## Running the Project Locally

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd facebook_page_analysis
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

#### Windows

```bash
.venv\Scripts\activate
```

#### macOS / Linux

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Streamlit application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## Using the Dashboard

The application can be used in two ways.

### Demo Dataset

If no file is uploaded, the application loads the included synthetic dataset automatically.

### Custom Dataset

Use the **Upload Facebook CSV** option in the sidebar to upload a compatible Facebook Page CSV export.

After uploading a valid dataset, the dashboard recalculates the analysis using the uploaded data.

Available filters include:

- Post Type
- Start Date
- End Date

All dashboard sections update based on the selected filters.

---

## Analytical Considerations

Several metrics in this project require careful interpretation.

### Reach and Views

Total Reach and Total Views are sums of post-level values.

They should not be interpreted as the number of unique people or unique viewers across the entire year.

### Hashtags

Posts may contain multiple hashtags.

Therefore, hashtag performance groups can overlap. A higher average performance for posts containing a particular hashtag does not demonstrate that the hashtag itself caused the performance.

### Posting Time

The posting-time analysis identifies patterns within the dataset.

It does not establish that posting at a particular time directly causes higher or lower performance.

### Synthetic Data

Because the included dataset is synthetic, its results are intended to demonstrate the functionality of the application rather than provide real-world Facebook performance conclusions.

---

## Notebook

The project also includes an exploratory analysis notebook:

```text
notebooks/facebook_analysis.ipynb
```

The notebook contains the underlying data exploration, validation, metric calculations, and analysis used to understand the dataset before building the interactive dashboard.

---

## Future Improvements

Potential future extensions include:

- Additional Facebook export column support
- More interactive visualizations
- Exporting filtered results
- Automated report generation
- Additional content-performance metrics
- Support for additional social-media export formats

---

## Disclaimer

This project is for educational and portfolio demonstration purposes.

The included dataset is synthetic and modeled on the structure of a Meta Business Suite export. It is not real Facebook Page data and should not be used to make real business decisions.
