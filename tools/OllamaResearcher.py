from ollama import Client   # Native Ollama client
import psycopg2
import psycopg2.extras
from pprint import pformat
from pathlib import Path
import textwrap
from datetime import datetime
import json
import os
from dotenv import load_dotenv
load_dotenv()


class OllamaResearcher:
    def __init__(self, logger):
        self.logger = logger

        # Ollama setup
        self.model_name = os.getenv("OLLAMA_SUMMARIZATION_MODEL")
        self.client = Client()   # or AsyncClient() if you want async

        self.logger.info(f"Ollama Researcher initialized with model: {self.model_name}")


    def _write_report(self, keyword: str, markdown: str) -> None:
        
        # generate filename by daily press release url.
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Job_Report_keyword-{keyword}_{ts}.md"
        filepath = "./reports/"
        
        # check whether the report folder is created. if no, create a new folder.
        os.makedirs(filepath, exist_ok=True)
        
        # generate report in text file.
        with open(os.path.join(filepath, filename), "w", encoding="utf-8") as file:
            file.write(markdown + "\n")
            
        return


    def generate_job_market_report(self, keyword: str, job_titles, skills, responsibilities, qualifications, experiences) -> None:
        self.logger.info(f"Generating job market report for keyword: '{keyword}'")

        try:
            total_jobs = sum(row["count"] for row in job_titles)

            # 2. Prepare clean insights (much smaller than before)
            insights = {
                "keyword": keyword,
                "total_jobs": total_jobs,
                "top_job_titles": [{"title": r["job_title"], "count": r["count"]} for r in job_titles],
                "top_skills": [{"skill": r["element"], "count": r["freq"]} for r in skills],
                "top_responsibilities": [{"item": r["element"], "count": r["freq"]} for r in responsibilities],
                "top_qualifications": [{"item": r["element"], "count": r["freq"]} for r in qualifications],
                "top_experiences": [{"item": r["element"], "count": r["freq"]} for r in experiences]
            }

            # 3. Strong system + user prompt
            system_prompt = "You are a precise, data-driven job market analyst. Generate reports using ONLY the provided data. Never invent information."

            user_prompt = f"""Generate a professional Job Market Research Report based on the following data.

            Data:
            {json.dumps(insights, indent=2, ensure_ascii=False)}

            Rules:
            - Use only the exact items and counts from the data above.
            - Do not add any job titles, skills, or experiences that are not listed.
            - Be factual and specific.
            - Output in clean Markdown format.

            Return the full report in Markdown.
            """

            # 4. Call Ollama directly
            response = self.client.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                options={
                    "temperature": 0.0,      # Very important for factual report
                    "num_ctx": 16384,
                    "num_predict": 4096,     # Allow long report
                }
            )

            report_text = response['message']['content']
            self.logger.info("#"*50)
            self.logger.info("Report generated: \n%s", report_text)
            self.logger.info("#"*50)
            self._write_report(keyword=keyword, markdown=report_text)
            
            return

        except Exception as e:
            self.logger.error(f"Failed to generate report for '{keyword}': {e}")
            raise

            
       