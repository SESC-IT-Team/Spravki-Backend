from typing import Any
import asyncio
from fastapi import HTTPException

from aiohttp import ClientSession, ClientTimeout

class RequestsService:
    @staticmethod
    async def request(
            url: str,
            method: str = "GET",
            retries: int = 3,
            timeout: int = 5,
            backoff_factor: float = 0.5,
            expected_status: int = 200,
            raise_for_status: dict[int, Exception] | None = None,
            **kwargs
    ) -> Any:
        if raise_for_status is None:
            raise_for_status = {}
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=timeout)) as session:
                    async with session.request(method, url, **kwargs) as response:
                        if response.status != expected_status:
                            if response.status in raise_for_status:
                                raise raise_for_status[response.status]
                            if response.status == 401:
                                raise HTTPException(response.status)
                            if response.status == 403:
                                raise HTTPException(response.status, response.reason)
                            raise Exception(f"Unexpected status: {response.status} {await response.json()}")
                        if response.status == 204:
                            return None
                        return await response.json()
            except HTTPException:
                raise
            except Exception as e:
                if attempt == retries - 1:
                    raise HTTPException(500, str(e))
                delay = backoff_factor * (2 ** attempt)
                await asyncio.sleep(delay)

    @staticmethod
    async def authorized_request(
            url: str,
            token: str,
            method: str = "GET",
            retries: int = 3,
            timeout: int = 5,
            backoff_factor: float = 0.5,
            expected_status: int = 200,
            raise_for_status: dict[int, Exception] | None = None,
            **kwargs
    ) -> Any:
        headers = kwargs.get('headers', {})
        headers['Authorization'] = f'Bearer {token}'
        kwargs['headers'] = headers
        return await RequestsService.request(url, method, retries, timeout, backoff_factor, expected_status, raise_for_status, **kwargs)