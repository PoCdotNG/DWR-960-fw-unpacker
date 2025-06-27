#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
===============================================================================
Project Name: DWR-960-fw-unpacker
Script Name: DWR-960-fw-unpacker.py
Description: A proof of concept to unpack Firmware for  : 
                DWR-920 Rev B,
                DWR-932 Rev F, 
                DWR-933 Rev B,
                DWR-960 Rev B,  
             and maybe some other model producted by BroadMobi for D-Link
             
Author: PoC(dot)NG <poc@poc.ng>
License: MIT License
Created: 2025-06-21
===============================================================================
MIT License

Copyright (c) 2025 PoC(dot)ng

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import argparse
import os
import re
import shutil
import struct
import subprocess
import sys

def check_dependencies():
    """Checks if required command-line tools are installed."""
    print("[*] Checking for required tools (binwalk, 7za)...")
    if not shutil.which("binwalk"):
        print("[!] Error: 'binwalk' is not installed or not in the system's PATH.")
        sys.exit(1)
    if not shutil.which("7za"):
        print("[!] Error: '7za' is not installed or not in the system's PATH.")
        sys.exit(1)
    print("[*] All required tools are available.")

def decrypt_firmware_xor(encrypted_path: str, decrypted_path: str):
    """Decrypts the firmware file using a simple XOR cipher."""
    key = 0x92
    print(f"[*] Starting decryption of '{encrypted_path}'!")
    try:
        with open(encrypted_path, 'rb') as encrypted_file, open(decrypted_path, 'wb') as decrypted_file:
            encrypted_data = encrypted_file.read()
            decrypted_data = bytearray(byte ^ key for byte in encrypted_data)
            decrypted_file.write(decrypted_data)
        print("[*] Decryption complete!")
        print(f"   -> Encrypted file: '{encrypted_path}'")
        print(f"   -> Decrypted file: '{decrypted_path}'")
    except FileNotFoundError:
        print(f"[!] Error: File '{encrypted_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"[!] An exception occurred during decryption: {e}")
        sys.exit(2)

def check_magic(decrypted_path: str) -> bool:
    """Reads the header of the decrypted file and checks for magic numbers."""
    print("[*] Reading and verifying file header...")
    try:
        with open(decrypted_path, 'rb') as f:
            main_header = f.read(600)
            if len(main_header) < 600:
                print("[!] Error: File is too small to be a valid firmware image.")
                return False

            magic1, magic2, version = struct.unpack_from('<III', main_header, 0)
            print(f"    -> Magic1: {hex(magic1)}, Magic2: {hex(magic2)}, Version: {version}")

            if not (magic1 == 0x12344321 and magic2 == 0x89abcdef and version == 1):
                print("[!] WARNING: Magic number check failed! The file may not be a valid firmware.")
                return False

            print("[*] Magic number check passed.")
            return True
    except FileNotFoundError:
        print(f"[!] Error: Decrypted file '{decrypted_path}' not found for magic check.")
        sys.exit(1)
    except Exception as e:
        print(f"[!] An exception occurred during magic check: {e}")
        sys.exit(2)

def run_binwalk(binary_file: str) -> str:
    """Runs binwalk on the decrypted file to identify embedded file types."""
    print("[*] Running binwalk on decrypted file...")
    try:
        result = subprocess.run(
            ["binwalk", binary_file],
            capture_output=True, text=True, check=True
        )
        print("[*] Binwalk analysis complete.")
        return result.stdout
    except FileNotFoundError:
        print("[!] Error: 'binwalk' command not found!")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"[!] Error running binwalk: {e.stderr}")
        sys.exit(1)

def extract_zip_archives(binwalk_output: str, binary_file: str, output_dir: str):
    """Parses binwalk output to find and extract ZIP archives (First PK file header to next footer header) """
    print(f"[*] Extracting ZIP archives to '{os.path.abspath(output_dir)}'...")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    zip_pattern = re.compile(r"(\d+)\s+0x([0-9A-Fa-f]+)\s+Zip archive data.*name:\s+(\S+)")
    footer_pattern = re.compile(r"(\d+)\s+0x([0-9A-Fa-f]+)\s+End of Zip archive")

    zip_entries = []
    lines = binwalk_output.splitlines()

    i = 0
    while i < len(lines):
        line = lines[i]
        zip_match = zip_pattern.search(line)

        if zip_match:
            offset_dec, _, filename = zip_match.groups()
            current_zip = {
                "start": int(offset_dec),
                "filename": filename.strip(','),
                "end": None
            }
            zip_entries.append(current_zip)

            # Ignore subsequent lines until a footer for zip is found.
            while i + 1 < len(lines):
                i += 1  # Consume the next line
                next_line = lines[i]
                footer_match = footer_pattern.search(next_line)
                if footer_match:
                    end_offset_dec, _ = footer_match.groups()
                    current_zip["end"] = int(end_offset_dec)
                    break  # Found the footer, break from inner loop

            continue

        i += 1

    if not zip_entries:
        print("[*] No ZIP archives found by binwalk.")
        return

    try:
        with open(binary_file, "rb") as f:
            for entry in zip_entries:
                if entry["end"] is None:
                    print(
                        f"[!] Warning: Missing footer for archive '{entry['filename']}' starting at offset {hex(entry['start'])}. Skipping.")
                    continue

                start = entry["start"]
                length = entry["end"] - start + 22

                output_filename = os.path.join(output_dir, f'{os.path.basename(entry["filename"])}.zip')
                print(
                    f"[*] Extracting '{os.path.basename(output_filename)}' (offsets: {hex(start)}-{hex(entry['end'])})")

                f.seek(start)
                data = f.read(length)
                with open(output_filename, "wb") as out:
                    out.write(data)
    except FileNotFoundError:
        print(f"[!] Error: File '{binary_file}' not found during extraction.")
        sys.exit(1)
    except Exception as e:
        print(f"[!] An exception occurred during ZIP extraction: {e}")
        sys.exit(2)


def unzip_archives(source_dir: str, destination_dir: str):
    """Unzips all .zip files from a source directory to a destination directory using 7za."""
    print(f"[*] Unzipping archives from '{os.path.abspath(source_dir)}' to '{os.path.abspath(destination_dir)}'...")
    if not os.path.exists(source_dir):
        print(f"[!] Source directory '{source_dir}' does not exist.")
        return

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
        print(f"[*] Created destination directory '{os.path.abspath(destination_dir)}'.")

    zip_files = [f for f in os.listdir(source_dir) if f.endswith('.zip')]

    if not zip_files:
        print("[*] No .zip files found to extract in the source directory.")
        return

    for zip_file in zip_files:
        zip_file_path = os.path.join(source_dir, zip_file)
        command = [
            '7za', 'x', zip_file_path,
            f'-o{destination_dir}',
            '-pbroadmobi123',
            '-y'
        ]
        try:
            print(f"[*] Unzipping '{zip_file}'...")
            subprocess.run(command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"[!] Error unzipping '{zip_file}': {e.stderr}")


def main():
    """Main function to orchestrate the firmware unpacking process."""
    print("DWR-960 rev B Firmware Unpacker")
    print("-" * 30)

    parser = argparse.ArgumentParser(description="Decrypt and unpack DWR-960 rev B firmware files.")
    parser.add_argument("encrypted_file", help="Path to the encrypted firmware file (.dfw).")
    parser.add_argument(
        "-o", "--output",
        help="Path for the decrypted firmware file. If not specified, it's created next to the input file with a '_DECRYPTED' suffix."
    )
    parser.add_argument(
        "--zip-dir",
        help="Optional. Directory to store extracted ZIP archives."
    )
    parser.add_argument(
        "--unzip-dir",
        help="Optional. Directory to store the final unzipped contents."
    )
    args = parser.parse_args()

    # --- Directory Handling ---
    encrypted_file_path = os.path.abspath(args.encrypted_file)

    if args.zip_dir is None and args.unzip_dir is None:
        # Default behavior: create a WORKDIR next to the input file
        base_dir = os.path.dirname(encrypted_file_path)
        base_name = os.path.splitext(os.path.basename(encrypted_file_path))[0]
        work_dir = os.path.join(base_dir, f"WORKDIR_{base_name}")

        zip_dir = os.path.join(work_dir, "ZIPS")
        unzip_dir = os.path.join(work_dir, "UNZIPPED")

        print(
            f"[*] No output directories specified. Using '{os.path.abspath(work_dir)}' as the base working directory.")
        os.makedirs(work_dir, exist_ok=True)
    else:
        # User provided at least one path, use defaults for any missing ones.
        zip_dir = args.zip_dir if args.zip_dir is not None else "./ZIPS"
        unzip_dir = args.unzip_dir if args.unzip_dir is not None else "./UNZIPPED"

    # Determine the output file path for the decrypted file
    if args.output:
        decrypted_firmware_file = args.output
    else:
        base, _ = os.path.splitext(args.encrypted_file)
        decrypted_firmware_file = base + "_DECRYPTED.dfw"

    # --- Process Start ---
    check_dependencies()
    decrypt_firmware_xor(args.encrypted_file, decrypted_firmware_file)

    if not check_magic(decrypted_firmware_file):
        print("[!] Aborting due to failed magic number check.")
        sys.exit(1)

    binwalk_output = run_binwalk(decrypted_firmware_file)
    print(f'[*] Binwalk output:\n{binwalk_output}' + '-' * 20)

    extract_zip_archives(binwalk_output, decrypted_firmware_file, zip_dir)
    unzip_archives(zip_dir, unzip_dir)

    # --- Final Summary ---
    print("\n" + "=" * 30)
    print("         Operation Summary")
    print("=" * 30)
    print(f"-> Decrypted Firmware: {os.path.abspath(decrypted_firmware_file)}")
    print(f"-> Extracted ZIPs:     {os.path.abspath(zip_dir)}")
    print(f"-> Unzipped Contents:  {os.path.abspath(unzip_dir)}")
    print("=" * 30)
    print("\n[*] Process finished.")


if __name__ == '__main__':
    main()
