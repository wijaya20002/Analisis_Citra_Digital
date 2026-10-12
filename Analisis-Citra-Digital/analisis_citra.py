
from pathlib import Path
from PIL import Image, ExifTags
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

NAMA_FOTO = Path("foto_saya.jpg")
FOLDER_HASIL = Path("images")


def baca_citra(path):
    """Buka foto dan siapkan array RGB untuk analisis."""
    if not path.exists():
        raise FileNotFoundError("Letakkan foto_saya.jpg satu folder dengan script ini.")
    foto = Image.open(path)
    piksel_rgb = np.asarray(foto.convert("RGB"))
    return foto, piksel_rgb


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
    print("\n=== DATA EXIF ===")
    if exif:
        for tag_id, nilai in exif.items():
            nama_tag = ExifTags.TAGS.get(tag_id, str(tag_id))
            print(f"{nama_tag}: {nilai}")
    else:
        print("Foto tidak menyimpan metadata EXIF yang dapat dibaca.")
    return exif


def analisis_warna(piksel_rgb):
    """Hitung statistik RGB dan tingkat kecerahan rata-rata."""
    rata_rgb = piksel_rgb.mean(axis=(0, 1))
    minimum = piksel_rgb.min(axis=(0, 1))
    maksimum = piksel_rgb.max(axis=(0, 1))
    # Rumus luminansi memberi bobot berbeda pada kanal RGB.
    kecerahan = (0.299 * piksel_rgb[:, :, 0] +
                 0.587 * piksel_rgb[:, :, 1] +
                 0.114 * piksel_rgb[:, :, 2])
    print("\n=== HASIL PEMERIKSAAN PIXEL ===")
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


def buat_visualisasi(foto, piksel_rgb, exif, kecerahan, rata_rgb):
    """Simpan empat visualisasi analisis ke folder images."""
    FOLDER_HASIL.mkdir(exist_ok=True)
    tinggi, lebar, _ = piksel_rgb.shape
    ukuran = NAMA_FOTO.stat().st_size

    # 1. Ringkasan identitas file dan foto sumber.
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
            ax[1].text(x, y, f"{r}\n{g}\n{b}", ha="center", va="center", fontsize=6.5, color=warna_teks)
    fig.tight_layout(); fig.savefig(FOLDER_HASIL / "02_bedah_piksel.png", dpi=180, bbox_inches="tight"); plt.close(fig)
    print("\nContoh matriks RGB 5x5 (baris pertama):", sampel[0].tolist())

    # 3. Peta kecerahan khusus sebagai pembeda analisis.
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Karakteristik Cahaya dan Warna", fontsize=14, fontweight="bold")
    ax[0].imshow(foto); ax[0].set_title("Foto sumber"); ax[0].axis("off")
    peta = ax[1].imshow(kecerahan, cmap="gray", vmin=0, vmax=255)
    ax[1].set_title("Peta kecerahan (luminansi)"); ax[1].axis("off")
    fig.colorbar(peta, ax=ax[1], fraction=.046, pad=.04, label="Kecerahan 0-255")
    fig.tight_layout(); fig.savefig(FOLDER_HASIL / "03_peta_kecerahan.png", dpi=160, bbox_inches="tight"); plt.close(fig)

    # 4. Bandingkan sebaran intensitas kanal RGB.
    fig, ax = plt.subplots(figsize=(10, 5))
    for kanal, label, warna in [(0, "Merah (R)", "red"), (1, "Hijau (G)", "green"), (2, "Biru (B)", "blue")]:
        hitung, batas = np.histogram(piksel_rgb[:, :, kanal], bins=256, range=(0, 256))
        ax.plot(batas[:-1], hitung, color=warna, label=f"{label} | rata-rata {rata_rgb[kanal]:.1f}", linewidth=1)
    ax.set_title("Distribusi Intensitas Warna RGB", fontweight="bold")
    ax.set_xlabel("Intensitas (0 = gelap, 255 = terang)"); ax.set_ylabel("Jumlah piksel")
    ax.legend(); ax.grid(alpha=.2); fig.tight_layout()
    fig.savefig(FOLDER_HASIL / "04_distribusi_rgb.png", dpi=160, bbox_inches="tight"); plt.close(fig)


def main():
    foto, piksel_rgb = baca_citra(NAMA_FOTO)
    exif = tampilkan_metadata(foto, NAMA_FOTO, piksel_rgb)
    kecerahan, rata_rgb = analisis_warna(piksel_rgb)
    buat_visualisasi(foto, piksel_rgb, exif, kecerahan, rata_rgb)
    print("\nAnalisis selesai. Hasil visualisasi ada di folder 'images'.")
    print("Catatan: foto sumber hanya dibaca; file aslinya tidak ditimpa.")


if __name__ == "__main__":
    main()
