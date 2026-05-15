from tools.logger import Logger
from tools.WebCrawler import WebCrawler
from tools.OllamaSummarizer import OllamaSummarizer
from tools.DBHandler import DBHandler
from tools.OllamaResearcher import OllamaResearcher

from pprint import pformat
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()


# main program.
def main():
    # initiate classes.
    logger = Logger(__name__).get_logger()
    crawler = WebCrawler(logger=logger)
    summarizer = OllamaSummarizer(logger=logger)
    dbhandler = DBHandler(logger=logger)
    researcher = OllamaResearcher(logger=logger)
    
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
        job_results = crawler.crawl_all_job_pages(
            keyword=keyword, 
            total_pages=int(total_search_pages)
        )
        
        # Extract informattion from job ads and save the info to postgresql by batches.
        batch_size = 10
        batches = [job_results[i:i+batch_size] for i in range(0, len(job_results), batch_size)]
        
        for batch in batches:
            # Extract information from job ads.
            job_infos = asyncio.run(summarizer.summarize_all_jobs(results=batch, keyword=keyword))

            # save data to postgresql.
            for job in job_infos:
                dbhandler.insert_job(job_item=job)
        
        # fetch data from postgresql for generating report.
        job_titles = dbhandler.get_top_job_titles(
            keyword=keyword, 
            limit=10
        )
        skills = dbhandler.get_top_items(
            keyword=keyword, 
            column="skills", 
            limit=15
        )
        responsibilities = dbhandler.get_top_items(
            keyword=keyword, 
            column="responsibilities", 
            limit=15
        )
        qualifications = dbhandler.get_top_items(
            keyword=keyword, 
            column="qualifications", 
            limit=10
        )
        experiences = dbhandler.get_top_items(
            keyword=keyword, 
            column="experiences", 
            limit=10
        )
        
        # generate report.
        researcher.generate_job_market_report(
            keyword=keyword,
            job_titles=job_titles,
            skills=skills,
            responsibilities=responsibilities,
            qualifications=qualifications,
            experiences=experiences
        )
       
    return

# main program entry point.
if __name__ == "__main__":
    main()
