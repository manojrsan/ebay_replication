import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('input/PaidSearch.csv')
df['date'] = pd.to_datetime(df['date'])
df['log_revenue'] = np.log(df['revenue'])

treated = df[df['search_stays_on'] == 0]
untreated = df[df['search_stays_on'] == 1]

treated_pivot = treated.pivot_table(
    index='dma',
    columns='treatment_period',
    values='log_revenue',
    aggfunc='mean'
)

untreated_pivot = untreated.pivot_table(
    index='dma',
    columns='treatment_period',
    values='log_revenue',
    aggfunc='mean'
)

treated_pivot = treated_pivot.rename(columns={
    0: 'log_revenue_pre',
    1: 'log_revenue_post'
})

untreated_pivot = untreated_pivot.rename(columns={
    0: 'log_revenue_pre',
    1: 'log_revenue_post'
})

treated_pivot['log_revenue_diff'] = (
    treated_pivot['log_revenue_post'] -
    treated_pivot['log_revenue_pre']
)

untreated_pivot['log_revenue_diff'] = (
    untreated_pivot['log_revenue_post'] -
    untreated_pivot['log_revenue_pre']
)

treated_pivot.to_csv('temp/treated_pivot.csv')
untreated_pivot.to_csv('temp/untreated_pivot.csv')

print(f"Treated DMAs: {treated['dma'].nunique()}")
print(f"Untreated DMAs: {untreated['dma'].nunique()}")
print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")

avg_rev = (
    df.groupby(['date', 'search_stays_on'])['revenue']
      .mean()
      .reset_index()
)

plt.figure()
for group, label in [(1, 'Control (search stays on)'),
                     (0, 'Treatment (search goes off)')]:
    subset = avg_rev[avg_rev['search_stays_on'] == group]
    plt.plot(subset['date'], subset['revenue'], label=label)

plt.axvline(pd.to_datetime('2012-05-22'), linestyle='--')
plt.xlabel('Date')
plt.ylabel('Revenue')
plt.title('Average Revenue Over Time by Group')
plt.legend()

plt.tight_layout()
plt.savefig('output/figures/figure_5_2.png')
plt.close()

avg_log_rev = (
    df.groupby(['date', 'search_stays_on'])['log_revenue']
      .mean()
      .reset_index()
)

pivot_log = avg_log_rev.pivot(
    index='date',
    columns='search_stays_on',
    values='log_revenue'
)

pivot_log['log_diff'] = pivot_log[1] - pivot_log[0]

plt.figure()
plt.plot(pivot_log.index, pivot_log['log_diff'])

plt.axvline(pd.to_datetime('2012-05-22'), linestyle='--')
plt.xlabel('Date')
plt.ylabel('log(rev_control) - log(rev_treat)')
plt.title('Log Revenue Difference Over Time')

plt.tight_layout()
plt.savefig('output/figures/figure_5_3.png')
plt.close()
