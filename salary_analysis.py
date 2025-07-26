import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter

# -----------------------------
# CONFIGURATION
# -----------------------------
EU_COUNTRIES = {
    'Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic',
    'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary',
    'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta',
    'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia',
    'Spain', 'Sweden'
}

USD_PER_TRY_2023 = 1 / 19.25  # ~0.052
USD_PER_EUR_2023 = 1.08        # 1 EUR = 1.08 USD
# Note: salary_data.csv values appear to be already in USD. Exchange constants are
# retained for transparency in case adjustment is required later.

# -----------------------------
# HELPERS
# -----------------------------

def annualize(row, salary_col: str = 'median_salary') -> float:
    """Convert monthly salaries to yearly if wage_span == 'Monthly'."""
    if row['wage_span'].lower().startswith('month'):
        return row[salary_col] * 12
    return row[salary_col]


def compute_gini(array: np.ndarray) -> float:
    """Compute Gini coefficient of array of values."""
    if array.size == 0:
        return np.nan
    array = array.flatten()
    if np.amin(array) < 0:
        array -= np.amin(array)  # make non-negative
    array = np.sort(array)
    n = array.size
    cumulative = np.cumsum(array)
    gini = (2 * np.sum((np.arange(1, n + 1) * array))) / (n * np.sum(array)) - (n + 1) / n
    return gini


def format_usd(x, pos):
    return f"${int(x / 1000)}k"


# -----------------------------
# LOAD DATA
# -----------------------------

salary_country_df = pd.read_csv('salary_data.csv')
row_count_country = salary_country_df.shape[0]
print(f"Loaded salary_data.csv with {row_count_country} rows")

salary_role_df = pd.read_csv('Salary.csv')
row_count_role = salary_role_df.shape[0]
print(f"Loaded Salary.csv with {row_count_role} rows")

# -----------------------------
# DATA PREPARATION - COUNTRY LEVEL (salary_data.csv)
# -----------------------------

salary_country_df['median_salary_yearly_usd'] = salary_country_df.apply(annualize, axis=1)

# Map regions

def map_region(country: str) -> str | None:
    if country == 'Turkey':
        return 'TR'
    if country == 'United States':
        return 'US'
    if country in EU_COUNTRIES:
        return 'EU'
    return None

salary_country_df['Region'] = salary_country_df['country_name'].apply(map_region)
region_country_df = salary_country_df.dropna(subset=['Region'])

print("Country-level rows kept for regions:")
print(region_country_df['Region'].value_counts())

# -----------------------------
# DATA PREPARATION - ROLE LEVEL (Salary.csv)
# -----------------------------

# Region mapping
COUNTRY_TO_REGION = {c: 'EU' for c in EU_COUNTRIES}
COUNTRY_TO_REGION.update({
    'UK': 'EU',  # Treat United Kingdom as EU for comparative purposes
    'USA': 'US',
    'United States': 'US',
    'Turkey': 'TR'
})

salary_role_df['Region'] = salary_role_df['Country'].map(COUNTRY_TO_REGION)

# Experience categorisation
bins = [-np.inf, 3, 7, 15, np.inf]
labels = ['Entry', 'Mid', 'Senior', 'Expert']
salary_role_df['Experience_Level'] = pd.cut(salary_role_df['Years of Experience'], bins=bins, labels=labels)

# Standardise job titles (simple lowercase trim)

def clean_title(title: str) -> str:
    title = title.lower().replace('sr.', 'senior').replace('sr ', 'senior ').replace('sr_', 'senior ')
    title = title.replace('jr.', 'junior').replace('jr ', 'junior ').replace('jr_', 'junior ')
    title = ' '.join(title.split())
    return title

salary_role_df['Job_Title_Norm'] = salary_role_df['Job Title'].astype(str).apply(clean_title)

role_region_df = salary_role_df.dropna(subset=['Region'])
print("Role-level rows kept for regions:")
print(role_region_df['Region'].value_counts())

# -----------------------------
# ANALYSIS LAYER 1: SALARY RATIOS (LIKE-FOR-LIKE)
# -----------------------------

ratio_results = []
regions = ['TR', 'EU', 'US']

for base in regions:
    for compare in regions:
        if base == compare:
            continue
        # Identify common jobs between the two regions
        jobs_base = role_region_df.loc[role_region_df['Region'] == base, 'Job_Title_Norm'].unique()
        jobs_compare = role_region_df.loc[role_region_df['Region'] == compare, 'Job_Title_Norm'].unique()
        common_jobs = set(jobs_base).intersection(jobs_compare)
        if not common_jobs:
            continue
        subset = role_region_df[role_region_df['Job_Title_Norm'].isin(common_jobs)]
        median_by_region = subset.groupby(['Region'])['Salary'].median()
        if base in median_by_region and compare in median_by_region:
            ratio = median_by_region[compare] / median_by_region[base]
            ratio_results.append({'Base': base, 'Compare': compare, 'MedianSalaryBase': median_by_region[base], 'MedianSalaryCompare': median_by_region[compare], 'Ratio': ratio})

ratio_df = pd.DataFrame(ratio_results)
print("Computed salary ratios based on median salaries for common roles:")
print(ratio_df)

# -----------------------------
# ANALYSIS LAYER 2: INCOME DISTRIBUTION & WELFARE
# -----------------------------

# Use role-level salaries where available, fall back to country-level medians for TR missing role data

# Prepare combined distribution list

dist_records = []
for region in regions:
    role_salaries = role_region_df.loc[role_region_df['Region'] == region, 'Salary']
    if role_salaries.empty:
        # Use country-level median salary yearly USD from salary_country_df
        med_val = region_country_df.loc[region_country_df['Region'] == region, 'median_salary_yearly_usd']
        if not med_val.empty:
            role_salaries = pd.Series(med_val.values)
    if role_salaries.empty:
        continue
    dist_records.append({'Region': region, 'Salaries': role_salaries})

dist_df = pd.DataFrame(dist_records)

# Compute Gini coefficients

gini_scores = {}
for _, row in dist_df.iterrows():
    gini_scores[row['Region']] = compute_gini(row['Salaries'].values)

print("Gini coefficients by region:")
print(gini_scores)

# Percentiles
percentile_table = {}
for _, row in dist_df.iterrows():
    arr = row['Salaries'].values
    percentiles = np.percentile(arr, [25, 50, 75, 90])
    percentile_table[row['Region']] = percentiles
print("Income percentiles (25th, 50th, 75th, 90th) by region:")
print(percentile_table)

# Career value: salary gain from entry to senior per region and job
career_gain_records = []
for region in regions:
    regional_df = role_region_df[role_region_df['Region'] == region]
    if regional_df.empty:
        continue
    for job in regional_df['Job_Title_Norm'].unique():
        job_df = regional_df[regional_df['Job_Title_Norm'] == job]
        if job_df.empty:
            continue
        entry_salary = job_df[job_df['Experience_Level'] == 'Entry']['Salary'].median()
        senior_salary = job_df[job_df['Experience_Level'] == 'Senior']['Salary'].median()
        if not np.isnan(entry_salary) and not np.isnan(senior_salary):
            gain = (senior_salary - entry_salary) / entry_salary * 100
            career_gain_records.append({'Region': region, 'Job': job, 'EntrySalary': entry_salary, 'SeniorSalary': senior_salary, 'GainPercent': gain})
career_gain_df = pd.DataFrame(career_gain_records)

# -----------------------------
# VISUALISATIONS
# -----------------------------

sns.set(style='whitegrid', palette='pastel')

# 1. Salary Ratio Bar Charts
if not ratio_df.empty:
    plt.figure(figsize=(8, 6))
    sns.barplot(data=ratio_df, x='Base', y='Ratio', hue='Compare')
    plt.axhline(1, color='grey', linestyle='--')
    plt.title('Salary Ratios Compared to Base Region (Median of Common Roles)')
    plt.ylabel('Ratio (Compare / Base)')
    plt.tight_layout()
    plt.savefig('salary_ratios.png')
    plt.close()

# 2. Overlaid KDE Distributions
plt.figure(figsize=(8, 6))
for _, row in dist_df.iterrows():
    sns.kdeplot(row['Salaries'], label=row['Region'], fill=True, alpha=0.3)
plt.title('Salary Distributions by Region')
plt.xlabel('Salary (USD)')
plt.legend()
plt.tight_layout()
plt.savefig('salary_distribution_kde.png')
plt.close()

# 3. Boxplot for Salary Distributions
plt.figure(figsize=(8, 6))
sns.boxplot(data=[row['Salaries'] for _, row in dist_df.iterrows()], orient='h')
plt.yticks(ticks=range(len(dist_df)), labels=[row['Region'] for _, row in dist_df.iterrows()])
plt.title('Salary Ranges by Region')
plt.xlabel('Salary (USD)')
plt.tight_layout()
plt.savefig('salary_distribution_box.png')
plt.close()

# 4. Career Gain Barplot
if not career_gain_df.empty:
    career_summary = career_gain_df.groupby('Region')['GainPercent'].median().reset_index()
    plt.figure(figsize=(8, 6))
    sns.barplot(data=career_summary, x='Region', y='GainPercent', palette='pastel')
    plt.title('Median Salary Increase from Entry to Senior Level')
    plt.ylabel('Gain (%)')
    plt.tight_layout()
    plt.savefig('career_gain.png')
    plt.close()

# -----------------------------
# REPORT GENERATION (Markdown)
# -----------------------------

with open('salary_report.md', 'w') as f:
    f.write('# Comparative Salary & Welfare Analysis Report (TR vs EU vs US)\n')
    f.write('Generated automatically by salary_analysis.py\n\n')
    f.write('## Executive Summary\n')
    top_ratios = ratio_df.sort_values('Ratio', ascending=False).head(5)
    f.write('Key salary disparities observed include:\n')
    for _, r in top_ratios.iterrows():
        f.write(f"* **{r['Compare']}** salaries are **{r['Ratio']:.2f}×** those in **{r['Base']}** for common roles.\n")
    f.write('\n')
    for region, g in gini_scores.items():
        f.write(f"* Income inequality (Gini) in **{region}** is **{g:.2f}**.\n")
    f.write('\n')

    f.write('## Methodology\n')
    f.write('Data from two sources were merged, converted, and normalised. See the Python script for detailed steps.\n\n')

    f.write('## Detailed Findings\n')
    f.write('### Salary Ratios\n')
    f.write(ratio_df.to_markdown(index=False))
    f.write('\n\n')

    f.write('### Income Percentiles\n')
    percentile_df = pd.DataFrame(percentile_table, index=['25th', '50th (Median)', '75th', '90th']).T
    f.write(percentile_df.to_markdown())
    f.write('\n\n')

    f.write('### Career Gain (Entry → Senior)\n')
    if not career_summary.empty:
        f.write(career_summary.to_markdown(index=False))
    f.write('\n\n')

    f.write('## Visuals\n')
    f.write('![Salary Ratios](salary_ratios.png)\n')
    f.write('![Salary Distribution KDE](salary_distribution_kde.png)\n')
    f.write('![Salary Distribution Box](salary_distribution_box.png)\n')
    f.write('![Career Gain](career_gain.png)\n')

print("Analysis complete. Report saved to salary_report.md and figures saved as PNG files.")