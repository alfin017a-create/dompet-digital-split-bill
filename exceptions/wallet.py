class TransferLimitException(Exception):
    """Diangkat saat nominal transfer melebihi limit harian."""
    def __init__(self, message: str = "Transaksi gagal: Limit transfer harian terlampaui!"):
        super().__init__(message)


class InsufficientFundsException(Exception):
    """Diangkat saat saldo tidak mencukupi."""
    def __init__(self, message: str = "Transaksi gagal: Saldo akun tidak mencukupi!"):
        super().__init__(message)


class AccountFrozenException(Exception):
    """Diangkat saat transaksi dilakukan pada akun status dibekukan."""
    def __init__(self, message: str = "Transaksi gagal: Akun Anda sedang dibekukan (frozen)!"):
        super().__init__(message)