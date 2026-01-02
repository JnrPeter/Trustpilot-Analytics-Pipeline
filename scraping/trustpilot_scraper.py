"""
Trustpilot Appliance Store Scraper - Production v2.0
Scrapes companies with 1000+ reviews, 500 reviews each
Fixed selectors - Last verified: December 2025


Project: Trustpilot Analytics Pipeline
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from datetime import datetime
import os
import random
import re
import json

class TrustpilotApplianceScraper:
    """Production scraper with comprehensive field extraction and fixed selectors"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive'
        })
        
        if not os.path.exists("Trustpilot_data"):
            os.makedirs("Trustpilot_data")
    
    def detect_topic_tags(self, title, text):
        """Detect topic mentions in review content"""
        combined = f"{title} {text}".lower()
        
        patterns = {
            'delivery': ['deliver', 'shipping', 'ship', 'arrived', 'transit', 'fedex', 'ups', 'usps', 'fast', 'slow', 'late', 'on time'],
            'price': ['price', 'cost', 'expensive', 'cheap', 'value', 'deal', 'money', 'affordable', 'worth', 'overpriced', 'budget'],
            'service': ['service', 'support', 'help', 'assist', 'representative', 'customer service', 'helpful', 'responsive'],
            'product': ['product', 'item', 'quality', 'condition', 'broken', 'defective', 'working', 'perfect', 'damaged', 'excellent'],
            'staff': ['staff', 'employee', 'manager', 'associate', 'friendly', 'rude', 'polite', 'professional', 'knowledgeable'],
            'order': ['order', 'purchase', 'buy', 'bought', 'ordered', 'shopping', 'checkout', 'transaction'],
            'location': ['store', 'location', 'branch', 'visit', 'pickup', 'pick up', 'warehouse', 'showroom', 'in-store'],
            'refund': ['refund', 'return', 'exchange', 'money back', 'replacement', 'warranty', 'cancel']
        }
        
        detected = []
        flags = {}
        for topic, keywords in patterns.items():
            has_topic = any(kw in combined for kw in keywords)
            flags[f'mentions_{topic}'] = has_topic
            if has_topic:
                detected.append(topic)
        
        return ', '.join(detected) if detected else 'general', flags
    
    def get_appliance_companies(self, min_reviews=1000):
        """
        Discover appliance companies with minimum review threshold.
        Uses fixed selectors for 2024 Trustpilot layout.
        """
        companies = []
        
        urls = [
            "https://www.trustpilot.com/categories/appliance_store?sort=reviews_count",
            "https://www.trustpilot.com/categories/appliance_store?page=2&sort=reviews_count",
            "https://www.trustpilot.com/categories/appliance_store?page=3&sort=reviews_count"
        ]
        
        for url in urls:
            print(f"Scanning: {url}")
            try:
                response = self.session.get(url, timeout=15)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Fixed: Correct card selector for 2024
                company_cards = soup.select('div.styles_card__WMwue')
                print(f"Found {len(company_cards)} company cards")
                
                for card in company_cards:
                    try:
                        # Fixed: Get main content div
                        main_div = card.select_one('div.styles_businessUnitMain__wRgqU')
                        if not main_div:
                            continue
                        
                        # Company name has class containing "heading-s"
                        name_el = main_div.select_one('p[class*="heading-s"]')
                        company_name = name_el.get_text(strip=True) if name_el else None
                        
                        # Domain has class "styles_websiteUrlDisplayed"
                        domain_el = main_div.select_one('p[class*="websiteUrlDisplayed"]')
                        domain = domain_el.get_text(strip=True) if domain_el else None
                        
                        # Skip if no company name found
                        if not company_name:
                            continue
                        
                        # Get rating from rating div
                        rating_div = card.select_one('div.styles_rating__lOWGj')
                        rating = None
                        if rating_div:
                            rating_span = rating_div.select_one('span')
                            rating = rating_span.get_text(strip=True) if rating_span else None
                        
                        # Get review count - account for rating prefix
                        # Page format is "4.216,726 reviews" where 4.2 is rating and 16,726 is review count
                        review_count = 0
                        rating_text_el = main_div.select_one('p[class*="ratingText"]')
                        if rating_text_el:
                            text = rating_text_el.get_text(strip=True)
                            # Pattern: skip rating (X.X) and capture actual review count
                            match = re.search(r'\d\.\d([\d,]+)\s*reviews', text)
                            if match:
                                review_count = int(match.group(1).replace(',', ''))
                        else:
                            # Fallback: look in spans
                            for span in card.select('span'):
                                if 'reviews' in span.get_text().lower():
                                    text = span.get_text()
                                    match = re.search(r'\d\.\d([\d,]+)', text)
                                    if match:
                                        review_count = int(match.group(1).replace(',', ''))
                                    break
                        
                        # Filter by minimum reviews
                        if review_count < min_reviews:
                            continue
                        
                        # Get URL
                        link = card.select_one('a[href*="/review/"]')
                        if not link:
                            continue
                        
                        company_url = f"https://www.trustpilot.com{link['href']}"
                        
                        # Get location
                        loc_div = card.select_one('div.styles_businessLocation__PIJjr')
                        location = loc_div.get_text(strip=True) if loc_div else 'Unknown'
                        
                        companies.append({
                            'company_name': company_name,
                            'domain': domain,
                            'rating': rating,
                            'review_count': review_count,
                            'location': location,
                            'company_url': company_url
                        })
                        
                        print(f"Found: {company_name} | {review_count:,} reviews")
                        
                    except Exception as e:
                        continue
                
                time.sleep(random.uniform(2, 4))
                
            except Exception as e:
                print(f"Error: {e}")
        
        # Remove duplicates
        seen = set()
        unique = []
        for c in companies:
            key = c['company_name'].lower()
            if key not in seen:
                seen.add(key)
                unique.append(c)
        
        print(f"\nDiscovered {len(unique)} companies with {min_reviews}+ reviews")
        return unique
    
    def scrape_company_profile(self, company_url, company_name):
        """Scrape comprehensive company profile - 17 fields"""
        print(f"Scraping profile: {company_name}")
        
        profile = {
            'company_name': company_name,
            'trustpilot_url': company_url,
            'scraped_at': datetime.now().isoformat()
        }
        
        try:
            response = self.session.get(company_url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            page_text = soup.get_text()
            
            # Rating extraction - multiple methods for reliability
            profile['overall_rating'] = None
            
            # Method A: Regex on raw JSON-LD (most reliable)
            for script in soup.select('script[type="application/ld+json"]'):
                if script.string:
                    match = re.search(r'"ratingValue"\s*:\s*"?(\d\.?\d?)"?', script.string)
                    if match:
                        profile['overall_rating'] = float(match.group(1))
                        break
            
            # Method B: Deep parse JSON-LD
            if not profile['overall_rating']:
                for script in soup.select('script[type="application/ld+json"]'):
                    try:
                        data = json.loads(script.string)
                        def find_rating(obj):
                            if isinstance(obj, dict):
                                if 'ratingValue' in obj:
                                    return obj['ratingValue']
                                for v in obj.values():
                                    r = find_rating(v)
                                    if r: return r
                            elif isinstance(obj, list):
                                for i in obj:
                                    r = find_rating(i)
                                    if r: return r
                            return None
                        found = find_rating(data)
                        if found:
                            profile['overall_rating'] = float(found)
                            break
                    except:
                        pass
            
            # Method C: Page text fallback
            if not profile['overall_rating']:
                match = re.search(r'Reviews\s+[\d,]+\s*[•·]\s*(\d\.\d)', page_text)
                if match:
                    profile['overall_rating'] = float(match.group(1))
            
            # Extract other profile fields
            trust = re.search(r'(Excellent|Great|Good|Average|Poor|Bad)\s*\n?\s*[\d,]+K?\s+reviews', page_text, re.I)
            profile['trust_category'] = trust.group(1) if trust else 'Unknown'
            
            reviews = re.search(r'Reviews\s+([\d,]+)', page_text)
            profile['total_reviews'] = int(reviews.group(1).replace(',', '')) if reviews else 0
            
            profile['claimed_profile'] = 'Claimed profile' in page_text
            
            loc = re.search(r'(\d+)\s+Locations?', page_text, re.I)
            profile['num_locations'] = int(loc.group(1)) if loc else 1
            
            # Business type
            profile['business_type'] = 'Unknown'
            for link in soup.select('a[href*="/categories/"]'):
                txt = link.get_text(strip=True)
                if 'Store' in txt or 'Shop' in txt:
                    profile['business_type'] = txt
                    break
            
            # Website URL
            profile['website_url'] = None
            for link in soup.select('a'):
                if 'Visit website' in link.get_text():
                    href = link.get('href', '')
                    if 'utm_source=trustpilot' in href or 'trustpilot.com' not in href:
                        profile['website_url'] = href
                        break
            
            # Response metrics
            resp = re.search(r'Replied to\s+(\d+%)', page_text, re.I)
            profile['negative_response_rate'] = resp.group(1) if resp else 'Unknown'
            
            time_match = re.search(r'Typically replies within\s+(\d+\s*\w+)', page_text, re.I)
            profile['response_time'] = time_match.group(1) if time_match else 'Unknown'
            
            profile['verified_company'] = 'Verified company' in page_text
            
            # Contact information
            phone = re.search(r'(\d{3}[-.\s]?\d{3}[-.\s]?\d{4})', page_text)
            profile['phone'] = phone.group(1) if phone else None
            
            email = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', page_text)
            profile['email'] = email.group(1) if email else None
            
            # Address
            addr = re.search(r'(\d+[^,\n]+,\s*\d{5},?\s*[^,\n]+,\s*United States)', page_text)
            if not addr:
                addr = re.search(r'(\d+[^,\n]+,\s*[^,\n]+,\s*United States)', page_text)
            profile['address'] = addr.group(1) if addr else None
            
            # Founded year
            founded = re.search(r'[Ff]ounded\s+(?:in\s+)?(\d{4})', page_text)
            profile['founded_year'] = int(founded.group(1)) if founded else None
            
            # Active subscription
            profile['has_active_subscription'] = 'Active Trustpilot subscription' in page_text
            
            # Company description
            about = re.search(r'About\s+' + re.escape(company_name) + r'[\s\S]*?Written by the company\s*([\s\S]*?)(?=Contact info|Categories|\n\n\n)', page_text, re.I)
            profile['company_description'] = about.group(1).strip()[:500] if about else None
            
            print(f"Profile extracted: {profile['overall_rating']} stars | {profile['trust_category']} | {profile['num_locations']} locations")
            
        except Exception as e:
            print(f"Error extracting profile: {e}")
            # Set default values for failed extraction
            profile.update({
                'overall_rating': None, 'trust_category': 'Unknown', 'total_reviews': 0,
                'claimed_profile': False, 'num_locations': 1, 'business_type': 'Unknown',
                'website_url': None, 'negative_response_rate': 'Unknown', 'response_time': 'Unknown',
                'verified_company': False, 'phone': None, 'email': None,
                'address': None, 'founded_year': None,
                'has_active_subscription': False, 'company_description': None
            })
        
        return profile
    
    def scrape_company_reviews(self, company_url, company_name, target_reviews=500):
        """Scrape reviews with topic detection - 21 fields"""
        reviews_data = []
        page = 1
        max_pages = 100  # 500 reviews / ~20 per page
        
        print(f"Scraping {target_reviews} reviews...")
        
        while len(reviews_data) < target_reviews and page <= max_pages:
            try:
                response = self.session.get(f"{company_url}?page={page}", timeout=15)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                
                containers = soup.select('article[data-service-review-card-paper]')
                if not containers:
                    break
                
                page_count = 0
                for container in containers:
                    if len(reviews_data) >= target_reviews:
                        break
                    try:
                        # Reviewer name
                        name_el = container.select_one('span[data-consumer-name-typography]')
                        name = name_el.get_text(strip=True) if name_el else "Anonymous"
                        
                        # Rating
                        rating_el = container.select_one('img[alt*="star"]')
                        rating = rating_el.get('alt', 'No rating') if rating_el else "No rating"
                        
                        # Review text
                        text_el = container.select_one('p')
                        review_text = text_el.get_text(strip=True) if text_el else ""
                        
                        # Date
                        date_el = container.select_one('time')
                        review_date = date_el.get('datetime', 'Unknown') if date_el else "Unknown"
                        
                        # Title
                        title_el = container.select_one('h2')
                        review_title = title_el.get_text(strip=True) if title_el else "No title"
                        
                        # Verified
                        verified = bool(container.select_one('[data-service-review-verified-review]'))
                        
                        # Location
                        loc_el = container.select_one('span[data-consumer-country-typography]')
                        location = loc_el.get_text(strip=True) if loc_el else "Unknown"
                        
                        # Company reply
                        card_text = container.get_text()
                        has_reply = 'Company replied' in card_text or 'Reply from' in card_text
                        
                        # Topic detection
                        topic_tags, topic_flags = self.detect_topic_tags(review_title, review_text)
                        
                        reviews_data.append({
                            'company_name': company_name,
                            'reviewer_name': name,
                            'reviewer_location': location,
                            'rating': rating,
                            'review_date': review_date,
                            'review_title': review_title,
                            'review_text': review_text,
                            'review_length': len(review_text),
                            'verified_review': verified,
                            'has_company_reply': has_reply,
                            'topic_tags': topic_tags,
                            **topic_flags,
                            'page_number': page,
                            'scraped_at': datetime.now().isoformat()
                        })
                        page_count += 1
                        
                    except:
                        continue
                
                if page % 10 == 0:
                    print(f"Page {page}: {len(reviews_data)} reviews collected")
                
                if page_count == 0:
                    break
                
                time.sleep(random.uniform(1, 2))
                page += 1
                
            except Exception as e:
                print(f"Page {page} error: {e}")
                break
        
        print(f"Collected {len(reviews_data)} reviews")
        return reviews_data
    
    def save_datasets(self, all_profiles, all_reviews):
        """Save profiles and reviews to CSV"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        profiles_file = None
        if all_profiles:
            profiles_file = f"Trustpilot_data/company_profiles_{timestamp}.csv"
            pd.DataFrame(all_profiles).to_csv(profiles_file, index=False)
            print(f"Profiles saved: {profiles_file}")
        
        reviews_file = None
        if all_reviews:
            reviews_file = f"Trustpilot_data/reviews_{timestamp}.csv"
            pd.DataFrame(all_reviews).to_csv(reviews_file, index=False)
            print(f"Reviews saved: {reviews_file}")
        
        return profiles_file, reviews_file
    
    def run_full_scrape(self, min_reviews=1000, reviews_per_company=500):
        """Execute complete scraping pipeline"""
        print("=" * 70)
        print("TRUSTPILOT APPLIANCE SCRAPER v2.0")
        print("=" * 70)
        print(f"Configuration: Companies with {min_reviews}+ reviews, {reviews_per_company} reviews each")
        print()
        
        # Step 1: Discover companies
        print("STEP 1: Discovering companies")
        print("-" * 50)
        companies = self.get_appliance_companies(min_reviews=min_reviews)
        
        if not companies:
            print("No companies found!")
            return None, None
        
        # Step 2: Scrape profiles and reviews
        print("\nSTEP 2: Scraping profiles & reviews")
        print("-" * 50)
        
        all_profiles = []
        all_reviews = []
        
        for i, company in enumerate(companies, 1):
            print(f"\n[{i}/{len(companies)}] {company['company_name']} ({company['review_count']:,} reviews)")
            
            # Scrape profile
            profile = self.scrape_company_profile(company['company_url'], company['company_name'])
            all_profiles.append(profile)
            
            # Scrape reviews
            reviews = self.scrape_company_reviews(
                company['company_url'], 
                company['company_name'], 
                target_reviews=reviews_per_company
            )
            all_reviews.extend(reviews)
            
            # Rest between companies
            if i < len(companies):
                print("Resting 10 seconds...")
                time.sleep(10)
        
        # Step 3: Save
        print("\nSTEP 3: Saving datasets")
        print("-" * 50)
        profiles_file, reviews_file = self.save_datasets(all_profiles, all_reviews)
        
        # Summary
        print("\n" + "=" * 70)
        print("SCRAPING COMPLETE")
        print("=" * 70)
        print(f"Companies: {len(all_profiles)}")
        print(f"Reviews: {len(all_reviews):,}")
        print(f"Profiles file: {profiles_file}")
        print(f"Reviews file: {reviews_file}")
        
        # Topic analysis
        if all_reviews:
            df = pd.DataFrame(all_reviews)
            print("\nTOPIC DISTRIBUTION:")
            for col in ['mentions_delivery', 'mentions_price', 'mentions_service', 'mentions_product',
                       'mentions_staff', 'mentions_order', 'mentions_location', 'mentions_refund']:
                if col in df.columns:
                    pct = (df[col].sum() / len(df)) * 100
                    print(f"   {col.replace('mentions_', '').title():12} {pct:.1f}%")
            
            if 'has_company_reply' in df.columns:
                reply_pct = (df['has_company_reply'].sum() / len(df)) * 100
                print(f"\nCompany Reply Rate: {reply_pct:.1f}%")
        
        print("\nDatasets ready for dbt transformation!")
        return profiles_file, reviews_file


if __name__ == "__main__":
    scraper = TrustpilotApplianceScraper()
    
    profiles_file, reviews_file = scraper.run_full_scrape(
        min_reviews=1000,        # Only companies with 1000+ reviews
        reviews_per_company=500  # Scrape 500 reviews per company
    )
    
    if profiles_file and reviews_file:
        print("\n" + "=" * 70)
        print("SUCCESS!")
        print(f"Profiles: {profiles_file}")
        print(f"Reviews: {reviews_file}")
        print("=" * 70)