# Flipkart Television Web Scraping & Multivariate EDA Pipeline

A data science pipeline designed to dynamically extract product detail matrices from commercial web search queries, structure anomalies, perform missing data imputations, and synthesize multivariate interactions across television specifications, manufacturing pricing, and consumer evaluation ranks.

## 🚀 Key Functional Features
- **Dynamic Web Scraping**: Leverages `requests` and defensive multi-selector fallbacks via `BeautifulSoup` to map raw text pages safely.
- **Robust Cleaning**: Programmed to replace deprecated pipeline methods, handling nested configurations and text string noise automatically.
- **Univariate Distribution Profiling**: Extracts statistical features across numeric boundaries (Skewness, Kurtosis, Variance) paired with clean 4-quadrant layout visuals.
- **Multivariate Synthesis Matrix**: Utilizes categorical grouping overlays on top-tier continuous distributions to analyze how feature specifications drive pricing changes.

## 📦 Setting Up the Environment

1. **Clone the Repository to your computer:**
   ```bash
   git clone https://github.com
   cd flipkart-tv-analysis
   ```

2. **Install all required libraries at once:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the master script pipeline:**
   ```bash
   python scraper_and_analysis.py
   ```

## 📊 Core Data Insights & Analysis Summary

### 🔍 Display Specifications & Architecture
- **Market Dominance**: Standard LED screen builds remain the most common offering in the marketplace, followed closely by QLED display models. Ultra-premium OLED sets have very limited availability.
- **Resolution Trends**: 4K Ultra HD resolution has emerged as the baseline standard across almost all display varieties. HD Ready configurations occupy a secondary market tier, while traditional Full HD structures show low representation.

### 📐 Physical Layout & Consumer Metrics
- **Physical Footprint Constraints**: Physical builds cluster heavily around medium dimensions (specifically targeting the 80 cm to 140 cm range). Product frequency values scale down smoothly as sizes transition into premium high-end areas.
- **Consumer Ratings Stability**: Customer evaluation patterns cluster consistently between 4.0 and 4.3 stars, presenting a left-skewed shape. This shows a high level of overall buyer satisfaction across different product tiers.

### 💵 Manufacturing Cost & Price Drivers
- **Pricing Core**: The target marketplace focuses heavily on affordable products, with standard system listings concentrated heavily between ₹20,000 and ₹50,000.
- **Feature Interaction (Multivariate Map)**: System heatmaps demonstrate a weak positive correlation between price adjustments and consumer ratings. Premium pricing tiers do not guarantee a higher star score, proving that product evaluation is driven by features other than just high retail costs.
- **Standard Logistics**: A 1-year coverage plan remains the baseline system standard across different brands and display resolutions.
