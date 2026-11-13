# [A2] Dompet Digital & Split Bill (CLI)

Aplikasi Command Line Interface (CLI) berbasis **Python Object-Oriented Programming (OOP)** untuk mengelola transaksi dompet digital personal serta pencatatan dan pembagian tagihan bersama (*split bill*) dalam kelompok.

---

## Informasi Akademik & Kelompok

- **Institusi:** Universitas Mikroskil — Fakultas Informatika, Program Studi Teknik Informatika
- **Mata Kuliah:** Perancangan dan Pemrograman Berorientasi Objek (`11.OODP.201`)
- **Semester:** Ganjil TA 2026/2027
- **Kelas / Kelompok:** IF-C Sore — Kelompok 2
- **Dosen Pengampu:** Kelvin, S.Kom., M.Kom.

### Daftar Anggota Kelompok

| No | Nama Lengkap | NIM |
| :---: | :--- | :--- |
| 1 | Jonathan Jovin | 251110105 |
| 2 | Vincent Lim | 251110685 |
| 3 | Alfin Max Leandro | 251110249 |
| 4 | Jovin Evan Chumadin | 251111299 |
| 5 | Nealsen Anthony | 251110566 |

---

## Fitur Utama (Antarmuka CLI)

Program dijalankan melalui `main.py` dengan 10 pilihan menu utama:

1. **Tambah Pengguna Baru** — Registrasi `User` dan inisialisasi `DigitalWallet` (termasuk pengaturan batas transfer harian).
2. **Top Up Saldo Wallet** — Pengisian saldo disertai akumulasi poin *reward* (`+1` poin per Rp10.000) dan pencatatan riwayat transaksi.
3. **Transfer Saldo Antar-Pengguna** — Pengiriman dana antar-pengguna dengan validasi akun beku, kecukupan saldo, dan limit transfer harian (*custom exceptions*).
4. **Bayar Tagihan Rutin** — Pembayaran tagihan `LISTRIK`, `AIR`, dan `INTERNET` melalui kelas `BillPayment`.
5. **Buat Grup Split Bill** — Membuat grup tagihan bersama (`Group`) dan menambahkan anggota (`User`).
6. **Tambah Pengeluaran Kelompok** — Mencatat `GroupExpense` sekaligus memotong saldo pembayar awal secara otomatis.
7. **Hitung Split Bill & Simplifikasi Utang** — Pembagian tagihan merata (`calculate_flat_split()`) dan ringkasan saldo bersih utang-piutang (`DebtSimplifier.simplify_debts()`).
8. **Lihat Saldo & Riwayat Transaksi** — Menampilkan saldo, poin *reward*, status akun, serta filter riwayat berdasarkan kategori menggunakan `TransactionIterator`.
9. **Ekspor Riwayat ke File CSV** — Mengekspor log riwayat transaksi pengguna ke file `riwayat_<username>.csv` melalui `CSVExporter`.
10. **Keluar** — Mengakhiri sesi aplikasi CLI.

---

## Struktur Folder Proyek

```text
.
├── main.py                # Entry point aplikasi & menu CLI interaktif (Menu 1-10)
├── README.md              # Dokumentasi proyek & panduan menjalankan program
├── requirements.txt       # Daftar dependensi Python
├── .gitignore             # Daftar file/folder yang diabaikan Git
├── exceptions/
│   └── wallet.py          # TransferLimitException, InsufficientFundsException, AccountFrozenException
├── models/
│   ├── bill.py            # Entitas pembayaran tagihan rutin (BillPayment)
│   ├── expense.py         # Entitas pengeluaran kelompok (GroupExpense)
│   ├── group.py           # Pengelola grup & kalkulasi split bill rata (Group)
│   ├── transaction.py     # Model data log riwayat transaksi (Transaction)
│   ├── user.py            # Entitas pengguna & relasi komposisi ke wallet (User)
│   └── wallet.py          # WalletBase (ABC) & DigitalWallet
├── services/
│   ├── reward.py          # Layanan perhitungan rasio & konversi poin reward (RewardSystem)
│   └── simplifier.py      # Layanan kalkulasi ringkasan utang-piutang grup (DebtSimplifier)
└── utils/
    ├── exporter.py        # Utilitas ekspor riwayat transaksi ke CSV (CSVExporter)
    └── iterator.py        # Iterator penelusuran riwayat transaksi per kategori (TransactionIterator)
```

---

## Prasyarat

- **Python 3.x** (dikembangkan dan diuji pada Python 3.13)
- Seluruh fitur utama hanya menggunakan **Python Standard Library** (`abc`, `datetime`), sehingga tidak memerlukan instalasi paket eksternal.

---

## Cara Instalasi & Menjalankan Program

1. **Clone repository ini:**
   ```bash
   git clone https://github.com/<username>/<nama-repository>.git
   cd <nama-repository>
   ```

2. **(Opsional) Buat virtual environment dan cek dependensi:**
   ```bash
   python -m venv .venv
   # Windows PowerShell:
   .venv\Scripts\Activate.ps1
   # macOS / Linux:
   source .venv/bin/activate

   pip install -r requirements.txt
   ```

3. **Jalankan program:**
   ```bash
   python main.py
   ```
