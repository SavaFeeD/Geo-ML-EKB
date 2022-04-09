from fastapi import Header, HTTPException

from typing import Optional


async def get_token_header(x_token: Optional[str] = Header(None)):
    if x_token != 'token':
        raise HTTPException(status_code=400, detail='X-Token header invalid')


async def get_query_token(token: str):
    if token != 'token':
        raise HTTPException(status_code=400, detail='No Alex token provided')
