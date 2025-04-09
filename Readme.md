
---

# Blog Generator with LangChain & Groq

This project creates a blog generator using the Groq model and LangChain's graph-based system. It allows for generating blog content and reviewing it through a series of interconnected steps. The goal is to automate the process of blog generation and reviewing using a custom pipeline.

### Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.8 or higher
- Required libraries and dependencies

You can install the necessary dependencies by running:

```bash
pip install langchain langgraph langchain_groq python-dotenv
```

### Setup

1. **Create a `.env` file**:
   Create a `.env` file in the root directory of the project to store your API keys.

   ```bash
   GROQ_API_KEY=your_groq_api_key
   LANGCHAIN_API_KEY=your_langchain_api_key
   ```

2. **Environment Variables**:
   - `GROQ_API_KEY`: API key for accessing the Groq model.
   - `LANGCHAIN_API_KEY`: API key for LangChain.

   These keys are loaded using the `dotenv` library.

### Code Overview

- **Imports**:
    - The `langchain_core`, `langgraph`, and `langchain_groq` libraries are used to create and run the blog generation and review pipeline.
    - Environment variables are loaded via the `dotenv` library for API keys.

- **LLM Initialization**:
    - The LLM (Groq model) is initialized using `ChatGroq` with the model `gemma2-9b-it`.

- **State Structure**:
    - The `State` class is used to define the structure of the workflow, which includes a list of messages.

- **Blog Generation**:
    - A simple `blog_generator` function generates blog content based on the provided state and system message ("write a blog").
    - This function calls the Groq model and returns the result.

- **Blog Review**:
    - The `blog_reviewer` function is a placeholder for future review logic (e.g., checking grammar or suggesting improvements).

- **Graph Workflow**:
    - A graph workflow is defined using `StateGraph` from LangGraph.
    - The graph consists of two nodes: the `Blog Generator` and `Blog Reviewer`, connected sequentially.
    - The workflow is compiled and executed using `graph_workflow.compile()`.

### Running the Blog Generator

To run the blog generator, simply execute the script. Here's an example of how to run the blog generation and review process:

```python
from langchain_core.messages import SystemMessage
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

# Initialize environment variables and LLM
load_dotenv()

# Function to create and run the graph
def run_blog_generator():
    result = make_alternative_graph()  # Create the graph
    return result  # The result will contain the generated blog and review flow

# Run the blog generator
run_blog_generator()
```

### Workflow Diagram

The generated workflow consists of the following steps:
1. **Blog Generator**: Generates the blog content.
2. **Blog Reviewer**: (Currently empty) This node can later be filled with logic for reviewing and enhancing the generated content.

### Extending the Project

1. **Add Review Logic**: You can modify the `blog_reviewer` function to add review logic (e.g., grammar checks, content analysis).
2. **Custom Messages**: You can modify the `SystemMessage` to include different instructions for the blog generator.
3. **Multiple Outputs**: You can extend the graph to include more nodes for additional steps like content optimization, SEO checks, etc.

### License

This project is open source. Feel free to fork, modify, and contribute!

---
