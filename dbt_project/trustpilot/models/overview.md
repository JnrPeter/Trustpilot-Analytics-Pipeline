{% docs __overview__ %}
# Welcome to the Trustpilot Analytics Pipeline Documentation

This documentation site contains comprehensive information about our Trustpilot review analytics pipeline built with dbt. Our project transforms raw web-scraped review data into analytics-ready datasets for customer sentiment analysis and business intelligence.

## Navigation Guide

### Sources Section
**Click on "trustpilot"** to view our raw data sources from Snowflake that feed the pipeline.

### Exposures Section  
**Click on "Dashboard"** to see how our transformed data connects to the Power BI dashboard for business intelligence.

### Projects Section
This shows the dbt packages and dependencies used in the project:
- **trustpilot** - Our main analytics pipeline project
- **dbt_date, dbt_expectations, dbt_utils** - External dbt packages for enhanced functionality

### Project Tab (Main Navigation)
**Click on the "trustpilot" folder to expand and view all models** organized by our two-layer architecture:
- `staging/` - Data cleaning, deduplication, and standardization
- `marts/` - Business-ready analytical datasets with derived metrics
- `seeds/` - Reference data for geographic and categorical mapping

### Database Tab
Browse the actual Snowflake database structure showing how our models materialize in the `TRUSTPILOT_REVIEWS.DEV` schema.

### Graph Exploration
Click the blue graph icon (bottom-right) to visualize data lineage and model dependencies. This shows how raw Trustpilot data flows through staging transformations to final analytical models.

## Project Overview

Our Trustpilot analytics pipeline processes:
- **Company profiles**: Business details, ratings, response metrics, and operational data
- **Customer reviews**: Review content, sentiment analysis, and topic classification
- **Geographic data**: Customer location insights across 61 countries
- **Topic intelligence**: Automated detection of review themes (delivery, price, service, etc.)

## Business Impact

**25 appliance companies analyzed** • **4,500+ reviews processed** • **76% positive sentiment discovered**

Key insights delivered:
- Review complexity correlates with lower customer satisfaction
- Geographic concentration reveals market expansion opportunities
- Response strategy gaps identified in customer service approach

## Data Architecture

### 📥 **Staging Layer (`staging/`)**
Clean and standardize raw Trustpilot data with deduplication and validation
- `stg_profile` - Company profiles with calculated response metrics
- `stg_reviews` - Deduplicated reviews with topic detection

### 🎯 **Mart Layer (`marts/`)**
Analytics-ready datasets optimized for business intelligence
- `dim_company_profile` - Company dimension with business tiers and flags
- `fct_reviews` - Review facts with sentiment analysis and geographic mapping

### 🌱 **Seeds (`seeds/`)**
Reference data for enhanced analysis
- `country_codes` - ISO country code mappings for geographic insights

## Key Business Metrics Enabled

Our pipeline enables analysis of:
- 📊 **Sentiment Analysis**: Customer satisfaction patterns across companies
- 🏷️ **Topic Intelligence**: Review themes and complexity analysis  
- 🌍 **Geographic Insights**: Customer distribution and market opportunities
- 📞 **Response Analytics**: Company engagement strategies and effectiveness
- ⭐ **Rating Analysis**: Performance tiers and satisfaction drivers

## Data Quality & Testing

**18 automated tests** ensure data integrity:
- Schema validation and constraint enforcement
- Business rule validation for rating tiers and sentiment classification
- Deduplication verification (5,794 duplicates handled)
- Referential integrity between companies and reviews

## Technical Highlights

- **Modern dbt patterns**: Staging → Marts architecture
- **Surrogate key management**: Consistent relationship modeling
- **Geographic enrichment**: Country code standardization
- **Comprehensive testing**: Schema, business logic, and custom validation

---

*Built using dbt, Snowflake, and modern analytics engineering practices*

**Contact**: Peter Enning Junior - Data Analyst  
**Project**: [Trustpilot Analytics Pipeline](https://github.com/JnrPeter/Trustpilot-Analytics-Pipeline)
{% enddocs %}
