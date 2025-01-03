from fastapi import HTTPException, Security
from fastapi.security import api_key
from starlette import status
import os


api_key_header = api_key.APIKeyHeader(name="Authorization")
API_KEY = os.environ['API_KEY']
if not API_KEY:
    raise Exception("API Key not defined! Terminating service ...")


async def validate_api_key(key: str = Security(api_key_header)):
    if key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized - API Key is wrong"
        )
    return None
