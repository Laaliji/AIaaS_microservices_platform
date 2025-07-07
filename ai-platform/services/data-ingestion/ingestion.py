import httpx
import logging
import os
from typing import List, Dict, Any, Optional
import uuid
import asyncio
from text_splitter import TextSplitter

logger = logging.getLogger("ai_platform.data_ingestion")

class DataIngestion:
    """
    A class to handle document ingestion into the vector database.
    """
    
    def __init__(self, vector_db_url=None, chunk_size=1000, chunk_overlap=200):
        """
        Initialize the data ingestion service.
        
        Args:
            vector_db_url: URL of the vector database service
            chunk_size: Maximum size of each chunk in characters
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.vector_db_url = vector_db_url or os.getenv("VECTOR_DB_SERVICE_URL", "http://vector-db:8000")
        self.text_splitter = TextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        logger.info(f"DataIngestion initialized with vector DB URL: {self.vector_db_url}")
    
    async def create_collection(self, collection_name: str) -> Dict[str, Any]:
        """
        Create a new collection in the vector database.
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            Result of the operation
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.vector_db_url}/collections",
                    json={"collection_name": collection_name}
                )
                
                if response.status_code != 200:
                    logger.error(f"Error creating collection: {response.text}")
                    return {"success": False, "error": response.text}
                
                result = response.json()
                logger.info(f"Created collection: {collection_name}")
                return {"success": True, "result": result}
                
        except Exception as e:
            logger.error(f"Error creating collection: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def process_document(self, text: str, metadata: Dict[str, Any], collection_name: str) -> Dict[str, Any]:
        """
        Process a document and add it to the vector database.
        
        Args:
            text: The document text
            metadata: Metadata for the document
            collection_name: Name of the collection to add the document to
            
        Returns:
            Result of the operation
        """
        try:
            # Split the text into chunks
            chunks = self.text_splitter.split_text(text)
            
            if not chunks:
                logger.warning("No chunks were created from the document")
                return {"success": False, "error": "No chunks were created from the document"}
            
            # Prepare documents for the vector database
            documents = []
            
            for i, chunk in enumerate(chunks):
                # Generate a unique ID for each chunk
                doc_id = f"{metadata.get('id', str(uuid.uuid4()))}_chunk_{i}"
                
                # Create metadata for each chunk
                chunk_metadata = {
                    **metadata,
                    "chunk_id": i,
                    "chunk_count": len(chunks)
                }
                
                documents.append({
                    "text": chunk,
                    "metadata": chunk_metadata,
                    "id": doc_id
                })
            
            # Add documents to the vector database
            result = await self._add_documents(documents, collection_name)
            
            logger.info(f"Processed document with {len(chunks)} chunks")
            return result
            
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def process_batch(self, documents: List[Dict[str, Any]], collection_name: str) -> Dict[str, Any]:
        """
        Process a batch of documents and add them to the vector database.
        
        Args:
            documents: List of documents with text and metadata
            collection_name: Name of the collection to add the documents to
            
        Returns:
            Result of the operation
        """
        try:
            results = []
            
            # Process each document
            for doc in documents:
                result = await self.process_document(
                    text=doc["text"],
                    metadata=doc.get("metadata", {}),
                    collection_name=collection_name
                )
                results.append(result)
            
            # Check if all documents were processed successfully
            success = all(result["success"] for result in results)
            
            logger.info(f"Processed batch of {len(documents)} documents, success: {success}")
            return {
                "success": success,
                "results": results
            }
            
        except Exception as e:
            logger.error(f"Error processing batch: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _add_documents(self, documents: List[Dict[str, Any]], collection_name: str) -> Dict[str, Any]:
        """
        Add documents to the vector database.
        
        Args:
            documents: List of documents with text, metadata, and ID
            collection_name: Name of the collection to add the documents to
            
        Returns:
            Result of the operation
        """
        try:
            # Format documents for the vector database
            formatted_docs = {
                "documents": [
                    {
                        "text": doc["text"],
                        "metadata": doc["metadata"],
                        "id": doc["id"]
                    }
                    for doc in documents
                ],
                "collection_name": collection_name
            }
            
            # Add documents to the vector database
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.vector_db_url}/documents",
                    json=formatted_docs
                )
                
                if response.status_code != 200:
                    logger.error(f"Error adding documents to vector DB: {response.text}")
                    return {"success": False, "error": response.text}
                
                result = response.json()
                logger.info(f"Added {len(documents)} documents to collection: {collection_name}")
                return {"success": True, "result": result}
                
        except Exception as e:
            logger.error(f"Error adding documents to vector DB: {str(e)}")
            return {"success": False, "error": str(e)}
