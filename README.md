# D-Link DWR-960 Firmware Unpacker

A Python script to decrypt, analyze, and unpack firmware for the D-Link DWR-960 (Revision B) and D-Link DWR-933 (Revision B) router. This tool automates the process of handling the XOR-encrypted firmware files, extracting the embedded ZIP archives, and unzipping the final contents.

## warning "Disclaimer"
This content is shared exclusively for **educational and research purposes**, including the analysis of systems through reverse engineering to better understand their behavior and improve technical knowledge.

**Legal Framework:**

- In accordance with **Article 5 of the EU Directive on the legal protection of computer programs (2009/24/EC)**, reverse engineering is permitted when it is necessary to achieve interoperability and does not conflict with the normal use of the software.

- Under **17 U.S. Code § 101 (United States Copyright Law)** and the principles of "fair use", reverse engineering may be considered lawful for purposes such as analysis and education, provided that no copyright or contractual restrictions are violated.

⚖️ **Important:**

We do **not condone any violation of laws, terms of service, or intellectual property rights**. The information provided should only be used in legal environments (e.g., your own devices or systems you are authorized to analyze).

**Use this material responsibly and at your own risk.**

## Prerequisites

Before running the script, you must have the following command-line tools installed and accessible in your system's PATH:

- **Binwalk**: A tool for analyzing and extracting firmware images.
- **7-Zip (7za)**: A file archiver with a high compression ratio. The script specifically calls the `7za` command.

### Installation on Debian/Ubuntu

```bash
sudo apt-get update
sudo apt-get install binwalk p7zip-full -y
```

### Installation on macOS (using Homebrew)

```bash
brew install binwalk p7zip
```

## Usage

Clone or download the `DWR-960-fw-unpacker.py` script to your local machine.

### Basic Usage

The simplest way to run the script is by providing the path to the encrypted firmware file. The script will handle everything else automatically.

```bash
python3 DWR-960-fw-unpacker.py /path/to/your/firmware.dfw
```

In this mode, the script will:
1.  Create a decrypted file named `firmware_DECRYPTED.dfw` in the same directory.
2.  Create a working directory named `WORKDIR_firmware` in the same directory.
3.  Store the extracted ZIP archives in `WORKDIR_firmware/ZIPS/`.
4.  Store the final unzipped content in `WORKDIR_firmware/UNZIPPED/`.

### Advanced Usage

You can specify custom paths for the decrypted file and the output directories.

```bash
python3 firmware_decryptor.py <encrypted_file> [options]
```

**Options:**

- `-o, --output <path>`: Specify the path for the decrypted firmware file.
- `--zip-dir <path>`: Specify the directory to store the extracted ZIP archives.
- `--unzip-dir <path>`: Specify the directory to store the final unzipped contents.

**Example:**

```bash
python3 firmware_decryptor.py C_1.0.1.4.dfw \
    --output decrypted_firmware.bin \
    --zip-dir ./extracted_zips \
    --unzip-dir ./final_content
```

### Displaying Help

To see all available options, use the `-h` or `--help` flag:

```bash
python3 firmware_decryptor.py -h
```

## How It Works

The script follows a sequential process to unpack the firmware:

1.  **Decrypt Firmware**: The input `.dfw` file is read, and each byte is XORed with a static key (`0x92`) to produce a decrypted binary file.
2.  **Check Magic Numbers**: The script reads the header of the decrypted file to verify it contains the expected magic numbers (`0x12344321` and `0x89abcdef`). If the check fails, the script aborts.
3.  **Run Binwalk**: `binwalk` is executed on the decrypted file to scan for embedded file signatures. The script specifically looks for ZIP archive entries.
4.  **Extract ZIP Archives**: The output from `binwalk` is parsed to identify the start and end offsets of each ZIP archive. The script then carves out these archives from the decrypted binary and saves them as `.zip` files.
5.  **Unzip Archives**: The script uses `7za` to extract the contents of each `.zip` file using the known hardcoded password (`broadmobi123`).
6.  **Summarize**: Finally, a summary of the output file locations is printed to the console.

## License

This project is licensed under the MIT License.

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

