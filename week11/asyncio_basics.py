import asyncio
import aiohttp  # pip install aiohttp

async def fetch_account_data(session: aiohttp.ClientSession, account_id: int) -> dict:
    """Async fetch — yields control to event loop while waiting for response."""
    url = f"https://api.fintrust.internal/accounts/{account_id}"
    async with session.get(url) as response:
        data = await response.json()
        return data

async def fetch_all_accounts(account_ids: list) -> list:
    """Run all fetches concurrently using asyncio.gather."""
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_account_data(session, account_id)
            for account_id in account_ids
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results

# Entry point: run the event loop
account_ids = [range(1, 1001)]  # 1000 accounts
results = asyncio.run(fetch_all_accounts(account_ids))