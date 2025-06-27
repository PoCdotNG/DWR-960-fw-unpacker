# Analyzing and decrypting D-Link DWR-960 & DWR-933 firmware

# Warning 
This content is shared exclusively for **educational and research purposes**, including the analysis of systems through reverse engineering to better understand their behavior and improve technical knowledge.

**Legal Framework:**

- In accordance with **Article 5 of the EU Directive on the legal protection of computer programs (2009/24/EC)**, reverse engineering is permitted when it is necessary to achieve interoperability and does not conflict with the normal use of the software.

- Under **17 U.S. Code § 101 (United States Copyright Law)** and the principles of "fair use", reverse engineering may be considered lawful for purposes such as analysis and education, provided that no copyright or contractual restrictions are violated.

⚖️ **Important:**

We do **not condone any violation of laws, terms of service, or intellectual property rights**. The information provided should only be used in legal environments (e.g., your own devices or systems you are authorized to analyze).

**Use this material responsibly and at your own risk.**

# The Reverse story and notes....

On the D-Link support site, two firmware versions were available for the DWR-960 router:

- Version 1.010EU: `https://media.dlink.eu/support/products/dwr/dwr-960/driver_software/dwr-960_fw_revb1_01-01-eu_eu_multi_20211209.zip`
- Version 1.014EU: `https://media.dlink.eu/products/DWR-960W/DWR-960W_A34_A47_V1.0.1.4_240301.zip`

These two firmwares appear to be "encrypted"; the `binwalk` command doesn't yield any relevant information.

No other firmware is available for this model. However, another 4G router from the same brand seems to have a similar firmware.... the D-Link DWR-933: 

Links : `https://www.dlink.com/fr/fr/products/dwr-933-4g-lte-cat-6-wifi-hotspot`

This model has many more firmware versions available. A italian UNOFFICIAL D-Link forum provides a fairly complete download list on this post : `https://www.dlink-forum.it/index.php?topic=4235.0`

Thanks to member Pondera and other members for this compilation work :)


So:

| Version | Release Date | Comments |
|---|---|---|
| 1.15 EU | 2024-11-24 | External Backup |
| 1.13 EU | 2023-05-18 | Release notes included |
| 1.12 EU | 2023-04-26 | Cumulative release notes & installation instructions included |
| 1.11 EU | 2021-05-10 | Release notes included (V1.0.1.9) |
| 1.08 EU | 2020-11-02 | Release notes included (V1.0.1.4), intermediate version 1.06 EU (V1.0.1.2) with installation instructions |
| 1.05 EU | 2020-07-03 | Release notes included |
| 1.04 EU | 2020-06-29 | Release notes included |
| 1.03 EU | 2020-03-06 | Release notes included (V1.0.0.8) |
| 1.02 EU | 2019-10-11 | Release notes included (V1.0.0.5), update tool available ONLY for Windows PC |

Another interesting URL:
`https://ftp.dlink.net.pl/TELCO/Firmware/Plus/DWR-933_CP/`

We will focus on the following firmwares:
1.  **1.02 EU** -> Windows application
2.  **1.08 EU** -> Contains 2 firmware versions and a note mentioning **binwalk**! Probably a change in the firmware structure for hide sensitive information of old firmware...

### v1.02

Version 1.02EU is a Windows utility for updating the firmware:
```
ls -lh | awk '{print "Filename: " $9 , "(size: " $5" )"}'
Filename: Anleitung (size: 285K )
Filename: changes.txt (size: 121 )
Filename: DLKE0_R800E_00_A34_A00_V1.0.0.5_191011_Release(01.02.EU).exe (size: 107M )
```

`DLKE0_R800E_00_A34_A00_V1.0.0.5_191011_Release(01.02.EU).exe` is a self-extracting RAR archive:

```bash
strings DLKE0_R800E_00_A34_A00_V1.0.0.5_191011_Release\(01.02.EU\).exe | grep sfx
```

```
d:\Projects\WinRAR\SFX\build\sfxrar32\Release\sfxrar.pdb
sfx.
...[truncate]...
sfx5
[sfx
```

Good extract it!:

```bash
unrar x DLKE0_R800E_00_A34_A00_V1.0.0.5_191011_Release\(01.02.EU\).exe

Extracting  img/restore.bat                                           OK
Creating    img/restore_data                                          OK
Extracting  img/restore_data/restore.ini                              OK
All OK
[....]
Extracting  img/restore.bat                                           OK
Creating    img/restore_data                                          OK
Extracting  img/restore_data/restore.ini                              OK
All OK
```

Perfect, let's now see what's inside:

```
tree -h -L 2
[  290]  .
├── [  303]  1key.bat
├── [ 491K]  adb.exe
├── [  94K]  AdbWinApi.dll
├── [  60K]  AdbWinUsbApi.dll
├── [ 9.8K]  back.ini
├── [  125]  CDSwitch.ini
├── [ 372K]  dl.exe
├── [ 1.6K]  DownLoad.bat
├── [  276]  Driver
│   ├── [   12]  ADB
│   ├── [  268]  Common
│   ├── [  21K]  dev_inst64.exe
│   ├── [ 211K]  DevInstall.dll
│   ├── [  21K]  dev_remove64.exe
│   ├── [  21K]  dev_remove.exe
│   ├── [  536]  DriverSetting.ini
│   ├── [ 159K]  InstallDriver.exe
│   ├── [ 159K]  UninstallDriver.exe
│   ├── [  170]  Vista
│   ├── [  174]  Win7
│   ├── [  174]  Win8
│   └── [  170]  WinXP
├── [ 159K]  fastboot.exe
├── [ 1.1K]  image
│   ├── [ 478K]  appsboot.mbn
│   ├── [   30]  boot_release_notes
│   ├── [ 3.4M]  cdrom.img
│   ├── [ 3.3M]  cdrom.iso
│   ├── [ 1.3M]  efs2.mbn
│   ├── [  99K]  ENPRG9x45.mbn
│   ├── [ 8.5K]  mcfg_band_hw.mbn
│   ├── [ 8.5K]  mcfg_band.mbn
│   ├── [ 8.1K]  mcfg_cust.mbn
│   ├── [ 781K]  MCFG_SW_Items_List_Macro-9x40.xlsm
│   ├── [ 1.9M]  mdm9640-2k-perf-bmbak.ubi
│   ├── [ 7.9M]  mdm9640-2k-perf-bmfs.ubi
│   ├── [ 1.9M]  mdm9640-2k-perf-bmlog.ubi
│   ├── [ 6.5M]  mdm9640-2k-perf-boot.img
│   ├── [ 4.4M]  mdm9640-2k-perf-cdrom.ubi
│   ├── [  46M]  mdm9640-2k-perf-sysfs.ubi
│   ├── [ 7.2M]  mdm-perf-recovery-image-mdm9640-2k-perf.ubi
│   ├── [  43M]  NON-HLOS.ubi
│   ├── [  99K]  NPRG9x45.mbn
│   ├── [ 8.0K]  partition_complete_p2K_b128K.mbn
│   ├── [  492]  partition.mbn
│   ├── [  740]  patch_p2K_b128K.xml
│   ├── [ 131K]  prog_nand_firehose_9x45.mbn
│   ├── [ 3.1K]  rawprogram_nand_p2K_b128K.xml
│   ├── [ 158K]  rpm.mbn
│   ├── [ 221K]  sbl1.mbn
│   ├── [ 425K]  tz.mbn
│   ├── [ 131K]  validated_nand_firehose_9x45.mbn
│   └── [ 1.0K]  VariantImgInfo_9645.LEgen.prodQ.json
├── [ 1.6K]  QuickDownLoad.bat
├── [  151]  restore.bat
└── [   22]  restore_data
    └── [ 197K]  restore.ini
```

Let's focus on the interesting **image** directory:

```
file ./image/*
appsboot.mbn:                                ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), statically linked, not stripped
boot_release_notes:                          Unicode text, UTF-8 text
cdrom.img:                                   YAFFS filesystem root entry (little endian), type root or directory, v1 root directory
cdrom.iso:                                   ISO 9660 CD-ROM filesystem data 'D-LINK RNDIS'
efs2.mbn:                                    data
ENPRG9x45.mbn:                               ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), statically linked, no section header
mcfg_band_hw.mbn:                            ELF 32-bit LSB executable, no machine, version 1 (SYSV), staticall1.08y linked, no section header
mcfg_band.mbn:                               ELF 32-bit LSB executable, no machine, version 1 (SYSV), statically linked, no section header
mcfg_cust.mbn:                               ELF 32-bit LSB executable, no machine, version 1 (SYSV), statically linked, no section header
MCFG_SW_Items_List_Macro-9x40.xlsm:          Microsoft Excel 2007+
mdm9640-2k-perf-bmbak.ubi:                   UBI image, version 1
mdm9640-2k-perf-bmfs.ubi:                    UBI image, version 1
mdm9640-2k-perf-bmlog.ubi:                   UBI image, version 1
mdm9640-2k-perf-boot.img:                    Android bootimg, kernel, page size: 2048, cmdline (noinitrd rw console=ttyHSL0,115200,n8 androidboot.hardware=qcom ehci-hcd.park=3 msm_rtb.filter=0x37)
mdm9640-2k-perf-cdrom.ubi:                   UBI image, version 1
mdm9640-2k-perf-sysfs.ubi:                   UBI image, version 1
mdm-perf-recovery-image-mdm9640-2k-perf.ubi: UBI image, version 1
NON-HLOS.ubi:                                UBI image, version 1
NPRG9x45.mbn:                                ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), statically linked, no section header
partition_complete_p2K_b128K.mbn:            data
partition.mbn:                               OpenPGP Public Key
patch_p2K_b128K.xml:                         XML 1.0 document, ASCII text
prog_nand_firehose_9x45.mbn:                 ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), statically linked, no section header
rawprogram_nand_p2K_b128K.xml:               XML 1.0 document, ASCII text, with CRLF line terminators
rpm.mbn:                                     ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), statically linked, no section header
sbl1.mbn:                                    data
tz.mbn:                                      ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), statically linked, no section header
validated_nand_firehose_9x45.mbn:            ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), statically linked, no section header
VariantImgInfo_9645.LEgen.prodQ.json:        JSON text data
```

| File Name                                     | Type                     | Description                                                                                     |
|-----------------------------------------------|--------------------------|-------------------------------------------------------------------------------------------------|
| `appsboot.mbn`                                | ELF Executable           | ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), statically linked, not stripped         |
| `ENPRG9x45.mbn`                               | ELF Executable           | ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), statically linked, no section header    |
| `mcfg_band_hw.mbn`                            | ELF Executable           | ELF 32-bit LSB executable, no machine, version 1 (SYSV), statically linked, no section header   |
| `mcfg_band.mbn`                               | ELF Executable           | ELF 32-bit LSB executable, no machine, version 1 (SYSV), statically linked, no section header   |
| `mcfg_cust.mbn`                               | ELF Executable           | ELF 32-bit LSB executable, no machine, version 1 (SYSV), statically linked, no section header   |
| `NPRG9x45.mbn`                                | ELF Executable           | ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), statically linked, no section header    |
| `prog_nand_firehose_9x45.mbn`                 | ELF Executable           | ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), statically linked, no section header    |
| `rpm.mbn`                                     | ELF Executable           | ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), statically linked, no section header    |
| `tz.mbn`                                      | ELF Executable           | ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), statically linked, no section header    |
| `validated_nand_firehose_9x45.mbn`            | ELF Executable           | ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), statically linked, no section header    |
| `boot_release_notes`                          | Text File                | Unicode text, UTF-8 text                                                                        |
| `patch_p2K_b128K.xml`                         | XML File                 | XML 1.0 document, ASCII text                                                                    |
| `rawprogram_nand_p2K_b128K.xml`               | XML File                 | XML 1.0 document, ASCII text, with CRLF line terminators                                        |
| `VariantImgInfo_9645.LEgen.prodQ.json`        | JSON File                | JSON text data                                                                                  |
| `cdrom.img`                                   | YAFFS Filesystem          | YAFFS filesystem root entry (little endian), type root or directory, v1 root directory          |
| `cdrom.iso`                                   | ISO Filesystem            | ISO 9660 CD-ROM filesystem data 'D-LINK RNDIS'                                                  |
| `mdm9640-2k-perf-bmbak.ubi`                   | UBI Image                 | UBI image, version 1                                                                            |
| `mdm9640-2k-perf-bmfs.ubi`                    | UBI Image                 | UBI image, version 1                                                                            |
| `mdm9640-2k-perf-bmlog.ubi`                   | UBI Image                 | UBI image, version 1                                                                            |
| `mdm9640-2k-perf-cdrom.ubi`                   | UBI Image                 | UBI image, version 1                                                                            |
| `mdm9640-2k-perf-sysfs.ubi`                   | UBI Image                 | UBI image, version 1                                                                            |
| `mdm-perf-recovery-image-mdm9640-2k-perf.ubi` | UBI Image                 | UBI image, version 1                                                                            |
| `NON-HLOS.ubi`                                | UBI Image                 | UBI image, version 1                                                                            |
| `mdm9640-2k-perf-boot.img`                    | Android Boot Image        | Android bootimg, kernel, page size: 2048, cmdline (noinitrd rw console=ttyHSL0,115200,n8 androidboot.hardware=qcom ehci-hcd.park=3 msm_rtb.filter=0x37) |
| `MCFG_SW_Items_List_Macro-9x40.xlsm`          | Microsoft Excel File      | Microsoft Excel 2007+                                                                           |
| `efs2.mbn`                                    | Binary Data               | Data                                                                                            |
| `partition_complete_p2K_b128K.mbn`            | Binary Data               | Data                                                                                            |
| `sbl1.mbn`                                    | Binary Data               | Data                                                                                            |
| `partition.mbn`                               | OpenPGP Public Key        | OpenPGP Public Key                                                                              |


Look! UBI image, that's very cool...

Let's explore these UDI files more closely with `ubi_reader` tool (https://github.com/onekey-sec/ubi_reader)

>Note : `pip install --user ubi_reader` 

```bash
mkdir ~/tmp/ubi_extracted/
for file in *.ubi; do
    ubireader_extract_files "$file" -o ~/tmp/ubi_extracted/
done
cd ~/tmp/ubi_extracted/
```

Alright, let's move on  **~/tmp/ubi_extracted/**:

```
tree -h -L 2
[  132]  .
├── [   10]  1278842913
│   └── [   10]  modem
├── [   12]  1660224684
│   └── [  190]  rootfs
├── [   10]  2085995982
│   └── [    0]  bmlog
├── [   12]  237418527
│   └── [   22]  backup
├── [    8]  573190784
│   └── [   36]  bmfs
├── [   36]  803335646
│   ├── [    0]  cachefs
│   ├── [  228]  rootfs
│   └── [  108]  usrfs
└── [   10]  981075104
    └── [   18]  cdrom
```

Perfect, we have extracted the firmware files. Let's move on to analyzing the update process...

### Quick Upgrade Firmware Analysis

First of all, let's have a look at what could be related to the embedded http web server, starting by looking for configurations (Upgrade process is possible with WEBUI)


```
find . -type d -iname "etc"
./573190784/bmfs/etc
./803335646/rootfs/etc
./1660224684/rootfs/etc
```
Notes:
- 3 directories have `etc` files
- a "bmfs" directory and 2 "rootfs" directories

In the `./573190784/bmfs/etc` directory, we observe a web server configuration file `lighttpd.conf`.

#### lighttpd?

Let's take a look at this configuration file : 

`grep -v '^#' ./573190784/bmfs/etc/lighttpd.conf | grep -v '^\s*$'`

```
[TRUNCATED]
fastcgi.server = (
  "/webpost.cgi" =>
  (( "socket" => "/tmp/fcgi.sock",
	 "check-local"=>"disable",
	 "bin-path"=>"/bmfs/usr/bin/qcmap_fcgi",
	 "max-procs" => 1,
  )),
  "/login.cgi" =>
  (( "socket" => "/tmp/fcgi.sock",
	 "check-local"=>"disable",
	 "bin-path"=>"/bmfs/usr/bin/qcmap_fcgi",
	 "max-procs" => 1,
[TRUNCATED]
  "/debug_at_info.cgi" =>
  (( "socket" => "/tmp/debug_fcgi.sock",
	 "check-local"=>"disable",
	 "bin-path"=>"/bmfs/usr/bin/debug_fcgi",
	 "max-procs" => 1,
  ))
)
[TRUNCATED]
```

We observe two binaries mainly used for the web server's CGI calls:

| bin-path | Pages URL |
|---|---|
| `/bmfs/usr/bin/qcmap_fcgi` | `/webpost.cgi`, `/login.cgi`, `/data.ria`, `/cfg/all`, `/webupload.cgi` |
| `/bmfs/usr/bin/debug_fcgi` | `/debug_basic_info.cgi`, `/debug_device_info.cgi`, `/debug_post_set.cgi`, `/debug_wireless_info.cgi`, `/debug_login.cgi`, `/debug_at_info.cgi` |

Note: Our dwr-960 router has the same calls! We also see that the binaries are called from the bmfs partition.

Let's put these binaries aside...

```bash
mkdir cgibin_1-02/
cp ./573190784/bmfs/usr/bin/qcmap_fcgi cgibin_1-02/
cp ./573190784/bmfs/usr/bin/debug_fcgi cgibin_1-02/
cd cgibin_1-02/
md5sum *
ebe9a657140e04598727cf999095ae55  debug_fcgi
da216f9b656a3824ba1b563fde6c8db1  qcmap_fcgi
```

## v1.08

The zip for this firmware contains 2 firmwares and a release note:
```
ZIP
[  360]  .
├── [  79M]  DLKE0_R800E_00_A34_A00_V1.0.1.2_200825_Release(01.06.EU)_middle.dfw
├── [  79M]  DLKE0_R800E_00_A34_A00_V1.0.1.4_201102_Release(01.08.EU)_ENCRYPTED.dfw
└── [  69K]  DWR-933 B1_01.08.EU_D-lab release note.doc
```

The doc file, marked as "confidential," is a release note indicating a fix:
"Fix BINWALK issue"

This information is interesting....

Let's look at the two firmwares with binwalk:

```
binwalk *.dfw

Scan Time:     2025-06-27 15:21:50
Target File:   /home/ngo/tmp/cpe/dlink/920/new_test/autre dlink/933/dwr-933_fw_revb1_01-08_eu_multi_20201216/DLKE0_R800E_00_A34_A00_V1.0.1.2_200825_Release(01.06.EU)_middle.dfw
MD5 Checksum:  ae8c2e3a1a86fe16857d30ef0a473305
Signatures:    411

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
600           0x258           Zip archive data, encrypted at least v2.0 to extract, compressed size: 145063, uncompressed size: 1368064, name: efs2.mbn
145807        0x2398F         End of Zip archive, footer length: 22
145829        0x239A5         Zip archive data, encrypted at least v2.0 to extract, compressed size: 5965257, uncompressed size: 6799360, name: mdm9640-2k-perf-boot.img
6111262       0x5D401E        End of Zip archive, footer length: 22
6111284       0x5D4034        Zip archive data, encrypted at least v2.0 to extract, compressed size: 3931441, uncompressed size: 8257536, name: mdm9640-2k-perf-bmfs.ubi
10042901      0x993E15        End of Zip archive, footer length: 22
10042923      0x993E2B        Zip archive data, encrypted at least v2.0 to extract, compressed size: 36792174, uncompressed size: 44826624, name: NON-HLOS.ubi
46835249      0x2CAA631       End of Zip archive, footer length: 22
46835271      0x2CAA647       Zip archive data, encrypted at least v2.0 to extract, compressed size: 36219715, uncompressed size: 48496640, name: mdm9640-2k-perf-sysfs.ubi
83055164      0x4F3523C       End of Zip archive, footer length: 22
83055786      0x4F354AA       Zip archive data, at least v2.0 to extract, compressed size: 298, uncompressed size: 8336, name: mcfg_cust.mbn
83056127      0x4F355FF       Zip archive data, at least v2.0 to extract, compressed size: 459, uncompressed size: 8664, name: mcfg_band.mbn
83056629      0x4F357F5       Zip archive data, at least v2.0 to extract, compressed size: 458, uncompressed size: 8664, name: mcfg_band_hw.mbn
83057421      0x4F35B0D       End of Zip archive, footer length: 22


Scan Time:     2025-06-27 15:21:51
Target File:   /home/ngo/tmp/cpe/dlink/920/new_test/autre dlink/933/dwr-933_fw_revb1_01-08_eu_multi_20201216/DLKE0_R800E_00_A34_A00_V1.0.1.4_201102_Release(01.08.EU)_ENCRYPTED.dfw
MD5 Checksum:  e77e2df6b7ae342d06e67bdc79db7603
Signatures:    411

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
8765752       0x85C138        LZ4 compressed data, legacy
31168667      0x1DB989B       MySQL ISAM compressed data file Version 1
34785911      0x212CA77       COBALT boot rom data (Flat boot rom or file system)
79591401      0x4BE77E9       MySQL ISAM compressed data file Version 5
```

Binwalk detects "valid" ZIP archives embedded in the **01.06.EU** version of the firmware file, but this data is encrypted! In the second firmware, **01.08.EU**, only false positives are detected; the data is encrypted.

Let's focus on the first firmware:

Two methods are possible: 
- the first is to reverse engineer the firmware update functions....
- the second is to try a brute force attack :)

1.  Let's quickly extract the zips from the BMFS file:

```
6111284 0x5D4034 Zip archive data, encrypted at least v2.0 to extract, compressed size: 3931441, uncompressed size: 8257536, name: mdm9640-2k-perf-bmfs.ubi
10042901 0x993E15 End of Zip archive, footer length: 22
```

Extracting the BMFS UBIFS zip file : 

```
dd if='DLKE0_R800E_00_A34_A00_V1.0.1.2_200825_Release(01.06.EU)_middle.dfw' of="bmfs-ubi.zip" bs=1 skip=$((0x5D4034)) count=$((0x993E2B - 0x5D4034))

unzip -t bmfs-ubi.zip
Archive:  bmfs-ubi.zip
[bmfs-ubi.zip] mdm9640-2k-perf-bmfs.ubi password:
```

Oh no! Password realy?
What is this password?

Two methods:

- Smart brute force :)
- Reverse engineering the firmware with Ghidra or other Reverse tools....

Let's try the first method.

Let's go back to `qcmap_fcgi` file.

## qcmap_fcgi: quick reverse without decompilation

We know that the firmware contains encrypted zip files... let's see if there are any signs of the unzip command in this binary....

```
file qcmap_fcgi
qcmap_fcgi: ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.3, for GNU/Linux 2.6.16, BuildID[sha1]=1b00bde4d7e77b4ccde8a39806d239f860bd2c96, stripped
```

We know it unzips (the `funzip` command is also available in the binaries directory of firmware)...

Let's look at the strings:


```bash
strings qcmap_fcgi | grep "zip"
```

```
rm -f /cache/[^u]*.zip /cache/*.bin /cache/lighttpd*
fcgi_api_do_zip_fw_save
fcgi_api_do_zip_fw_upgrade
fcgi_api_upload_zip_fw
%s() zip packet version ="%s"
/cache/%s.zip
/cache/upgrade.zip
%s() FCGX_GetStr() END: i=[%d], zip_imgsize=[%d], read_len=[%d]
%s() %d ERROR: i=[%d], zip_imgsize=[%d], read total_len=[%d]
%s() ERROR: i=[%d], zip_imgsize=[%d], write_len=[%d]
%s() %d upgrade: i=[%d] [%s], zip_imgsize=[%d],imgsize=[%d]
unzip %s/%s.zip -q -d /etc/backup/ -o
/bmfs/usr/bin/funzip -%s %s > %s 2>/tmp/unzip_result
%s : path=[%s] funzip return [%d]
/tmp/unzip_result
%s %d :%s funzip result err[%s]
rm -rf %s /tmp/unzip_result
Unzip Error
Unzip size Error
rm -f /cache/update.zip
Content-Type: application/x-gzip-compressed
cd /tmp && base64 -d cfg.sav > cfg.zip && tar -zxvf cfg.zip -C /etc/backup/conf
cd /tmp/backup/ && tar -czvf cfg.zip  * && base64 cfg.zip >/$BM/WEBSERVER/webpages/cfg.sav
```

Interesting:
```
/bmfs/usr/bin/funzip -%s %s > %s 2>/tmp/unzip_result
```

Here we have the `funzip` command to decompress the firmware. Check man of funzip : the `-%s` is the zip "password"...

Maybe the password is somewhere in the file as plain text data?

Let's create a text file with strings... for the length, let's first take all strings from 6 to 20 characters :

```
strings qcmap_fcgi | awk 'length($0) >= 6 && length($0) <= 20 && $0 !~ /[\s%]/' | sort -u > possible.password
```

This file is only 755 lines long, so 755 passwords to check! 

Now that we have our wordlist run `7zip` command to test zip file ... :

```bash
while IFS= read -r line; do
  output=$(7za t ./bmfs-ubi.zip -p"$line" 2>&1)
  # exit code 0 = found! :)
  if [ $? -eq 0 ]; then
	 echo ""
	 echo "Password found!  : $line"
	 echo "7z log : "
	 echo "$output"
	 break
  else
	 printf "."
  fi
done < ~/tmp/ubi_extracted/cgibin_1-02/possible.password
```

Ok script is writen, let's run Brute Forcing!!! :)

```
bash simplezipbruteforce.bash
.................................................................................................................................................................
Password found!  : broadmobi123
7z log :

7-Zip (a) [64] 16.02 : Copyright (c) 1999-2016 Igor Pavlov : 2016-05-21
p7zip Version 16.02 ([...])

Scanning the drive for archives:
1 file, 3931639 bytes (3840 KiB)

Testing archive: ./bmfs-ubi.zip
--
Path = ./bmfs-ubi.zip
Type = zip
Physical Size = 3931639

Everything is Ok

Size:       8257536
Compressed: 3931639
```

Now we have our password to decrypt our ZIP files! 

- We will extract all ZIP archive with this password : **broadmobi123**
- Retrieve the new `qcmap_fcgi` binary and analyze it with Ghidra

# qcmap_fcgi from 1.06EU 

Ok starting Ghidra and analysing the pseudo-C code for firmware upgrade!


We can see that a check is made on the file header after the firmware file has been downloaded...

```
memcpy(&DAT_0012b53c,local_2e0,600);
iVar12 = DAT_0012b540;
if (((DAT_0012b53c == 0x12344321) && (DAT_0012b540 == -0x76543211)) &&
   (iVar12 = -0x76543211, DAT_0012b544 == 1)) {
  bVar1 = false;
else {
    iVar2 = DAT_0012b544;
    syslog(0x1e240,
           "%s() Magic check failed magic1=[0x%x],magic2=[0x%x] version=[0x%x] try encryption pr ocess"
           ,"fcgi_api_do_zip_fw_save",DAT_0012b53c,iVar12,DAT_0012b544);
    FUN_0001c84c(local_2e0,pcVar13);
    memcpy(&DAT_0012b53c,local_2e0,600);
    if (((DAT_0012b53c == 0x12344321) && (DAT_0012b540 == -0x76543211)) && (DAT_0012b544 == 1))
```

So if magic1 and 2 are ok, we do the classic process, otherwise we try to decrypt the firmware with
 `FUN_0001c84c(local_2e0,pcVar13);`

```c
void FUN_0001c84c(int param_1,int param_2)

{
  undefined1 uVar1;
  int iVar2;
  int iVar3;

  if (param_2 == 0) {
    return;
  }
  iVar3 = 0;
  do {
    uVar1 = FUN_0001c840(*(undefined1 *)(param_1 + iVar3),0x92);
    iVar2 = iVar3 + 1;
    *(undefined1 *)(param_1 + iVar3) = uVar1;
    iVar3 = iVar2;
  } while (iVar2 != param_2);
  return;
}

byte FUN_0001c840(byte param_1,byte param_2)

{
  return param_2 ^ param_1;
}
```

Oh my goodness! it's a simple XOR.... and the key is: `0x92`!

Ok let's make a quick python script to decrypt our firmware with XOR and then test the MAGICS :)

```python
import struct

def decrypt_firmware_xor(encrypted_path: str, decrypted_path: str):
    key = 0x92

    try:
        with open(encrypted_path, 'rb') as encrypted_file, open(decrypted_path, 'wb') as decrypted_file:
            print(f"[*] Starting decrypting {encrypted_path}!")
            encrypted_data = encrypted_file.read()
            decrypted_data = bytearray()
            for byte in encrypted_data:
                decrypted_byte = byte ^ key
                decrypted_data.append(decrypted_byte)
            decrypted_file.write(decrypted_data)

        print(f"[*] Operation done!")
        print(f"   -> Encrypted file  : '{encrypted_path}'")
        print(f"   -> Decrypted file : '{decrypted_path}'")

    except FileNotFoundError:
        print(f"[!] Error : file '{encrypted_path}' not dound")
        exit(1)
    except Exception as e:
        print(f"[!] Exeption error! : {e}")
        exit(2)

def check_magic(decrypted_path):

    with open(decrypted_path, 'rb') as f:

        print("[*] Read header")
        main_header = f.read(600)
        if len(main_header) < 600:
            print("[!] Error : File too small")
            return

        # magic in little-endian
        magic1, magic2, version = struct.unpack_from('<III', main_header, 0)
        print(f"    -> Magic1: {hex(magic1)}, Magic2: {hex(magic2)}, Version: {version}")

        if not (magic1 == 0x12344321 and magic2 == 0x89abcdef and version == 1):
            print("[!] WARNING : Magic check failed!!!!")

if __name__ == '__main__':
    print("First step: XOR DECRYPTING! :)")
    encrypted_firmware_file = 'encrypt_DLKER_R820B_18_A34_A47_V1.0.1.4.dfw'
    decrypted_firmware_file = 'DLKER_R820B_18_A34_A47_V1.0.1.4.dfw'

    decrypt_firmware_xor(encrypted_firmware_file, decrypted_firmware_file)
    check_magic(decrypted_firmware_file)
```

Perfect! I'm a gambler, I tested it directly with the DWR-960 firmware :)

Let's look with binwalk now....

```
binwalk DLKER_R820B_18_A34_A47_V1.0.1.4.dfw

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
600           0x258           Zip archive data, encrypted at least v2.0 to extract, compressed size: 164708, uncompressed size: 1605632, name: efs2.mbn
165452        0x2864C         End of Zip archive, footer length: 22
165474        0x28662         Zip archive data, encrypted at least v2.0 to extract, compressed size: 6319858, uncompressed size: 7141376, name: mdm9640-2k-perf-boot.img
6485508       0x62F604        End of Zip archive, footer length: 22
6485530       0x62F61A        Zip archive data, encrypted at least v2.0 to extract, compressed size: 4067499, uncompressed size: 6946816, name: mdm9640-2k-perf-bmfs.ubi
10553205      0xA10775        End of Zip archive, footer length: 22
10553227      0xA1078B        Zip archive data, encrypted at least v2.0 to extract, compressed size: 36829142, uncompressed size: 44826624, name: NON-HLOS.ubi
47382521      0x2D2FFF9       End of Zip archive, footer length: 22
47382543      0x2D3000F       Zip archive data, encrypted at least v2.0 to extract, compressed size: 42272801, uncompressed size: 58851328, name: mdm9640-2k-perf-sysfs.ubi
89655522      0x55808E2       End of Zip archive, footer length: 22
89656144      0x5580B50       Zip archive data, at least v2.0 to extract, compressed size: 505, uncompressed size: 8784, name: mcfg_cust.mbn
89656692      0x5580D74       Zip archive data, at least v2.0 to extract, compressed size: 471, uncompressed size: 8680, name: mcfg_band.mbn
89657206      0x5580F76       Zip archive data, at least v2.0 to extract, compressed size: 464, uncompressed size: 8664, name: mcfg_band_hw.mbn
89658004      0x5581294       End of Zip archive, footer length: 22
```

Great! Our 960 firmware uses the same technique as the 933!!! It's confirmed!

Now, is the ZIP password the same?
We extract again and test and... Yes, it's good!

We now have access to the UBI images and all the files present in the firmware!

Now we'll finally be able to play with him a bit.



Rocks!

PoC.ng
