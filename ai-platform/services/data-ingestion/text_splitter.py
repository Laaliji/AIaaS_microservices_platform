import re
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger("ai_platform.data_ingestion")

class TextSplitter:
    """
    A class to split text into chunks of appropriate size for embedding.
    """
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the text splitter.
        
        Args:
            chunk_size: Maximum size of each chunk in characters
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        logger.info(f"TextSplitter initialized with chunk_size={chunk_size}, chunk_overlap={chunk_overlap}")
    
    def split_text(self, text: str) -> List[str]:
        """
        Split text into chunks.
        
        Args:
            text: The text to split
            
        Returns:
            List of text chunks
        """
        if not text or len(text.strip()) == 0:
            return []
        
        # Normalize line breaks
        text = re.sub(r'\r\n', '\n', text)
        text = re.sub(r'\r', '\n', text)
        
        # First try to split by paragraphs
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = []
        current_length = 0
        
        # Process each paragraph
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
                
            paragraph_length = len(paragraph)
            
            # If a single paragraph is too long, split it by sentences
            if paragraph_length > self.chunk_size:
                paragraph_chunks = self._split_paragraph(paragraph)
                for chunk in paragraph_chunks:
                    if current_length + len(chunk) + (1 if current_chunk else 0) <= self.chunk_size:
                        if current_chunk:
                            current_chunk.append('\n\n')
                        current_chunk.append(chunk)
                        current_length += len(chunk) + (2 if current_chunk else 0)
                    else:
                        if current_chunk:
                            chunks.append(''.join(current_chunk))
                        current_chunk = [chunk]
                        current_length = len(chunk)
            else:
                # Add paragraph to current chunk if it fits
                if current_length + paragraph_length + (2 if current_chunk else 0) <= self.chunk_size:
                    if current_chunk:
                        current_chunk.append('\n\n')
                    current_chunk.append(paragraph)
                    current_length += paragraph_length + (2 if current_chunk else 0)
                else:
                    # Finish current chunk and start a new one
                    if current_chunk:
                        chunks.append(''.join(current_chunk))
                    current_chunk = [paragraph]
                    current_length = paragraph_length
        
        # Add the last chunk if it's not empty
        if current_chunk:
            chunks.append(''.join(current_chunk))
        
        # Apply overlap if needed
        if self.chunk_overlap > 0 and len(chunks) > 1:
            chunks = self._apply_overlap(chunks)
        
        logger.info(f"Split text into {len(chunks)} chunks")
        return chunks
    
    def _split_paragraph(self, paragraph: str) -> List[str]:
        """
        Split a paragraph into smaller chunks by sentences.
        
        Args:
            paragraph: The paragraph to split
            
        Returns:
            List of sentence chunks
        """
        # Simple sentence splitting by common punctuation
        sentences = re.split(r'(?<=[.!?])\s+', paragraph)
        
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            sentence_length = len(sentence)
            
            # If a single sentence is too long, split it by character count
            if sentence_length > self.chunk_size:
                sentence_chunks = [sentence[i:i+self.chunk_size] for i in range(0, len(sentence), self.chunk_size)]
                chunks.extend(sentence_chunks)
            else:
                # Add sentence to current chunk if it fits
                if current_length + sentence_length + (1 if current_chunk else 0) <= self.chunk_size:
                    if current_chunk:
                        current_chunk.append(' ')
                    current_chunk.append(sentence)
                    current_length += sentence_length + (1 if current_chunk else 0)
                else:
                    # Finish current chunk and start a new one
                    if current_chunk:
                        chunks.append(''.join(current_chunk))
                    current_chunk = [sentence]
                    current_length = sentence_length
        
        # Add the last chunk if it's not empty
        if current_chunk:
            chunks.append(''.join(current_chunk))
            
        return chunks
    
    def _apply_overlap(self, chunks: List[str]) -> List[str]:
        """
        Apply overlap between chunks.
        
        Args:
            chunks: List of text chunks
            
        Returns:
            List of overlapping text chunks
        """
        if len(chunks) <= 1:
            return chunks
            
        result = []
        for i in range(len(chunks)):
            if i == 0:
                # First chunk remains as is
                result.append(chunks[i])
            else:
                # For subsequent chunks, try to include overlap from previous chunk
                prev_chunk = chunks[i-1]
                current_chunk = chunks[i]
                
                # Calculate how much text to take from the end of the previous chunk
                overlap_size = min(self.chunk_overlap, len(prev_chunk))
                overlap_text = prev_chunk[-overlap_size:]
                
                # Ensure we don't exceed chunk_size
                available_size = self.chunk_size - overlap_size
                if available_size < len(current_chunk):
                    current_chunk = current_chunk[:available_size]
                    
                result.append(overlap_text + current_chunk)
                
        return result
