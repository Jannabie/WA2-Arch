# WA2-Arch KCAP Repacker untuk White Album 2

Tool untuk mengekstrak dan merepack arsip `.pak` (format KCAP) dari game visual novel **White Album 2**.

---

## Proof of Concept

Hasil terjemahan yang berhasil dipack kembali ke dalam game:

| Preview |
|:---:|
| ![Proof of Translation](https://i.imgur.com/YablNs4.jpeg) |
| Terjemahan berhasil terbaca oleh game setelah repack |

---

## Apa Ini?

White Album 2 menyimpan aset-asetnya — script, gambar, font, dan lainnya — dalam satu file arsip berformat KCAP dengan ekstensi `.pak`. Repo ini menyediakan tool untuk membongkar dan membangun ulang arsip tersebut, yang menjadi pondasi utama untuk keperluan modding maupun translation.

Proses ekstraksi ditangani oleh **exkizpak** (karya asmodean), sementara untuk repack disediakan script Python bernama `kcap_repack.py`. Perbaikan utama di versi ini adalah dukungan penuh terhadap encoding **Shift-JIS** untuk nama file berbahasa Jepang — hal yang krusial karena game ini menggunakan nama file seperti `14pt袋.tga` untuk font-nya. Tanpa encoding yang benar, font tidak akan terbaca oleh game.

---

## Struktur File

| File | Peran |
|---|---|
| `exkizpak_v2.exe` | Tool ekstraksi arsip `.pak` (binary siap pakai) |
| `exkizpak.cpp` | Source code C++ dari exkizpak |
| `kcap_repack.py` | Script Python untuk merepack folder hasil ekstrak kembali ke `.pak` |

---

## Cara Pakai

Alurnya terdiri dari tiga tahap: **persiapan → ekstrak → edit → repack**.

### Tahap 1 — Persiapan Folder

Sebelum mulai, buat satu folder khusus sebagai ruang kerja. Ini penting agar isi `.pak` tidak bercampur dengan file tool itu sendiri, sehingga tidak ikut terepack secara tidak sengaja.

```
workspace/
└── exkizpak_v2.exe   ← taruh dulu di sini
```

Masukkan `exkizpak_v2.exe` ke dalam folder tersebut, lalu letakkan file `.pak` yang ingin diekstrak ke dalamnya juga.

### Tahap 2 — Ekstrak File PAK

Jalankan `exkizpak_v2.exe` lewat command line dengan memberikan nama file `.pak` sebagai argumen:

```bash
exkizpak_v2.exe script.pak
```

Seluruh isi arsip akan diekstrak ke subfolder baru secara otomatis. Setelah proses selesai, **pindahkan keluar** file `.pak` asli dan `exkizpak_v2.exe` dari folder tersebut. Jika dibiarkan, keduanya akan ikut terepack bersama file-file aset saat proses repack dijalankan.

Struktur yang benar sebelum mulai edit:

```
workspace/
└── script/           ← folder hasil ekstrak, ini saja yang tersisa
    ├── 001.bin
    ├── 001.txt
    └── ...
```

### Tahap 3 — Edit File

Buka dan edit file-file hasil ekstrak sesuai kebutuhan, baik itu script dialog, gambar, maupun file lainnya.

> **Penting:** Jangan mengganti nama file apapun, terutama file yang namanya mengandung karakter Jepang. Nama file yang berubah akan menyebabkan game tidak bisa menemukannya dan berpotensi crash.

### Tahap 4 — Repack via CLI

Setelah selesai mengedit, jalankan repacker lewat command line:

```bash
python kcap_repack.py <folder_hasil_ekstrak> <nama_output.pak>
```

Contoh:

```bash
python kcap_repack.py script/ en.pak
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
