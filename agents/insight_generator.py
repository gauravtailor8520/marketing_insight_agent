# File: agents/insight_generator.py
"""LangGraph agent pipeline using Gemini 2.0 Flash for marketing insights."""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
import pandas as pd
from agents.retriever import hybrid_retrieve
from agents.self_refine import self_refine

# Load Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.3,
    max_output_tokens=2048,
)

# Sample prompt template
PROMPT = ChatPromptTemplate.from_template("""
You're a marketing analyst. Analyze the campaign performance data and answer the question.

**CSV Summary**:
{csv_summary}

**Related Blog Insights**:
{related_blog_chunks}

**User Question**:
{question}

Be concise, data-backed, and actionable.
""")

# Helper to summarize DataFrame for LLM
def summarize_csv(df: pd.DataFrame) -> str:
    try:
        summary = df.describe(include='all').to_string()
        return summary[:2000]  # limit to avoid token overflow
    except Exception:
        return "Could not summarize CSV."

# Main pipeline function

def run_agent_pipeline(question: str, df: pd.DataFrame) -> dict:
    csv_summary = summarize_csv(df)
    blog_chunks = hybrid_retrieve(question)
    blog_context = "\n\n".join(blog_chunks)

    chain = PROMPT | llm
    raw_response = chain.invoke({
        "csv_summary": csv_summary,
        "related_blog_chunks": blog_context,
        "question": question
    })

    improved = self_refine(raw_response.content)

    return {
        "answer": improved,
        "evidence": blog_context
    }