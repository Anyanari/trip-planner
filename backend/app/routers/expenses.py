from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from ..database import get_db
from ..models import (
    Expense as ExpenseModel, ExpenseShare as ExpenseShareModel,
    Trip as TripModel, User as UserModel
)
from ..schemas import (
    Expense as ExpenseSchema, ExpenseCreate, ExpenseUpdate,
    ExpenseShare as ExpenseShareSchema, Balance
)

router = APIRouter(prefix="/api/expenses", tags=["expenses"])


@router.post("/", response_model=ExpenseSchema)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    # Check if trip exists
    trip = db.query(TripModel).filter(TripModel.id == expense.trip_id).first()
    if not trip:
        raise HTTPException(status_code=400, detail="Trip not found")
    
    # Check if user exists
    user = db.query(UserModel).filter(UserModel.id == expense.paid_by).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    shares = expense.shares or [{"user_id": expense.paid_by, "share": 1.0}]
    total_shares = sum(s["share"] if isinstance(s, dict) else s.share for s in shares)
    if abs(total_shares - 1.0) > 0.001:
        raise HTTPException(status_code=400, detail=f"Sum of shares must equal 1.0, current sum: {total_shares}")
    
    # Create expense
    db_expense = ExpenseModel(
        trip_id=expense.trip_id,
        title=expense.title,
        amount=expense.amount,
        currency=expense.currency,
        paid_by=expense.paid_by,
        date=expense.date or date.today()
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    
    # Create expense shares
    for share_data in shares:
        db_share = ExpenseShareModel(
            expense_id=db_expense.id,
            user_id=share_data["user_id"] if isinstance(share_data, dict) else share_data.user_id,
            share=share_data["share"] if isinstance(share_data, dict) else share_data.share,
        )
        db.add(db_share)
    
    db.commit()
    db.refresh(db_expense)
    return db_expense


@router.get("/", response_model=List[ExpenseSchema])
def get_expenses(
    skip: int = 0,
    limit: int = 100,
    trip_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(ExpenseModel)
    if trip_id is not None:
        query = query.filter(ExpenseModel.trip_id == trip_id)
    expenses = query.offset(skip).limit(limit).all()
    return expenses


@router.get("/trip/{trip_id}", response_model=List[ExpenseSchema])
def get_trip_expenses(trip_id: int, db: Session = Depends(get_db)):
    expenses = db.query(ExpenseModel).filter(ExpenseModel.trip_id == trip_id).all()
    return expenses


@router.get("/{expense_id}", response_model=ExpenseSchema)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.patch("/{expense_id}", response_model=ExpenseSchema)
def update_expense(expense_id: int, expense_update: ExpenseUpdate, db: Session = Depends(get_db)):
    expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    update_data = expense_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(expense, field):
            setattr(expense, field, value)
    
    db.commit()
    db.refresh(expense)
    return expense


@router.put("/{expense_id}", response_model=ExpenseSchema)
def update_expense_put(expense_id: int, expense_update: ExpenseUpdate, db: Session = Depends(get_db)):
    return update_expense(expense_id=expense_id, expense_update=expense_update, db=db)


@router.delete("/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    db.delete(expense)
    db.commit()
    return {"message": "Expense deleted successfully"}


@router.get("/trip/{trip_id}/balances", response_model=List[Balance])
def get_trip_balances(trip_id: int, db: Session = Depends(get_db)):
    # Check if trip exists
    trip = db.query(TripModel).filter(TripModel.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    # Call database function to calculate balances
    result = db.execute(
        text("SELECT * FROM calculate_trip_balances(:trip_id)"),
        {"trip_id": trip_id}
    ).fetchall()
    
    balances = []
    for row in result:
        balances.append(Balance(
            debtor_id=row.debtor_id,
            debtor_name=row.debtor_name,
            creditor_id=row.creditor_id,
            creditor_name=row.creditor_name,
            amount=float(row.amount)
        ))
    
    return balances
