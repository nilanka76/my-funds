from fastapi import FastAPI, Depends
from db.database import localSession, engine
from schemas.database_schemas import Base, T_funds, T_transactions
from models.models import Fund, Transaction
from sqlalchemy.orm import Session
from datetime import date

app = FastAPI()
Base.metadata.create_all(bind=engine)

# funds = [
#     Funds(
#     fnd_id = 1,
#     fnd_account = "SBI",
#     fnd_type = "Bank",
#     fnd_amount = 100.00,
#     fnd_active_flag = "Y"),
#     Funds(
#     fnd_id = 2,
#     fnd_account = "ICICI",
#     fnd_type = "Bank",
#     fnd_amount = 200.00,
#     fnd_active_flag = "Y"),
#     Funds(
#     fnd_id = 3,
#     fnd_account = "Groww",
#     fnd_type = "MF",
#     fnd_amount = 150.00,
#     fnd_active_flag = "Y"),
#     Funds(
#     fnd_id = 4,
#     fnd_account = "Stable_money",
#     fnd_type = "FD",
#     fnd_amount = 400.00,
#     fnd_active_flag = "Y"),
#     Funds(
#     fnd_id = 5,
#     fnd_account = "Stable_money",
#     fnd_type = "Bond",
#     fnd_amount = 50.00,
#     fnd_active_flag = "Y")
# ]

# def init_db():
#     db = localSession()

#     if db.query(Funds).count ==0 :
#         for fund in funds:
#             db.add(fund)

#         db.commit()
# init_db()

def get_db():
    db = localSession()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def hello():
    return {"msg": "hello"}

@app.get("/all_funds")
def get_all_funds(db: Session = Depends(get_db)):
    res = db.query(T_funds).filter(T_funds.fnd_active_flag == "Y").all()
    return res

@app.get("/funds_by_type/{type}")
def get_funds_by_type(type: str, db: Session = Depends(get_db)):
    db_funds = db.query(T_funds).filter(T_funds.fnd_type == type).all()
    if db_funds:
        return db_funds
    return "No Fund Found!!"

@app.post("/add_new_fund")
def add_new_fund(fund: Fund, db: Session = Depends(get_db)):
    db.add(T_funds(**fund.model_dump()))
    db.commit()
    return "Aew fund added!!"

@app.post("/update_fund")
def update_fund(account: str, type: str, amt: float, db: Session = Depends(get_db)):
    fnd = T_funds
    db_funds = db.query(fnd).filter(fnd.fnd_account == account, fnd.fnd_type == type).first()
    if db_funds:
        prev_amt = db_funds.fnd_amount
        db_funds.fnd_amount = amt
        db.commit()
        updated_funds = db.query(fnd).filter(fnd.fnd_account == account, fnd.fnd_type == type).first()
        return {
            "prev_fnd_amt ": prev_amt,
            "curr_fnd_amt": updated_funds.fnd_amount
        }
    return "No fund found!!"

@app.post("/remove")
def del_fund(account: str, type: str, db: Session = Depends(get_db)):
    fnd = T_funds
    db_funds = db.query(fnd).filter(fnd.fnd_account == account, fnd.fnd_type == type).first()
    if db_funds:
        rm_msg = f"Account: {db_funds.fnd_account}, Type: {db_funds.fnd_type} - Removed"
        db_funds.fnd_active_flag = "N"
        db.commit()
        return rm_msg
    return "No fund found!!"

@app.delete("/hard_remove_fund")
def hard_del_fund(account: str, type: str, db: Session = Depends(get_db)):
    fnd = T_funds
    db_funds = db.query(fnd).filter(fnd.fnd_account == account, fnd.fnd_type == type).first()
    if db_funds:
        rm_msg = ""
        if db_funds.fnd_active_flag == "N":
            rm_msg = f"Account: {db_funds.fnd_account}, Type: {db_funds.fnd_type} - fully removed"
            db.delete(db_funds)
            db.commit()
        else :
            rm_msg = "Unable to fully remove an active fund"
        
        return rm_msg
    return "No fund found!!"