# RAG System with Session Management and Cost Calculation

This project implements a Retrieval-Augmented Generation (RAG) system that processes user queries, optimizes them using an AI agent, retrieves relevant content, and generates responses using a specified model (e.g., deepseek-chat or deepseek-reasoner). The system also manages chat history, calculates API token costs, and updates the conversation context automatically.

## Key Features

### Session Management
- Each query is associated with a `session_id` to maintain chat history across multiple interactions.

### Query Optimization
- If no chat history exists, the system uses an AI agent to optimize the user's query for better search results.

### RAG Search
- The optimized query is passed to the RAG system to retrieve relevant content.

### Response Generation
- The system generates a response using the specified model, taking into account the chat history (if available).

### Token Cost Calculation
- The system calculates the cost of API usage based on the model and the number of tokens used.

### Chat History Update
- After each interaction, the system automatically updates the chat history with the query and response.

## How It Works

### 1. User Sends a Query
- The user sends a query along with a `session_id`.
- If no chat history exists for the `session_id`, the query is optimized using an AI agent.

### 2. RAG Search
- The optimized query is passed to the RAG system to retrieve relevant content.

### 3. Response Generation
- The system generates a response using the specified model (e.g., deepseek-chat or deepseek-reasoner).
- The response is generated based on the retrieved content and the chat history (if available).

### 4. Token Cost Calculation
- The system calculates the cost of API usage based on the model and the number of tokens used.

### 5. Update Chat History
- The system updates the chat history with the query and response for future interactions.

### 6. Return Response
- The final response is returned to the user.

## Example Workflow

### Input:
```json
  "session_id": "12345",
  "query": "What is the capital of France?",
  "model": "deepseek-chat"
```
### Process:
- If no chat history exists, the query is optimized (e.g., "Tell me about the capital of France").
- The optimized query is passed to the RAG system, which retrieves relevant content.
- The model generates a response (e.g., "The capital of France is Paris.").
- The token cost is calculated based on the model and tokens used.
- The chat history is updated with the query and response.

### Output:
```json
  "response": "The capital of France is Paris.",
  "token_cost": 0.0025
