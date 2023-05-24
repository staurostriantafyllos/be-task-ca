"""
NOTE:

Instead of directly getting db from request.state.db, we can use a service to encapsulate this logic, 
providing a higher level of abstraction and decoupling the specific implementation details.
"""

from fastapi import Request


def get_db(request: Request):
    return request.state.db
