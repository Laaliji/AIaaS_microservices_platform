import os
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import logging

logger = logging.getLogger("ai_platform.vector_db")

class ChromaClient:
    """
    A wrapper around ChromaDB client to handle vector database operations.
    """
    
    def __init__(self, persist_directory="./chroma_db"):
        """
        Initialize the ChromaDB client.
        
        Args:
            persist_directory: Directory to persist the database
        """
        self.persist_directory = persist_directory
        
        # Create the directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)
        
        # Initialize the client
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Use sentence-transformers for embedding
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        logger.info(f"ChromaDB client initialized with persist directory: {persist_directory}")
    
    def create_collection(self, collection_name):
        """
        Create a new collection or get an existing one.
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            The collection object
        """
        try:
            collection = self.client.get_or_create_collection(
                name=collection_name,
                embedding_function=self.embedding_function
            )
            logger.info(f"Collection '{collection_name}' created or retrieved")
            return collection
        except Exception as e:
            logger.error(f"Error creating collection '{collection_name}': {str(e)}")
            raise
    
    def add_documents(self, collection_name, documents, metadatas=None, ids=None):
        """
        Add documents to a collection.
        
        Args:
            collection_name: Name of the collection
            documents: List of document texts
            metadatas: List of metadata dictionaries
            ids: List of document IDs
            
        Returns:
            Result of the add operation
        """
        collection = self.create_collection(collection_name)
        
        if ids is None:
            # Generate IDs if not provided
            ids = [f"doc_{i}" for i in range(len(documents))]
        
        if metadatas is None:
            # Create empty metadata if not provided
            metadatas = [{} for _ in range(len(documents))]
        
        try:
            result = collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"Added {len(documents)} documents to collection '{collection_name}'")
            return result
        except Exception as e:
            logger.error(f"Error adding documents to collection '{collection_name}': {str(e)}")
            raise
    
    def query(self, collection_name, query_text, n_results=5):
        """
        Query the collection for similar documents.
        
        Args:
            collection_name: Name of the collection
            query_text: Text to query
            n_results: Number of results to return
            
        Returns:
            Query results
        """
        collection = self.create_collection(collection_name)
        
        try:
            results = collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            logger.info(f"Query executed on collection '{collection_name}' with {n_results} results")
            return results
        except Exception as e:
            logger.error(f"Error querying collection '{collection_name}': {str(e)}")
            raise
    
    def get_collection_info(self, collection_name):
        """
        Get information about a collection.
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            Collection information
        """
        collection = self.create_collection(collection_name)
        
        try:
            count = collection.count()
            return {
                "name": collection_name,
                "count": count
            }
        except Exception as e:
            logger.error(f"Error getting collection info for '{collection_name}': {str(e)}")
            raise
    
    def list_collections(self):
        """
        List all collections in the database.
        
        Returns:
            List of collection names
        """
        try:
            collections = self.client.list_collections()
            return [collection.name for collection in collections]
        except Exception as e:
            logger.error(f"Error listing collections: {str(e)}")
            raise
    
    def delete_collection(self, collection_name):
        """
        Delete a collection.
        
        Args:
            collection_name: Name of the collection
        """
        try:
            self.client.delete_collection(collection_name)
            logger.info(f"Collection '{collection_name}' deleted")
            return True
        except Exception as e:
            logger.error(f"Error deleting collection '{collection_name}': {str(e)}")
            raise
