import random

def swap_mutation(kromosom):
    """
    Melakukan Swap Mutation (Mutasi Tukar).
    Memilih dua gen secara acak dan menukar nilainya.
    """
    kromosom_baru = list(kromosom)
    if len(kromosom_baru) < 2:
        return kromosom_baru
        
    posisi1, posisi2 = random.sample(range(len(kromosom_baru)), 2)
    kromosom_baru[posisi1], kromosom_baru[posisi2] = kromosom_baru[posisi2], kromosom_baru[posisi1]
    
    return kromosom_baru


def inversion_mutation(kromosom):
    """
    Melakukan Inversion Mutation (Mutasi Inversi).
    Membalik urutan segmen gen di antara dua indeks acak.
    """
    kromosom_baru = list(kromosom)
    panjang = len(kromosom_baru)
    if panjang < 2:
        return kromosom_baru
        
    idx1, idx2 = sorted(random.sample(range(panjang), 2))
    
    # Membalikkan segmen gen dari idx1 sampai idx2 (inclusive)
    kromosom_baru[idx1:idx2+1] = reversed(kromosom_baru[idx1:idx2+1])
    
    return kromosom_baru


def uniform_mutation(kromosom, probabilitas_gen=0.15):
    """
    Melakukan Uniform Mutation (Mutasi Biner/Flip Gen).
    Setiap bit gen memiliki probabilitas kecil untuk dibalik (flip dari 0 ke 1, atau 1 ke 0).
    """
    kromosom_baru = list(kromosom)
    for i in range(len(kromosom_baru)):
        if random.random() < probabilitas_gen:
            # Membalik bit gen (0 menjadi 1, dan 1 menjadi 0)
            kromosom_baru[i] = 1 - kromosom_baru[i]
            
    return kromosom_baru
