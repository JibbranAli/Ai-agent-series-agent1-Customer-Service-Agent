import requests
import json
from typing import Dict, Any, Optional

def http_get(url: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Make a safe HTTP GET request with proper error handling.
    
    Args:
        url (str): The URL to request
        headers (Optional[Dict[str, str]]): HTTP headers
        params (Optional[Dict[str, Any]]): Query parameters
        
    Returns:
        Dict[str, Any]: Response with status_code, success, text, and error fields
    """
    try:
        # Add default timeout and validate URL
        if not url or not url.startswith(('http://', 'https://')):
            return {
                "success": False,
                "status_code": 0,
                "text": "",
                "error": "Invalid URL format"
            }
            
        # Set default headers
        default_headers = {'User-Agent': 'CustomerServiceAgent/1.0'}
        if headers:
            default_headers.update(headers)
            
        response = requests.get(url, headers=default_headers, params=params, timeout=10)
        
        # Limit response text size to prevent memory issues
        response_text = response.text[:4000] if response.text else ""
        
        return {
            "success": True,
            "status_code": response.status_code,
            "text": response_text,
            "headers": dict(response.headers),
            "error": None
        }
        
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "status_code": 0,
            "text": "",
            "error": "Request timed out"
        }
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "status_code": 0,
            "text": "",
            "error": "Connection error"
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "status_code": 0,
            "text": "",
            "error": f"Request error: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "status_code": 0,
            "text": "",
            "error": f"Unexpected error: {str(e)}"
        }

def http_post(url: str, data: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None, 
              headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Make a safe HTTP POST request with proper error handling.
    
    Args:
        url (str): The URL to request
        data (Optional[Dict[str, Any]]): Form data
        json_data (Optional[Dict[str, Any]]): JSON data
        headers (Optional[Dict[str, str]]): HTTP headers
        
    Returns:
        Dict[str, Any]: Response with status_code, success, text, and error fields
    """
    try:
        if not url or not url.startswith(('http://', 'https://')):
            return {
                "success": False,
                "status_code": 0,
                "text": "",
                "error": "Invalid URL format"
            }
            
        default_headers = {'User-Agent': 'CustomerServiceAgent/1.0'}
        if headers:
            default_headers.update(headers)
            
        response = requests.post(url, data=data, json=json_data, headers=default_headers, timeout=10)
        
        response_text = response.text[:4000] if response.text else ""
        
        return {
            "success": True,
            "status_code": response.status_code,
            "text": response_text,
            "headers": dict(response.headers),
            "error": None
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "status_code": 0,
            "text": "",
            "error": f"Request error: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "status_code": 0,
            "text": "",
            "error": f"Unexpected error: {str(e)}"
        }
