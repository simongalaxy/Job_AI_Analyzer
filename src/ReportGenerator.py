import textwrap
from datetime import datetime
import json
import os
from mdutils.mdutils import MdUtils

from src.Settings import settings

def create_report_object(keyword: str) -> MdUtils:

    # generate filename by daily press release url.
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Job_Report_keyword-{keyword}_{ts}.md"
    filepath = settings.report_path
    
    # check whether the report folder is created. if no, create a new folder.
    os.makedirs(filepath, exist_ok=True)
    
    # Create a new markdown file
    md_file = MdUtils(file_name=filename, 
                      title=f"Job Market Insights Report - {keyword}", 
                      author="Job AI Analyzer",
                      description=f"Insights report for the keyword: {keyword}",
                      cover_image_path=None, 
                      css_path=None, 
                      language='en',
                      toc=True, 
                      toc_depth=2, 
                      filepath=filepath
                    )
    
    return md_file


def write_section(md_file: MdUtils, insights_dict: dict, keyword: str, i: int, total_sections: int) -> None:
    
    # Iterate through the insights dictionary and add content to the markdown file
    for column, insights in insights_dict.items():
        md_file.new_header(level=2, title=f"{column.replace('_', ' ')}")
        
        if isinstance(insights, dict):
            for key, value in insights.items():
                md_file.new_paragraph(f"**{key}:**")
                md_file.new_line()
                md_file.new_paragraph(textwrap.fill(str(value), width=80))
                md_file.new_line()
        else:
            md_file.new_paragraph(str(insights))

    # Save the markdown file
    if i == total_sections - 1:
        md_file.create_md_file()
    
    return