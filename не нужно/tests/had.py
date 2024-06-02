import asyncio
from aiocfscrape import CloudflareScraper

async def test_open_page(url):
    async with CloudflareScraper() as session:
        async with session.get(url) as resp:
            return await resp.text()

if __name__ == '__main__':
    asyncio.run(test_open_page('https://uae.yallamotor.com/used-cars/pr_1000_100000/km_100_160000/sl_individual?page=1&sort=updated_desc'))