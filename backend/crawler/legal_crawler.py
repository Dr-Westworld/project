"""
Legal Document Web Crawler
Crawls authoritative legal sources to gather up-to-date information for RAG pipeline
"""

import asyncio
import aiohttp
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import hashlib
from playwright.async_api import async_playwright
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class LegalSource:
    """Represents a legal source with metadata"""
    url: str
    title: str
    content: str
    source_type: str  # government, court, legal_portal, law_firm, other
    jurisdiction: str
    authority_level: str  # high, medium, low
    last_crawled: datetime
    content_hash: str
    metadata: Dict[str, Any]

class LegalCrawler:
    """Crawler for legal sources with intelligent content extraction"""
    
    def __init__(self):
        self.session = None
        self.legal_sources = []
        self.crawled_urls = set()
        self.rate_limits = {}  # Track rate limits per domain
        
        # Authoritative legal source patterns
        self.legal_domains = {
            'government': [
                r'.*\.gov$',
                r'.*\.ca\.gov$',
                r'.*\.state\.us$',
                r'.*\.courts\.gov$',
                r'.*\.ftb\.ca\.gov$',
                r'.*\.sos\.ca\.gov$'
            ],
            'court': [
                r'.*\.courts\.gov$',
                r'.*\.court\.gov$',
                r'.*\.uscourts\.gov$',
                r'.*\.ca\.courts\.gov$'
            ],
            'legal_portal': [
                r'.*\.justia\.com$',
                r'.*\.findlaw\.com$',
                r'.*\.law\.cornell\.edu$',
                r'.*\.nolo\.com$'
            ]
        }
        
        # Keywords for legal content identification
        self.legal_keywords = [
            'incorporation', 'llc', 'corporation', 'partnership', 'business license',
            'filing', 'registration', 'compliance', 'regulation', 'statute',
            'court', 'litigation', 'lawsuit', 'contract', 'agreement',
            'tax', 'irs', 'ftb', 'franchise tax', 'employment law',
            'intellectual property', 'patent', 'trademark', 'copyright'
        ]

    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                'User-Agent': 'Legal Assistant Bot 1.0 (Educational Purpose)',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            }
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()

    def is_legal_domain(self, url: str) -> Optional[str]:
        """Check if URL belongs to a legal domain and return type"""
        domain = urlparse(url).netloc.lower()
        
        for source_type, patterns in self.legal_domains.items():
            for pattern in patterns:
                if re.match(pattern, domain):
                    return source_type
        return None

    def extract_jurisdiction(self, url: str, content: str) -> str:
        """Extract jurisdiction from URL and content"""
        domain = urlparse(url).netloc.lower()
        
        # Extract from domain
        if '.ca.gov' in domain:
            return 'California, USA'
        elif '.state.us' in domain:
            state = domain.split('.')[0]
            return f"{state.title()}, USA"
        elif '.gov' in domain:
            return 'Federal, USA'
        
        # Extract from content
        content_lower = content.lower()
        if 'california' in content_lower:
            return 'California, USA'
        elif 'new york' in content_lower:
            return 'New York, USA'
        elif 'texas' in content_lower:
            return 'Texas, USA'
        
        return 'Unknown'

    def determine_authority_level(self, url: str, source_type: str) -> str:
        """Determine authority level based on source type and URL"""
        if source_type == 'government':
            return 'high'
        elif source_type == 'court':
            return 'high'
        elif source_type == 'legal_portal':
            return 'medium'
        else:
            return 'low'

    def clean_content(self, html: str) -> str:
        """Clean and extract meaningful content from HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Remove navigation and footer elements
        for element in soup(["nav", "footer", "header", "aside"]):
            element.decompose()
        
        # Remove elements with common non-content classes
        for element in soup.find_all(class_=re.compile(r'(nav|menu|sidebar|footer|header|ad|banner)', re.I)):
            element.decompose()
        
        # Extract text
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text

    def is_legal_content(self, content: str) -> bool:
        """Check if content is relevant to legal matters"""
        content_lower = content.lower()
        keyword_matches = sum(1 for keyword in self.legal_keywords if keyword in content_lower)
        return keyword_matches >= 3  # At least 3 legal keywords

    async def crawl_url(self, url: str, use_playwright: bool = False) -> Optional[LegalSource]:
        """Crawl a single URL and extract legal content"""
        try:
            # Check rate limits
            domain = urlparse(url).netloc
            if domain in self.rate_limits:
                if time.time() - self.rate_limits[domain] < 1:  # 1 second between requests
                    await asyncio.sleep(1)
            
            self.rate_limits[domain] = time.time()
            
            if use_playwright:
                return await self.crawl_with_playwright(url)
            else:
                return await self.crawl_with_aiohttp(url)
                
        except Exception as e:
            logger.error(f"Error crawling {url}: {str(e)}")
            return None

    async def crawl_with_aiohttp(self, url: str) -> Optional[LegalSource]:
        """Crawl URL using aiohttp (faster for simple pages)"""
        try:
            async with self.session.get(url) as response:
                if response.status != 200:
                    return None
                
                html = await response.text()
                return self.process_html(url, html)
                
        except Exception as e:
            logger.error(f"aiohttp error for {url}: {str(e)}")
            return None

    async def crawl_with_playwright(self, url: str) -> Optional[LegalSource]:
        """Crawl URL using Playwright (for JavaScript-heavy pages)"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                await page.goto(url, wait_until='networkidle')
                html = await page.content()
                
                await browser.close()
                return self.process_html(url, html)
                
        except Exception as e:
            logger.error(f"Playwright error for {url}: {str(e)}")
            return None

    def process_html(self, url: str, html: str) -> Optional[LegalSource]:
        """Process HTML content and create LegalSource object"""
        try:
            # Clean content
            content = self.clean_content(html)
            
            # Check if content is legal-related
            if not self.is_legal_content(content):
                return None
            
            # Extract title
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.find('title')
            title_text = title.get_text().strip() if title else urlparse(url).path
            
            # Determine source type and authority
            source_type = self.is_legal_domain(url) or 'other'
            authority_level = self.determine_authority_level(url, source_type)
            jurisdiction = self.extract_jurisdiction(url, content)
            
            # Create content hash for deduplication
            content_hash = hashlib.md5(content.encode()).hexdigest()
            
            # Extract metadata
            metadata = {
                'word_count': len(content.split()),
                'has_forms': bool(soup.find('form')),
                'has_tables': bool(soup.find('table')),
                'has_links': len(soup.find_all('a')),
                'last_modified': soup.find('meta', attrs={'name': 'last-modified'})
            }
            
            return LegalSource(
                url=url,
                title=title_text,
                content=content,
                source_type=source_type,
                jurisdiction=jurisdiction,
                authority_level=authority_level,
                last_crawled=datetime.now(),
                content_hash=content_hash,
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"Error processing HTML for {url}: {str(e)}")
            return None

    async def discover_legal_sources(self, seed_urls: List[str], max_depth: int = 2) -> List[LegalSource]:
        """Discover legal sources starting from seed URLs"""
        discovered_sources = []
        urls_to_crawl = seed_urls.copy()
        crawled_count = 0
        max_urls = 100  # Limit total URLs to crawl
        
        while urls_to_crawl and crawled_count < max_urls:
            current_batch = urls_to_crawl[:10]  # Process in batches
            urls_to_crawl = urls_to_crawl[10:]
            
            tasks = [self.crawl_url(url) for url in current_batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in results:
                if isinstance(result, LegalSource):
                    discovered_sources.append(result)
                    crawled_count += 1
                    
                    # Add new URLs from this page (if within depth limit)
                    if crawled_count < max_urls:
                        new_urls = self.extract_links_from_content(result.content, result.url)
                        for new_url in new_urls:
                            if new_url not in self.crawled_urls and len(urls_to_crawl) < 50:
                                urls_to_crawl.append(new_url)
                                self.crawled_urls.add(new_url)
            
            # Rate limiting
            await asyncio.sleep(1)
        
        return discovered_sources

    def extract_links_from_content(self, content: str, base_url: str) -> List[str]:
        """Extract relevant links from content"""
        soup = BeautifulSoup(content, 'html.parser')
        links = []
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            
            # Only include legal domains
            if self.is_legal_domain(full_url):
                links.append(full_url)
        
        return links

    async def crawl_legal_sources(self, jurisdictions: List[str] = None) -> List[LegalSource]:
        """Main method to crawl legal sources for specified jurisdictions"""
        if jurisdictions is None:
            jurisdictions = ['California', 'New York', 'Texas', 'Federal']
        
        # Seed URLs for different jurisdictions
        seed_urls = {
            'California': [
                'https://sos.ca.gov/business/',
                'https://www.ftb.ca.gov/',
                'https://www.dol.ca.gov/',
                'https://bizfileonline.sos.ca.gov/'
            ],
            'New York': [
                'https://www.dos.ny.gov/',
                'https://www.tax.ny.gov/',
                'https://www.labor.ny.gov/'
            ],
            'Texas': [
                'https://mycpa.cpa.state.tx.us/',
                'https://comptroller.texas.gov/',
                'https://www.twc.texas.gov/'
            ],
            'Federal': [
                'https://www.irs.gov/',
                'https://www.sba.gov/',
                'https://www.sec.gov/',
                'https://www.uspto.gov/'
            ]
        }
        
        all_sources = []
        
        for jurisdiction in jurisdictions:
            if jurisdiction in seed_urls:
                logger.info(f"Crawling legal sources for {jurisdiction}")
                sources = await self.discover_legal_sources(seed_urls[jurisdiction])
                all_sources.extend(sources)
                logger.info(f"Found {len(sources)} sources for {jurisdiction}")
        
        return all_sources

    def save_sources(self, sources: List[LegalSource], filename: str = "legal_sources.json"):
        """Save crawled sources to JSON file"""
        data = []
        for source in sources:
            data.append({
                'url': source.url,
                'title': source.title,
                'content': source.content,
                'source_type': source.source_type,
                'jurisdiction': source.jurisdiction,
                'authority_level': source.authority_level,
                'last_crawled': source.last_crawled.isoformat(),
                'content_hash': source.content_hash,
                'metadata': source.metadata
            })
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(sources)} legal sources to {filename}")

    def load_sources(self, filename: str = "legal_sources.json") -> List[LegalSource]:
        """Load sources from JSON file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            sources = []
            for item in data:
                sources.append(LegalSource(
                    url=item['url'],
                    title=item['title'],
                    content=item['content'],
                    source_type=item['source_type'],
                    jurisdiction=item['jurisdiction'],
                    authority_level=item['authority_level'],
                    last_crawled=datetime.fromisoformat(item['last_crawled']),
                    content_hash=item['content_hash'],
                    metadata=item['metadata']
                ))
            
            return sources
        except FileNotFoundError:
            logger.warning(f"File {filename} not found")
            return []
        except Exception as e:
            logger.error(f"Error loading sources: {str(e)}")
            return []

# Example usage
async def main():
    """Example usage of the legal crawler"""
    async with LegalCrawler() as crawler:
        # Crawl legal sources
        sources = await crawler.crawl_legal_sources(['California'])
        
        # Save sources
        crawler.save_sources(sources)
        
        # Print summary
        print(f"Crawled {len(sources)} legal sources")
        for source in sources[:5]:  # Show first 5
            print(f"- {source.title} ({source.source_type}) - {source.jurisdiction}")

if __name__ == "__main__":
    asyncio.run(main())
