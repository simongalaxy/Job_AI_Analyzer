from pprint import pformat
import asyncio
import json

from src.Settings import settings
from src.logger import Logger
from src.JobAdCrawler import JobAdCrawler
from src.JobExtractor import JobExtractor
from src.DBHandler import DBHandler
from src.InsightProcessor import InsightProcessor
from src.ReportGenerator import create_report_object, write_section


# main program.
def main():
    # initiate classes.
    logger = Logger(__name__).get_logger()
    crawler = JobAdCrawler(logger=logger)
    extractor = JobExtractor(logger=logger)
    dbhandler = DBHandler(logger=logger)
    insight_processor = InsightProcessor(logger=logger)
    
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
        batch_size = settings.batch_size
        batches = [job_results[i:i+batch_size] for i in range(0, len(job_results), batch_size)]
        
        for batch in batches:
            # Extract information from job ads.
            job_infos = asyncio.run(extractor.summarize_all_jobs(results=batch, keyword=keyword))

            # save data to postgresql.
            for job in job_infos:
                 dbhandler.insert_job(job_item=job)
        
        # fetch data from postgresql for generating insights from each columns.
        schema = dbhandler.get_schema()
        
        # Ensure schema is a dict. DBHandler may return a JSON string.
        if isinstance(schema, str):
            try:
                schema = json.loads(schema)
            except json.JSONDecodeError:
                logger.error("Failed to parse database schema JSON.")
                schema = {}
        
        logger.info(f"Database schema: {pformat(schema)}")

        # generate insights for selected columns in the database.
        order = ["industry", "job_title", "responsibilities", "qualifications", "experiences", "technical_skills", "soft_skills"]
        
        # generate report for each column.
        md_file = create_report_object(keyword=keyword)
        logger.info(f"Report file created: {md_file.file_name}.md")
        
        for i in range(len(order)):
            if schema[order[i]] == "text":   
                items = dbhandler.get_items_from_column(
                    keyword=keyword, 
                    column=order[i]
                )
            else:
                items = dbhandler.get_items_from_array_column(
                    keyword=keyword, 
                    column=order[i]
                )
                
            insights_dict = insight_processor.generate_insights(
                column=order[i],
                data=items,
            )
            logger.info(f"Insights for column '{order[i]}': {pformat(insights_dict)}")

            write_section(
                md_file=md_file, 
                insights_dict=insights_dict, 
                keyword=keyword, 
                i=i, 
                total_sections=len(order)
            )
            
            logger.info(f"Insights for column '{order[i]}' written to report.")

        logger.info(f"Report generation completed for keyword '{keyword}'. Report file: {md_file.file_name}.md")
       
    return

# main program entry point.
if __name__ == "__main__":
    main()
