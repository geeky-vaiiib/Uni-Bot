"""
SIT RAG Chatbot - Context Prompt Builder
Builds the context injection template that treats retrieved chunks as the sole source of truth.
"""

from typing import List, Dict, Any


def build_context_prompt(
    retrieved_chunks: List[Dict[str, Any]],
    user_query: str,
    mode_instruction: str = ""
) -> str:
    """
    Build the context-aware prompt for the LLM.
    
    Args:
        retrieved_chunks: List of retrieved document chunks with metadata
        user_query: The user's original question
        mode_instruction: Mode-specific instruction (student/exam/faculty)
    
    Returns:
        Formatted prompt with context injection
    """
    
    # Build context section from retrieved chunks
    if not retrieved_chunks:
        context_section = "<context>\nNo relevant documents found in the SIT knowledge base.\n</context>"
    else:
        context_parts = []
        for i, chunk in enumerate(retrieved_chunks, 1):
            source = chunk.get("source", "Unknown Document")
            page = chunk.get("page", "N/A")
            section = chunk.get("section", "")
            content = chunk.get("content", "")
            
            chunk_header = f"[Document {i}]"
            chunk_meta = f"Source: {source}"
            if page != "N/A":
                chunk_meta += f" | Page: {page}"
            if section:
                chunk_meta += f" | Section: {section}"
            
            context_parts.append(f"{chunk_header}\n{chunk_meta}\n---\n{content}")
        
        context_section = "<context>\n" + "\n\n".join(context_parts) + "\n</context>"
    
    # Build the complete prompt
    prompt = f"""
{context_section}

<instructions>
CRITICAL: Your response MUST be based ONLY on the information provided in the <context> section above.
- If the answer is found in the context, respond accurately and cite the source.
- If the answer is NOT found in the context, respond with the standard refusal message.
- Do NOT use any external knowledge or make assumptions.
{mode_instruction}
</instructions>

<user_query>
{user_query}
</user_query>

Provide your response:"""
    
    return prompt.strip()


def build_retrieval_query(user_query: str) -> str:
    """
    Optionally enhance the user query for better retrieval.
    
    Args:
        user_query: Original user question
    
    Returns:
        Enhanced query for vector search
    """
    # For now, return as-is. Can be enhanced with query expansion.
    return user_query


# Template for when context is empty
EMPTY_CONTEXT_TEMPLATE = """
<context>
No relevant documents were found in the SIT knowledge base for this query.
</context>

<instructions>
Since no relevant information was found, you MUST respond with the standard refusal message.
Do NOT attempt to answer from general knowledge.
</instructions>

<user_query>
{user_query}
</user_query>

Provide your response:"""
