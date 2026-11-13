#kontribusi oleh Nealsen anthony
from datetime import datetime

class Transaction:
    def __init__(self, trx_id: str, trx_type: str, amount: float, category: str):
        self._trx_id = trx_id
        self._type = trx_type
        self._amount = amount
        self._category = category
        self._timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_details(self) -> dict:
        return {
            "trx_id": self._trx_id,
            "type": self._type,
            "amount": self._amount,
            "category": self._category,
            "timestamp": self._timestamp
        }

    def to_csv_row(self) -> str:
        return f"{self._trx_id},{self._type},{self._amount},{self._category},{self._timestamp}"
