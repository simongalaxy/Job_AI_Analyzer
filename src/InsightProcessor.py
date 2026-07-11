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
        self.clustering_model = settings.ollama_clustering_model
        self.categorizing_model = settings.ollama_categorizing_model
        self.gen_insight_model = settings.ollama_insight_model
        
        self.client = Client()   # or AsyncClient() if you want async.

    
    def _ask_ollama(self, prompt:str, model: str) -> str:
        response = self.client.chat(
                        model=model,
                        messages=[{"role": "user", "content": prompt}]
                    )["message"]["content"]
        
        return response
    
    
    def _cluster_items(self, column_name: str, data: list[str]) -> str:
        
        self.logger.info(f"Clustering item for column - '{column_name}'")
        
        # Step 1: Cluster
        cluster_prompt = f"""
        Group the following {column_name} into clusters of similar or related items.
        Output only clusters by descending order. no explanation.

        {column_name}:
        {data}
        """
        
        clusters = self._ask_ollama(
            prompt=cluster_prompt, 
            model=self.clustering_model
        )

        return clusters
    
    
    def _categorize_cluster(self, column_name: str, clusters: str) -> str:
        
        self.logger.info(f"Clustering item for column - '{column_name}'")
        
        category_prompt = f"""
        Categorize the following {column_name} clusters into high-level categories by descending order.

        Clusters:
        {clusters}
        """
        categories = self._ask_ollama(
            prompt=category_prompt, 
            model=self.categorizing_model
        )
        
        return categories
    
    
    def _generate_insights(self, column_name: str, categories: str) -> str:
         
        self.logger.info(f"Clustering item for column - '{column_name}'") 
        # Step 3: Insights
        insight_prompt = f"""
        Based on the categorized {column_name}, extract insights such as:
        - most common {column_name} areas

        Categorized {column_name}:
        {categories}
        """
        insights = self._ask_ollama(
            prompt=insight_prompt, 
            model=self.gen_insight_model
        )
        
        return insights
    
     
    def process_items_to_insights(self, column: str, data: list[str]) -> dict:
        
        column_name = column.replace("_", " ").capitalize()
        
        # consolidate the results into a dictionary.
        dict = {}
        
        clusters = self._cluster_items(column_name=column_name, data=data)
        categories = self._categorize_cluster(column_name=column_name, clusters=clusters)
        insights = self._generate_insights(column_name=column_name, categories=categories)
        
        dict[column] = column_name
        dict["clusters"] = clusters
        dict["categories"] = categories
        dict["insights"] = insights

        return dict