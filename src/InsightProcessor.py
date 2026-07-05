from ollama import Client   # Native Ollama client
from pprint import pformat
from pathlib import Path

from src.Settings import settings

class InsightProcessor:
    def __init__(self, logger):
        # logger setting.
        self.logger = logger
        
        # report path setting.
        self.report_path = settings.report_path

        # Ollama setup
        self.model_name = settings.ollama_insight_model
        self.client = Client()   # or AsyncClient() if you want async

        self.logger.info(f"Insigher Processor initialized with model: {self.model_name}")

    
    def _ask_ollama(self, prompt:str, column_name: str, stage: str) -> str:
        response = self.client.chat(
                        model=self.model_name,
                        messages=[{"role": "user", "content": prompt}]
                    )["message"]["content"]
        # self.logger.info(f"Ollama response for {column_name} - {stage}:\n{response}")
        
        return response
    
    
    def generate_insights(self, column: str, data: list[str]) -> dict:
        
        dict = {}
        
        column_name = column.replace("_", " ")
        
        self.logger.info(f"Generating insights for column: '{column_name}'")
        
        # Step 1: Cluster
        cluster_prompt = f"""
        Group the following {column_name} into clusters of similar or related items.
        Output only clusters, no explanation.

        {column_name}:
        {data}
        """
        clusters = self._ask_ollama(cluster_prompt, column_name=column_name, stage="Cluster")

        # Step 2: Categorize
        category_prompt = f"""
        Categorize the following {column_name} clusters into high-level categories.

        Clusters:
        {clusters}
        """
        categories = self._ask_ollama(category_prompt, column_name=column_name, stage="Categorize")

        # Step 3: Insights
        insight_prompt = f"""
        Based on the categorized {column_name}, extract insights such as:
        - most common {column_name} areas

        Categorized {column_name}:
        {categories}
        """
        insights = self._ask_ollama(insight_prompt, column_name=column_name, stage="Insights")
        
        # consolidate the results into a dictionary.
        dict[column] = column_name
        dict["clusters"] = clusters
        dict["categories"] = categories
        dict["insights"] = insights

        return dict