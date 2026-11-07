# Project Reflection

## Challenge: resolving a dataset path error

During dashboard development, the application initially failed to load because Python could not find `Sample - Superstore.csv`. The terminal showed a `FileNotFoundError`.

I checked the project folders and confirmed that the CSV file was not in the location expected by `app.py`. I corrected the file placement, checked the spelling of the filename and installed the required libraries. After that, I ran the application again and confirmed that the dashboard opened in the browser.

**What I learned:** a working Python script depends not only on correct code but also on correct file paths, project structure and installed dependencies.

## Data-cleaning decision: retaining outliers

I used the IQR method and box plots to identify unusual sales and profit values. I decided not to remove business-relevant outliers automatically. Very large orders may be legitimate bulk purchases, while negative profit and large discounts may be exactly the transactions the business needs to investigate.

**What I learned:** data-cleaning decisions should be justified by the meaning of the data and the business question. Removing extreme values without understanding them can hide useful information.

## Visualisation choice

I considered a pie chart for regional sales, but it did not make it easy to compare sales and profit together. A grouped bar chart was more appropriate because the two measures could be compared side by side for each region.

**What I learned:** choosing an appropriate chart improves the clarity and usefulness of analysis.

## Most surprising finding

The analysis showed a negative relationship between discount and profit (approximately -0.22). The scatter plot also made it possible to see loss-making transactions at different sales and discount levels.

**What I learned:** higher sales do not automatically mean higher profit. Discount decisions should be assessed against profitability, and correlation should not be mistaken for proof of causation.

## What I would improve next time

If I repeated the project, I would:
- Spend more time investigating customer purchasing patterns and repeat purchases.
- Validate every headline statistic directly from the final dataset and code.
- Add predictive analysis to estimate future sales and profit.
- Include additional operational-cost data to explain regional and product performance in more depth.
- Add automated checks for data loading, calculated columns and dashboard filtering.

## Overall reflection

Building this project improved my confidence in using Python for data manipulation, exploratory analysis and visualisation. I learned how to connect data analysis to business questions and present findings through an interactive dashboard. I also gained practical experience troubleshooting application errors and organising a project so that another person can install and run it.
