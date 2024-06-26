import asyncio
from typing import List
import httpx


async def call_api_single(size: int = 1, ssl=True) -> List[dict]:
    url = "https://random-data-api.com/api/v2/users"
    async with httpx.AsyncClient(verify=ssl) as client:
        tasks = [client.get(url) for i in range(0, size)]
        result = await asyncio.gather(*tasks)
        return result
