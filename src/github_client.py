import datetime
import os
import random

import requests
import aiohttp
from typing import Dict, List, AsyncIterator

from reactivex import from_iterable, Observable

from message import GithubEvent

GITHUB_API_URL = "https://api.github.com"
REQUESTS_PER_MINUTE = 30


def _get_authorization_headers() -> Dict:
    return {
        "Authorization": f"Bearer {os.getenv('ACCESS_TOKEN')}",
        "Accept": "application/vnd.github.v3+json"
    }


def _fetch_github_api(url: str) -> Dict:
    response = requests.get(url, headers=_get_authorization_headers())
    assert response.status_code == 200, f"status code {response.status_code}"
    return response.json()


async def _fetch_github_api_async(url: str) -> Dict:
    headers = _get_authorization_headers()
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            assert response.status == 200, f"status code {response.status}"
            return await response.json()


async def _get_languages_async(languages_url: str) -> List[str]:
    languages_data = await _fetch_github_api_async(languages_url)
    return list(languages_data.keys()) if languages_data else []


async def _fetch_data_as_async_generator(
        keyword: str,
) -> AsyncIterator[GithubEvent]:
    url = f"{GITHUB_API_URL}/search/code?q={keyword}"
    results = await _fetch_github_api_async(url)
    for item in results.get("items", []):
        yield GithubEvent(
            repo_fullname=item["repository"]["full_name"],
            keyword=keyword,
            found_date=datetime.datetime.now(),
            stars_cnt=random.randint(
                1, 10000
            ),
            langs=await _get_languages_async(item["repository"]["languages_url"]),
        )


async def fetch_data_as_observable(keyword: str) -> Observable[GithubEvent]:
    async def iterator_to_list():
        return [event async for event in _fetch_data_as_async_generator(keyword)]

    return from_iterable(await iterator_to_list())
