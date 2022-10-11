# stat.csv

`stat` is provided binary from Linux system.  
This binary will be display file or file system status and and it's really helpful for linux filesystem forensic.

But only problem is we can't see that as structed data.

in this situlation `stat.csv` should be help you.

---

## Prerequisites

`stat.csv` requires result file of Linux stat command. Run the following command to make result.

```bash
find / -exec stat '{}' \; > stat.meta
```

## Usage

```bash
python stat.py -h
```

This will display help for the tool. Here are all the options it supports.

```bash
usage: ['-h'] [-h] [-f STAT_FILE] [-o OUTPUT_FILENAME]

optional arguments:
  -h, --help          show this help message and exit
  -f STAT_FILE        result file of Linux stat command
  -o OUTPUT_FILENAME  file to write output
  ```

## Simple Examples

Excute with a Python

```powershell
python stat.py -f "C:\Temp\stat.meta" -o stat.csv
```

Excute with a EXE binary

```powershell
stat_x64.exe -f "C:\Temp\stat.meta" -o stat.csv
```

## For 4n6

View CSV and Excel files, filter, group, sort, etc. with ease

Can be download **Timeline Explorer** from [Eric Zimmerman's tools](https://ericzimmerman.github.io/#!index.md)

---

## Notes

- Support the timestamp with nanosecond