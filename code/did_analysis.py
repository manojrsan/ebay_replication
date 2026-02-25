import pandas as pd
import numpy as np

treated_pivot = pd.read_csv("temp/treated_pivot.csv", index_col="dma")
untreated_pivot = pd.read_csv("temp/untreated_pivot.csv", index_col="dma")

r1 = treated_pivot["log_revenue_diff"]
r0 = untreated_pivot["log_revenue_diff"]

r1_bar = r1.mean()
r0_bar = r0.mean()

gamma_hat = r1_bar - r0_bar

n1 = len(r1)
n0 = len(r0)

se = np.sqrt(r1.var() / n1 + r0.var() / n0)

ci_lower = gamma_hat - 1.96 * se
ci_upper = gamma_hat + 1.96 * se

print("DID Results (Log Scale)")
print("=======================")
print(f"Gamma hat: {gamma_hat:.4f}")
print(f"Std Error: {se:.4f}")
print(f"95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")

latex = r"""\begin{table}[h]
\centering
\caption{Difference-in-Differences Estimate of the Effect of Paid Search on Revenue}
\begin{tabular}{lc}
\hline
& Log Scale \\
\hline
Point Estimate ($\hat{\gamma}$) & $%.4f$ \\
Standard Error & $%.4f$ \\
95\%% CI & $[%.4f, \; %.4f]$ \\
\hline
\end{tabular}
\label{tab:did}
\end{table}""" % (gamma_hat, se, ci_lower, ci_upper)

with open("output/tables/did_table.tex", "w") as f:
    f.write(latex)
