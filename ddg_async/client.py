import asyncio
import re
import httpx
from bs4 import BeautifulSoup
from .models import SearchResult, ImageResult
from .exceptions import DDGTokenError
import urllib.parse

class AsyncDDG:
    def __init__(self):
        self.headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Referer": "https://duckduckgo.com/",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-origin",
                }
        self.client = None

    async def __aenter__(self):
            self.client = httpx.AsyncClient(
                headers=self.headers,
                timeout=30.0,
                http2=True,
                follow_redirects=True
            )
            return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()

    async def _get_vqd(self, query:str):
        url = "https://duckduckgo.com/"
        response = await self.client.get(url, params={"q": query})
        response.raise_for_status()

        match = re.search(r'vqd="([^"]+)"', response.text)
        if not match:
            raise DDGTokenError("Не удалось найти токен vqd. Проверьте заголовки или IP")

        return match.group(1)

    async def search_images(self, query: str):
            vqd = await self._get_vqd(query)

            await asyncio.sleep(1.0)

            url = "https://duckduckgo.com/i.js"

            payload = {
                "q": query,
                "o": "json",
                "vqd": vqd,
                "f": ",,,",
                "l": "wt-wt",
                "p": "1"
            }

            response = await self.client.get(url, params=payload)
            response.raise_for_status()

            data = response.json()

            results = data.get("results", [])

            images = []
            for item in results:
                images.append(ImageResult(
                    title=item.get("title"),
                    image=item.get("image"),
                    url=item.get("url"),
                    source=item.get("source")
                ))

            return images

    async def search_text(self, query: str, page: int = 1):
        skip = (page - 1) * 30
        url = "https://html.duckduckgo.com/html/"

        if skip > 0:
            response = await self.client.get(url, params={"q": query, "s": skip})
        else:
            response = await self.client.get(url, params={"q": query})

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.select('.result__body')

        links = []
        for item in results:
            title_tag = item.select_one('.result__title a')
            snippet_tag = item.select_one('.result__snippet')

            if not title_tag:
                continue

            raw_url = title_tag.get('href')
            if raw_url and 'uddg=' in raw_url:
                encoded_url = raw_url.split('uddg=')[1].split('&')[0]
                clean_url = urllib.parse.unquote(encoded_url)
            else:
                clean_url = raw_url

            links.append(SearchResult(
                title=title_tag.text.strip(),
                url=clean_url,
                body=snippet_tag.text.strip() if snippet_tag else ""
            ))

        return links
