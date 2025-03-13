import unittest
import os
import sys
from pathlib import Path
import docker
import requests
from sqlalchemy import create_engine, text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SystemValidationTest(unittest.TestCase):
    def setUp(self):
        self.root_path = Path("C:/AlgoTradPro5")
        self.required_directories = [
            "models/llm", "models/ml", "src/core", "data", 
            "trade_logs", "frontend"
        ]
        self.docker_client = docker.from_env()

    def test_1_directory_structure(self):
        """Verify all required directories exist"""
        for dir_path in self.required_directories:
            full_path = self.root_path / dir_path
            self.assertTrue(full_path.exists(), f"Missing directory: {dir_path}")

    def test_2_docker_setup(self):
        """Verify Docker is running and FreqTrade container exists"""
        containers = self.docker_client.containers.list()
        freqtrade_running = any("freqtrade" in container.name for container in containers)
        self.assertTrue(freqtrade_running, "FreqTrade container not running")

    def test_3_model_availability(self):
        """Check if required AI models are present"""
        required_llm_models = ["deepseek", "mistral", "mixtral", "qwen"]
        llm_path = self.root_path / "models/llm"
        for model in required_llm_models:
            model_exists = any(Path(llm_path).glob(f"*{model}*"))
            self.assertTrue(model_exists, f"Missing LLM model: {model}")

    def test_4_database_connection(self):
        """Test SQL database connectivity"""
        try:
            engine = create_engine('sqlite:///C:/AlgoTradPro5/data/trading.db')
            with engine.connect() as conn:
                result = conn.execute(text('SELECT 1'))
                self.assertEqual(result.scalar(), 1)
        except Exception as e:
            self.fail(f"Database connection failed: {e}")

    def test_5_freqtrade_api(self):
        """Test FreqTrade API connectivity"""
        try:
            response = requests.get('http://localhost:8080/api/v1/ping')
            self.assertEqual(response.status_code, 200)
        except requests.exceptions.RequestException:
            self.fail("FreqTrade API not accessible")

    def test_6_environment_variables(self):
        """Verify required environment variables"""
        required_vars = [
            'FREQTRADE_API_KEY',
            'DATABASE_URL',
            'INITIAL_CAPITAL',
            'RISK_PERCENTAGE'
        ]
        for var in required_vars:
            self.assertIsNotNone(os.getenv(var), f"Missing environment variable: {var}")

if __name__ == '__main__':
    unittest.main(verbosity=2)
