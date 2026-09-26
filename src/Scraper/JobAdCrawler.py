from crawl4ai import (
    AsyncWebCrawler,
    CrawlerRunConfig,
    CacheMode,
    BrowserConfig,
    MemoryAdaptiveDispatcher,
    CrawlResult,
)
from typing import List, AsyncGenerator
import asyncio
import re

from src.Settings import settings

class JobAdCrawler:
    def __init__(self, logger):
        self.logger = logger

        # 全局 browser 設定：只開一次
        self.browser_config = BrowserConfig(
            headless=True,
            verbose=True,
            browser_type="chromium",
        )

        # 搜尋頁 config（多頁）
        self.crawl_config_search = CrawlerRunConfig(
            exclude_all_images=True,
            exclude_external_links=True,
            exclude_social_media_domains=True,
            cache_mode=CacheMode.BYPASS,
            wait_for_timeout=20000,
            stream=True,  # 用 streaming 處理大量 URL
        )

        # job 詳情頁 config
        self.crawl_config_job = CrawlerRunConfig(
            target_elements=[
                'h1[data-automation="job-detail-title"]',
                'div[data-automation="jobAdDetails"]',
            ],
            exclude_all_images=True,
            cache_mode=CacheMode.BYPASS,
            wait_for_timeout=20000,
            stream=True,
        )

        # 單一 crawler 實例
        self.crawler = AsyncWebCrawler(config=self.browser_config)

        self.logger.info(f"{JobAdCrawler.__name__} initiated (large-scale mode).")

    # -----------------------------
    # helpers
    # -----------------------------
    def _generate_search_urls(self, keyword: str, total_pages: int) -> List[str]:
        urls = [
            f"https://hk.jobsdb.com/{keyword}-jobs?page={page}"
            for page in range(1, total_pages + 1)
        ]
        self.logger.info(f"Generated {len(urls)} search URLs.")
        return urls

    def _extract_job_links(self, results: List[CrawlResult]) -> List[str]:
        job_links = []
        for res in results:
            if not res.success:
                continue
            links = res.links.get("internal", [])
            filtered = [
                link["href"]
                for link in links
                if re.search(r"\d+\?type=standard", link["href"])
            ]
            job_links.extend(filtered)

        self.logger.info(f"Extracted {len(job_links)} job links.")
        return job_links

    # -----------------------------
    # core async crawling
    # -----------------------------
    async def _crawl_many_streaming(
        self, urls: List[str], config: CrawlerRunConfig
    ) -> List[CrawlResult]:
        """
        用 streaming 模式處理大量 URL：
        - 邊爬邊處理
        - 唔需要一次性全部載入記憶體
        """
        results: List[CrawlResult] = []

        async for result in await self.crawler.arun_many(
            urls=urls,
            config=config,
            # dispatcher=self.dispatcher,
            dispatcher=None
        ):
            results.append(result)

        self.logger.info(f"Streaming crawl completed: {len(results)} results.")
        return results

    async def crawl_async(self, keyword: str, total_pages: int) -> List[CrawlResult]:
        # 開 browser 一次
        await self.crawler.start()

        # 1. 搜尋頁
        search_urls = self._generate_search_urls(keyword, total_pages)
        self.logger.info(f"Start crawling {len(search_urls)} search pages.")

        search_results = await self._crawl_many_streaming(
            urls=search_urls,
            config=self.crawl_config_search,
        )

        # 2. 抽 job links
        job_links = self._extract_job_links(search_results)

        # 3. job pages 分批 crawl（避免一次過幾千個 URL）
        batch_size = settings.batch_size
        all_job_results: List[CrawlResult] = []

        self.logger.info(
            f"Start crawling {len(job_links)} job pages in batches of {batch_size}."
        )

        for i in range(0, len(job_links), batch_size):
            batch = job_links[i : i + batch_size]
            self.logger.info(f"Crawling batch {i // batch_size + 1}: {len(batch)} URLs")

            batch_results = await self._crawl_many_streaming(
                urls=batch,
                config=self.crawl_config_job,
            )
            all_job_results.extend(batch_results)

        # 收尾：關 browser 一次
        await self.crawler.close()

        self.logger.info(
            f"Completed crawling {len(all_job_results)} job pages (keyword={keyword})."
        )
        return all_job_results

    # -----------------------------
    # sync wrapper（如果你喺純 script 用）
    # -----------------------------
    def crawl(self, keyword: str, total_pages: int) -> List[CrawlResult]:
        """
        注意：如果你喺已有 event loop 環境（例如 FastAPI / Jupyter），
        唔好用呢個，用 `await crawl_async(...)` 直接。
        """
        return asyncio.run(self.crawl_async(keyword, total_pages))
