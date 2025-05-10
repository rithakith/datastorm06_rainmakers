# Insurance Agent Performance Prediction & Management System

A comprehensive analytics solution for predicting at-risk insurance agents and providing tailored intervention strategies based on performance classification.

## Project Overview

This project focuses on analyzing insurance agent performance data to:

1. Predict agents at risk of achieving zero new policies ("NILL risk")
2. Classify agents into performance categories (Low, Medium, High)
3. Provide personalized action plans and intervention strategies based on analytics

## Repository Structure

- **part1.docx**: Document detailing key factors influencing early agent performance and indicators of NILL risk
- **part2.docx**: Document outlining agent performance classification methodology and intervention strategies
- **part1(NILL Predicting).ipynb**: Jupyter notebook containing the NILL risk prediction model
- **part2(clustering).ipynb**: Jupyter notebook implementing K-means clustering for agent performance classification
- **app.py**: Streamlit application for personalized action plan recommendations for at-risk agents

## Key Features

### NILL Risk Prediction

The system identifies agents at risk of achieving zero new policies by analyzing:

- Historical policy count trends
- Proposal and quotation activity
- New agent onboarding status
- Time delays in first sales
- Irregular sales patterns

### Agent Performance Classification

Using K-means clustering with the following KPIs:

- New policy count
- ANBP value
- Unique customers
- Unique proposals
- Proposal to quotation ratio
- Quotation to policy ratio

### Intervention Strategies

Tailored approaches for each performance category:

#### High Performers

- Recognition and rewards programs
- Leadership and mentorship opportunities
- Advanced development offerings
- Strategic involvement in company initiatives
- Increased autonomy and challenges

#### Medium Performers

- Skill gap analysis and targeted coaching
- Peer learning and best practice sharing
- Goal setting and specific incentives
- Pipeline management support

#### Low Performers

- Intensive coaching on lead qualification and proposal development
- Structured activity targets for small wins
- Dedicated mentorship programs
- Performance improvement plans when necessary

## Getting Started

### Prerequisites

- Python 3.x
- Required packages: pandas, numpy, scikit-learn, streamlit, matplotlib, seaborn

### Running the Application

```bash
streamlit run app.py
```

### Accessing the Notebooks

The analysis notebooks can be opened using Jupyter Notebook or JupyterLab:

```bash
jupyter notebook part1\(NILL\ Predicting\).ipynb
jupyter notebook part2\(clustering\).ipynb
```

Alternatively, you can access the clustering notebook via Google Colab: [Clustering Notebook](https://colab.research.google.com/drive/1w2jd0k7so7J_VnocH5IV8Xkoki2rfsK9?usp=sharing)

## Data Analysis Methodology

### NILL Risk Prediction

The model analyzes historical patterns and key performance indicators to identify agents at risk of achieving zero new policies in the upcoming month.

### Performance Classification

The system uses K-means clustering (k=3) to objectively categorize agents into Low, Medium, and High performers based on standardized performance metrics.
