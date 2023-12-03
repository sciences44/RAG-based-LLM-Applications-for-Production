# This script should normally be handle by an orchestrator. Will do it once I will have a little time.

import os
from RAGbasedLLMApplicationsforProduction import config
from ray.job_submission import JobSubmissionClient

from dotenv import load_dotenv
load_dotenv()

client = JobSubmissionClient(os.getenv("RAY_ADDRESS"))

job_id = client.submit_job(
    # Entrypoint shell command to execute
    entrypoint="python ray_script.py",
    # Path to the local directory that contains the script.py file
    runtime_env={
        "env_vars": {
            "ANYSCALE_API_BASE": os.environ["ANYSCALE_API_BASE"],
            "ANYSCALE_API_KEY": os.environ["ANYSCALE_API_KEY"],
        },
        "working_dir": "./",
        "pip": [
            "matplotlib",
            "beautifulsoup4",
            "langchain",
            "sentence_transformers",
            "pymilvus",
            ],
        "num_workers": 2,
    }
)
