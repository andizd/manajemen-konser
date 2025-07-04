from sqlalchemy import Column, Integer, String, create_engine, Date
from sqlalchemy.orm import declarative_base, sessionmaker

# Setup Database
db_url = 'sqlite:///database.db'
engine = create_engine(db_url)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Model Event Konser
class Concerts(Base):
    __tablename__ = 'concerts'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)

Base.metadata.create_all(engine)

# --- CREATE ---
def add_concert():
    name = input("Nama Konser: ")
    location = input("Lokasi: ")
    
    try:
        new_concert = Concerts(name=name, location=location)
        session.add(new_concert)
        session.commit()
        print(f"Konser '{name}' berhasil ditambahkan.")
    except ValueError:
        print("Inputan Tidak Valid\n")

# --- READ ---
def list_concerts():
    concerts = session.query(Concerts).all()
    if not concerts:
        print("Tidak ada konser terdaftar.\n")
        return
    print("Daftar Konser:")
    for c in concerts:
        print(f"{c.id}. {c.name} - {c.location}")
    print()

# --- SEARCH ---
def search_concert():
    keyword = input("Masukkan nama konser yang ingin dicari: ")
    results = session.query(Concerts).filter(Concerts.name.ilike(f"%{keyword}%")).all()

    if results:
        print("\nHasil Pencarian:")
        for concert in results:
            print(f"{concert.id}. {concert.name} - {concert.location}")
    else:
        print("Tidak ditemukan konser dengan nama tersebut.")
    print()

# --- UPDATE ---
def update_concert():
    try:
        concert_id = int(input('ID Konser: '))
        concert = session.query(Concerts).get(concert_id)
        if concert:
            name = input(f'Nama Baru ({concert.name}): ') or concert.name
            location = input(f'Lokasi Baru ({concert.location}): ') or concert.location

            concert.name = name
            concert.location = location

            session.commit()
            print('Data Berhasil Diperbarui!')
        else:
            print('ID Tidak Ditemukan!')
    except ValueError:
        print('Input Tidak Benar')

# --- DELETE ---
def delete_concert():
    try:
        concert_id = int(input('ID Konser: '))
        concert = session.query(Concerts).get(concert_id)

        if concert:
            session.delete(concert)
            session.commit()
            print('Konser Berhasil Dihapus!')
        else:
            print('Konser Tidak Ditemukan!')
    except ValueError:
        print('Inputan Tidak Valid!')

# --- MENU ---
def menu():
    while True:
        print("=== MENU MANAJEMEN KONSER ===")
        print("1. Tambah Konser")
        print("2. Lihat Semua Konser")
        print("3. Cari Konser ")  # ← Tambahkan opsi ini
        print("4. Update Konser")
        print("5. Hapus Konser")
        print("6. Keluar")
        pilihan = input("Pilih menu (1-6): ")

        if pilihan == '1':
            add_concert()
        elif pilihan == '2':
            list_concerts()
        elif pilihan == '3':
            search_concert()  # ← Fungsi pencarian dipanggil di sini
        elif pilihan == '4':
            update_concert()
        elif pilihan == '5':
            delete_concert()
        elif pilihan == '6':
            break
        else:
            print('Menu Tidak Ditemukan')

if __name__ == '__main__':
    menu()