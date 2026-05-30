#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KCAP Repacker for White Album 2 (FIXED VERSION)
Based on exkizpak by asmodean
Coded for modding purposes

CHANGELOG v1.1:
- Fixed: Shift-JIS encoding for Japanese filenames (fonts now work!)
- Added: Better error handling
- Added: File validation
"""

import os
import struct
import sys
from pathlib import Path

KCAP_VERSION = 2

class KCAPRepacker:
    def __init__(self, input_folder, output_pak):
        self.input_folder = Path(input_folder)
        self.output_pak = output_pak
        self.files = []
        
    def scan_files(self):
        """Scan all files in the input folder"""
        print(f"Scanning folder: {self.input_folder}")
        
        for file_path in sorted(self.input_folder.rglob('*')):
            if file_path.is_file():
                relative_path = file_path.relative_to(self.input_folder)
                # Convert to string and limit to 24 characters (KCAP limitation)
                filename = str(relative_path).replace('\\', '/')
                
                # Check if filename can be encoded in Shift-JIS (for Japanese games)
                try:
                    filename_bytes = filename.encode('shift-jis')
                    if len(filename_bytes) > 23:  # 24 bytes including null terminator
                        print(f"WARNING: Filename too long in Shift-JIS, truncating: {filename}")
                        # Truncate carefully to avoid breaking multi-byte characters
                        filename_bytes = filename_bytes[:23]
                        filename = filename_bytes.decode('shift-jis', errors='ignore')
                except UnicodeEncodeError:
                    print(f"WARNING: Filename cannot be encoded in Shift-JIS: {filename}")
                    print(f"         Using ASCII fallback (may cause issues in game)")
                    filename = filename.encode('ascii', errors='replace').decode('ascii')[:23]
                
                self.files.append({
                    'path': file_path,
                    'name': filename,
                    'size': file_path.stat().st_size
                })
        
        print(f"Found {len(self.files)} files")
        return len(self.files) > 0
    
    def pack(self):
        """Pack all files into KCAP archive"""
        if not self.files:
            print("ERROR: No files to pack!")
            return False
        
        # Calculate header size
        header_size = 16  # KCAP header (signature + unknown1 + unknown2 + entry_count)
        entry_size = 44   # Each entry (compressed_flag + filename[24] + unknown1 + unknown2 + offset + length)
        entries_total_size = entry_size * len(self.files)
        
        # Data starts after header and all entries
        data_offset = header_size + entries_total_size
        
        print(f"\nBuilding KCAP archive: {self.output_pak}")
        print(f"Header size: {header_size} bytes")
        print(f"Entries size: {entries_total_size} bytes ({len(self.files)} entries x {entry_size} bytes)")
        print(f"Data starts at: {data_offset} bytes")
        
        try:
            with open(self.output_pak, 'wb') as pak:
                # Write KCAP header
                pak.write(b'KCAP')                           # signature
                pak.write(struct.pack('<I', 0))              # unknown1
                pak.write(struct.pack('<I', 0))              # unknown2 (KCAP v2)
                pak.write(struct.pack('<I', len(self.files))) # entry_count
                
                # Prepare entries and calculate offsets
                current_offset = data_offset
                entries_data = []
                
                for file_info in self.files:
                    file_size = file_info['size']
                    
                    # Build entry
                    entry = bytearray(entry_size)
                    
                    # compressed_flag (0 = not compressed)
                    struct.pack_into('<I', entry, 0, 0)
                    
                    # filename (24 bytes, null-padded)
                    # Use Shift-JIS encoding for Japanese filenames (White Album 2 uses this)
                    try:
                        filename_bytes = file_info['name'].encode('shift-jis')[:24]
                    except UnicodeEncodeError:
                        # Fallback to ASCII if Shift-JIS fails
                        filename_bytes = file_info['name'].encode('ascii', errors='replace')[:24]
                    entry[4:4+len(filename_bytes)] = filename_bytes
                    
                    # unknown1, unknown2 (KCAP v2)
                    struct.pack_into('<I', entry, 28, 0)
                    struct.pack_into('<I', entry, 32, 0)
                    
                    # offset and length
                    struct.pack_into('<I', entry, 36, current_offset)
                    struct.pack_into('<I', entry, 40, file_size)
                    
                    entries_data.append(bytes(entry))
                    
                    current_offset += file_size
                
                # Write all entries
                for entry in entries_data:
                    pak.write(entry)
                
                # Write file data
                for i, file_info in enumerate(self.files):
                    print(f"Packing [{i+1}/{len(self.files)}]: {file_info['name']} ({file_info['size']} bytes)")
                    
                    try:
                        with open(file_info['path'], 'rb') as f:
                            data = f.read()
                            pak.write(data)
                    except Exception as e:
                        print(f"  ERROR reading file: {e}")
                        return False
            
            final_size = os.path.getsize(self.output_pak)
            print(f"\n{'='*60}")
            print(f"✓ SUCCESS! PAK file created with Shift-JIS encoding!")
            print(f"{'='*60}")
            print(f"Output: {self.output_pak}")
            print(f"Size: {final_size:,} bytes ({final_size/1024/1024:.2f} MB)")
            print(f"Files: {len(self.files)}")
            print(f"\nJapanese filenames (fonts) are now properly encoded!")
            return True
            
        except Exception as e:
            print(f"\n{'='*60}")
            print(f"✗ ERROR: Failed to create PAK file!")
            print(f"{'='*60}")
            print(f"Error: {e}")
            return False

def main():
    if len(sys.argv) < 3:
        print("="*60)
        print("KCAP Repacker for White Album 2 - v1.1 (FIXED)")
        print("="*60)
        print("Based on exkizpak by asmodean")
        print("Fixed: Shift-JIS encoding for Japanese filenames\n")
        print("Usage: python kcap_repack.py <input_folder> <output.pak>")
        print("\nExample:")
        print("  python kcap_repack.py extracted/ script.pak")
        print("\nFeatures:")
        print("  ✓ Shift-JIS encoding (Japanese font files work!)")
        print("  ✓ Proper KCAP v2 format")
        print("  ✓ No compression (raw data)")
        return 1
    
    input_folder = sys.argv[1]
    output_pak = sys.argv[2]
    
    if not os.path.isdir(input_folder):
        print(f"ERROR: Input folder not found: {input_folder}")
        return 1
    
    repacker = KCAPRepacker(input_folder, output_pak)
    
    if not repacker.scan_files():
        print("ERROR: No files found in input folder!")
        return 1
    
    if repacker.pack():
        return 0
    else:
        return 1

if __name__ == '__main__':
    sys.exit(main())
