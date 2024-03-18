from loguru import logger

from ..core.db import Database
from ..mint.crud import LedgerCrud
from ..mint.ledger import Ledger


class LedgerStartup:
    crud: LedgerCrud
    db: Database

    def __init__(self, ledger: Ledger):
        self.ledger = ledger
        self.crud = ledger.crud
        self.db = ledger.db

    async def check_pending_melt_quotes(self):
        unpaid_melt_quotes = await self.crud.get_melt_quotes(db=self.db, paid=False)
        if not unpaid_melt_quotes:
            return
        for melt_quote_db in unpaid_melt_quotes:
            # we check with the backend whether the quote has been paid during downtime
            melt_quote = await self.ledger.get_melt_quote(
                quote_id=melt_quote_db.quote, check_quote_with_backend=True
            )
            if melt_quote.paid:
                # get pending proofs associated to this melt quote
                pending_proofs = await self.crud.get_proofs_pending(
                    db=self.db, quote_id=melt_quote.quote
                )
                logger.debug(f"Checking pending melt quote: {melt_quote}")
                await self.ledger.melt(proofs=pending_proofs, quote=melt_quote.quote)

    async def startup_ledger(self):
        await self.check_pending_melt_quotes()
