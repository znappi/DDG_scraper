import pytest
from ddg_async.client import AsyncDDG
from ddg_async.models import SearchResult, ImageResult

pytestmark = pytest.mark.asyncio

async def test_get_vqd():
    """Проверяем, что парсер вытаскивает валидный токен"""
    async with AsyncDDG() as ddg:
        vqd = await ddg._get_vqd("python")

        assert vqd is not None
        assert isinstance(vqd, str)
        assert len(vqd) > 5

async def test_search_text():
    """Проверяем текстовый поиск и типизацию ответа"""
    async with AsyncDDG() as ddg:
        results = await ddg.search_text("rust lang", page=1)

        assert len(results) > 0
        assert isinstance(results[0], SearchResult)
        assert "rust" in results[0].title.lower() or "rust" in results[0].body.lower()

async def test_search_images():
    """Проверяем поиск картинок без блюра"""
    async with AsyncDDG() as ddg:
        results = await ddg.search_images("linux")

        assert len(results) > 0
        assert isinstance(results[0], ImageResult)
        assert results[0].image.startswith("http")
