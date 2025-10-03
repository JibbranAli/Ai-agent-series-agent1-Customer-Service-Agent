"""
Customer Service Agent Tools Package

This package contains all the tools used by the Customer Service Agent:
- kb: Knowledge base search functionality
- tickets: Support ticket management
- http_tool: External API integration
- email_tool: Email notification support
"""

from . import kb
from . import tickets  
from . import http_tool

__all__ = ['kb', 'tickets', 'http_tool']
