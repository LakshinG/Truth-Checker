from typing import List, Dict
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
)
# Depending on Ragas version, these might be imported differently or initialized.
# For 0.4.x, they are usually objects.

def run_ragas_evaluation(
    questions: List[str],
    answers: List[str],
    contexts: List[List[str]],
    ground_truths: List[List[str]]
) -> Dict:
    """
    Runs RAGAs evaluation metrics on the provided data.
    
    Args:
        questions: List of user queries.
        answers: List of generated answers/critiques.
        contexts: List of lists of retrieved context strings.
        ground_truths: List of lists of ground truth strings (required for context_recall).
        
    Returns:
        Dictionary containing the evaluation results.
    """
    
    data = {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths
    }
    
    # Create HuggingFace Dataset
    dataset = Dataset.from_dict(data)
    
    # Run evaluation
    # Note: This requires OPENAI_API_KEY to be set in the environment
    try:
        results = evaluate(
            dataset=dataset,
            metrics=[
                faithfulness,
                answer_relevancy,
                context_recall,
            ],
        )
        return results
    except Exception as e:
        print(f"Error running RAGAs evaluation: {e}")
        return {"error": str(e)}
