import asyncio
from typing import AsyncGenerator, Dict, Union

from ..core.base import MeltQuote, MintQuote


class QuoteQueue:
    """QuoteQueue is a simple in-memory queue for quotes.

    Yields:
        _type_: Union[MintQuote, MeltQuote]
    """

    queues: Dict[str, asyncio.Queue] = {}

    async def submit(self, quote_id: str, quote: Union[MintQuote, MeltQuote]):
        if quote_id in self.queues:
            # send to queue only if it exists
            await self.queues[quote_id].put(quote)

    async def watch(
        self, quote_id: str
    ) -> AsyncGenerator[Union[MintQuote, MeltQuote], None]:
        try:
            # create queue if it does not exist
            self.queues.setdefault(quote_id, asyncio.Queue())
            while True:
                quote = await self.queues[quote_id].get()
                yield quote
        finally:
            # remove queue when generator is done
            self.queues.pop(quote_id, None)
