import pyinputplus as pyip
from tabulate import tabulate
import os

# Tentukan database dengan kunci utama 'product_id'
db = [
    ['No.', 'BARCODE', 'Nama', 'Stock', 'Satuan', 'Harga'],
    [1, 'AAB901C', 'Beras Kendi', 100, 'kg', 12000],
    [2, 'AAB901A', 'Beras Delanggu', 150, 'kg', 15000],
    [3, 'AAB902E', 'Beras Mentik Wangi', 500, 'kg', 13500],
    [4, 'AAB903B', 'Beras Organik', 200, 'kg', 11500],
    [5, 'AAB904A', 'Beras Ketan', 500, 'kg', 14000],
    [6, 'AAB905C', 'Beras Naga Mutiara', 300, 'kg', 13000]
]

# Daftar untuk melacak barcode yang digunakan saat menambahkan produk baru
used_barcodes = []

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def search_by_barcode(database):
    barcode = input('Masukkan barcode beras yang ingin dicari: ').lower()  # Konversi ke huruf kecil
    found_items = []

    for row in database[1:]:
        if barcode in row[1].lower():  # Bandingkan dengan barcode dalam huruf kecil
            found_items.append(row)

    if found_items:
        print('Hasil Pencarian:')
        show(found_items)
    else:
        print(f'Beras dengan barcode "{barcode}" tidak ditemukan.')

def show(database, title='Daftar Jenis Beras Tersedia'):
    clear_screen()
    header = database[0]
    data = database[1:]
    print(tabulate(data, headers=header, tablefmt="pretty"))

def add(database, used_barcodes):
    clear_screen()
    barcode = input('Input BARCODE Beras (harus unik): ')
    barcode = barcode.upper()  # Konversi ke huruf besar
    if barcode in used_barcodes:
        print('BARCODE sudah ada dalam database. Mohon input BARCODE yang unik.')
        return

    name = input('Input nama Beras: ').capitalize()

    try:
        stock = int(input('Input stock Beras: '))
        satuan = input('Input satuan (kg): ')
        harga = int(input('Input harga Beras per satuan: '))

        # Cari nomor terakhir dalam database
        last_no = database[-1][0] if database else 0

        product_id = last_no + 1  # Nomor berurutan
        database.append([product_id, barcode, name, stock, satuan, harga])
        used_barcodes.append(barcode)  # Tambahkan ke daftar barcode yang sudah digunakan
        print(f'Data beras {name} berhasil ditambahkan.')

        while True:
            pilihan = input('Apakah Anda ingin menambahkan beras lainnya? (y/n/kembali): ').lower()
            if pilihan == 'n':
                return  # Kembali ke menu utama
            elif pilihan == 'y':
                add(database, used_barcodes)  # Rekursif untuk menambahkan beras lainnya
                return
            elif pilihan == 'kembali':
                return  # Kembali ke menu utama
            else:
                print('Pilihan tidak valid. Silakan masukkan "y" untuk Ya, "n" untuk Tidak, atau "kembali" untuk kembali ke menu utama.')
    except ValueError:
        print('Input tidak valid. Pastikan stock dan harga adalah angka.')

def delete(database):
    clear_screen()
    barcode_to_delete = input('Input BARCODE beras yang akan dihapus (atau ketik "batal" untuk membatalkan): ').upper()  # Konversi ke huruf besar
    if barcode_to_delete.lower() == 'batal':
        print('Penghapusan beras dibatalkan.')
        return

    found_item = None
    for row in database[1:]:
        if barcode_to_delete == row[1]:
            found_item = row
            break

    if found_item:
        print('Informasi Beras yang akan dihapus:')
        show([database[0], found_item])
        confirm = pyip.inputChoice(['y', 'n'], prompt='Apakah Anda yakin ingin menghapus beras ini? (y/n): ').lower()
        if confirm == 'y':
            database.remove(found_item)
            print(f'Beras dengan BARCODE {barcode_to_delete} berhasil dihapus.')
            # Mengatur ulang nomor
            for i, row in enumerate(database[1:], start=1):
                row[0] = i
        else:
            print(f'Beras dengan BARCODE {barcode_to_delete} tidak dihapus.')
    else:
        print(f'Beras dengan BARCODE {barcode_to_delete} tidak ditemukan.')

def update(database):
    clear_screen()
    barcode = input('Input BARCODE beras yang akan diupdate (atau ketik "kembali" untuk kembali ke menu utama): ')
    barcode = barcode.upper()  # Konversi ke huruf besar
    
    if barcode.lower() == 'kembali':
        return  # Kembali ke menu utama

    for row in database[1:]:
        if row[1] == barcode:
            print(f'Pilihan Update untuk {row[2]}:')
            print('1. Update Stok')
            print('2. Update Harga')
            print('3. Kembali ke menu utama')
            update_option = pyip.inputChoice(['1', '2', '3'], prompt='> Silahkan pilih opsi update:')
            
            if update_option == '1':
                new_stock = int(input('Input stock baru untuk beras ini: '))
                row[3] = new_stock
                print(f'Stock untuk {row[2]} berhasil diupdate menjadi {new_stock}.')
            elif update_option == '2':
                new_price = int(input('Input harga baru per satuan untuk beras ini: '))
                row[5] = new_price
                print(f'Harga per satuan untuk {row[2]} berhasil diupdate menjadi {new_price} Rupiah.')
            elif update_option == '3':
                return  # Kembali ke menu utama
            else:
                print('Opsi update tidak valid.')
            break
    else:
        print(f'Beras dengan BARCODE {barcode} tidak ditemukan.')

def buy(database):
    # Menampilkan detail sebelum pembayaran
    show(database)
    clear_screen()
    cart = []  # Menyimpan beras yang akan dibeli beserta jumlahnya

    while True:
        barcode = input('Input BARCODE Beras yang ingin dibeli (atau ketik "selesai" untuk menyelesaikan pembelian): ')
        if barcode.lower() == 'selesai':
            break
        
        barcode = barcode.upper()  # Konversi ke huruf besar
        quantity = int(input('Input jumlah beras yang ingin dibeli: '))

        for row in database[1:]:
            if row[1] == barcode:
                if row[3] >= quantity:
                    total_price = row[5] * quantity
                    cart.append({'name': row[2], 'quantity': quantity, 'unit': row[4], 'price_per_unit': row[5]})
                    print(f'{quantity} {row[4]} {row[2]} x {row[5]} per {row[4]} = {total_price} Rupiah ditambahkan ke keranjang.')
                    row[3] -= quantity  # Mengurangi stok
                else:
                    print(f'Stok {row[2]} tidak mencukupi untuk pembelian ini.')
                    print(f'Stok sisa untuk {row[2]} adalah {row[3]} {row[4]}.')
                    top_up = input(f'Apakah Anda ingin menambah stok {row[2]}? (y/n): ').lower()
                    if top_up == 'y':
                        additional_quantity = int(input(f'Masukkan jumlah {row[4]} {row[2]} yang ingin ditambahkan: '))
                        row[3] += additional_quantity
                        print(f'Stok {row[2]} telah ditambahkan sebanyak {additional_quantity} {row[4]}.')
                    else:
                        print('Pembelian dibatalkan.')
                break
        else:
            print(f'Beras dengan BARCODE {barcode} tidak ditemukan.')

    if not cart:
        print('Keranjang belanja kosong. Pembelian dibatalkan.')
        return

    total_purchase_price = sum(item['quantity'] * item['price_per_unit'] for item in cart)
    print(f'\nTotal Harga Pembelian: {total_purchase_price} Rupiah')

    # Pilihan metode pembayaran
    payment_option = pyip.inputMenu(['Tunai', 'Kartu Kredit'], numbered=True, prompt='Pilih metode pembayaran (1-Tunai/2-Kartu Kredit): ')
    clear_screen()
    if payment_option == 'Tunai':
        while True:
            payment_amount = float(input('Input jumlah uang yang diberikan: '))
            if payment_amount < total_purchase_price:
                print('Jumlah uang yang diberikan kurang. Silakan masukkan jumlah yang mencukupi.')
            else:
                change = payment_amount - total_purchase_price
                print(f'Uang kembalian: {change:.2f} Rupiah')
                print('Terima kasih! Pembelian berhasil.')
                break
    elif payment_option == 'Kartu Kredit':
        print('Anda akan dibawa ke halaman pembayaran dengan Kartu Kredit...')
    else:
        print('Pembelian dibatalkan.')

PROMPT = ('''==========================================================
          SELAMAT DATANG DI KIOS BERAS ADITYA JAYA
                
          __Siap Melengkapi Kebutuhan Dapur Anda__
==========================================================  
        Menu 1 : Menampilkan data
        Menu 2 : Menambah data beras
        Menu 3 : Mengupdate data beras
        Menu 4 : Menghapus data beras
        Menu 5 : Membeli data beras
        Menu 6 : Exit 
''')

def main():
    while True:
        print(PROMPT)
        menu_input = pyip.inputInt(prompt='> Silahkan pilih menu:', min=1, max=6)
        
        if menu_input == 1:
            while True:
                print("Menu 1 - Tampilkan data:")
                print("1. Tampilkan semua data beras")
                print("2. Pencarian beras (dengan barcode)")
                print("3. Kembali ke menu utama")
                submenu_input = pyip.inputChoice(["1", "2", "3"], prompt='> Silahkan pilih submenu:')
                
                if submenu_input == '1':
                    show(db)
                elif submenu_input == '2':
                    search_by_barcode(db)
                elif submenu_input == '3':
                    break  # Kembali ke menu utama
                else:
                    print('Submenu tidak valid. Silahkan pilih submenu 1-3.')
        elif menu_input == 2:
            add(db, used_barcodes)
        elif menu_input == 3:
            update(db)
        elif menu_input == 4:
            delete(db)
        elif menu_input == 5:
            buy(db)
        elif menu_input == 6:
            print('Terima kasih! Datang kembali.')
            break  # Keluar dari loop dan program
        else:
            print('Menu tidak ada. Silahkan pilih menu 1-6.')

if __name__ == '__main__':
    main()
