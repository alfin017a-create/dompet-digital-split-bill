class RewardSystem:
    def __init__(self, poin_rate: float = 0.001):
        self._poin_rate = poin_rate

    def calculate_reward(self, amount: float) -> int:
        return int(amount * self._poin_rate)

    def convert_poin_to_saldo(self, poin: int) -> float:
        return float(poin * 100)