import streamlit as st
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from typing_extensions import TypedDict
from langgraph.graph import add_messages, StateGraph, END, START
from langchain_core.messages import AIMessage
from typing import Annotated, List, Dict, Any
from langdetect import detect

## Langsmith Tracking
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"]="Blog Generator"
if 'blog_state' not in st.session_state:
    st.session_state.blog_state = None
if 'graph' not in st.session_state:
    st.session_state.graph = None
if 'graph_image' not in st.session_state:
    st.session_state.graph_image = None


# Define BlogState TypedDict
class BlogState(TypedDict):
    topic: str
    title: str
    blog_content: Annotated[List, add_messages]
    reviewed_content: Annotated[List, add_messages]





# Node functions with state management
def generate_title(state: BlogState):
    prompt = f"""Generate compelling blog title options about {state["topic"]} that are:
    - SEO-friendly
    - Attention-grabbing
    - Between 6-12 words"""
    
    
    response = llm.invoke(prompt)
    state["title"] = response.content.split("\n")[0].strip('"')
    return state


def generate_content(state: BlogState):
    prompt = f"""Write a comprehensive blog post titled "{state['title']}" with:
    1. Engaging introduction with hook
    2. 3-5 subheadings with detailed content
    3. Practical examples/statistics
    4. Clear transitions between sections
    5. Actionable conclusion
    Style: Professional yet conversational (Flesch-Kincaid 60-70). Use markdown formatting"""
    
    with st.status("📝 Generating Content..."):
        response = llm.invoke(prompt)
        state["blog_content"].append(AIMessage(content=response.content))
        st.markdown(response.content)
    return state

def review_content(state: BlogState):
    content = state["blog_content"][-1].content
    prompt = f"""Critically review this blog content:
    - Clarity & Structure
    - Grammar & Style
    - SEO optimization
    - Reader engagement
    Provide specific improvement suggestions. Content:\n{content}"""
    
    with st.status("🔍 Reviewing Content..."):
        feedback = llm.invoke(prompt)
        state["reviewed_content"].append(AIMessage(content=feedback.content))
        st.write(feedback.content)
    return state
def update_content(state: BlogState):
    content = state["blog_content"][-1].content
    feedback = state["reviewed_content"][-1].content
    
    prompt = f"""Revise the blog content based on the given  feedback:
    Content: {content}
    Feedback: {feedback}
    Revise the content to improve clarity, grammar, SEO, and engagement. Use markdown formatting."""
    
    with st.status("🔄 Updating Content..."):
        response = llm.invoke(prompt)
        state["blog_content"].append(AIMessage(content=response.content))
        st.write(response.content)
    return state

def init_graph(api_key: str):
    
    global llm
    llm  = ChatGroq(model="qwen-2.5-32b", api_key=api_key)
    
    builder = StateGraph(BlogState)
    
    builder.add_node("title_generator", generate_title) ## Generate Title
    builder.add_node("content_generator", generate_content) ## Generate Content using the output of title_generator and search_web
    builder.add_node("content_reviewer", review_content) ## Review Content and generate feedback
    builder.add_node("content_updater", update_content)

    builder.add_edge(START, "title_generator")
    builder.add_edge("title_generator", "content_generator")
    builder.add_edge("content_generator", "content_reviewer")

    builder.add_edge("content_reviewer", "content_updater")
    builder.add_edge("content_updater", END)
    graph=builder.compile()
    from IPython.display import Image, display

    display(Image(graph.get_graph().draw_mermaid_png()))
    return builder.compile()






# Streamlit UI components
st.title("🚀 Blog Creator Agent")
st.markdown("""
**Smart Blog Generation with Auto-Refinement**  

""")

# Sidebar components
with st.sidebar:

    st.subheader("Configuration")
        
    # Groq API Key Input
    api_key = st.text_input("Groq API Key:", 
                          type="password",
                          value=os.getenv("GROQ_API_KEY", ""))
    
     # Validate API key
    if not api_key:
        st.warning("⚠️ Please enter your GROQ API key to proceed. Don't have? refer : https://console.groq.com/keys ")
        


        
        
    st.subheader("Workflow Overview")
    st.image("workflow_graph.png")



        
# Main content
topic = st.text_input("Enter your blog topic:", placeholder="Generative AI in Healthcare")
generate_btn = st.button("Generate Blog Post")

if generate_btn:
    if not api_key:
        st.error("Please provide a Groq API key in the sidebar!")
        st.stop()
    
    if not topic:
        st.error("Please enter a blog topic!")
        st.stop()
    
    try:
        
        # Initialize and run graph
        st.session_state.graph = init_graph(api_key)
        
        st.session_state.blog_state = BlogState(
            topic=topic,
            title="",
           # search_results=[],
            blog_content=[],
            reviewed_content=[],
           # is_blog_ready=""
        )
        
        # Execute the graph
        final_state = st.session_state.graph.invoke(st.session_state.blog_state)
        st.session_state.blog_state = final_state
        
        
        # Display results
        st.success("Blog post generation complete!")
        st.markdown("---")
        st.subheader("Final Blog Post")
        st.markdown(final_state["blog_content"][-1].content)
        
        st.markdown("---")
        st.subheader("Generated Title")
        st.write(final_state["title"])

        st.markdown("---")
        st.subheader("Quality Assurance Report")
        st.write(final_state["reviewed_content"][-1].content)
        
        if st.session_state.blog_state:
        
            
            st.write(f"**Topic:** {st.session_state.blog_state['topic']}")
            
            st.write(f"**Review Cycles**: {len(st.session_state.blog_state['reviewed_content']) - 1}")
        
    except Exception as e:
        st.error(f"Error in blog generation: {str(e)}")