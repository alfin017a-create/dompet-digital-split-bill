#kontribusi oleh Nealsen anthony
from models.wallet import DigitalWallet

class User:
    def __init__(self, user_id: str, username: str, email: str, wallet: DigitalWallet):
        self._user_id = user_id
        self._username = username
        self._email = email
        self._wallet = wallet

    def get_wallet(self) -> DigitalWallet:
        return self._wallet

    def get_username(self) -> str:
        return self._username

    def get_user_id(self) -> str:
        return self._user_id
