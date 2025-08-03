import logging
import os
from datetime import datetime

def setup_logger():
    """Sets up application logging."""
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Create logger
    logger = logging.getLogger("RelayHub")
    logger.setLevel(logging.INFO)
    
    # Create file handler with timestamp
    timestamp = datetime.now().strftime("%Y%m%d")
    log_file = f"logs/relay_hub_{timestamp}.log"
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    if not logg