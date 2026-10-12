# Bedah Citra Digital — Metadata, Piksel, dan Kecerahan

**Nama:** Andre Wijaya  
**NIM:** 24260024

## 1. Gambaran proyek

Proyek ini membedah foto digital dari dua sisi: informasi yang tersimpan pada file dan angka-angka penyusun gambarnya. Analisis tetap mengikuti inti tugas, yaitu membaca metadata serta membuktikan bahwa gambar digital tersusun dari nilai piksel. Pengembangan tambahannya adalah menghitung tingkat kecerahan, menampilkan sampel nilai RGB berukuran 5×5, dan membuat histogram setiap kanal warna.

Foto sumber **tidak diedit atau ditimpa**. Program hanya membaca foto dan menyimpan visualisasi baru ke folder `images`.

## 2. Struktur folder

```text
Analisis-Citra-Digital/
├── analisis_citra.py
├── foto_saya.jpg
├── README.md
├── LAPORAN.md
└── images/
    ├── 01_identitas_citra.png
    ├── 02_bedah_piksel.png
    ├── 03_peta_kecerahan.png
    └── 04_distribusi_rgb.png
```

## 3. Instalasi dan cara menjalankan

Buka terminal VS Code di folder proyek, lalu jalankan:

```bash
python -m pip install Pillow numpy matplotlib
python analisis_citra.py
```

Jika perintah `python` tidak dikenali di Windows, coba gunakan `py`. Pastikan foto yang akan dianalisis bernama `foto_saya.jpg` dan berada satu folder dengan program.

---

# 4. Source code dan penjelasan per bagian

Setiap bagian di bawah mengikuti urutan program `analisis_citra.py`. Penjelasan diberikan terlebih dahulu, kemudian potongan kode yang berkaitan. Dengan begitu, pembaca bisa memahami tujuan kode sebelum melihat perintahnya.

## Bagian A — Memanggil library yang diperlukan

Pillow (`PIL`) dipakai untuk membuka foto dan membaca metadata EXIF. NumPy dipakai untuk mengolah nilai piksel sebagai matriks angka. Matplotlib digunakan untuk membuat gambar hasil analisis, sedangkan `Rectangle` menandai area sampel piksel pada foto. `Path` membantu mengelola lokasi file dan folder.

```python
from pathlib import Path
from PIL import Image, ExifTags
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
```

## Bagian B — Menentukan file sumber dan folder keluaran

Dua konstanta ini menyimpan nama foto yang akan dibaca dan nama folder tempat visualisasi disimpan. Kalau nama file foto berbeda, sesuaikan `foto_saya.jpg` dengan nama file yang dipakai. File foto sumber tidak ditulis ulang oleh program.

```python
NAMA_FOTO = Path("foto_saya.jpg")
FOLDER_HASIL = Path("images")
```

## Bagian C — Membuka foto dan menyiapkan data piksel

Fungsi `baca_citra()` memeriksa apakah foto tersedia. Jika file tidak ditemukan, program menghentikan proses dengan pesan yang menjelaskan apa yang harus diperiksa. Setelah foto dibuka, `convert("RGB")` menyiapkan representasi tiga kanal warna—merah, hijau, dan biru—untuk analisis. `np.asarray()` mengubah data gambar menjadi array angka. Konversi ini hanya dilakukan pada data di memori, bukan menyimpan ulang atau mengubah foto sumber.

```python
def baca_citra(path):
    """Buka foto dan siapkan array RGB untuk analisis."""
    if not path.exists():
        raise FileNotFoundError("Letakkan foto_saya.jpg satu folder dengan script ini.")
    foto = Image.open(path)
    piksel_rgb = np.asarray(foto.convert("RGB"))
    return foto, piksel_rgb
```

## Bagian D — Membaca metadata dan EXIF

Fungsi ini menampilkan identitas file, format, dimensi, mode warna, ukuran file, jumlah piksel, dan jumlah nilai kanal RGB. Bentuk array NumPy nantinya berurutan `(tinggi, lebar, kanal)`, sementara dimensi yang ditampilkan kepada pengguna ditulis sebagai `lebar × tinggi`. Program lalu membaca EXIF jika tersedia. EXIF dapat berisi informasi tambahan dari kamera atau perangkat, tetapi tidak semua foto memilikinya.

```python
def tampilkan_metadata(foto, path, piksel_rgb):
    """Cetak informasi file, dimensi, jumlah piksel, dan EXIF."""
    tinggi, lebar, kanal = piksel_rgb.shape
    exif = foto.getexif()
    print("=== IDENTITAS DAN METADATA CITRA ===")
    print(f"Nama file       : {path.name}")
    print(f"Format          : {foto.format}")
    print(f"Dimensi         : {lebar} x {tinggi} piksel")
    print(f"Mode file       : {foto.mode}")
    print(f"Ukuran file     : {path.stat().st_size:,} byte")
    print(f"Total piksel    : {lebar * tinggi:,}")
    print(f"Nilai kanal RGB : {piksel_rgb.size:,}")
    print("\\n=== DATA EXIF ===")
    if exif:
        for tag_id, nilai in exif.items():
            nama_tag = ExifTags.TAGS.get(tag_id, str(tag_id))
            print(f"{nama_tag}: {nilai}")
    else:
        print("Foto tidak menyimpan metadata EXIF yang dapat dibaca.")
    return exif
```

**Cara membaca hasilnya:** jika dimensi foto `lebar × tinggi`, jumlah piksel diperoleh dari `lebar × tinggi`. Karena citra RGB mempunyai tiga kanal per piksel, jumlah nilai kanal adalah jumlah piksel dikalikan tiga.

## Bagian E — Menghitung karakteristik warna dan kecerahan

Fungsi `analisis_warna()` menghitung nilai RGB minimum, maksimum, dan rata-rata pada seluruh foto. Nilai setiap kanal gambar 8-bit berada pada rentang 0–255. Fungsi ini juga menghitung luminansi atau perkiraan kecerahan menggunakan rumus `0.299R + 0.587G + 0.114B`. Bobot tiap kanal berbeda, sehingga kecerahan tidak sekadar dihitung dari rata-rata R, G, dan B.

Untuk membantu interpretasi, rata-rata kecerahan dikelompokkan menjadi cenderung gelap, menengah, atau terang. Batas tersebut merupakan kategori sederhana untuk pembacaan awal, bukan standar penilaian kualitas foto.

```python
def analisis_warna(piksel_rgb):
    """Hitung statistik RGB dan tingkat kecerahan rata-rata."""
    rata_rgb = piksel_rgb.mean(axis=(0, 1))
    minimum = piksel_rgb.min(axis=(0, 1))
    maksimum = piksel_rgb.max(axis=(0, 1))
    # Rumus luminansi memberi bobot berbeda pada kanal RGB.
    kecerahan = (0.299 * piksel_rgb[:, :, 0] +
                 0.587 * piksel_rgb[:, :, 1] +
                 0.114 * piksel_rgb[:, :, 2])
    print("\\n=== HASIL PEMERIKSAAN PIXEL ===")
    print("Bentuk array (tinggi, lebar, kanal):", piksel_rgb.shape)
    print("RGB minimum [R, G, B]             :", minimum.tolist())
    print("RGB maksimum [R, G, B]             :", maksimum.tolist())
    print("Rata-rata RGB                      :", np.round(rata_rgb, 2).tolist())
    print(f"Kecerahan rata-rata (0-255)         : {kecerahan.mean():.2f}")
    if kecerahan.mean() < 85:
        kategori = "cenderung gelap"
    elif kecerahan.mean() < 170:
        kategori = "kecerahan menengah"
    else:
        kategori = "cenderung terang"
    print("Interpretasi kecerahan              :", kategori)
    return kecerahan, rata_rgb
```

## Bagian F — Menyiapkan visualisasi identitas foto

Visualisasi pertama menampilkan foto sumber di satu sisi dan tabel metadata di sisi lain. Informasi yang dirangkum sama dengan data yang dicetak ke terminal. Tujuannya supaya pembaca dapat melihat gambar yang dianalisis sekaligus mengetahui identitas dasarnya.

```python
def buat_visualisasi(foto, piksel_rgb, exif, kecerahan, rata_rgb):
    """Simpan empat visualisasi analisis ke folder images."""
    FOLDER_HASIL.mkdir(exist_ok=True)
    tinggi, lebar, _ = piksel_rgb.shape
    ukuran = NAMA_FOTO.stat().st_size

    isi_metadata = [
        ["Nama file", NAMA_FOTO.name], ["Format", str(foto.format)],
        ["Dimensi", f"{lebar} x {tinggi} piksel"], ["Mode warna", foto.mode],
        ["Ukuran file", f"{ukuran:,} byte"], ["Jumlah piksel", f"{lebar*tinggi:,}"],
        ["Kanal analisis", "RGB (3 kanal)"], ["EXIF", "Tersedia" if exif else "Tidak ditemukan"]
    ]
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    fig.suptitle("BEDAH CITRA DIGITAL | Identitas Foto", fontsize=15, fontweight="bold")
    ax[0].imshow(foto); ax[0].set_title("Foto sumber (tidak diubah)"); ax[0].axis("off")
    ax[1].axis("off")
    tabel = ax[1].table(cellText=isi_metadata, colLabels=["Atribut", "Hasil"],
                        cellLoc="left", loc="center", colWidths=[.38, .62])
    tabel.auto_set_font_size(False); tabel.set_fontsize(9); tabel.scale(1, 1.55)
    fig.tight_layout(); fig.savefig(FOLDER_HASIL / "01_identitas_citra.png", dpi=160, bbox_inches="tight"); plt.close(fig)
```

## Bagian G — Mengambil sampel nilai RGB berukuran 5×5

Tidak praktis menampilkan seluruh nilai piksel foto yang besar. Karena itu, program mengambil 25 piksel dari area tengah foto sebagai sampel. Kotak kuning pada foto menunjukkan lokasi sampel tersebut. Visualisasi kedua memperbesar area kecil itu dan menuliskan tiga angka untuk setiap piksel: merah, hijau, dan biru. Ini menjadi bukti langsung bahwa gambar digital direpresentasikan oleh angka.

```python
    # 2. Ambil area 5x5 di tengah, tampilkan nilai RGB setiap piksel.
    xc, yc = lebar // 2, tinggi // 2
    x0 = max(0, min(xc - 2, lebar - 5)); y0 = max(0, min(yc - 2, tinggi - 5))
    sampel = piksel_rgb[y0:y0+5, x0:x0+5]
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Bedah Piksel | Lokasi Sampel dan Nilai RGB", fontsize=14, fontweight="bold")
    ax[0].imshow(foto); ax[0].add_patch(Rectangle((x0-.5, y0-.5), 5, 5, linewidth=2, edgecolor="yellow", facecolor="none"))
    ax[0].set_title(f"Area sampel: X={x0}, Y={y0}"); ax[0].axis("off")
    ax[1].imshow(sampel, interpolation="nearest"); ax[1].set_title("Setiap sel menampilkan R / G / B")
    ax[1].set_xticks(range(5)); ax[1].set_yticks(range(5))
    ax[1].set_xticklabels([str(x0+i) for i in range(5)]); ax[1].set_yticklabels([str(y0+i) for i in range(5)])
    ax[1].set_xticks(np.arange(-.5, 5, 1), minor=True); ax[1].set_yticks(np.arange(-.5, 5, 1), minor=True)
    ax[1].grid(which="minor", color="white", linewidth=1); ax[1].tick_params(which="minor", bottom=False, left=False)
    for y in range(5):
        for x in range(5):
            r, g, b = map(int, sampel[y, x])
            warna_teks = "white" if r + g + b < 380 else "black"
            ax[1].text(x, y, f"{r}\\n{g}\\n{b}", ha="center", va="center", fontsize=6.5, color=warna_teks)
    fig.tight_layout(); fig.savefig(FOLDER_HASIL / "02_bedah_piksel.png", dpi=180, bbox_inches="tight"); plt.close(fig)
    print("\\nContoh matriks RGB 5x5 (baris pertama):", sampel[0].tolist())
```

## Bagian H — Membuat peta kecerahan

Peta kecerahan adalah pengembangan dari analisis dasar metadata dan piksel. Program menampilkan foto sumber di sebelah kiri dan hasil perhitungan luminansi dalam skala abu-abu di sebelah kanan. Bagian yang lebih terang pada peta mempunyai nilai luminansi lebih tinggi; bagian yang gelap mempunyai nilai lebih rendah. Peta ini hanya visualisasi analisis dan tidak menggantikan foto asli.

```python
    # 3. Peta kecerahan khusus sebagai pembeda analisis.
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Karakteristik Cahaya dan Warna", fontsize=14, fontweight="bold")
    ax[0].imshow(foto); ax[0].set_title("Foto sumber"); ax[0].axis("off")
    peta = ax[1].imshow(kecerahan, cmap="gray", vmin=0, vmax=255)
    ax[1].set_title("Peta kecerahan (luminansi)"); ax[1].axis("off")
    fig.colorbar(peta, ax=ax[1], fraction=.046, pad=.04, label="Kecerahan 0-255")
    fig.tight_layout(); fig.savefig(FOLDER_HASIL / "03_peta_kecerahan.png", dpi=160, bbox_inches="tight"); plt.close(fig)
```

## Bagian I — Membandingkan distribusi intensitas RGB

Histogram memperlihatkan jumlah piksel pada setiap tingkat intensitas untuk kanal merah, hijau, dan biru. Sumbu horizontal menunjukkan intensitas 0–255, sedangkan sumbu vertikal menunjukkan jumlah piksel. Kurva yang menumpuk di kiri menandakan banyak nilai intensitas rendah pada kanal terkait; kurva di kanan menandakan banyak nilai tinggi. Interpretasi histogram sebaiknya tetap dibandingkan dengan foto sumber.

```python
    # 4. Bandingkan sebaran intensitas kanal RGB.
    fig, ax = plt.subplots(figsize=(10, 5))
    for kanal, label, warna in [(0, "Merah (R)", "red"), (1, "Hijau (G)", "green"), (2, "Biru (B)", "blue")]:
        hitung, batas = np.histogram(piksel_rgb[:, :, kanal], bins=256, range=(0, 256))
        ax.plot(batas[:-1], hitung, color=warna, label=f"{label} | rata-rata {rata_rgb[kanal]:.1f}", linewidth=1)
    ax.set_title("Distribusi Intensitas Warna RGB", fontweight="bold")
    ax.set_xlabel("Intensitas (0 = gelap, 255 = terang)"); ax.set_ylabel("Jumlah piksel")
    ax.legend(); ax.grid(alpha=.2); fig.tight_layout()
    fig.savefig(FOLDER_HASIL / "04_distribusi_rgb.png", dpi=160, bbox_inches="tight"); plt.close(fig)
```

## Bagian J — Mengatur urutan program

Fungsi `main()` menjadi pengatur jalannya analisis. Urutannya adalah membuka foto, menampilkan metadata, menghitung karakteristik warna dan kecerahan, lalu menyimpan visualisasi. Blok `if __name__ == "__main__":` memastikan `main()` dijalankan ketika file ini dieksekusi langsung.

```python
def main():
    foto, piksel_rgb = baca_citra(NAMA_FOTO)
    exif = tampilkan_metadata(foto, NAMA_FOTO, piksel_rgb)
    kecerahan, rata_rgb = analisis_warna(piksel_rgb)
    buat_visualisasi(foto, piksel_rgb, exif, kecerahan, rata_rgb)
    print("\\nAnalisis selesai. Hasil visualisasi ada di folder 'images'.")
    print("Catatan: foto sumber hanya dibaca; file aslinya tidak ditimpa.")


if __name__ == "__main__":
    main()
```

## 5. Cara memahami hasil analisis

- **Metadata:** menjelaskan identitas dasar file, dimensi, ukuran, dan EXIF yang tersedia.
- **Jumlah piksel:** diperoleh dari lebar dikalikan tinggi. Setiap piksel RGB menyimpan tiga nilai kanal.
- **RGB minimum, maksimum, dan rata-rata:** memberi gambaran rentang serta kecenderungan warna pada foto.
- **Sampel 5×5:** menampilkan 25 piksel beserta nilai R, G, dan B masing-masing.
- **Peta kecerahan:** membantu melihat perbedaan relatif area terang dan gelap.
- **Histogram RGB:** menunjukkan sebaran intensitas di masing-masing kanal warna.

Nilai numerik yang muncul akan mengikuti foto yang digunakan. Jika foto tidak menyimpan EXIF, program melaporkan bahwa datanya tidak tersedia.

## 6. Ringkasan inovasi

Analisis tetap berada dalam konteks tugas: membongkar informasi foto dan angka yang merepresentasikan gambar. Pengembangan yang ditambahkan adalah interpretasi tingkat kecerahan, visualisasi sampel RGB 5×5, peta kecerahan, dan histogram tiga kanal. Kode dipisah menjadi fungsi agar alur kerja lebih mudah dibaca dan dijelaskan.
