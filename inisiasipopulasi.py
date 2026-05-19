import random

def inisialisasi_populasi(jumlah_populasi, jumlah_gen):
    """
    Fungsi untuk menginisialisasi populasi awal secara acak.
    Setiap individu direpresentasikan sebagai list biner (kromosom).
    """
    populasi = []
    for _ in range(jumlah_populasi):
        # Setiap gen diisi secara acak dengan nilai 0 atau 1
        kromosom = [random.randint(0, 1) for _ in range(jumlah_gen)]
        populasi.append(kromosom)
    return populasi
