# LAPORAN TUGAS PENGOLAHAN CITRA DIGITAL

**Nama:** Andre Wijaya  
**NIM:** 24260024  
**Judul:** Mata Kulia Citra Digital 

## Tujuan

Mempelajari informasi dasar pada sebuah file foto serta memahami bagaimana gambar digital direpresentasikan sebagai matriks nilai piksel. Analisis mencakup metadata, data EXIF, nilai RGB, kecerahan, dan distribusi intensitas warna.

## Metode

Foto dibuka menggunakan Pillow, kemudian dikonversi ke representasi RGB untuk dianalisis dengan NumPy. Program mencetak dimensi, ukuran file, jumlah piksel, informasi EXIF yang tersedia, nilai minimum/maksimum/rata-rata RGB, serta rata-rata kecerahan. Matplotlib digunakan untuk menghasilkan visualisasi.

Foto sumber tidak diubah. Seluruh gambar dalam folder `images` merupakan keluaran visualisasi terpisah.

## Hasil visualisasi

1. **Identitas citra** — `images/01_identitas_citra.png`, memperlihatkan foto sumber dan ringkasan metadata.
2. **Bedah piksel** — `images/02_bedah_piksel.png`, menunjukkan lokasi sampel 5×5 dan angka RGB pada tiap piksel.
3. **Peta kecerahan** — `images/03_peta_kecerahan.png`, memperlihatkan sebaran luminansi dari area gelap ke terang.
4. **Distribusi RGB** — `images/04_distribusi_rgb.png`, membandingkan histogram intensitas kanal merah, hijau, dan biru.

## Pembahasan

Resolusi menunjukkan banyaknya piksel secara horizontal dan vertikal. Setiap piksel RGB memiliki tiga nilai kanal dengan rentang umum 0–255. Nilai minimum, maksimum, dan rata-rata memberi gambaran rentang warna dalam foto. Peta kecerahan dihitung menggunakan rumus luminansi `0.299R + 0.587G + 0.114B`; hasil rata-ratanya digunakan sebagai gambaran umum tingkat terang citra. Histogram menunjukkan frekuensi nilai intensitas untuk setiap kanal.

Metadata EXIF dapat memuat informasi tambahan, tetapi keberadaan dan kelengkapannya bergantung pada file sumber. Karena itu, program memeriksa EXIF yang benar-benar tersedia dan tidak mengasumsikan setiap foto memilikinya.

## Kesimpulan

Pengolahan citra digital dapat dimulai dengan membaca metadata dan mengubah gambar menjadi matriks angka. Dengan memeriksa contoh piksel, statistik RGB, peta kecerahan, dan histogram, karakteristik warna dan cahaya foto dapat dijelaskan melalui data. Pemisahan kode ke dalam beberapa fungsi juga membuat proses lebih rapi, mudah dipahami, dan lebih mudah dikembangkan.

## Library

- **Pillow:** membaca gambar dan metadata EXIF.
- **NumPy:** mengolah matriks piksel dan menghitung statistik.
- **Matplotlib:** membuat visualisasi hasil analisis.
