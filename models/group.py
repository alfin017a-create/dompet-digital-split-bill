# kontribusi modul oleh vincent lim (251110685)
from models.user import User
from models.expense import GroupExpense

class Group:
    def __init__(self, group_id: str, group_name: str):
        self._group_id = group_id
        self._group_name = group_name
        self._members = []
        self._expenses = []

    def add_member(self, user: User):
        if user not in self._members:
            self._members.append(user)

    def add_expense(self, expense: GroupExpense):
        self._expenses.append(expense)

    def calculate_flat_split(self) -> dict:
        if not self._members or not self._expenses:
            return {}
        total = sum(exp.get_amount() for exp in self._expenses)
        per_person = total / len(self._members)
        return {m.get_username(): per_person for m in self._members}

    def get_members(self) -> list:
        return self._members

    def get_group_name(self) -> str:
        return self._group_name
