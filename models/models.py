from datetime import date
from pydantic import BaseModel

class Fund(BaseModel):

    fnd_id: int
    fnd_account: str
    fnd_type: str
    fnd_amount: float
    fnd_active_flag: str

class Transaction(BaseModel):

    txn_id: int
    txn_account: str
    txn_date: date
    txn_amount: float
    txn_type: str
    txn_tag: str
    txn_active_flag: str