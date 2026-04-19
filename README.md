# WA2-Arch — KCAP Repacker untuk White Album 2

Tool untuk mengekstrak dan merepack arsip `.pak` (format KCAP) dari game visual novel **White Album 2**.

---

## Apa Ini?

White Album 2 menyimpan aset-asetnya — script, gambar, font, dan lainnya — dalam satu file arsip berformat KCAP dengan ekstensi `.pak`. Repo ini menyediakan tool untuk membongkar dan membangun ulang arsip tersebut, yang menjadi pondasi utama untuk keperluan modding maupun translation.

Proses ekstraksi ditangani oleh **exkizpak** (karya asmodean), sementara untuk repack disediakan script Python bernama `kcap_repack_v1.1.py`. Perbaikan utama di versi 1.1 ini adalah dukungan penuh terhadap encoding **Shift-JIS** untuk nama file berbahasa Jepang — hal yang krusial karena game ini menggunakan nama file seperti `14pt袋.tga` untuk font-nya. Tanpa encoding yang benar, font tidak akan terbaca oleh game.

---

## Struktur File

| File | Peran |
|---|---|
| `exkizpak_v2.exe` | Tool ekstraksi arsip `.pak` (versi binary siap pakai) |
| `exkizpak.cpp` | Source code C++ dari exkizpak |
| `kcap_repack_v1.1.py` | Script Python untuk merepack folder hasil ekstrak kembali ke `.pak` |
| `repack_v1.1_interactive.bat` | Batch script interaktif — drag-and-drop folder lalu ketik nama output |
| `repack_simple.bat` | Batch script sederhana tanpa input interaktif |
| `files.zip` | File-file tambahan pendukung |

---

## Cara Pakai

Alurnya terdiri dari dua tahap: **ekstrak → edit → repack**.

### Tahap 1 — Ekstrak File PAK

Gunakan `exkizpak_v2.exe` untuk membongkar file `.pak` ke sebuah folder:

```bash
exkizpak_v2.exe script.pak
```

Seluruh isi arsip akan diekstrak ke folder baru secara otomatis.

### Tahap 2 — Edit File

Buka dan edit file-file hasil ekstrak sesuai kebutuhan, baik itu script dialog, gambar, maupun file lainnya. **Jangan mengganti nama file apapun**, terutama file yang namanya mengandung karakter Jepang. Nama file yang berubah akan menyebabkan game tidak bisa menemukannya dan berpotensi crash.

### Tahap 3 — Repack

Ada dua cara untuk merepack:

**Cara pertama — drag-and-drop (lebih mudah):** Seret folder hasil ekstrak yang sudah diedit langsung ke atas file `repack_v1.1_interactive.bat`. Setelah terbuka, ketik nama file output yang diinginkan (contoh: `en.pak`) lalu tekan Enter.

**Cara kedua — via command line:**

```bash
python kcap_repack_v1.1.py folder_hasil_ekstrak/ output.pak
```

Hasil repack akan langsung menghasilkan file `.pak` baru yang siap digunakan.

---

## Catatan Teknis

Format KCAP membatasi panjang nama file hingga **24 byte dalam encoding Shift-JIS**. Nama file yang terlalu panjang akan dipotong otomatis oleh repacker. Selain itu, arsip yang dihasilkan tidak menggunakan kompresi sama sekali — ini memang sesuai dengan format original game-nya.

---

## Requirements

Tool ini membutuhkan **Python 3.6 atau lebih baru**. Tidak ada dependensi eksternal yang perlu diinstall. Untuk ekstraksi, cukup gunakan `exkizpak_v2.exe` yang sudah tersedia di repo ini tanpa perlu build dari source.

---

## Disclaimer

Tool ini dibuat semata-mata untuk keperluan edukasi, penelitian, dan modding personal. Pengguna bertanggung jawab penuh untuk memastikan penggunaannya sesuai dengan aturan copyright dan Terms of Service dari game original.

---

## Kredit

Proses ekstraksi didasarkan pada **exkizpak** oleh asmodean. Repacker ini dikembangkan di atasnya dengan perbaikan dukungan Shift-JIS dan penanganan error yang lebih baik.
