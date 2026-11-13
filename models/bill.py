from models.wallet import DigitalWallet

class BillPayment:
    def __init__(self, bill_id: str, category: str, amount: float):
        self._bill_id = bill_id
        self._category = category
        self._amount = amount

    @property
    def bill_id(self) -> str:
        return self._bill_id

    @property
    def category(self) -> str:
        return self._category

    @property
    def amount(self) -> float:
        return self._amount

    def pay_bill(self, wallet: DigitalWallet) -> bool:
        return wallet.withdraw(self._amount, category=self._category)
