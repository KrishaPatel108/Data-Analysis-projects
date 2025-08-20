import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Load dataset
ga4 = pd.read_csv("websiteandfunnelconversio/ga4_dummy_dataset.csv")

# --- 1. Traffic Source Breakdown ---
traffic_breakdown = ga4['traffic_source'].value_counts(normalize=True) * 100

plt.figure(figsize=(6,6))
plt.pie(traffic_breakdown, labels=traffic_breakdown.index, autopct='%1.1f%%', startangle=90)
plt.title("Traffic Source Breakdown (%)")
plt.show()
# --- 2. Bounce Rate per Page ---
bounce_rates = ga4.groupby("page")["bounce"].mean() * 100

plt.figure(figsize=(8,5))
sns.barplot(x=bounce_rates.index, y=bounce_rates.values, palette="Blues_d")
plt.title("Bounce Rate by Page (%)")
plt.ylabel("Bounce Rate (%)")
plt.xticks(rotation=45)
plt.show()
# --- 3. Exit Rate per Page ---
exit_rates = ga4.groupby("page")["exit_page"].mean() * 100

plt.figure(figsize=(8,5))
sns.barplot(x=exit_rates.index, y=exit_rates.values, palette="Oranges_d")
plt.title("Exit Rate by Page (%)")
plt.ylabel("Exit Rate (%)")
plt.xticks(rotation=45)
plt.show()
# --- 4. Conversion Funnel Analysis ---
# Define funnel order
funnel_stages = ["/", "/product", "/signup", "/checkout", "/thank-you"]


funnel_counts = [ga4.loc[ga4["page"] == stage, "user_id"].nunique() for stage in funnel_stages]
plt.figure(figsize=(8,5))
sns.lineplot(x=funnel_stages, y=funnel_counts, marker="o", linewidth=3)
plt.title("Conversion Funnel (Unique Users)")
plt.xlabel("Funnel Stages")
plt.ylabel("Users")
plt.grid(True)
plt.show()

# Count unique users at each stage
funnel_counts = {}
for stage in funnel_stages:
    funnel_counts[stage] = ga4.loc[ga4["page"] == stage, "user_id"].nunique()

# Calculate drop-off between stages
funnel_dropoffs = {}
stage_list = list(funnel_counts.keys())
for i in range(len(stage_list) - 1):
    start = funnel_counts[stage_list[i]]
    end = funnel_counts[stage_list[i+1]]
    drop_rate = ((start - end) / start * 100) if start > 0 else 0
    funnel_dropoffs[f"{stage_list[i]} → {stage_list[i+1]}"] = round(drop_rate, 2)

# --- 5. Overall Conversion Rate ---
conversion_rate = ga4["conversion"].mean() * 100

# --- Print Results ---
print("=== Traffic Source Breakdown (%) ===")
print(traffic_breakdown.round(2), "\n")

print("=== Bounce Rates by Page (%) ===")
print(bounce_rates.round(2), "\n")

print("=== Exit Rates by Page (%) ===")
print(exit_rates.round(2), "\n")

print("=== Funnel Stage User Counts ===")
print(funnel_counts, "\n")

print("=== Funnel Drop-off Rates (%) ===")
print(funnel_dropoffs, "\n")

print("=== Overall Conversion Rate (%) ===")
print(round(conversion_rate, 2))
