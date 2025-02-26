from typing import List

def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
    """Split text into overlapping chunks of approximately the chunk size."""
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        # Find the end of the chunk
        end = min(start + chunk_size, len(text))
        
        # If we're not at the end of the text, try to find a good break point
        if end < len(text):
            # Try to break at paragraph
            next_para = text.find("\n\n", end - chunk_size // 2, end)
            if next_para != -1:
                end = next_para
            else:
                # Try to break at sentence
                next_sentence = max(
                    text.find(". ", end - chunk_size // 2, end),
                    text.find("? ", end - chunk_size // 2, end),
                    text.find("! ", end - chunk_size // 2, end)
                )
                if next_sentence != -1:
                    end = next_sentence + 2
        
        # Extract the chunk and add to the list
        chunks.append(text[start:end])
        
        # Move the start position, accounting for overlap
        start = end - chunk_overlap if end < len(text) else end
    
    return chunks 