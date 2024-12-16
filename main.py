import os
import time
import uuid
import logging
from typing import Dict

from kserve import Model, ModelServer
from fastapi.exception_handlers import RequestValidationError

import torch
from transformers import pipeline

# Logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Config
MODEL_NAME = "meta-llama/Llama-3.2-1B-Instruct"
HUGGINGFACE_AUTH_TOKEN = ""

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
logger.info(f"Using device: {DEVICE}")


class MetaLlama(Model):
    def __init__(self):
        self.name = "Meta-Llama-3.2-1B-Instruct"
        super().__init__(self.name)
         
        self.load()
        
    def load(self):
        self.pipe = pipeline(
            "text-generation",
            model=MODEL_NAME,
            device_map=DEVICE,
            token=HUGGINGFACE_AUTH_TOKEN,
        )
        
        logger.info("Model Loaded Successfully")
        self.ready = True
      
    def predict(self, payload: Dict, headers=None) -> Dict:
        request_id = uuid.uuid4()
        logger.info(f"Received request with ID: {request_id}")

        try:
            # Validate input payload
            messages = payload['messages']
            max_tokens = payload.get('max_tokens', 256)
        except KeyError:
            raise RequestValidationError(f"Request ID {request_id}: Missing field - ['messages']")

        # Generate response using specified parameters
        start_time = time.time()
        outputs = self.pipe(
            messages,
            max_new_tokens=max_tokens,
        )
        logger.info(f"Request ID {request_id}:Text Generation time - {(time.time() - start_time):.2f}")                    
        
        return outputs[0]["generated_text"][-1]

if __name__ == "__main__":
    ModelServer(http_port=8080).start([MetaLlama()])