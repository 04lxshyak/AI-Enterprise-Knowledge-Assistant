import tiktoken

def calculate_indexing_cost(chunks):

    price_per_1M_tokens_embedding = 0.06  # voyage 3.5
    
    encoder = tiktoken.get_encoding("cl100k_base")
    
    # Calculate total tokens across all chunks.
    total_tokens = 0
    for chunk in chunks:
        # Handle both LangChain Document objects and dicts.
        if hasattr(chunk, 'page_content'):
            text = chunk.page_content
        elif hasattr(chunk, 'text'):
            text = chunk.text
        elif isinstance(chunk, dict):
            text = chunk.get("text", "")
        else:
            text = str(chunk)
        total_tokens += len(encoder.encode(text))
    
    # Calculate embedding cost.
    embedding_cost = (total_tokens / 1000000) * price_per_1M_tokens_embedding
    
    return round(embedding_cost, 6)  # Currently embeddings only; other costs can be added later.
    


def calculate_prices(chunks, answer, query, request):
    price_per_1M_tokens_vector = 0.06  # Price per 1M tokens for vector retrieval.
    price_per_1M_tokens_llm_input = 0.15  # gpt-4o-mini
    price_per_1M_tokens_llm_output = 0.60  # gpt-4o-mini

    # Initialize the tiktoken encoder using cl100k_base for GPT-3.5/GPT-4.
    encoder = tiktoken.get_encoding("cl100k_base")
    
    # Count tokens for all chunks and the query to determine LLM input tokens.
    chunks_text = " ".join([chunk.get("text", "") for chunk in chunks])
    llm_input_text = query + " " + chunks_text
    llm_input_tokens = len(encoder.encode(llm_input_text))
    
    # Count LLM output tokens.
    llm_output_tokens = len(encoder.encode(answer))
    
    # Tokens for vector retrieval (query).
    vector_tokens = len(encoder.encode(query))
    
    # Calculate costs.
    vector_cost = (vector_tokens / 1000000) * price_per_1M_tokens_vector
    llm_input_cost = (llm_input_tokens / 1000000) * price_per_1M_tokens_llm_input
    llm_output_cost = (llm_output_tokens / 1000000) * price_per_1M_tokens_llm_output
    llm_total_cost = llm_input_cost + llm_output_cost
    

    return [vector_cost, llm_total_cost]
