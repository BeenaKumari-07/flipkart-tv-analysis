import os
import re
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import seaborn as sns
from bs4 import BeautifulSoup

# =====================================================================
# PHASE 1: WEB SCRAPING PIPELINE
# =====================================================================
print("🚀 Phase 1: Initiating Flipkart Web Scraper...")

brand, screen_size, resolution, tv_type = [], [], [], []
year, ratings, price, warranty = [], [], [], []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

# Scraping pages 1 to 43 safely
for page in range(1, 44):
    url = f"https://flipkart.com{page}"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"⚠️ Skipping page {page}: Status {response.status_code}")
            continue
    except Exception as e:
        print(f"❌ Connection error on page {page}: {e}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.find_all("div", class_=["ZFwe0M", "row", "_75nlfW"])
    if not products:
        products = soup.select("div[data-id]")

    for prod in products:
        # Extract Product Name & derive technical fields
        title_tag = prod.find("div", class_=["RG5Slk", "KzDlHZ", "w1YILc"])
        if title_tag:
            name_text = title_tag.text.strip()
            brand.append(name_text.split()[0] if name_text.split() else "NA")
            
            size_match = re.search(r"(\d+)\s*cm", name_text)
            screen_size.append(int(size_match.group(1)) if size_match else "NA")

            if any(x in name_text for x in ["4K", "Ultra HD", "UHD"]):
                resolution.append("4K Ultra HD")
            elif "Full HD" in name_text:
                resolution.append("Full HD")
            elif "HD Ready" in name_text:
                resolution.append("HD Ready")
            else:
                resolution.append("NA")

            if "QLED" in name_text:
                tv_type.append("QLED")
            elif "OLED" in name_text:
                tv_type.append("OLED")
            elif "LED" in name_text:
                tv_type.append("LED")
            else:
                tv_type.append("NA")

            year_match = re.search(r"(20\d{2})", name_text)
            year.append(year_match.group(1) if year_match else "NA")
        else:
            for list_obj in [brand, screen_size, resolution, tv_type, year]:
                list_obj.append("NA")

        # Extract Star Ratings
        star_div = prod.find("div", class_=["MKiFS6", "XQDwOf", "XqR6sj"])
        ratings.append(float(star_div.text.strip()) if star_div and star_div.text else "NA")

        # Extract Price
        price_tag = prod.find("div", class_=["hZ3P6w", "Nx96nJ", "Cg31wA"])
        if price_tag and price_tag.text:
            clean_p = re.sub(r"[^\d]", "", price_tag.text)
            price.append(int(clean_p) if clean_p else "NA")
        else:
            price.append("NA")

        # Extract Warranty Info
        warranty_tag = prod.find(lambda t: t.name in ["div", "li"] and "warranty" in t.text.lower())
        if warranty_tag:
            w_match = re.search(r"(\d+)\s*(year|years|yr|yrs|month|months)", warranty_tag.text, re.IGNORECASE)
            warranty.append(w_match.group(0) if w_match else "NA")
        else:
            warranty.append("NA")

    time.sleep(1)  # Polite scraping interval

# Build Initial DataFrame
df = pd.DataFrame({
    "Brand": brand, "Screen_Size_cm": screen_size, "Resolution": resolution,
    "TV_Type": tv_type, "Launch_Year": year, "Rating": ratings,
    "Price": price, "Warranty": warranty
})

# Clean string inconsistencies from brand names
df["Brand"] = df["Brand"].astype(str).str.replace(r"[\[\]']", "", regex=True)

# Save raw dataset backup
os.makedirs("data", exist_ok=True)
df.to_csv("data/raw_scraped_televisions.csv", index=False)
print(f"📦 Scraping Complete! Initial Rows Found: {len(df)}")

# =====================================================================
# PHASE 2: MODERN DATA CLEANING & IMPUTATION
# =====================================================================
print("\n🧹 Phase 2: Processing Missing Data & Enforcing Types...")

cols = ["Launch_Year", "Screen_Size_cm", "Rating", "Warranty", "Resolution", "TV_Type", "Price"]
df[cols] = df[cols].astype(str).apply(lambda x: x.str.strip()).replace(["NA", "na", "", " ", "None", "nan"], np.nan)

# Enforce clean datatypes securely
df["Screen_Size_cm"] = pd.to_numeric(df["Screen_Size_cm"], errors="coerce")
df["Launch_Year"] = pd.to_numeric(df["Launch_Year"], errors="coerce")
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

# Impute missing records safely
df["Screen_Size_cm"] = df["Screen_Size_cm"].fillna(df["Screen_Size_cm"].median())
df["Resolution"] = df["Resolution"].fillna(df["Resolution"].mode()[0] if not df["Resolution"].mode().empty else "4K Ultra HD")
df["TV_Type"] = df["TV_Type"].fillna(df["TV_Type"].mode()[0] if not df["TV_Type"].mode().empty else "LED")
df["Launch_Year"] = df["Launch_Year"].fillna(df["Launch_Year"].mode()[0] if not df["Launch_Year"].mode().empty else 2025)
df["Rating"] = df["Rating"].fillna(df["Rating"].mean())
df["Warranty"] = df["Warranty"].fillna(df["Warranty"].mode()[0] if not df["Warranty"].mode().empty else "1 Year")
df["Price"] = df["Price"].fillna(df["Price"].median())

# Handle duplicates securely
df = df.drop_duplicates()
df.to_csv("data/cleaned_televisions.csv", index=False)
print(f"✅ Cleaned Dataset Saved! Active Deduplicated Rows: {len(df)}")

# =====================================================================
# PHASE 3: EXPLORATORY DATA ANALYSIS (EDA)
# =====================================================================
print("\n📊 Phase 3: Executing Statistical and Graphical Profiling...")

# 1. Continuous Distribution Subplots
num_cols = df.select_dtypes(include=[np.number]).columns.values
for col in num_cols:
    fig, ax = plt.subplots(2, 2, figsize=(10, 7))
    ax[0, 0].hist(df[col].dropna(), bins=20, color="skyblue", edgecolor="black")
    ax[0, 0].set_title(f"Histogram of {col}")
    
    sns.kdeplot(data=df, x=col, ax=ax[0, 1], fill=True, color="teal")
    ax[0, 1].set_title(f"Density Plot of {col}")
    
    ax[1, 0].boxplot(df[col].dropna(), patch_artist=True, boxprops=dict(facecolor="lightgreen"))
    ax[1, 0].set_title(f"Boxplot of {col}")
    
    sns.scatterplot(data=df, x=df.index, y=col, ax=ax[1, 1], color="coral", alpha=0.5)
    ax[1, 1].set_title(f"Index Scatter Matrix of {col}")
    
    plt.suptitle(f"Continuous Univariate Profile: {col}", weight="bold")
    plt.tight_layout()
    plt.show()

# 2. Categorical Market Share Breakdown
cat_cols = df.select_dtypes(include=["object", "category"]).columns.values
for col in cat_cols:
    clean_series = df[col].dropna()
    vc = clean_series.value_counts()
    if vc.empty: continue
    
    top_limit = min(5, len(vc))
    top_n = vc.head(top_limit)
    
    # Secure Pie chart market calculations
    pie_data = pd.concat([top_n, pd.Series([vc.iloc[top_limit:].sum()], index=["Others"])]) if len(vc) > top_limit else top_n

    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    ax[0].barh(top_n.index[::-1], top_n.values[::-1], color="royalblue", edgecolor="black")
    ax[0].set_title(f"Top {top_limit} Dominant Values")
    ax[0].set_xlabel("Frequency Count")
    
    ax[1].pie(pie_data, labels=pie_data.index, autopct="%1.1f%%", startangle=140, colors=sns.color_palette("pastel"))
    ax[1].set_title("True Market Allocation")
    
    plt.suptitle(f"Categorical Profile: {col}", weight="bold", fontsize=14)
    plt.tight_layout()
    plt.show()

# =====================================================================
# PHASE 4: MULTIVARIATE CORRELATION INTERACTION
# =====================================================================
print("\n📈 Phase 4: Constructing Multivariate Matrix Analysis...")

# Clean Multivariate Matrix Pairplot
sns.pairplot(data=df.dropna(subset=["Price", "Rating"]), vars=["Price", "Rating", "Screen_Size_cm"], hue="TV_Type", palette="Dark2", diag_kind="kde")
plt.suptitle("Multivariate Feature Grid Breakdown", y=1.02, weight="bold")
plt.show()

# Precise white-lined structural Heatmap
plt.figure(figsize=(6, 4))
sns.heatmap(df[["Price", "Rating", "Screen_Size_cm"]].corr(), annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, linewidths=1, linecolor="white", square=True)
plt.title("System Feature Correlation Matrix Map", weight="bold", pad=12)
plt.tight_layout()
plt.show()

print("\n🎯 Complete pipeline executed seamlessly without warning traps!")
