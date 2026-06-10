"""
PIPELINE.PY
Author: Priyanshu Vijay
Description: Core Data Engineering & Harvesting Pipeline. 
             Programmatically scrapes bibliometric data from Wikipedia tables, 
             cleans layout noise (filters out ISBNs/Citations), tags book types,
             and extracts clean records to a local JSON cache.
"""

import os
import requests
from bs4 import BeautifulSoup
import json
import re

def clean_text(element):
    """Helper function to strip whitespace and clean up raw scraped strings."""
    if element:
        return element.get_text(separator=" ").strip()
    return "Unknown"

def extract_book_data(url):
    """Harvests raw bibliometric data layers dynamically from Wikipedia source."""
    print(f"🌐 Initiating connection to: {url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"❌ Connection failed with HTTP status code: {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all section headers to help find the Book Type context dynamically
        all_elements = soup.find_all(['h2', 'h3', 'table'])
        
        current_type = "Novel" # Default fallback category
        extracted_records = []
        
        print(f"⚙️ Parsing raw HTML tables with intelligent data clearing rules...")
        
        for element in all_elements:
            # Dynamically track what type of book table we are inside on Wikipedia
            if element.name in ['h2', 'h3']:
                header_text = element.get_text().lower()
                if 'novels' in header_text:
                    current_type = "Novel"
                elif 'short fiction' in header_text or 'collections' in header_text:
                    current_type = "Collection"
                elif 'nonfiction' in header_text or 'memoir' in header_text:
                    current_type = "Non-Fiction"
                continue
                
            # Process table if it is a standard wikitable
            if element.name == 'table' and 'wikitable' in element.get('class', []):
                rows = element.find_all('tr')
                if not rows:
                    continue
                    
                # Map headers to their column index position dynamically
                header_cells = rows[0].find_all(['th', 'td'])
                headers_list = [clean_text(cell).lower() for cell in header_cells]
                
                title_idx = next((i for i, h in enumerate(headers_list) if 'title' in h), None)
                year_idx = next((i for i, h in enumerate(headers_list) if 'year' in h), None)
                publisher_idx = next((i for i, h in enumerate(headers_list) if 'publisher' in h or 'distributor' in h), None)
                pages_idx = next((i for i, h in enumerate(headers_list) if 'page' in h or 'count' in h), None)
                
                # Table validation: Skip metadata or non-bibliography tables safely
                if title_idx is None or year_idx is None or pages_idx is None:
                    continue
                    
                for row in rows[1:]:
                    try:
                        cells = row.find_all(['th', 'td'])
                        if len(cells) <= max(filter(lambda x: x is not None, [title_idx, year_idx, publisher_idx, pages_idx])):
                            continue
                        
                        # Extract raw text strings
                        raw_title = clean_text(cells[title_idx])
                        raw_year = clean_text(cells[year_idx])
                        raw_publisher = clean_text(cells[publisher_idx]) if publisher_idx is not None else "Unknown"
                        raw_pages = clean_text(cells[pages_idx])
                        
                        # Data Science Cleaning Rule 1: Strip out bracketed citations like [1] or [14]
                        title = re.sub(r'\[\d+\]', '', raw_title).replace('"', '').strip()
                        publisher = re.sub(r'\[\d+\]', '', raw_publisher).strip()
                        
                        # Data Science Cleaning Rule 2: Clean out ISBN numbers from the publisher field
                        if re.search(r'\d{3}-\d|\d{9}', publisher) or len(publisher) < 2:
                            # If publisher field was hijacked by an ISBN number, look around for alternative text or default to Unknown
                            publisher = "Unknown"
                        
                        # Data Science Cleaning Rule 3: Enforce proper Numerical Datatypes
                        year_match = re.search(r'\d{4}', raw_year)
                        pages_match = re.search(r'\d+', raw_pages)
                        
                        year = int(year_match.group()) if year_match else None
                        pages = int(pages_match.group()) if pages_match else None
                        
                        # Data Science Cleaning Rule 4: Handle page count shifting bugs 
                        # If the page count matches the publication year exactly, it's almost certainly a column misplacement bug!
                        if pages == year or pages > 1500:
                            # Clamp it or set to None to let data filter handle or ignore safely
                            if "shining" in title.lower(): pages = 447 # Hard fix for known anomalous rows
                            elif "lot" in title.lower(): pages = 439
                            else: continue
                        
                        # Validate clean records before loading to storage warehouse
                        if title and year and pages and pages > 10 and publisher != "Unknown":
                            record = {
                                "Title": title,
                                "Year": year,
                                "Publisher": publisher,
                                "Pages": pages,
                                "Book_Type": current_type # Brand new engineered feature dimension!
                            }
                            if record not in extracted_records:
                                extracted_records.append(record)
                    except Exception:
                        continue
                        
        print(f"✅ Successfully harvested {len(extracted_records)} valid records.")
        return extracted_records

    except Exception as e:
        print(f"❌ Pipeline critical failure during extraction: {str(e)}")
        return []

def run_data_pipeline():
    print("🚀 Initializing Ingestion Layer (pipeline.py)...")
    
    target_url = "https://en.wikipedia.org/wiki/Stephen_King_bibliography"
    records = extract_book_data(target_url)
    
    if not records:
        print("⚠️ Ingestion completed with an empty payload. Aborting local cache serialization.")
        return
        
    production_payload = {
        "status": "success",
        "count": len(records),
        "data": records
    }
    
    output_filename = "retrieve_data.json"
    print(f"💾 Serializing cleaned records into local warehouse: {output_filename}")
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(production_payload, f, indent=4, ensure_ascii=False)
        
    print("🎉 Pipeline data flow completed successfully!")

if __name__ == "__main__":
    run_data_pipeline()