import httpx
import logging
import os
from typing import List, Dict, Any, Optional
import jinja2

logger = logging.getLogger("ai_platform.rag_orchestrator")

class RAGOrchestrator:
    """
    A class to orchestrate the Retrieval-Augmented Generation process.
    """
    
    def __init__(self, retriever_url=None, text_gen_url=None):
        """
        Initialize the RAG Orchestrator with service URLs.
        
        Args:
            retriever_url: URL of the retriever service
            text_gen_url: URL of the text generation service
        """
        self.retriever_url = retriever_url or os.getenv("RETRIEVER_SERVICE_URL", "http://retriever:8000")
        self.text_gen_url = text_gen_url or os.getenv("TEXT_GEN_SERVICE_URL", "http://text-gen:8000")
        
        # Initialize template environment for prompt construction
        self.template_env = jinja2.Environment(
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        logger.info(f"RAG Orchestrator initialized with retriever URL: {self.retriever_url} and text-gen URL: {self.text_gen_url}")
    
    async def retrieve_documents(self, query: str, collection_name: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a query.
        
        Args:
            query: The query text
            collection_name: The name of the collection to query
            n_results: Number of results to return
            
        Returns:
            List of retrieved documents
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.retriever_url}/retrieve",
                    json={
                        "query": query,
                        "collection_name": collection_name,
                        "n_results": n_results
                    }
                )
                
                if response.status_code != 200:
                    logger.error(f"Error retrieving documents: {response.text}")
                    return []
                
                result = response.json()
                return result.get("documents", [])
                
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            return []
    
    def construct_prompt(self, query: str, documents: List[Dict[str, Any]]) -> str:
        """
        Construct a prompt for the text generation model using the retrieved documents.
        
        Args:
            query: The original query
            documents: The retrieved documents
            
        Returns:
            A formatted prompt string
        """
        # Simple prompt template
        template_str = """
        Answer the following question based on the provided context.
        
        Context:
        {% for doc in documents %}
        {{ doc.text }}
        {% endfor %}
        
        Question: {{ query }}
        
        Answer:
        """
        
        template = self.template_env.from_string(template_str)
        prompt = template.render(query=query, documents=documents)
        
        return prompt.strip()
    
    async def generate_text(self, prompt: str) -> str:
        """
        Generate text using the text generation service.
        
        Args:
            prompt: The prompt for text generation
            
        Returns:
            Generated text
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.text_gen_url}/generate",
                    params={"text": prompt}
                )
                
                if response.status_code != 200:
                    logger.error(f"Error generating text: {response.text}")
                    return "Error generating response."
                
                result = response.json()
                return result.get("generated_text", "No text generated.")
                
        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            return f"Error: {str(e)}"
    
    async def process_query(self, query: str, collection_name: str, n_results: int = 5) -> Dict[str, Any]:
        """
        Process a query through the full RAG pipeline.
        
        Args:
            query: The query text
            collection_name: The name of the collection to query
            n_results: Number of results to return from retrieval
            
        Returns:
            A dictionary containing the generated answer and retrieved documents
        """
        # Step 1: Retrieve relevant documents
        documents = await self.retrieve_documents(query, collection_name, n_results)
        
        if not documents:
            return {
                "answer": "I couldn't find any relevant information to answer your question.",
                "documents": []
            }
        
        # Step 2: Construct a prompt using the retrieved documents
        prompt = self.construct_prompt(query, documents)
        
        # Step 3: Generate text using the constructed prompt
        answer = await self.generate_text(prompt)
        
        return {
            "answer": answer,
            "documents": documents
        }
    
    async def list_collections(self) -> List[str]:
        """
        List all available collections.
        
        Returns:
            List of collection names
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.retriever_url}/collections")
                
                if response.status_code != 200:
                    logger.error(f"Error listing collections: {response.text}")
                    return []
                
                result = response.json()
                return result.get("collections", [])
                
        except Exception as e:
            logger.error(f"Error listing collections: {str(e)}")
            return []
