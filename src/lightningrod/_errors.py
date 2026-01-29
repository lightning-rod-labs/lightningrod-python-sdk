import json
from http import HTTPStatus
from typing import Any, TypeVar

from lightningrod._display import display_error
from lightningrod._generated.models import HTTPValidationError
from lightningrod._generated.types import Response

T = TypeVar("T")


def extract_error_message(response: Response[Any], operation: str) -> str:
    """
    Extract a detailed error message from a Response object.
    
    Args:
        response: The Response object from sync_detailed
        operation: Description of the operation that failed (e.g., "create dataset")
        
    Returns:
        A detailed error message string
    """
    if isinstance(response.parsed, HTTPValidationError):
        return f"Failed to {operation}: {response.parsed.detail}"
    
    if response.parsed is None:
        status_code = response.status_code.value if isinstance(response.status_code, HTTPStatus) else response.status_code
        
        try:
            error_data = json.loads(response.content.decode('utf-8'))
            if isinstance(error_data, dict) and 'detail' in error_data:
                detail = error_data['detail']
                return f"Failed to {operation}: {detail} (HTTP {status_code})"
            elif isinstance(error_data, dict):
                return f"Failed to {operation}: {json.dumps(error_data)} (HTTP {status_code})"
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass
        
        content_preview = response.content.decode('utf-8', errors='ignore')[:500]
        if content_preview:
            return f"Failed to {operation}: HTTP {status_code} - {content_preview}"
        else:
            return f"Failed to {operation}: HTTP {status_code} (no response body)"
    
    return f"Failed to {operation}: unexpected response format"


def handle_response_error(response: Response[T], operation: str) -> T:
    """
    Validate a Response object and return the parsed response, raising an exception if there's an error.
    
    Args:
        response: The Response object from sync_detailed
        operation: Description of the operation that failed (e.g., "create dataset")
        
    Returns:
        The parsed response object
        
    Raises:
        Exception: If the response indicates an error (parsed is None or HTTPValidationError)
    """
    if response.parsed is None or isinstance(response.parsed, HTTPValidationError):
        error_msg = extract_error_message(response, operation)
        display_error(error_msg, title=f"API Error: {operation}")
        raise Exception(error_msg)

    return response.parsed
