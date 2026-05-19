import tkinter as tk
from tkinter import ttk, messagebox
import random
import numpy as np
import matplotlib
matplotlib.use("TkAgg")  # Set backend for Tkinter integration
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Import modul GA local
from inisiasipopulasi import inisialisasi_populasi
from EvaluasiFitness import hitung_fitness
from selection import roulette_wheel_selection, tournament_selection
from crossover import one_point_crossover, two_point_crossover, uniform_crossover
from mutation import swap_mutation, inversion_mutation, uniform_mutation

class GeneticAlgorithmGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Knapsack Solver - Algoritma Genetika 2 (H1D024009)")
        self.root.geometry("1100x700")
        self.root.minsize(1000, 650)
        
        # Konfigurasi Tema Warna (Dark Theme)
        self.bg_dark = "#1e1e1e"
        self.bg_panel = "#252526"
        self.fg_white = "#ffffff"
        self.fg_gray = "#cccccc"
        self.accent_blue = "#007acc"
        self.accent_green = "#4caf50"
        self.accent_red = "#f44336"
        
        self.root.configure(bg=self.bg_dark)
        
        # Mengatur gaya TTK agar serasi dengan tema gelap
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.style.configure(".", background=self.bg_panel, foreground=self.fg_white, fieldbackground=self.bg_panel)
        self.style.configure("TFrame", background=self.bg_dark)
        self.style.configure("Panel.TFrame", background=self.bg_panel)
        self.style.configure("TLabel", background=self.bg_panel, foreground=self.fg_white, font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", background=self.bg_panel, foreground=self.accent_blue, font=("Segoe UI", 12, "bold"))
        self.style.configure("TButton", background=self.accent_blue, foreground=self.fg_white, font=("Segoe UI", 10, "bold"), borderwidth=0)
        self.style.map("TButton", background=[("active", "#0098ff")])
        self.style.configure("TCombobox", background="#333333", foreground=self.fg_white, fieldbackground="#333333")
        
        # Daftar barang default sesuai Ketentuan Praktikum Shift Anda
        self.barang_default = [
            ("Barang1", 10, 5),
            ("Barang2", 40, 4),
            ("Barang3", 30, 6),
            ("Barang4", 50, 3),
            ("Barang5", 35, 7)
        ]
        
        self.barang_list = list(self.barang_default)
        
        # Membangun layout UI
        self.create_widgets()
        
    def create_widgets(self):
        # Grid layout: Kolom 0 (Konfigurasi & Barang), Kolom 1 (Hasil & Grafik)
        self.root.columnconfigure(0, weight=2)
        self.root.columnconfigure(1, weight=3)
        self.root.rowconfigure(0, weight=1)
        
        # ==========================================
        # PANEL KIRI: KONFIGURASI DAN BARANG
        # ==========================================
        left_container = ttk.Frame(self.root, style="TFrame")
        left_container.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        left_container.columnconfigure(0, weight=1)
        left_container.rowconfigure(0, weight=0) # Parameter GA
        left_container.rowconfigure(1, weight=1) # Daftar Barang
        
        # 1. Box Parameter GA
        ga_param_panel = ttk.Frame(left_container, style="Panel.TFrame", padding=15)
        ga_param_panel.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        ga_param_panel.columnconfigure((0, 1, 2, 3), weight=1)
        
        ttk.Label(ga_param_panel, text="PARAMETER ALGORITMA GENETIKA", style="Header.TLabel").grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))
        
        # Row 1 Inputs
        ttk.Label(ga_param_panel, text="Kapasitas Tas:").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_kapasitas = ttk.Entry(ga_param_panel, width=10)
        self.entry_kapasitas.grid(row=1, column=1, sticky="w", pady=5)
        self.entry_kapasitas.insert(0, "15")
        
        ttk.Label(ga_param_panel, text="Jumlah Populasi:").grid(row=1, column=2, sticky="w", pady=5)
        self.entry_populasi = ttk.Entry(ga_param_panel, width=10)
        self.entry_populasi.grid(row=1, column=3, sticky="w", pady=5)
        self.entry_populasi.insert(0, "20")
        
        # Row 2 Inputs
        ttk.Label(ga_param_panel, text="Jumlah Generasi:").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_generasi = ttk.Entry(ga_param_panel, width=10)
        self.entry_generasi.grid(row=2, column=1, sticky="w", pady=5)
        self.entry_generasi.insert(0, "50")
        
        ttk.Label(ga_param_panel, text="Prob Crossover:").grid(row=2, column=2, sticky="w", pady=5)
        self.entry_prob_cross = ttk.Entry(ga_param_panel, width=10)
        self.entry_prob_cross.grid(row=2, column=3, sticky="w", pady=5)
        self.entry_prob_cross.insert(0, "0.5")
        
        # Row 3 Inputs
        ttk.Label(ga_param_panel, text="Prob Mutasi:").grid(row=3, column=0, sticky="w", pady=5)
        self.entry_prob_mutasi = ttk.Entry(ga_param_panel, width=10)
        self.entry_prob_mutasi.grid(row=3, column=1, sticky="w", pady=5)
        self.entry_prob_mutasi.insert(0, "0.1")
        
        # Row 4 Dropdowns (Default disesuaikan NIM H1D024009: RWS, One Point, Swap)
        ttk.Label(ga_param_panel, text="Metode Seleksi:").grid(row=4, column=0, sticky="w", pady=5)
        self.combo_seleksi = ttk.Combobox(ga_param_panel, values=["Roulette Wheel (RWS)", "Tournament Selection (TS)"], state="readonly", width=22)
        self.combo_seleksi.grid(row=4, column=1, columnspan=3, sticky="we", pady=5, padx=(0, 10))
        self.combo_seleksi.set("Roulette Wheel (RWS)") # Default RWS (NIM Digit 1 = 0)
        
        ttk.Label(ga_param_panel, text="Metode Crossover:").grid(row=5, column=0, sticky="w", pady=5)
        self.combo_cross = ttk.Combobox(ga_param_panel, values=["One Point", "Two Point", "Uniform"], state="readonly", width=22)
        self.combo_cross.grid(row=5, column=1, columnspan=3, sticky="we", pady=5, padx=(0, 10))
        self.combo_cross.set("One Point") # Default One Point (NIM Digit 2 = 9)
        
        ttk.Label(ga_param_panel, text="Metode Mutasi:").grid(row=6, column=0, sticky="w", pady=5)
        self.combo_mutasi = ttk.Combobox(ga_param_panel, values=["Swap Mutation", "Inversion Mutation", "Uniform Mutation"], state="readonly", width=22)
        self.combo_mutasi.grid(row=6, column=1, columnspan=3, sticky="we", pady=5, padx=(0, 10))
        self.combo_mutasi.set("Swap Mutation") # Default Swap Mutation (Jumlah NIM 0+9 = 9)
        
        # Info NIM
        nim_label = ttk.Label(ga_param_panel, text="Identitas Mahasiswa: Iqsan Azhar N | NIM: H1D024009", foreground="#888888", font=("Segoe UI", 8, "italic"))
        nim_label.grid(row=7, column=0, columnspan=4, sticky="w", pady=(10, 0))

        # 2. Box Kelola Barang
        barang_panel = ttk.Frame(left_container, style="Panel.TFrame", padding=15)
        barang_panel.grid(row=1, column=0, sticky="nsew")
        barang_panel.rowconfigure(1, weight=1)
        barang_panel.columnconfigure(0, weight=1)
        
        ttk.Label(barang_panel, text="KELOLA DAFTAR BARANG GUDANG", style="Header.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))
        
        # Form tambah barang
        tambah_frame = ttk.Frame(barang_panel, style="Panel.TFrame")
        tambah_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        tambah_frame.columnconfigure((1, 3, 5), weight=1)
        
        ttk.Label(tambah_frame, text="Nama:").grid(row=0, column=0, padx=2)
        self.entry_item_nama = ttk.Entry(tambah_frame, width=8)
        self.entry_item_nama.grid(row=0, column=1, padx=2, sticky="ew")
        self.entry_item_nama.insert(0, "BarangX")
        
        ttk.Label(tambah_frame, text="Untung:").grid(row=0, column=2, padx=2)
        self.entry_item_untung = ttk.Entry(tambah_frame, width=5)
        self.entry_item_untung.grid(row=0, column=3, padx=2, sticky="ew")
        self.entry_item_untung.insert(0, "50")
        
        ttk.Label(tambah_frame, text="Ukuran:").grid(row=0, column=4, padx=2)
        self.entry_item_ukuran = ttk.Entry(tambah_frame, width=5)
        self.entry_item_ukuran.grid(row=0, column=5, padx=2, sticky="ew")
        self.entry_item_ukuran.insert(0, "10")
        
        btn_add = tk.Button(tambah_frame, text="+ Tambah", command=self.add_item, bg=self.accent_green, fg=self.fg_white, font=("Segoe UI", 9, "bold"), bd=0, padx=6)
        btn_add.grid(row=0, column=6, padx=5)
        
        # Treeview (Table)
        # Custom Treeview Colors
        self.style.configure("Treeview", background="#2a2a2a", foreground=self.fg_white, fieldbackground="#2a2a2a", rowheight=24)
        self.style.configure("Treeview.Heading", background="#333333", foreground=self.fg_white, font=("Segoe UI", 9, "bold"))
        self.style.map("Treeview", background=[("selected", self.accent_blue)])
        
        tree_scroll = ttk.Scrollbar(barang_panel)
        tree_scroll.grid(row=2, column=1, sticky="ns", pady=2)
        
        self.tree = ttk.Treeview(barang_panel, columns=("Nama", "Keuntungan", "Ukuran"), show="headings", yscrollcommand=tree_scroll.set)
        self.tree.grid(row=2, column=0, sticky="nsew", pady=2)
        tree_scroll.config(command=self.tree.yview)
        
        self.tree.heading("Nama", text="Nama Barang")
        self.tree.heading("Keuntungan", text="Keuntungan (Value)")
        self.tree.heading("Ukuran", text="Ukuran (Weight)")
        
        self.tree.column("Nama", width=120, anchor="center")
        self.tree.column("Keuntungan", width=100, anchor="center")
        self.tree.column("Ukuran", width=100, anchor="center")
        
        # Tombol Aksi Barang
        action_frame = ttk.Frame(barang_panel, style="Panel.TFrame")
        action_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        
        btn_del = tk.Button(action_frame, text="Hapus Barang Terpilih", command=self.delete_item, bg=self.accent_red, fg=self.fg_white, font=("Segoe UI", 9, "bold"), bd=0, padx=10, pady=5)
        btn_del.pack(side="left", padx=(0, 10))
        
        btn_reset = tk.Button(action_frame, text="Reset Default", command=self.reset_default_items, bg="#555555", fg=self.fg_white, font=("Segoe UI", 9, "bold"), bd=0, padx=10, pady=5)
        btn_reset.pack(side="left")
        
        # Populasikan tabel pertama kali
        self.update_treeview()

        # ==========================================
        # PANEL KANAN: HASIL DAN GRAFIK
        # ==========================================
        right_container = ttk.Frame(self.root, style="TFrame")
        right_container.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")
        right_container.columnconfigure(0, weight=1)
        right_container.rowconfigure(0, weight=1) # Box Grafik
        right_container.rowconfigure(1, weight=0) # Box Hasil
        right_container.rowconfigure(2, weight=0) # Tombol RUN
        
        # 1. Box Grafik Matplotlib
        self.chart_panel = ttk.Frame(right_container, style="Panel.TFrame", padding=10)
        self.chart_panel.grid(row=0, column=0, sticky="nsew", pady=(0, 15))
        self.chart_panel.rowconfigure(0, weight=1)
        self.chart_panel.columnconfigure(0, weight=1)
        
        # Setup Figure Awal
        self.fig, self.ax = plt.subplots(figsize=(6, 3.8), facecolor="#252526")
        self.ax.set_facecolor("#1e1e1e")
        self.ax.tick_params(colors=self.fg_white)
        self.ax.xaxis.label.set_color(self.fg_white)
        self.ax.yaxis.label.set_color(self.fg_white)
        self.ax.set_title("Grafik Perkembangan Fitness", color=self.fg_white, fontname="Segoe UI", fontsize=11, fontweight="bold")
        self.ax.set_xlabel("Generasi")
        self.ax.set_ylabel("Nilai Fitness")
        self.ax.grid(True, color="#333333", linestyle="--")
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_panel)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, sticky="nsew")
        
        # 2. Box Hasil Analisis
        self.results_panel = ttk.Frame(right_container, style="Panel.TFrame", padding=15)
        self.results_panel.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        self.results_panel.columnconfigure(0, weight=1)
        
        ttk.Label(self.results_panel, text="HASIL SOLUSI OPTIMAL ALGORITMA GENETIKA", style="Header.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.text_results = tk.Text(self.results_panel, height=8, bg="#1e1e1e", fg="#a9ff8f", font=("Consolas", 10), bd=0, highlightthickness=1, highlightcolor="#333333", padx=10, pady=8)
        self.text_results.grid(row=1, column=0, sticky="ew")
        self.text_results.insert("1.0", "Tekan tombol 'JALANKAN EVOLUSI' di bawah untuk memulai pencarian solusi optimal.")
        self.text_results.config(state="disabled")
        
        # 3. Tombol Utama RUN GA
        self.btn_run = tk.Button(right_container, text="🚀 JALANKAN EVOLUSI ALGORITMA GENETIKA", command=self.execute_ga, bg=self.accent_blue, fg=self.fg_white, font=("Segoe UI", 12, "bold"), bd=0, pady=10, activebackground="#0098ff", activeforeground=self.fg_white)
        self.btn_run.grid(row=2, column=0, sticky="ew")
        
    def update_treeview(self):
        # Bersihkan treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Isi ulang dengan data terbaru
        for item in self.barang_list:
            self.tree.insert("", "end", values=(item[0], item[1], item[2]))
            
    def add_item(self):
        nama = self.entry_item_nama.get().strip()
        untung_str = self.entry_item_untung.get().strip()
        ukuran_str = self.entry_item_ukuran.get().strip()
        
        if not nama or not untung_str or not ukuran_str:
            messagebox.showwarning("Input Salah", "Seluruh field tambah barang harus diisi!")
            return
            
        try:
            untung = int(untung_str)
            ukuran = int(ukuran_str)
            if untung <= 0 or ukuran <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Format Salah", "Nilai Keuntungan dan Ukuran harus berupa angka bulat positif!")
            return
            
        # Tambahkan ke daftar barang
        self.barang_list.append((nama, untung, ukuran))
        self.update_treeview()
        
        # Kosongkan entry & increment nama default
        self.entry_item_nama.delete(0, tk.END)
        self.entry_item_nama.insert(0, f"Barang{len(self.barang_list)+1}")
        
    def delete_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Pilih Barang", "Silakan klik barang pada tabel yang ingin dihapus!")
            return
            
        for sel in selected_item:
            item_values = self.tree.item(sel, "values")
            # Cari dan hapus dari list
            for i, item in enumerate(self.barang_list):
                if item[0] == item_values[0] and str(item[1]) == str(item_values[1]) and str(item[2]) == str(item_values[2]):
                    del self.barang_list[i]
                    break
                    
        self.update_treeview()
        
    def reset_default_items(self):
        self.barang_list = list(self.barang_default)
        self.update_treeview()
        
    def execute_ga(self):
        if not self.barang_list:
            messagebox.showerror("Gudang Kosong", "Daftar barang tidak boleh kosong! Silakan tambahkan barang terlebih dahulu.")
            return
            
        # Read parameter GA & validasi
        try:
            kapasitas_tas = int(self.entry_kapasitas.get().strip())
            jumlah_populasi = int(self.entry_populasi.get().strip())
            jumlah_generasi = int(self.entry_generasi.get().strip())
            prob_crossover = float(self.entry_prob_cross.get().strip())
            prob_mutasi = float(self.entry_prob_mutasi.get().strip())
            
            if kapasitas_tas <= 0 or jumlah_populasi <= 0 or jumlah_generasi <= 0:
                raise ValueError("Nilai numerik harus berupa angka positif!")
            if not (0 <= prob_crossover <= 1) or not (0 <= prob_mutasi <= 1):
                raise ValueError("Probabilitas harus berada di antara 0 dan 1!")
        except ValueError as e:
            messagebox.showerror("Parameter Salah", f"Pastikan seluruh parameter diisi dengan benar!\nDetail: {e}")
            return
            
        # Ambil metode terpilih dari Combobox
        metode_seleksi = self.combo_seleksi.get()
        metode_cross = self.combo_cross.get()
        metode_mutasi = self.combo_mutasi.get()
        
        jumlah_gen = len(self.barang_list)
        
        # 1. Inisialisasi Populasi Awal
        populasi = inisialisasi_populasi(jumlah_populasi, jumlah_gen)
        
        # List data histori untuk plotting grafik
        best_fitness_list = []
        worst_fitness_list = []
        avg_fitness_list = []
        scatter_x = []
        scatter_y = []
        
        best_kromosom_global = None
        best_fitness_global = -1
        
        # Perulangan Generasi GA
        for gen_idx in range(jumlah_generasi):
            # Hitung fitness populasi saat ini
            fitness_populasi = [hitung_fitness(ind, self.barang_list, kapasitas_tas) for ind in populasi]
            
            # Catat statistik generasi
            best_gen_fit = max(fitness_populasi)
            worst_gen_fit = min(fitness_populasi)
            avg_gen_fit = sum(fitness_populasi) / len(fitness_populasi)
            
            best_fitness_list.append(best_gen_fit)
            worst_fitness_list.append(worst_gen_fit)
            avg_fitness_list.append(avg_gen_fit)
            
            # Catat sebaran titik populasi
            for fit in fitness_populasi:
                scatter_x.append(gen_idx)
                scatter_y.append(fit)
                
            # Update Solusi Terbaik Global
            idx_best = np.argmax(fitness_populasi)
            if fitness_populasi[idx_best] > best_fitness_global:
                best_fitness_global = fitness_populasi[idx_best]
                best_kromosom_global = list(populasi[idx_best])
                
            # Pembuatan Generasi Baru
            populasi_baru = []
            
            # Elitisme: Pertahankan 2 individu terbaik langsung ke generasi berikutnya
            sorted_indices = np.argsort(fitness_populasi)[::-1]
            populasi_baru.append(list(populasi[sorted_indices[0]]))
            populasi_baru.append(list(populasi[sorted_indices[1]]))
            
            while len(populasi_baru) < jumlah_populasi:
                # 2. Seleksi Orang Tua
                if "Roulette Wheel" in metode_seleksi:
                    parent1, _ = roulette_wheel_selection(populasi, fitness_populasi)
                    parent2, _ = roulette_wheel_selection(populasi, fitness_populasi)
                else: # Tournament Selection
                    parent1, _ = tournament_selection(populasi, fitness_populasi, ukuran_turnamen=3)
                    parent2, _ = tournament_selection(populasi, fitness_populasi, ukuran_turnamen=3)
                    
                # 3. Penyilangan (Crossover)
                if random.random() < prob_crossover:
                    if metode_cross == "One Point":
                        anak1, anak2 = one_point_crossover(parent1, parent2)
                    elif metode_cross == "Two Point":
                        anak1, anak2 = two_point_crossover(parent1, parent2)
                    else: # Uniform Crossover
                        anak1, anak2 = uniform_crossover(parent1, parent2)
                else:
                    anak1, anak2 = list(parent1), list(parent2)
                    
                # 4. Mutasi Gen
                if random.random() < prob_mutasi:
                    if "Swap" in metode_mutasi:
                        anak1 = swap_mutation(anak1)
                    elif "Inversion" in metode_mutasi:
                        anak1 = inversion_mutation(anak1)
                    else: # Uniform Mutation
                        anak1 = uniform_mutation(anak1)
                        
                if random.random() < prob_mutasi:
                    if "Swap" in metode_mutasi:
                        anak2 = swap_mutation(anak2)
                    elif "Inversion" in metode_mutasi:
                        anak2 = inversion_mutation(anak2)
                    else: # Uniform Mutation
                        anak2 = uniform_mutation(anak2)
                        
                populasi_baru.append(anak1)
                if len(populasi_baru) < jumlah_populasi:
                    populasi_baru.append(anak2)
                    
            populasi = populasi_baru
            
        # ==========================================
        # PLOTTING GRAFIK REAL-TIME KE CANVAS
        # ==========================================
        self.ax.clear()
        self.ax.set_facecolor("#1e1e1e")
        self.ax.grid(True, color="#333333", linestyle="--")
        self.ax.tick_params(colors=self.fg_white)
        self.ax.xaxis.label.set_color(self.fg_white)
        self.ax.yaxis.label.set_color(self.fg_white)
        
        # Plot titik-titik populasi
        self.ax.scatter(scatter_x, scatter_y, color="gray", alpha=0.15, s=15, label="Individu")
        
        # Plot garis nilai statistik
        self.ax.plot(range(jumlah_generasi), best_fitness_list, color="#4fc3f7", linewidth=2.5, label="Terbaik")
        self.ax.plot(range(jumlah_generasi), avg_fitness_list, color="#ff7043", linewidth=2, label="Rata-rata")
        self.ax.plot(range(jumlah_generasi), worst_fitness_list, color="#ffeb3b", linewidth=1.5, label="Terendah")
        
        self.ax.set_title("Analisis Evolusi Nilai Fitness", color=self.fg_white, fontname="Segoe UI", fontsize=11, fontweight="bold")
        self.ax.set_xlabel("Generasi")
        self.ax.set_ylabel("Nilai Fitness (Total Keuntungan)")
        self.ax.legend(facecolor="#252526", edgecolor="#333333", labelcolor=self.fg_white)
        
        self.fig.tight_layout()
        self.canvas.draw()
        
        # Simpan grafik perkembangan ke file lokal
        self.fig.savefig("fitness_development.png", dpi=300, facecolor="#252526")
        
        # ==========================================
        # FORMATTING HASIL OPTIMAL KE TEXT PANEL
        # ==========================================
        # Hitung berat total barang terpilih
        total_bobot = 0
        barang_terpilih = []
        for i in range(len(best_kromosom_global)):
            if best_kromosom_global[i] == 1:
                total_bobot += self.barang_list[i][2]
                barang_terpilih.append(self.barang_list[i][0])
                
        # Tampilkan teks hasil
        self.text_results.config(state="normal")
        self.text_results.delete("1.0", tk.END)
        
        hasil_teks = f"--- STATUS HASIL OPTIMASI ---\n"
        hasil_teks += f"✔ Nilai Fitness Terbaik : {best_fitness_global} (Keuntungan Maksimal)\n"
        hasil_teks += f"✔ Total Bobot / Ukuran : {total_bobot} (Kapasitas Maksimal: {kapasitas_tas})\n"
        hasil_teks += f"✔ Representasi Biner   : {best_kromosom_global}\n"
        hasil_teks += f"✔ Barang yang Dibeli   :\n"
        
        if barang_terpilih:
            for brg in barang_terpilih:
                hasil_teks += f"   - {brg}\n"
        else:
            hasil_teks += f"   - (Tidak ada barang yang terpilih)\n"
            
        hasil_teks += f"\n* Grafik tersimpan otomatis sebagai: 'fitness_development.png'"
        
        self.text_results.insert("1.0", hasil_teks)
        self.text_results.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = GeneticAlgorithmGUI(root)
    root.mainloop()
