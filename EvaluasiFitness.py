def hitung_fitness(kromosom, barang, kapasitas_tas):
    """
    Fungsi untuk mengevaluasi nilai kebugaran (fitness) suatu individu/kromosom.
    Fitness diukur dari total keuntungan barang terpilih.
    Jika total ukuran (berat) barang terpilih melebihi kapasitas tas, 
    maka individu akan dikenakan penalti berupa fitness = 0.
    """
    total_keuntungan = 0
    total_ukuran = 0
    
    for i in range(len(kromosom)):
        if kromosom[i] == 1:
            total_keuntungan += barang[i][1]  # Menambahkan keuntungan
            total_ukuran += barang[i][2]      # Menambahkan ukuran (berat)
            
    # Skema penalti jika melebihi kapasitas maksimal tas
    if total_ukuran > kapasitas_tas:
        return 0
    else:
        return total_keuntungan
