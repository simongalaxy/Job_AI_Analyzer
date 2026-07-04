from src.Settings import settings
from src.logger import Logger
from src.JobAdCrawler import JobAdCrawler
from src.JobExtractor import JobExtractor
from src.DBHandler import DBHandler
from src.InsightProcessor import InsightProcessor
# from src.MarketResearcher import MarketResearcher

from pprint import pformat
import asyncio


# main program.
def main():
    # initiate classes.
    logger = Logger(__name__).get_logger()
    crawler = JobAdCrawler(logger=logger)
    extractor = JobExtractor(logger=logger)
    dbhandler = DBHandler(logger=logger)
    insight_processor = InsightProcessor(logger=logger)
    # researcher = MarketResearcher(logger=logger)
    
    # chat loop.
    while True:
        query = input("Enter your keyword to search jobs (or type 'q' for quit): ")
        
        if query.lower() == 'q':
            logger.info("User exited the application.")
            break
        total_search_pages = input("How many search pages to crawl? ")
        
        # must convert query to a string in format "text-text-text" before searching.
        keyword = query.replace(" ", "-")
        
        # crawl all job pages based on the keyword and save the extracted results to the postgresql database.
        # job_results = crawler.crawl_all_job_pages(
        #     keyword=keyword, 
        #     total_pages=int(total_search_pages)
        # )
        
        # # Extract informattion from job ads and save the info to postgresql by batches.
        # batch_size = settings.batch_size
        # batches = [job_results[i:i+batch_size] for i in range(0, len(job_results), batch_size)]
        
        # for batch in batches:
        #     # Extract information from job ads.
        #     job_infos = asyncio.run(extractor.summarize_all_jobs(results=batch, keyword=keyword))

        #     # save data to postgresql.
        #     for job in job_infos:
        #          dbhandler.insert_job(job_item=job)
        
        # fetch data from postgresql for generating insights from each columns.
        schema = dbhandler.get_schema()
        logger.info(f"Database schema: {pformat(schema)}")

        job_titles = dbhandler.get_items_from_column(
            keyword=keyword, 
            column="job_title"
        )
        logger.info(f"Job titles for keyword '{keyword}': {pformat(job_titles)}")
        
        insights = insight_processor.generate_insights(
            column="job_title",
            data=job_titles,
        )
        logger.info(f"Insights for job titles: {pformat(insights)}")
        
        
        # #generate report.
        # researcher.generate_job_market_report(
        #     keyword=keyword,
        #     job_titles=job_titles,
        #     industries=industries,
        #     skills=skills,
        #     responsibilities=responsibilities,
        #     qualifications=qualifications,
        #     experiences=experiences
        # )
       
    return

# main program entry point.
if __name__ == "__main__":
    main()
