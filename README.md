# Leaf Engine Arch

Tool for extracting and repacking `.pak` (KCAP format) archives from the visual novel **White Album 2**.

---

## Proof of Concept

Translation successfully repacked back into the game:

| Preview |
|:---:|
| ![Proof of Translation](https://i.imgur.com/YablNs4.jpeg) |
| Translation successfully read by the game after repacking |

---

## What Is This?

White Album 2 stores its assets — scripts, images, fonts, and more — in a single archive file using the KCAP format with the `.pak` extension. This repo provides tools to unpack and rebuild these archives, forming the main foundation for both modding and translation purposes.

Extraction is handled by **exkizpak** (created by asmodean), while repacking is handled by a Python script called `kcap_repack.py`. The main improvement in this version is full support for **Shift-JIS** encoding for Japanese filenames — which is crucial since this game uses filenames like `14pt袋.tga` for its fonts. Without proper encoding, fonts won't be readable by the game.

---

## File Structure

| File | Role |
|---|---|
| `exkizpak_v2.exe` | Tool for extracting `.pak` archives (ready-to-use binary) |
| `exkizpak.cpp` | C++ source code for exkizpak |
| `kcap_repack.py` | Python script for repacking an extracted folder back into a `.pak` |

---

## How to Use

The workflow consists of three stages: **preparation → extract → edit → repack**.

### Stage 1 — Prepare the Folder

Before starting, create a dedicated folder to use as a workspace. This is important so the contents of the `.pak` don't get mixed up with the tool's own files, which could accidentally get repacked along with them.

```
workspace/
└── exkizpak_v2.exe   ← place it here first
```

Put `exkizpak_v2.exe` into that folder, then place the `.pak` file you want to extract into it as well.

### Stage 2 — Extract the PAK File

Run `exkizpak_v2.exe` via the command line, passing the `.pak` filename as an argument:

```bash
exkizpak_v2.exe script.pak
```

The entire contents of the archive will be automatically extracted into a new subfolder. Once the process is complete, **move out** the original `.pak` file and `exkizpak_v2.exe` from that folder. If left in place, both will end up getting repacked along with the asset files when the repacking process is run.

The correct structure before you start editing:

```
workspace/
└── script/           ← extracted folder, this is all that should remain
    ├── 001.bin
    ├── 001.txt
    └── ...
```

### Stage 3 — Edit the Files

Open and edit the extracted files as needed, whether that's dialogue scripts, images, or other files.

> **Important:** Do not rename any files, especially files whose names contain Japanese characters. A renamed file will cause the game to fail to find it and may potentially crash.

### Stage 4 — Repack via CLI

Once editing is done, run the repacker via the command line:

```bash
python kcap_repack.py <extracted_folder> <output_name.pak>
```

Example:

```bash
python kcap_repack.py script/ en.pak
```

The repacking process will produce a new `.pak` file ready to use.

---

## Technical Notes

The KCAP format limits filename length to **24 bytes in Shift-JIS encoding**. Filenames that are too long will be automatically truncated by the repacker. Additionally, the resulting archive uses no compression at all — this matches the original game's format.

---

## Requirements

This tool requires **Python 3.6 or newer**. No external dependencies need to be installed. For extraction, simply use the `exkizpak_v2.exe` already included in this repo — no need to build from source.

---

## Disclaimer

This tool is created solely for educational, research, and personal modding purposes. Users are fully responsible for ensuring their use complies with copyright rules and the Terms of Service of the original game.

---

## Credits

The extraction process is based on **exkizpak** by asmodean. This repacker was built on top of it with added Shift-JIS support and improved error handling.
