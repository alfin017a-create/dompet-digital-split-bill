#kontribusi dari nealsen anthony
from abc import ABC, abstractmethod
from exceptions.wallet import TransferLimitException, InsufficientFundsException, AccountFrozenException
from models.transaction import Transaction

class WalletBase(ABC):
    def __init__(self, wallet_id: str, saldo_awal: float = 0.0):
        self._wallet_id = wallet_id
        self._saldo = saldo_awal

    @property
    def saldo(self) -> float:
        return self._saldo

    def get_saldo(self) -> float:
        return self._saldo

    @abstractmethod
    def top_up(self, amount: float) -> bool:
        pass

    @abstractmethod
    def withdraw(self, amount: float, category: str = "BELANJA") -> bool:
        pass


class DigitalWallet(WalletBase):
    def __init__(self, wallet_id: str, saldo_awal: float = 0.0, daily_limit: float = 2000000.0):
        super().__init__(wallet_id, saldo_awal)
        self._daily_limit = daily_limit
        self._daily_transacted = 0.0
        self._reward_poin = 0
        self._is_frozen = False
        self._history = []

    @property
    def daily_limit(self) -> float:
        return self._daily_limit

    @daily_limit.setter
    def daily_limit(self, value: float):
        if value < 0:
            raise ValueError("Limit harian tidak boleh negatif!")
        self._daily_limit = value

    @property
    def is_frozen(self) -> bool:
        return self._is_frozen

    @property
    def history(self) -> list:
        return self._history

    @property
    def reward_poin(self) -> int:
        return self._reward_poin

    def set_frozen_status(self, status: bool):
        self._is_frozen = status

    def top_up(self, amount: float, method: str = "TRANSFER") -> bool:
        if self._is_frozen:
            raise AccountFrozenException()
        if not self.is_valid_amount(amount):
            return False
        
        self._saldo += amount
        self._reward_poin += int(amount // 10000)
        
        trx = Transaction(f"TRX{len(self._history)+1:03d}", "TOPUP", amount, "SALDO")
        self._history.append(trx)
        return True

    def withdraw(self, amount: float, category: str = "BELANJA") -> bool:
        if self._is_frozen:
            raise AccountFrozenException()
        if amount > self._saldo:
            raise InsufficientFundsException()
        
        self._saldo -= amount
        trx = Transaction(f"TRX{len(self._history)+1:03d}", "WITHDRAW", amount, category)
        self._history.append(trx)
        return True

    def check_limit(self, amount: float):
        if (self._daily_transacted + amount) > self._daily_limit:
            raise TransferLimitException()

    def transfer(self, target_user, amount: float) -> bool:
        if self._is_frozen:
            raise AccountFrozenException()
        if amount > self._saldo:
            raise InsufficientFundsException()
        self.check_limit(amount)
        
        self._saldo -= amount
        self._daily_transacted += amount
        target_user.get_wallet().top_up(amount)
        
        trx = Transaction(f"TRX{len(self._history)+1:03d}", "TRANSFER", amount, "SESAMA")
        self._history.append(trx)
        return True

    def redeem_poin(self, poin: int) -> bool:
        if poin <= 0 or poin > self._reward_poin:
            return False
        nilai_konversi = poin * 100
        self._reward_poin -= poin
        self._saldo += nilai_konversi
        return True

    @staticmethod
    def is_valid_amount(amount: float) -> bool:
        return isinstance(amount, (int, float)) and amount > 0
