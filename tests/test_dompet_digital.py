import sys
from pathlib import Path
import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from exceptions.wallet import (
    AccountFrozenException,
    InsufficientFundsException,
    TransferLimitException,
)
from models.bill import BillPayment
from models.expense import GroupExpense
from models.group import Group
from models.user import User
from models.wallet import DigitalWallet
from services.reward import RewardSystem
from services.simplifier import DebtSimplifier
from utils.exporter import CSVExporter
from utils.iterator import TransactionIterator


def make_user(user_id: str, username: str, saldo_awal: float = 0.0, daily_limit: float = 2000000.0) -> User:
    wallet = DigitalWallet(f"W_{user_id}", saldo_awal=saldo_awal, daily_limit=daily_limit)
    return User(user_id=user_id, username=username, email=f"{username}@mikroskil.ac.id", wallet=wallet)


def test_top_up_berhasil_menambah_saldo_dan_poin():
    wallet = DigitalWallet("W01")
    result = wallet.top_up(50000)
    assert result is True
    assert wallet.saldo == 50000.0
    assert wallet.reward_poin == 5
    assert len(wallet.history) == 1
    assert wallet.history[0].get_details()["category"] == "SALDO"


def test_top_up_nominal_tidak_valid_mengembalikan_false():
    wallet = DigitalWallet("W01")
    assert wallet.top_up(0) is False
    assert wallet.top_up(-10000) is False
    assert wallet.saldo == 0.0
    assert len(wallet.history) == 0


def test_withdraw_berhasil_dan_gagal_jika_saldo_kurang():
    wallet = DigitalWallet("W01", saldo_awal=100000.0)
    assert wallet.withdraw(40000, category="BELANJA") is True
    assert wallet.saldo == 60000.0
    with pytest.raises(InsufficientFundsException):
        wallet.withdraw(100000)


def test_transfer_sukses_memindahkan_saldo_ke_penerima():
    pengirim = make_user("U01", "jonathan", saldo_awal=500000.0)
    penerima = make_user("U02", "alfin", saldo_awal=0.0)

    result = pengirim.get_wallet().transfer(penerima, 150000.0)
    assert result is True
    assert pengirim.get_wallet().saldo == 350000.0
    assert penerima.get_wallet().saldo == 150000.0


def test_transfer_melebihi_limit_harian_angkat_exception():
    pengirim = make_user("U01", "jonathan", saldo_awal=1000000.0, daily_limit=200000.0)
    penerima = make_user("U02", "alfin")

    with pytest.raises(TransferLimitException):
        pengirim.get_wallet().transfer(penerima, 250000.0)


def test_akun_dibekukan_angkat_account_frozen_exception():
    pengirim = make_user("U01", "jonathan", saldo_awal=200000.0)
    penerima = make_user("U02", "alfin")
    pengirim.get_wallet().set_frozen_status(True)

    with pytest.raises(AccountFrozenException):
        pengirim.get_wallet().top_up(50000.0)
    with pytest.raises(AccountFrozenException):
        pengirim.get_wallet().withdraw(10000.0)
    with pytest.raises(AccountFrozenException):
        pengirim.get_wallet().transfer(penerima, 10000.0)


def test_redeem_poin_berhasil_dan_batas_tidak_valid():
    wallet = DigitalWallet("W01")
    wallet.top_up(100000.0)  # menghasilkan 10 poin
    assert wallet.redeem_poin(5) is True
    assert wallet.reward_poin == 5
    assert wallet.saldo == 100500.0
    assert wallet.redeem_poin(0) is False
    assert wallet.redeem_poin(99) is False


def test_bill_payment_mengurangi_saldo_dan_catat_kategori():
    wallet = DigitalWallet("W01", saldo_awal=300000.0)
    bill = BillPayment(bill_id="PLN-01", category="LISTRIK", amount=75000.0)

    assert bill.pay_bill(wallet) is True
    assert wallet.saldo == 225000.0
    assert wallet.history[-1].get_details()["category"] == "LISTRIK"


def test_group_calculate_flat_split():
    u1 = make_user("U01", "jonathan", saldo_awal=300000.0)
    u2 = make_user("U02", "alfin")
    group = Group("G01", "Liburan Bali")
    group.add_member(u1)
    group.add_member(u2)
    group.add_expense(GroupExpense("EXP_1", u1, 200000.0, "Makan Malam"))

    split = group.calculate_flat_split()
    assert split == {"jonathan": 100000.0, "alfin": 100000.0}


def test_debt_simplifier_ringkasan_utang_piutang():
    u1 = make_user("U01", "jonathan", saldo_awal=300000.0)
    u2 = make_user("U02", "alfin")
    group = Group("G01", "Liburan Bali")
    group.add_member(u1)
    group.add_member(u2)
    group.add_expense(GroupExpense("EXP_1", u1, 200000.0, "Makan Malam"))

    summary = DebtSimplifier(group).simplify_debts()
    assert any("jonathan berhak menerima piutang sebesar Rp100,000.00" in line for line in summary)
    assert any("alfin harus membayar utang sebesar Rp100,000.00" in line for line in summary)


def test_reward_system_kalkulasi_dan_konversi():
    reward = RewardSystem(poin_rate=0.001)
    assert reward.calculate_reward(150000.0) == 150
    assert reward.convert_poin_to_saldo(15) == 1500.0


def test_transaction_iterator_dan_csv_exporter(tmp_path):
    wallet = DigitalWallet("W01")
    wallet.top_up(250000.0)
    BillPayment("PLN-01", "LISTRIK", 50000.0).pay_bill(wallet)
    BillPayment("PDAM-01", "AIR", 30000.0).pay_bill(wallet)

    filtered = list(TransactionIterator(wallet.history, category_filter="LISTRIK"))
    assert len(filtered) == 1
    assert filtered[0].get_details()["amount"] == 50000.0

    csv_file = tmp_path / "riwayat_uji.csv"
    assert CSVExporter.export_transactions(wallet.history, str(csv_file)) is True
    lines = csv_file.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "trx_id,type,amount,category,timestamp"
    assert len(lines) == 4
