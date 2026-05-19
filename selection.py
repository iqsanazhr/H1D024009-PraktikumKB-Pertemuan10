import random

def roulette_wheel_selection(populasi, fitness_populasi):
    """
    Metode seleksi orang tua berbasis Roulette Wheel Selection (Seleksi Roda Roulette).
    Memilih kromosom berdasarkan nilai probabilitas kebugaran proporsional.
    """
    total_fitness = sum(fitness_populasi)
    
    # Menghindari pembagian dengan nol jika seluruh populasi memiliki fitness 0
    if total_fitness == 0:
        idx = random.randrange(len(populasi))
        return populasi[idx], idx
        
    # Menghitung probabilitas masing-masing individu
    probabilitas = [fitness / total_fitness for fitness in fitness_populasi]
    
    # Menghitung probabilitas kumulatif
    kumulatif_prob = []
    kumulatif = 0
    for p in probabilitas:
        kumulatif += p
        kumulatif_prob.append(kumulatif)
        
    # Memutar roda roulette (memilih angka acak antara 0 dan 1)
    r = random.random()
    for i, kum_prob in enumerate(kumulatif_prob):
        if r <= kum_prob:
            return populasi[i], i
            
    # Kembalikan elemen terakhir sebagai fallback keamanan
    return populasi[-1], len(populasi) - 1


def tournament_selection(populasi, fitness_populasi, ukuran_turnamen=3):
    """
    Metode seleksi orang tua berbasis Tournament Selection.
    Memilih secara acak beberapa individu (ukuran turnamen) dan membandingkan
    untuk mendapatkan individu dengan nilai fitness tertinggi.
    """
    populasi_size = len(populasi)
    kandidat_indices = random.sample(range(populasi_size), ukuran_turnamen)
    
    terbaik_idx = kandidat_indices[0]
    terbaik_fitness = fitness_populasi[terbaik_idx]
    
    for idx in kandidat_indices[1:]:
        if fitness_populasi[idx] > terbaik_fitness:
            terbaik_idx = idx
            terbaik_fitness = fitness_populasi[idx]
            
    return populasi[terbaik_idx], terbaik_idx
