import httpx
import logging
import os
from typing import List, Dict, Any, Optional

logger = logging.getLogger("ai_platform.retriever")

class Retriever:
    """
    A class to handle document retrieval from the vector database.
    """
    
    def __init__(self, vector_db_url=None):
        """
        Initialize the Retriever with the vector database URL.
        
        Args:
            vector_db_url: URL of the vector database service
        """
        self.vector_db_url = vector_db_url or os.getenv("VECTOR_DB_SERVICE_URL", "http://vector-db:8000")
        logger.info(f"Retriever initialized with vector DB URL: {self.vector_db_url}")
    
    async def retrieve(self, query: str, collection_name: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a query from the vector database.
        
        Args:
            query: The query text
            collection_name: The name of the collection to query
            n_results: Number of results to return
            
        Returns:
            List of retrieved documents with their metadata
        """
        try:
            async with httpx.AsyncClient() as client:
                # Query the vector database
                response = await client.post(
                    f"{self.vector_db_url}/query",
                    json={
                        "query_text": query,
                        "collection_name": collection_name,
                        "n_results": n_results
                    }
                )
                
                if response.status_code != 200:
                    logger.error(f"Error querying vector DB: {response.text}")
                    return []
                
                # Process the response
                result = response.json()
                
                # Format the results into a more usable structure
                documents = []
                
                # Check if we have results
                if "ids" in result and len(result["ids"]) > 0:
                    for i in range(len(result["ids"][0])):
                        doc = {
                            "id": result["ids"][0][i],
                            "text": result["documents"][0][i],
                            "metadata": result["metadatas"][0][i] if "metadatas" in result else {},
                            "distance": result["distances"][0][i] if "distances" in result else None
                        }
                        documents.append(doc)
                
                logger.info(f"Retrieved {len(documents)} documents for query: {query}")
                return documents
                
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            return []
    
    async def list_collections(self) -> List[str]:
        """
        List all available collections in the vector database.
        
        Returns:
            List of collection names
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.vector_db_url}/collections")
                
                if response.status_code != 200:
                    logger.error(f"Error listing collections: {response.text}")
                    return []
                
                result = response.json()
                return result.get("collections", [])
                
        except Exception as e:
            logger.error(f"Error listing collections: {str(e)}")
            return []
    
    async def get_collection_info(self, collection_name: str) -> Dict[str, Any]:
        """
        Get information about a collection.
        
        Args:
            collection_name: The name of the collection
            
        Returns:
            Collection information
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.vector_db_url}/collections/{collection_name}")
                
                if response.status_code != 200:
                    logger.error(f"Error getting collection info: {response.text}")
                    return {}
                
                return response.json()
                
        except Exception as e:
            logger.error(f"Error getting collection info: {str(e)}")
            return {}
