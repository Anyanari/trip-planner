from typing import List, Dict, Any
from ..schemas import Balance


def calculate_balances_from_expenses(expenses: List[Dict[str, Any]]) -> List[Balance]:
    """Calculate who owes whom based on expenses"""
    balances = {}
    
    for expense in expenses:
        paid_by = expense["paid_by"]
        amount = float(expense["amount"])
        
        for share in expense["shares"]:
            user_id = share["user_id"]
            share_amount = amount * float(share["share"])
            
            if user_id != paid_by:
                # User owes money to the person who paid
                key = (user_id, paid_by)
                if key not in balances:
                    balances[key] = {
                        "debtor_id": user_id,
                        "debtor_name": share.get("username", f"User {user_id}"),
                        "creditor_id": paid_by,
                        "creditor_name": expense.get("paid_by_username", f"User {paid_by}"),
                        "amount": 0.0
                    }
                balances[key]["amount"] += share_amount
    
    return [Balance(**balance) for balance in balances.values()]


def simplify_balances(balances: List[Balance]) -> List[Balance]:
    """Simplify balances by offsetting mutual debts"""
    balance_dict = {}
    
    # Convert to dictionary for easier manipulation
    for balance in balances:
        key = (balance.debtor_id, balance.creditor_id)
        balance_dict[key] = balance.amount
    
    # Find and offset mutual debts
    simplified = {}
    for (debtor, creditor), amount in balance_dict.items():
        reverse_key = (creditor, debtor)
        if reverse_key in balance_dict:
            # There's a mutual debt
            reverse_amount = balance_dict[reverse_key]
            if amount > reverse_amount:
                # Net amount from debtor to creditor
                simplified[(debtor, creditor)] = amount - reverse_amount
            elif amount < reverse_amount:
                # Net amount from creditor to debtor
                simplified[(creditor, debtor)] = reverse_amount - amount
            # If equal, they cancel out
        else:
            simplified[(debtor, creditor)] = amount
    
    # Convert back to Balance objects
    result = []
    for (debtor, creditor), amount in simplified.items():
        if amount > 0.01:  # Only include significant amounts
            # Find names from original balances
            debtor_name = next(
                (b.debtor_name for b in balances if b.debtor_id == debtor),
                f"User {debtor}"
            )
            creditor_name = next(
                (b.creditor_name for b in balances if b.creditor_id == creditor),
                f"User {creditor}"
            )
            
            result.append(Balance(
                debtor_id=debtor,
                debtor_name=debtor_name,
                creditor_id=creditor,
                creditor_name=creditor_name,
                amount=round(amount, 2)
            ))
    
    return sorted(result, key=lambda x: x.amount, reverse=True)
