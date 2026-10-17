import asyncio
from ddg_async import AsyncDDG

async def main():
    async with AsyncDDG() as ddg:
        # Поиск текста (вторая страница)
        text_results = await ddg.search_text("python async", page=2)
        print(text_results[0].title)

        # Поиск картинок
        image_results = await ddg.search_images("капибара")
        print(image_results[0].image)

if __name__ == "__main__":
    asyncio.run(main())
