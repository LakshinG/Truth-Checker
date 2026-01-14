from typing import List, Dict, TypedDict, Optional
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END
from langchain_core.language_models import BaseChatModel

class AgentState(TypedDict):
    query: str
    documents: List[Document]
    critique: str

class CriticAgent:
    def __init__(self, llm: Optional[BaseChatModel] = None, model_name: str = "gpt-4o"):
        """
        Initialize the CriticAgent.
        
        Args:
            llm: Optional BaseChatModel instance. If None, ChatOpenAI is initialized.
            model_name: Model name to use if initializing ChatOpenAI.
        """
        self.llm = llm or ChatOpenAI(model=model_name, temperature=0)
        
        # Prompt for finding contradictions
        self.contradiction_prompt = ChatPromptTemplate.from_template(
            """
            You are an expert academic researcher and critic. 
            Your task is to analyze the following set of research paper excerpts and identify any contradictions, 
            discrepancies, or conflicting methodologies/results between them regarding the user's query.

            User Query: {query}

            Retrieved Contexts:
            {context}

            Instructions:
            1. Identify the sources (Author, Year) for each claim.
            2. Explicitly point out where papers disagree (e.g., "Paper A claims X, while Paper B claims Y").
            3. Highlight differences in methodology that might explain the discrepancy (e.g., sample size, population).
            4. If there are no contradictions, state that the findings are consistent.

            Analysis:
            """
        )
        
        self.chain = self.contradiction_prompt | self.llm | StrOutputParser()

    def format_context(self, docs: List[Document]) -> str:
        formatted = []
        for i, doc in enumerate(docs):
            source = doc.metadata.get('source', 'Unknown Source')
            author = doc.metadata.get('author', 'Unknown Author')
            year = doc.metadata.get('year', 'Unknown Year')
            content = doc.page_content
            formatted.append(f"--- Document {i+1} ---\nSource: {source} (Author: {author}, Year: {year})\nContent: {content}\n")
        return "\n".join(formatted)

    def analyze(self, state: AgentState) -> Dict:
        """
        Node function for LangGraph.
        """
        query = state["query"]
        docs = state["documents"]
        
        context = self.format_context(docs)
        response = self.chain.invoke({"query": query, "context": context})
        
        return {"critique": response}

def create_research_graph(critic_agent: CriticAgent):
    """
    Creates a simple LangGraph for the research workflow.
    """
    workflow = StateGraph(AgentState)
    
    workflow.add_node("critic", critic_agent.analyze)
    
    # Entry point is critic
    workflow.set_entry_point("critic")
    workflow.add_edge("critic", END)
    
    return workflow.compile()
