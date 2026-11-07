# Learning Outcomes

This document records the technical knowledge and practical skills developed during the Superstore Sales & Profitability Dashboard assignment.

## 1. Loading and understanding data

I learned how to:
- Import Python libraries needed for data analysis.
- Load a CSV file into a Pandas DataFrame.
- Preview the first and last records with `head()` and `tail()`.
- Check dataset dimensions with `shape`.
- Inspect column data types and non-null counts with `info()`.
- Generate descriptive summaries with `describe()`.
- Inspect unique values in categorical columns.

**Why it matters:** understanding the structure and contents of a dataset before analysing it helps prevent incorrect assumptions.

## 2. Data cleaning and preparation

I practised:
- Checking missing-value counts and percentages.
- Checking for fully duplicated rows.
- Converting date columns to datetime format.
- Creating calculated columns such as shipping duration and profit margin.
- Extracting year and month information from dates.
- Detecting outliers with quartiles and the interquartile range (IQR).

I also learned that an unusual value is not automatically an error. In this business case, very large orders, large losses and high discounts could be important business events. The decision to retain outliers was based on the assignment's business context.

## 3. Numerical analysis with NumPy and Pandas

I learned to calculate and interpret:
- Mean and median.
- Standard deviation.
- Percentiles.
- Minimum, maximum and range.
- Grouped totals and averages using `groupby()` and `agg()`.
- Correlation matrices for numerical variables.

A key interpretation lesson was that the mean can be pulled upward by a small number of large values. Comparing the mean with the median helped identify right-skewed sales and profit distributions.

## 4. Data visualisation

I gained experience choosing charts to communicate different types of information:

| Visualisation | What it helps communicate |
|---|---|
| Histogram | Distribution and frequency of profit values |
| Box plot | Spread and potential outliers |
| Horizontal bar chart | Average profit comparison across sub-categories |
| Heatmap | Strength and direction of correlations |
| Scatter plot | Relationship between sales and profit for individual records |
| Line chart | Monthly sales movement over time |
| Grouped bar chart | Sales and profit comparison across regions |

I learned that the chart type should match the business question. A visualisation should make a comparison or pattern easier to understand, not simply decorate a report.

## 5. Building an interactive dashboard

Using Dash and Plotly, I learned how to:
- Build a web dashboard from Python.
- Arrange content using rows, columns and Bootstrap components.
- Add dropdown filters and radio-button controls.
- Display key performance indicators (KPIs).
- Create interactive scatter, line and bar charts.
- Use Dash callbacks to connect filter inputs to dashboard outputs.
- Update KPI values and charts when users change filters.

This helped me understand how an interactive dashboard can make exploratory analysis more flexible than a collection of static charts.

## 6. Debugging and project organisation

I encountered a `FileNotFoundError` when the dashboard could not locate the CSV file. I learned to:
- Check the exact file name and directory.
- Keep the data file in a predictable project location.
- Install required libraries using `pip`.
- Run the application from the project environment.
- Organise code, data, documentation and screenshots into separate folders.

## 7. Business thinking

The assignment taught me to look beyond sales volume. A product or region can generate sales but still have weak or negative profit. I learned to investigate discounts, profit margins, loss-making transactions and differences between customer segments before making recommendations.

## 8. Skills demonstrated

- Python programming
- Data loading and preparation
- Data quality assessment
- Exploratory data analysis
- Descriptive statistics
- Outlier detection
- Grouped and comparative analysis
- Correlation interpretation
- Static and interactive data visualisation
- Dashboard development
- Debugging and documentation
- Communicating data-driven findings

## Personal takeaway

My biggest takeaway is that data analysis is a process: understand the question, inspect the data, prepare it carefully, analyse it, select suitable visualisations and explain what the results mean. I also learned to document decisions and validate reported figures before presenting conclusions.
