import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
#IMPORT DATASET
df1=pd.read_csv("socialm_analysis\\social_media_data.csv")
df2=pd.read_csv("socialm_analysis\\social_media_engagement1.csv")
print('The given dataset has the following info:',df1.info())
print('The first few rows of the dataset are: \n ',df1.head())
print('The given dataset has the following info:',df2.info())
print('The first few rows of the dataset are: \n ',df2.head())
# ==========================
# 2. CLEAN DF1
# ==========================
# Drop rows with missing essential columns
df1 = df1.dropna(subset=["platform", "day_of_week", "time_of_post", "content_type", "likes", "comments", "followers_count"])

# Convert time_of_post to datetime (extract hour for time analysis)
df1["time_of_post"] = pd.to_datetime(df1["time_of_post"], errors='coerce')
df1["post_hour"] = df1["time_of_post"].dt.hour

# Calculate Engagement Rate (if not already)
if "engagement_rate" not in df1.columns or df1["engagement_rate"].isnull().all():
    df1["engagement_rate"] = (
        (df1["likes"] + df1["comments"] + df1.get("shares", 0) + df1.get("saves", 0))
        / df1["followers_count"]
    ) * 100

# ==========================
# 3. CLEAN DF2
# ==========================
df2 = df2.dropna(subset=["platform", "post_time", "post_type", "likes", "comments"])
df2["post_time"] = pd.to_datetime(df2["post_time"], errors='coerce')
df2["post_hour"] = df2["post_time"].dt.hour
df2["post_day"] = df2["post_time"].dt.day_name()

# ==========================
# 4. BEST DAY (DF1 only)
# ==========================
print("=== BEST DAY FOR POSTING (DF1) ===")
best_day_per_platform = df1.groupby("platform")["engagement_rate"].mean().sort_values(ascending=False)
print("\nOverall best day (by engagement rate):", df1.groupby("day_of_week")["engagement_rate"].mean().idxmax())
print("\nBest day per platform:")
print(df1.groupby(["platform", "day_of_week"])["engagement_rate"].mean().reset_index()
      .sort_values(["platform", "engagement_rate"], ascending=[True, False]))

# ==========================
# 5. BEST TIME (DF1 & DF2)
# ==========================
def best_time(df, df_name):
    print(f"\n=== BEST TIME FOR POSTING ({df_name}) ===")
    print("Overall best posting hour:", df.groupby("post_hour")["likes"].mean().idxmax())
    print("\nBest posting hour per platform:")
    print(df.groupby("platform")["post_hour"].agg(lambda x: x.mode()[0]))

best_time(df1, "DF1")
best_time(df2, "DF2")

# ==========================
# 6. BEST POST TYPE (DF1 & DF2)
# ==========================
def best_post_type(df, type_col, df_name):
    print(f"\n=== BEST POST TYPE ({df_name}) ===")
    print("Overall best post type:", df.groupby(type_col)["likes"].mean().idxmax())
    print("\nBest post type per platform:")
    print(df.groupby("platform")[type_col].agg(lambda x: x.mode()[0]))

best_post_type(df1, "content_type", "DF1")
best_post_type(df2, "post_type", "DF2")

# ==========================
# 7. ENGAGEMENT RATE SUMMARY (DF1)
# ==========================
print("\n=== ENGAGEMENT RATE SUMMARY (DF1) ===")
print("Average Engagement Rate Overall:", df1["engagement_rate"].mean())
print("\nAverage Engagement Rate Per Platform:")
print(df1.groupby("platform")["engagement_rate"].mean())

# ==========================
# Save Insights as CSV/Excel
# ==========================

# Best Day per Platform (DF1)
best_day_df = df1.groupby(["platform", "day_of_week"])["engagement_rate"].mean().reset_index()
best_day_df.to_csv("socialm_analysis/best_day_per_platform.csv", index=False)

# Overall Best Day (DF1)
overall_best_day = df1.groupby("day_of_week")["engagement_rate"].mean().reset_index()
overall_best_day.to_csv("socialm_analysis/overall_best_day.csv", index=False)

# Best Time per Platform (DF1)
best_time_df = df1.groupby(["platform", "post_hour"])["likes"].mean().reset_index()
best_time_df.to_csv("socialm_analysis/best_time_per_platform.csv", index=False)

# Best Post Type per Platform (DF1)
best_post_type_df = df1.groupby(["platform", "content_type"])["likes"].mean().reset_index()
best_post_type_df.to_csv("socialm_analysis/best_post_type_per_platform.csv", index=False)

# Engagement Rate Summary (DF1)
engagement_summary_df = df1.groupby("platform")["engagement_rate"].mean().reset_index()
engagement_summary_df.to_csv("socialm_analysis/engagement_rate_summary.csv", index=False)

# Also save everything to a single Excel file with multiple sheets
with pd.ExcelWriter("socialm_analysis/social_media_insights.xlsx") as writer:
    best_day_df.to_excel(writer, sheet_name="Best Day Per Platform", index=False)
    overall_best_day.to_excel(writer, sheet_name="Overall Best Day", index=False)
    best_time_df.to_excel(writer, sheet_name="Best Time Per Platform", index=False)
    best_post_type_df.to_excel(writer, sheet_name="Best Post Type Per Platform", index=False)
    engagement_summary_df.to_excel(writer, sheet_name="Engagement Rate Summary", index=False)

print("✅ Insights saved to 'socialm_analysis/' folder as CSV and Excel.")
