from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode, BrowserConfig, MemoryAdaptiveDispatcher, CrawlResult
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy

from typing import List
import asyncio
from pprint import pformat
import re


class WebCrawler:
    def __init__(self, logger):
        self.logger = logger
        self.browser_config = BrowserConfig(
            headless=True,
            text_mode=True,
	        light_mode=True,
            verbose=True
        )
        self.crawl_config_job = CrawlerRunConfig(
            scraping_strategy=LXMLWebScrapingStrategy(),
            exclude_all_images=True,
            exclude_social_media_domains=True,
            exclude_external_links=True,
            target_elements=['h1[data-automation="job-detail-title"]', 'div[data-automation="jobAdDetails"]'],  # Use valid CSS attribute selectors for better compatibility
            cache_mode=CacheMode.BYPASS,
            wait_for_timeout=30000
        )
        self.crawl_config_search = CrawlerRunConfig(
            scraping_strategy=LXMLWebScrapingStrategy(),
            exclude_all_images=True,
            exclude_social_media_domains=True,
            exclude_external_links=True,
            cache_mode=CacheMode.BYPASS,
            wait_for_timeout=30000
        )
        self.dispatcher = MemoryAdaptiveDispatcher(
            memory_threshold_percent=70,
            check_interval=1,
            max_session_permit=4
        )
        self.crawler = None # Important.
        
        self.logger.info(f"{WebCrawler.__name__} initiated.")
    
    # supporting methods.
    def _extract_job_links(self, results: List[CrawlResult]) -> List[str]:
        # extract the job page links.
        job_links = []
        total_job_links = 0
        for i, result in enumerate(results):
            links = result.links.get("internal", [])
            filtered_links = [link["href"] for link in links if re.search(pattern=r"\d+\?type=standard", string=link["href"])]
            job_links.append(filtered_links)
            total_job_links += len(filtered_links)
            
        self.logger.info(f"Total {total_job_links} job page links crawled from {len(results)} search pages.")    
         
        return job_links


    def _generate_urls(self, keyword: str, total_page: int) -> list[str]:
        urls = [f"https://hk.jobsdb.com/{keyword}-jobs?page={page}" for page in range(1, total_page+1)]
        self.logger.info(f"Generated total {len(urls)} search pages - urls: {urls}")
        
        return urls

    async def init_crawler(self):
        self.crawler = AsyncWebCrawler(config=self.browser_config)

    # async crawler.
    async def _crawl_pages(self, urls: List[str], config: CrawlerRunConfig) -> List[CrawlResult]:
        async with self.crawler:
            results = await self.crawler.arun_many(
                urls=urls, 
                config=config,
                dispatcher=self.dispatcher
            )
        self.logger.info(f"Total {len(results)} pages crawled.")
                
        return results


    async def _crawl_all_job_pages_async(self, keyword: str, total_pages: int) -> List[CrawlResult]: 
        
        # initiate AsyncWebCrawler object.
        await self.init_crawler()
        
        # Generate search pages.
        urls = self._generate_urls(keyword=keyword, total_page=total_pages)
        for i, url in enumerate(urls):
            print(f"{i}: {url}")

        self.logger.info(f"Start crawling total {len(urls)} search pages.")
        # crawl all links for job pages from search pages.
        results = await self._crawl_pages(urls=urls, config=self.crawl_config_search)
        
        # extract job ad links.
        job_links = self._extract_job_links(results=results)
        
        # crawl all contents from each job pages by batch.
        job_results = []
        for links in job_links:
            results = await self._crawl_pages(urls=links, config=self.crawl_config_job)
            job_results.extend(results)
        
        return job_results
    
    
    def crawl_all_job_pages(self, keyword: str, total_pages: int) -> List[CrawlResult]:
        return asyncio.run(self._crawl_all_job_pages_async(keyword=keyword, total_pages=total_pages))
