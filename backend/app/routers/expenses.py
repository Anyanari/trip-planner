from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from ..database import get_db
from ..models import (
    Expense as ExpenseModel, ExpenseShare as ExpenseShareModel,
    Trip as TripModel, User as UserModel
)
from ..schemas import (
    Expense as ExpenseSchema, ExpenseCreate,
    ExpenseShare as ExpenseShareSchema, Balance
)

router = APIRouter(prefix="/api/expenses", tags=["expenses"])


@router.post("/", response_model=ExpenseSchema)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    # Check if trip exists
    trip = db.query(TripModel).filter(TripModel.id == expense.trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    # Check if user exists
    user = db.query(UserModel).filter(UserModel.id == expense.paid_by).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Validate shares sum to 1.0
    total_shares = sum(share["share"] for share in expense.shares)
    if abs(total_shares - 1.0) > 0.01:
        raise HTTPException(status_code=400, detail="Sum of shares must equal 1.0")
    
    # Create expense
    db_expense = ExpenseModel(
        trip_id=expense.trip_id,
        title=expense.title,
        amount=expense.amount,
        currency=expense.currency,
        paid_by=expense.paid_by
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    
    # Create expense shares
    for share_data in expense.shares:
        db_share = ExpenseShareModel(
            expense_id=db_expense.id,
            user_id=share_data["user_id"],
            share=share_data["share"]
        )
        db.add(db_share)
    
    db.commit()
    db.refresh(db_expense)
    return db_expense


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
