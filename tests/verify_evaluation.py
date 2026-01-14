from unittest.mock import patch, MagicMock
from src.evaluation import run_ragas_evaluation

@patch("src.evaluation.evaluate")
def run_test(mock_evaluate):
    # Mock the return value of evaluate
    mock_evaluate.return_value = {"faithfulness": 0.9, "answer_relevancy": 0.8, "context_recall": 0.95}
    
    questions = ["Does coffee improve code?"]
    answers = ["Yes, according to Paper A."]
    contexts = [["Paper A says coffee improves code."]]
    ground_truths = [["Coffee improves code."]]
    
    print("Running evaluation test...")
    res = run_ragas_evaluation(questions, answers, contexts, ground_truths)
    
    print("Evaluation Results:", res)
    
    # Verify evaluate was called
    mock_evaluate.assert_called_once()
    args, kwargs = mock_evaluate.call_args
    dataset = kwargs.get('dataset')
    if not dataset:
        dataset = args[0] if args else None
        
    if dataset:
        print("Dataset created with:", dataset.column_names)

if __name__ == "__main__":
    run_test()
