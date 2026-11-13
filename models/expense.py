# kontribusi modul oleh vincent lim (251110685)
from models.user import User

class GroupExpense:
    def __init__(self, expense_id: str, payer: User, total_amount: float, description: str):
        self._expense_id = expense_id
        self._payer = payer
        self._total_amount = total_amount
        self._description = description

    def get_amount(self) -> float:
        return self._total_amount

    def get_payer(self) -> User:
        return self._payer

    def get_description(self) -> str:
        return self._description
