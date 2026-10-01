from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from typing import Optional, List
import uuid
import datetime

app = FastAPI(
    title="FinTrust Transaction API",
    version="2.0.0"
)

class TransactionIn(BaseModel):
    account_id: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0)
    currency: str = Field(..., regex=r'^[A-Z]{3}$')
    description: Optional[str] = None

    @validator('amount')
    def amount_max(cls, v):
        if v > 1_000_000:
            raise ValueError(
                "Amount exceeds single-transaction limit"
            )
        return v

class TransactionOut(TransactionIn):
    id: str
    status: str
    created_at: str

class StatusUpdate(BaseModel):
    status: str

transactions: List[dict] = []

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())

    response = await call_next(request)

    response.headers["X-Request-ID"] = request_id

    return response

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post(
    "/transactions",
    response_model=TransactionOut,
    status_code=201
)
async def create_transaction(body: TransactionIn):

    txn = {
        "id": str(uuid.uuid4()),
        **body.dict(),
        "status": "pending",
        "created_at": datetime.datetime.utcnow().isoformat()
    }

    transactions.append(txn)

    return txn

@app.get(
    "/transactions",
    response_model=List[TransactionOut]
)
async def list_transactions(
        account_id: Optional[str] = Query(None)
):

    if account_id:
        return [
            t for t in transactions
            if t["account_id"] == account_id
        ]

    return transactions

@app.get("/transactions/{transaction_id}")
async def get_transaction(transaction_id: str):

    for txn in transactions:
        if txn["id"] == transaction_id:
            return txn

    raise HTTPException(
        status_code=404,
        detail="Transaction not found"
    )

@app.patch("/transactions/{transaction_id}/status")
async def update_status(
        transaction_id: str,
        update: StatusUpdate
):

    if update.status not in ["approved", "rejected"]:
        raise HTTPException(
            status_code=400,
            detail="Status must be approved or rejected"
        )

    for txn in transactions:
        if txn["id"] == transaction_id:
            txn["status"] = update.status
            return txn

    raise HTTPException(
        status_code=404,
        detail="Transaction not found"
    )