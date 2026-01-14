from unittest.mock import MagicMock
from src.critic import CriticAgent, AgentState
from langchain_core.documents import Document

if __name__ == "__main__":
    # Mock LLM
    mock_llm = MagicMock()
    
    # Instantiate agent with mock LLM
    agent = CriticAgent(llm=mock_llm)
    
    # Mock the chain invoke to avoid executing real prompt/LLM
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = "Contradiction found: Paper A claims coffee is good, while Paper B claims it decreases performance."
    agent.chain = mock_chain

    # Test data
    docs = [
        Document(page_content="Coffee improves performance.", metadata={"author": "Doe", "year": "2023", "source": "A.pdf"}),
        Document(page_content="Coffee decreases performance.", metadata={"author": "Smith", "year": "2024", "source": "B.pdf"})
    ]
    state = {"query": "Does coffee improve performance?", "documents": docs, "critique": ""}
    
    # Run analysis
    result = agent.analyze(state)
    
    print("Critique Result:")
    print(result["critique"])
    
    # Verify input to chain
    args, _ = mock_chain.invoke.call_args
    print("\nInput passed to chain:")
    print(args[0]['context'])
