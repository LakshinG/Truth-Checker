import os
import sys
from unittest.mock import patch, MagicMock

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.vector_store import VectorStoreManager
from src.critic import CriticAgent
from src.ingestion import IngestionPipeline

def test_provider_switching():
    print("Testing Provider Switching...")
    
    # Save original env
    original_openai = os.environ.get("OPENAI_API_KEY")
    original_google = os.environ.get("GOOGLE_API_KEY")
    
    try:
        # Scenario 1: Only Google Key is present
        if "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]
        os.environ["GOOGLE_API_KEY"] = "dummy_google_key"
        
        print("\n[Scenario 1] Only GOOGLE_API_KEY present")
        
        # Test Vector Store
        try:
            print("Initializing VectorStoreManager...")
            # We mock GoogleGenerativeAIEmbeddings to avoid actual init issues with dummy keys if any
            with patch('src.vector_store.GoogleGenerativeAIEmbeddings') as MockGoogleEmbeddings:
                vm = VectorStoreManager(persist_directory="./test_db_provider")
                print("VectorStoreManager initialized.")
                if MockGoogleEmbeddings.called:
                    print("SUCCESS: GoogleGenerativeAIEmbeddings was instantiated.")
                else:
                    print("FAILURE: GoogleGenerativeAIEmbeddings was NOT instantiated.")
        except Exception as e:
            print(f"FAILURE: VectorStoreManager init failed: {e}")

        # Test Critic Agent
        try:
            print("Initializing CriticAgent...")
            with patch('src.critic.ChatGoogleGenerativeAI') as MockChatGoogle:
                critic = CriticAgent()
                print("CriticAgent initialized.")
                if MockChatGoogle.called:
                    print("SUCCESS: ChatGoogleGenerativeAI was instantiated.")
                else:
                    print("FAILURE: ChatGoogleGenerativeAI was NOT instantiated.")
        except Exception as e:
            print(f"FAILURE: CriticAgent init failed: {e}")

        # Test Ingestion Pipeline
        try:
            print("Initializing IngestionPipeline...")
            with patch('src.ingestion.GoogleGenerativeAIEmbeddings') as MockGoogleEmbeddingsIngest:
                ip = IngestionPipeline()
                print("IngestionPipeline initialized.")
                if MockGoogleEmbeddingsIngest.called:
                    print("SUCCESS: GoogleGenerativeAIEmbeddings was instantiated for Ingestion.")
                else:
                    print("FAILURE: GoogleGenerativeAIEmbeddings was NOT instantiated for Ingestion.")
        except Exception as e:
            print(f"FAILURE: IngestionPipeline init failed: {e}")

        # Scenario 2: Only OpenAI Key is present
        if "GOOGLE_API_KEY" in os.environ:
            del os.environ["GOOGLE_API_KEY"]
        os.environ["OPENAI_API_KEY"] = "dummy_openai_key"
        
        print("\n[Scenario 2] Only OPENAI_API_KEY present")
        
        try:
            print("Initializing VectorStoreManager...")
            with patch('src.vector_store.OpenAIEmbeddings') as MockOpenAIEmbeddings:
                vm = VectorStoreManager(persist_directory="./test_db_provider")
                if MockOpenAIEmbeddings.called:
                    print("SUCCESS: OpenAIEmbeddings was instantiated.")
                else:
                    print("FAILURE: OpenAIEmbeddings was NOT instantiated.")
        except Exception as e:
            print(f"FAILURE: VectorStoreManager init failed: {e}")

    finally:
        # Restore env
        if original_openai:
            os.environ["OPENAI_API_KEY"] = original_openai
        elif "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]
            
        if original_google:
            os.environ["GOOGLE_API_KEY"] = original_google
        elif "GOOGLE_API_KEY" in os.environ:
            del os.environ["GOOGLE_API_KEY"]

if __name__ == "__main__":
    test_provider_switching()
