from ollama import AsyncClient
from psycopg2.extras import RealDictRow
import asyncio
from pprint import pformat
from typing import List

from src.DataClass import ExtractedJobInfo
from src.Settings import settings


class JobExtractor:
    def __init__(self, logger):
        self.logger = logger
        self.model_name = settings.ollama_extraction_model
        if not self.model_name:
            raise ValueError("OLLAMA_EXTRACTION_MODEL not set in .env file")
        
        self.client = AsyncClient()
        self.logger.info(f"Ollama Summarizer initialized with model: {self.model_name}")

    async def _summarize_job_info(self, result: RealDictRow, keyword: str) -> ExtractedJobInfo:
        
        # get the information from result.
        id = result.get('id')
        content = result.get("content")

        # Strong, clear prompt for extraction
        prompt = f"""You are an expert job‑ad analyst. Extract and infer information with high precision.

        TASKS:
        1. Extract explicit information exactly as written.
        2. Get the company name from the context. If company name is missing, just state None.
        3. Read the job ad and output one industry label only. No Explanation (e.g., “fintech company”, “global bank”, “AI startup”). 
        4. Extract core responsibilities explicitly mentioned in the job ad only.
        5. Extract core working experiences (e.g. 5 years experience in AI) explicitly mentioned in the job ad only.
        6. Extract technical skills (e.g. python, SQL, AWS) explicitly mentioned in the job ad.
        7. Extract soft skills (e.g. communication, teamwork, problem-solving) explicitly mentioned in the job ad.
        8. Extract all educational qualifications (e.g. Master or Bachelor in Engineering) and certificates (e.g. Certificate in PMP) explicitly mentioned in the job ad only.
        9. Summarize the job in structured JSON.

        Job Content:
        {content}
        """

        try:
            response = await self.client.chat(
                model=self.model_name,                    # ← This was becoming None before
                messages=[{'role': 'user', 'content': prompt}],
                format=ExtractedJobInfo.model_json_schema(),   # Native structured output
                options={
                    'temperature': 0.0,
                    'num_ctx': 16384,      # Good for long job descriptions
                    'num_predict': 1500,
                }
            )

            # Parse the JSON response directly into your Pydantic model
            extracted = ExtractedJobInfo.model_validate_json(
                response['message']['content']
            )
            extracted.id = id
            self.logger.info(f"Successfully extracted job for job id - {id}: \n%s", pformat(extracted.model_dump(), indent=4))
            self.logger.info("#"*50)
            
            return extracted

        except Exception as e:
            self.logger.error(f"Failed to extract job id - {id}: {e}")
            # Fallback: return basic info so the pipeline doesn't crash
            return ExtractedJobInfo(
                    id=id,
                    job_title="",
                    responsibilities=[],
                    qualifications=[],
                    experiences=[],
                    technical_skills=[],
                    soft_skills=[],
                    industry="",
                )


    async def summarize_all_jobs(self, results: List[RealDictRow], keyword: str) -> List[ExtractedJobInfo]:
        self.logger.info(f"Starting extraction for {len(results)} jobs...")

        semaphore = asyncio.Semaphore(4)   # Tune this (3~6) based on your GPU/RAM

        async def bounded_extract(result: RealDictRow):
            async with semaphore:
                return await self._summarize_job_info(result, keyword)

        tasks = [bounded_extract(result) for result in results]
        job_infos = await asyncio.gather(*tasks, return_exceptions=True)

        # Remove any exceptions
        successful = [j for j in job_infos if not isinstance(j, Exception)]
        self.logger.info(f"Extraction completed. {len(successful)}/{len(results)} jobs succeeded.")

        return successful