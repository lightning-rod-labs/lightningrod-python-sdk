import os
from typing import Optional


def get_secret(secret_name: str, default: Optional[str] = None) -> str:
    """
    Read a secret from environment variables, supporting both local and Google Colab environments.
    
    In Google Colab, reads from Colab Secrets using userdata.get().
    Locally, reads from .env file using python-dotenv.
    
    Args:
        secret_name: Name of the secret/environment variable to read
        default: Default value if secret is not found (only used for optional secrets)
        
    Returns:
        The secret value, or default if not found (for optional secrets)
        
    Raises:
        ValueError: If a required secret is not set
    """
    value = default
    
    try:
        from google.colab import userdata
        try:
            value = userdata.get(secret_name)
        except Exception:
            value = None
    except ImportError:
        from dotenv import load_dotenv
        load_dotenv()
        value = os.getenv(secret_name)
    
    if not value:
        raise ValueError(f"{secret_name} is not set. In Colab, set it via Secrets. Locally, set it in .env file.")
    
    return value
