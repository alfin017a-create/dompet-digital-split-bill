from models.wallet import DigitalWallet
from models.user import User
from models.group import Group
from models.expense import GroupExpense
from models.bill import BillPayment
from services.simplifier import DebtSimplifier
from utils.exporter import CSVExporter
from utils.iterator import TransactionIterator
from exceptions.wallet import InsufficientFundsException, TransferLimitException, AccountFrozenException

def main():
    users_db = {}
    groups_db = {}

    print("==================================================")
    print("   APLIKASI DOMPET DIGITAL & SPLIT BILL (CLI)   ")
    print("==================================================")

    while True:
        print("\n--- MENU UTAMA ---")
        print("1. Tambah Pengguna Baru")
        print("2. Top Up Saldo Wallet")
        print("3. Transfer Saldo (Cek Limit & Exception)")
        print("4. Bayar Tagihan (Listrik, Air, Internet)")
        print("5. Buat Grup Split Bill")
        print("6. Tambah Pengeluaran Kelompok")
        print("7. Hitung Split Bill & Simplifikasi Utang")
        print("8. Lihat Saldo & Riwayat Transaksi")
        print("9. Ekspor Riwayat ke File CSV")
        print("10. Keluar")

        pilihan = input("Pilih menu (1-10): ").strip()

        if pilihan == "1":
            uid = input("Masukkan ID User (misal: U01): ").strip()
            uname = input("Masukkan Username: ").strip()
            email = input("Masukkan Email: ").strip()
            limit_val = input("Masukkan Limit Transfer Harian (misal: 2000000): ").strip()
            limit = float(limit_val) if limit_val else 2000000.0
            
            wallet = DigitalWallet(wallet_id=f"W_{uid}", saldo_awal=0.0, daily_limit=limit)
            user = User(user_id=uid, username=uname, email=email, wallet=wallet)
            users_db[uname] = user
            print(f"✅ Pengguna '{uname}' berhasil didaftarkan!")

        elif pilihan == "2":
            uname = input("Masukkan Username: ").strip()
            if uname not in users_db:
                print("❌ Pengguna tidak ditemukan!")
                continue
            nominal = float(input("Masukkan Nominal Top Up: "))
            try:
                users_db[uname].get_wallet().top_up(nominal)
                print(f"✅ Top Up Berhasil! Saldo {uname} sekarang: Rp{users_db[uname].get_wallet().saldo:,.2f}")
            except Exception as e:
                print(f"❌ {e}")

        elif pilihan == "3":
            pengirim = input("Masukkan Username Pengirim: ").strip()
            penerima = input("Masukkan Username Penerima: ").strip()
            if pengirim not in users_db or penerima not in users_db:
                print("❌ Pengirim atau Penerima tidak ditemukan!")
                continue
            nominal = float(input("Masukkan Nominal Transfer: "))
            
            try:
                users_db[pengirim].get_wallet().transfer(users_db[penerima], nominal)
                print(f"✅ Transfer Berhasil Rp{nominal:,.2f} dari {pengirim} ke {penerima}!")
            except (InsufficientFundsException, TransferLimitException, AccountFrozenException) as e:
                print(f"⚠️ {e}")

        elif pilihan == "4":
            uname = input("Masukkan Username: ").strip()
            if uname not in users_db:
                print("❌ Pengguna tidak ditemukan!")
                continue
            
            print("\nPilih Jenis Tagihan:")
            print("1. Listrik (PLN)")
            print("2. Air (PDAM)")
            print("3. Internet / Wi-Fi")
            opsi_tagihan = input("Pilih jenis tagihan (1-3): ").strip()
            
            kategori_map = {
                "1": "LISTRIK",
                "2": "AIR",
                "3": "INTERNET"
            }
            if opsi_tagihan not in kategori_map:
                print("❌ Pilihan tagihan tidak valid!")
                continue
            
            kategori = kategori_map[opsi_tagihan]
            bill_id = input(f"Masukkan ID/No. Pelanggan {kategori}: ").strip()
            try:
                nominal = float(input(f"Masukkan Nominal Tagihan {kategori}: "))
                if nominal <= 0:
                    print("❌ Nominal tagihan harus lebih besar dari 0!")
                    continue
                
                bill = BillPayment(bill_id=bill_id, category=kategori, amount=nominal)
                wallet = users_db[uname].get_wallet()
                bill.pay_bill(wallet)
                print(f"✅ Tagihan {kategori} [{bill_id}] sebesar Rp{nominal:,.2f} berhasil dibayar!")
                print(f"   Sisa Saldo: Rp{wallet.saldo:,.2f}")
            except InsufficientFundsException:
                print("❌ Pembayaran Gagal: Saldo dompet tidak mencukupi!")
            except AccountFrozenException:
                print("❌ Pembayaran Gagal: Akun dompet sedang dibekukan!")
            except ValueError:
                print("❌ Nominal harus berupa angka yang valid!")

        elif pilihan == "5":
            gid = input("Masukkan ID Grup (misal: G01): ").strip()
            gname = input("Masukkan Nama Grup (misal: Liburan Bali): ").strip()
            group = Group(group_id=gid, group_name=gname)
            
            print("Pilih anggota yang akan dimasukkan (ketik 'selesai' jika cukup):")
            while True:
                uname = input("Masukkan Username Anggota: ").strip()
                if uname.lower() == 'selesai':
                    break
                if uname in users_db:
                    group.add_member(users_db[uname])
                    print(f"  -> {uname} ditambahkan ke grup.")
                else:
                    print("  -> Username tidak terdaftar!")
            
            groups_db[gname] = group
            print(f"✅ Grup '{gname}' berhasil dibuat!")

        elif pilihan == "6":
            gname = input("Masukkan Nama Grup: ").strip()
            if gname not in groups_db:
                print("❌ Grup tidak ditemukan!")
                continue
            payer_name = input("Masukkan Username Pembayar Awal: ").strip()
            if payer_name not in users_db:
                print("❌ Pembayar tidak terdaftar!")
                continue
            desc = input("Deskripsi Pengeluaran (misal: Makan Malam): ").strip()
            try:
                nominal = float(input("Total Nominal Pengeluaran: "))
                if nominal <= 0:
                    print("❌ Nominal pengeluaran harus lebih besar dari 0!")
                    continue
                
                payer_wallet = users_db[payer_name].get_wallet()
                payer_wallet.withdraw(nominal, category="SPLIT_BILL")
                
                exp = GroupExpense(f"EXP_{len(groups_db[gname]._expenses)+1}", users_db[payer_name], nominal, desc)
                groups_db[gname].add_expense(exp)
                print(f"✅ Pengeluaran '{desc}' sebesar Rp{nominal:,.2f} berhasil dicatat & saldo {payer_name} terpotong!")
                print(f"   Sisa Saldo {payer_name}: Rp{payer_wallet.saldo:,.2f}")
            except InsufficientFundsException:
                print(f"❌ Gagal: Saldo dompet {payer_name} tidak mencukupi untuk pengeluaran ini!")
            except AccountFrozenException:
                print(f"❌ Gagal: Akun dompet {payer_name} sedang dibekukan!")
            except ValueError:
                print("❌ Nominal harus berupa angka yang valid!")

        elif pilihan == "7":
            gname = input("Masukkan Nama Grup: ").strip()
            if gname not in groups_db:
                print("❌ Grup tidak ditemukan!")
                continue
            
            group = groups_db[gname]
            print(f"\n--- HASIL KALKULASI SPLIT BILL RATA ({group.get_group_name()}) ---")
            split = group.calculate_flat_split()
            for u, amt in split.items():
                print(f"• Tanggung Jawab Tagihan {u}: Rp{amt:,.2f}")
                
            print("\n--- SIMPLIFIKASI UTANG ---")
            simplifier = DebtSimplifier(group)
            res = simplifier.simplify_debts()
            for line in res:
                print(line)

        elif pilihan == "8":
            uname = input("Masukkan Username: ").strip()
            if uname not in users_db:
                print("❌ Pengguna tidak ditemukan!")
                continue
            
            w = users_db[uname].get_wallet()
            print(f"\n--- INFORMASI AKUN {uname.upper()} ---")
            print(f"Saldo Saat Ini : Rp{w.saldo:,.2f}")
            print(f"Poin Reward    : {w.reward_poin} Poin")
            print(f"Status Akun    : {'Dibekukan' if w.is_frozen else 'Aktif'}")
            filter_kat = input("Filter kategori (SALDO/BELANJA/SESAMA/LISTRIK/AIR/INTERNET/SPLIT_BILL atau Enter untuk semua): ").strip().upper()
            category_filter = filter_kat if filter_kat else None

            print("\n--- RIWAYAT TRANSAKSI ---")
            trx_iterator = TransactionIterator(w.history, category_filter=category_filter)
            count = 0
            for trx in trx_iterator:
                d = trx.get_details()
                print(f"[{d['timestamp']}] {d['type']} - Rp{d['amount']:,.2f} ({d['category']})")
                count += 1
            
            if count == 0:
                print("(Tidak ada riwayat transaksi ditemukan)")

        elif pilihan == "9":
            uname = input("Masukkan Username: ").strip()
            if uname not in users_db:
                print("❌ Pengguna tidak ditemukan!")
                continue
            path = f"riwayat_{uname}.csv"
            if CSVExporter.export_transactions(users_db[uname].get_wallet().history, path):
                print(f"✅ Riwayat berhasil diekspor ke file '{path}'!")
            else:
                print(f"❌ Gagal mengekspor riwayat ke file '{path}'. Pastikan file tidak sedang dibuka.")

        elif pilihan == "10":
            print("\nTerima kasih telah menggunakan aplikasi!")
            break

if __name__ == "__main__":
    main()