import json
from pathlib import Path
from datetime import datetime

DATA_FILE = Path('data.json')

saldo = 0
transactions = []  # list of {'type': 'pemasukan'|'pengeluaran', 'amount': float, 'time': isoformat, 'note': str}

def load_saldo():
    global saldo, transactions
    transactions = []
    if DATA_FILE.exists():
        try:
            with DATA_FILE.open('r', encoding='utf-8') as f:
                data = json.load(f)
                saldo = float(data.get('saldo', 0))
                transactions = data.get('transactions', []) or []
        except Exception:
            saldo = 0
            transactions = []

def save_saldo():
    try:
        with DATA_FILE.open('w', encoding='utf-8') as f:
            json.dump({'saldo': saldo, 'transactions': transactions}, f, ensure_ascii=False)
    except Exception as e:
        print('Gagal menyimpan data:', e)

def tambah_pemasukan():
    jumlah_pemasukan = float(input('Masukkan jumlah pemasukan: '))
    global saldo
    saldo += jumlah_pemasukan
    print('Pemasukan berhasil ditambahkan!')
    # catat transaksi
    transactions.append({
        'type': 'pemasukan',
        'amount': jumlah_pemasukan,
        'time': datetime.now().isoformat(),
        'note': ''
    })
    save_saldo()

def tambah_pengeluaran():
    jumlah_pengeluaran = float(input('Masukkan jumlah pengeluaran: '))
    global saldo
    if jumlah_pengeluaran > saldo:
        print('Saldo tidak cukup untuk melakukan pengeluaran!')
    else:
        saldo -= jumlah_pengeluaran
        print('Pengeluaran berhasil dilakukan!')
        transactions.append({
            'type': 'pengeluaran',
            'amount': jumlah_pengeluaran,
            'time': datetime.now().isoformat(),
            'note': ''
        })
        save_saldo()

def lihat_saldo():
    # Tampilkan saldo dalam format Rupiah (ribuan dipisah dengan titik, desimal dengan koma)
    def format_rupiah(v):
        s = f"{v:,.2f}"
        s = s.replace(',', 'X').replace('.', ',').replace('X', '.')
        return f'Rp {s}'

    print('=== Saldo Saat Ini ===')
    print(format_rupiah(saldo))

def laporan():
    def format_rupiah(v):
        s = f"{v:,.2f}"
        s = s.replace(',', 'X').replace('.', ',').replace('X', '.')
        return f'Rp {s}'

    total_in = sum(t.get('amount', 0) for t in transactions if t.get('type') == 'pemasukan')
    total_out = sum(t.get('amount', 0) for t in transactions if t.get('type') == 'pengeluaran')
    print('=== Laporan Transaksi ===')
    print('Total pemasukan :', format_rupiah(total_in))
    print('Total pengeluaran:', format_rupiah(total_out))
    print('Saldo sekarang   :', format_rupiah(saldo))
    print('\nDaftar transaksi:')
    if not transactions:
        print('  (belum ada transaksi)')
        return
    for t in transactions:
        waktu = t.get('time', '')
        tipe = t.get('type', '')
        amt = format_rupiah(t.get('amount', 0))
        note = t.get('note', '')
        print(f"- {waktu} | {tipe} | {amt} {'| ' + note if note else ''}")

def menu():
    print("=== Aplikasi Pengelola Uang Saku ===")
    print("1. Tambah pemasukan")
    print("2. Tambah pengeluaran")
    print("3. Lihat saldo")
    print("5. Laporan transaksi")
    print("4. Keluar")

while True:
    menu()
    pilihan = input("Pilih menu: ")

    if pilihan == "1":
        tambah_pemasukan()
    elif pilihan == "2":
        tambah_pengeluaran()
    elif pilihan == "3":
        lihat_saldo()
    elif pilihan == "4":
        save_saldo()
        print("Terima kasih!")
        break
    else:
        print("Pilihan tidak valid")