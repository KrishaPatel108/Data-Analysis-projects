import pandas as pd
import mysql.connector
import random

# -----------------------------
# Step 1: MySQL DB Connection
# -----------------------------
db_config = {
    "host": "localhost",      # Change if remote
    "user": "root",           # Your MySQL username
    "password": "Krisha@SQL45",  # Your MySQL password
    "database": "competitor_analysis"  # Must exist beforehand
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# -----------------------------
# Step 2: Competitors
# -----------------------------
competitors = ["AgencyX", "BrandBoost", "ClickHive", "PixelPulse", "MarketMinds"]

# -----------------------------
# Step 3: Dummy Data Generation
# -----------------------------

# Top Keywords Data
keywords_data = []
sample_keywords = [
    ("social media strategy", 1200),
    ("seo optimization tips", 1500),
    ("digital marketing trends 2025", 800),
    ("content calendar ideas", 1100),
    ("instagram reels growth", 950),
    ("email marketing automation", 1300),
    ("ppc campaign strategy", 700)
]

for comp in competitors:
    for kw, vol in random.sample(sample_keywords, 4):  # pick 4 keywords
        keywords_data.append({
            "Competitor": comp,
            "Keyword": kw,
            "SearchVolume": vol + random.randint(-100, 100),
            "RankingPosition": random.randint(1, 20)
        })

df_keywords = pd.DataFrame(keywords_data)

# Traffic Sources Data
traffic_data = []
traffic_sources = ["Organic Search", "Paid Search", "Referral", "Social", "Direct"]

for comp in competitors:
    total_visits = random.randint(5000, 20000)
    distribution = [random.randint(10, 40) for _ in traffic_sources]
    dist_sum = sum(distribution)
    distribution = [round((d / dist_sum) * total_visits) for d in distribution]
    for src, visits in zip(traffic_sources, distribution):
        traffic_data.append({
            "Competitor": comp,
            "TrafficSource": src,
            "Visits": visits
        })

df_traffic = pd.DataFrame(traffic_data)

# Social Media Data
social_data = []
platforms = ["Instagram", "LinkedIn", "Twitter", "Facebook"]

for comp in competitors:
    for platform in platforms:
        social_data.append({
            "Competitor": comp,
            "Platform": platform,
            "PostsPerMonth": random.randint(4, 20),
            "AvgEngagementRate": round(random.uniform(0.5, 5.0), 2)  # in %
        })

df_social = pd.DataFrame(social_data)

# -----------------------------
# Step 4: Save to Excel
# -----------------------------
with pd.ExcelWriter("competitor_analysis_dummy.xlsx") as writer:
    df_keywords.to_excel(writer, sheet_name="TopKeywords", index=False)
    df_traffic.to_excel(writer, sheet_name="TrafficSources", index=False)
    df_social.to_excel(writer, sheet_name="SocialMedia", index=False)

print("Excel file 'competitor_analysis_dummy.xlsx' created successfully.")

# -----------------------------
# Step 5: Save to MySQL
# -----------------------------

# Create tables if not exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS TopKeywords (
    Competitor VARCHAR(255),
    Keyword VARCHAR(255),
    SearchVolume INT,
    RankingPosition INT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS TrafficSources (
    Competitor VARCHAR(255),
    TrafficSource VARCHAR(255),
    Visits INT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS SocialMedia (
    Competitor VARCHAR(255),
    Platform VARCHAR(255),
    PostsPerMonth INT,
    AvgEngagementRate FLOAT
)
""")

# Clear old data
cursor.execute("TRUNCATE TABLE TopKeywords")
cursor.execute("TRUNCATE TABLE TrafficSources")
cursor.execute("TRUNCATE TABLE SocialMedia")

# Insert new data
for _, row in df_keywords.iterrows():
    cursor.execute("""
        INSERT INTO TopKeywords (Competitor, Keyword, SearchVolume, RankingPosition)
        VALUES (%s, %s, %s, %s)
    """, tuple(row))

for _, row in df_traffic.iterrows():
    cursor.execute("""
        INSERT INTO TrafficSources (Competitor, TrafficSource, Visits)
        VALUES (%s, %s, %s)
    """, tuple(row))

for _, row in df_social.iterrows():
    cursor.execute("""
        INSERT INTO SocialMedia (Competitor, Platform, PostsPerMonth, AvgEngagementRate)
        VALUES (%s, %s, %s, %s)
    """, tuple(row))

conn.commit()
cursor.close()
conn.close()

print("Data successfully inserted into MySQL database.")
