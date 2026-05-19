import random

def one_point_crossover(parent1, parent2):
    """
    Melakukan One-Point Crossover (Penyilangan Satu Titik).
    Membagi gen di satu titik acak dan menukarnya di antara kedua orang tua.
    """
    # Memilih titik potong acak antara indeks 1 dan len - 1
    titik_potong = random.randint(1, len(parent1) - 1)
    
    # Membuat anak1 dan anak2
    anak1 = parent1[:titik_potong] + parent2[titik_potong:]
    anak2 = parent2[:titik_potong] + parent1[titik_potong:]
    
    return anak1, anak2


def two_point_crossover(parent1, parent2):
    """
    Melakukan Two-Point Crossover (Penyilangan Dua Titik).
    Membagi gen di dua titik acak dan menukar gen yang berada di antara kedua titik tersebut.
    """
    panjang = len(parent1)
    if panjang < 3:
        return one_point_crossover(parent1, parent2)
        
    titik1, titik2 = sorted(random.sample(range(1, panjang), 2))
    
    anak1 = parent1[:titik1] + parent2[titik1:titik2] + parent1[titik2:]
    anak2 = parent2[:titik1] + parent1[titik1:titik2] + parent2[titik2:]
    
    return anak1, anak2


def uniform_crossover(parent1, parent2, probabilitas_swapping=0.5):
    """
    Melakukan Uniform Crossover.
    Menentukan secara acak untuk setiap gen apakah akan ditukar antara kedua orang tua.
    """
    anak1 = []
    anak2 = []
    
    for i in range(len(parent1)):
        if random.random() < probabilitas_swapping:
            anak1.append(parent2[i])
            anak2.append(parent1[i])
        else:
            anak1.append(parent1[i])
            anak2.append(parent2[i])
            
    return anak1, anak2
