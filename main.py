from asyncio.log import logger
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


def fetch_and_save_jobs(keyword: str, total_pages: int, logger: Logger, dbhandler: DBHandler) -> None:
    
    # declare crawler and extractor instances.
    crawler = JobAdCrawler(logger=logger)
    extractor = JobExtractor(logger=logger)
    
    # crawl all pages of job ads based on the keyword and total search pages.
    job_results = crawler.crawl_all_job_pages(
        keyword=keyword, 
        total_pages=int(total_pages)
    )
    
    logger.info(f"Total {len(job_results)} job advertisements crawled.")
    logger.info(f"Start saving the raw data of job advertisments into database.")
    
    for result in job_results:
        dbhandler.insert_job(keyword=keyword, result=result)
    
    logger.info(f"All crawled job advertisments raw data saved to the database.")
    
    # Extract information from job ads and save the info to postgresql by batches.
    batch_size = settings.batch_size
    job_results = dbhandler.retrieve_raw_job_data(keyword=keyword)
    logger.info(f"Total {len(job_results)} job advertisement retrieved for keyword - {keyword}")
    
    batches = [job_results[i:i+batch_size] for i in range(0, len(job_results), batch_size)]
    
    for i, batch in enumerate(batches, start=1):
        # Extract information from job ads.
        logger.info(f"Batch No. {i}: Start job information extraction.")
        extracted_infos = asyncio.run(extractor.summarize_all_jobs(results=batch, keyword=keyword))

        logger.info(f"Batch No. {i}: End job information extraction.")
        # save data to postgresql.
        for job in extracted_infos:
            dbhandler.update_job(job_item=job)
        logger.info(f"Batch No. {i}: Saved to Database.")
        
    return
    
    
    
def retrieve_and_generate_insights(keyword: str, logger: Logger, dbhandler: DBHandler) -> None:
    
    # declare insight processor instance.
    insight_processor = InsightProcessor(logger=logger)
    
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

    #  generate insights for selected columns in the database.
    order = ["industry", "job_title", "responsibilities", "qualifications", "experiences", "technical_skills", "soft_skills"]
    
    # generate report for each column.
    md_file = create_report_object(keyword=keyword)
    logger.info(f"Report file created: {md_file.file_name}")
        
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
            
        insights_dict = insight_processor.process_items_to_insights(
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

    logger.info(f"Report generation completed for keyword '{keyword}'. Report file: {md_file.file_name}")
       
    return
    

# main program.
def main():
    # initiate classes.
    logger = Logger(__name__).get_logger()
    dbhandler = DBHandler(logger=logger)
    
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
        fetch_and_save_jobs(keyword=keyword, total_pages=int(total_search_pages), logger=logger, dbhandler=dbhandler)
        
        # retrieve and generate insights and report.
        retrieve_and_generate_insights(keyword=keyword, logger=logger, dbhandler=dbhandler)
        
       
    return

# main program entry point.
if __name__ == "__main__":
    main()
