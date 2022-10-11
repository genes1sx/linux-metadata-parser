import argparse
import csv
import datetime
import pandas

# constants
FILE = []
FILE_PATH = []
FILE_NAME = []
SIZE = []
INODE = []
ACESS = []
UID = []
GID = []
ATIME = []
MTIME = []
CTIME = []
BTIME = []


def getTimeStamp(timeList):
    if len(timeList) == 3:
        UTC_INFO = timeList[2]
    
    linuxTime = ' '.join(timeList[0:2])
    return datetime.datetime.strptime(linuxTime[:-10], "%Y-%m-%d %H:%M:%S")

def splitFileInfo(fullpath):
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest='stat_file')
    parser.add_argument('-o', dest='output_filename')
    args = parser.parse_args()
    
    if args.stat_file is None:
        print(f"stat 명령어 결과 파일에 대한 경로를 입력하세요!")
        exit(0)
    else:
        STAT_FILE = args.stat_file
        
        if args.output_filename is None:
            OUTPUT_FILE = "stat.csv"
        else:
            OUTPUT_FILE = args.output_filename
    
    f = open(STAT_FILE, 'r', encoding='utf-8')
    lines = [line.rstrip() for line in f.readlines()]
    
    if 'Birth' in lines[7]: # Birth 정보가 있는 파일
        JMP_IDX = 8 # Birth: 가 존재하면 step 8
    else: # Birth 정보가 없는 파일
        JMP_IDX = 7 # Birth: 가 존재하지 않으면 step  7
        
    for i in range(0, len(lines), JMP_IDX):
        file_fullpath = lines[i].split()[1][1:-1]
        file_name = file_fullpath.split('/')[-1]
        if file_name == "":
            file_name = "."
        # print(file_name)
        file_path = file_fullpath.split('/')[0:-1]
        file_path_joined = "/".join(file_path)
        # print(file_path_joined)
        if file_path_joined == "":
            file_path_joined = "/"
        
        # print("/".join(file_path))
        FILE.append(file_fullpath)
        FILE_PATH.append(file_path_joined) # FILE
        FILE_NAME.append(file_name)
        SIZE.append(lines[i+1].split()[1]) # SIZE
        INODE.append(lines[i+2].split()[3]) # INODE
        ACESS.append(lines[i+3].split()[1][1:-1]) # ACESS
        UID.append(lines[i+3].split()[5][:-1]) # UID
        GID.append(lines[i+3].split('/')[3][:-1]) # GID
        ATIME.append(getTimeStamp(lines[i+4].split()[1:]).strftime("%Y-%m-%d %H:%M:%S")) # ATIME
        MTIME.append(getTimeStamp(lines[i+5].split()[1:]).strftime("%Y-%m-%d %H:%M:%S")) # MTIME
        CTIME.append(getTimeStamp(lines[i+6].split()[1:]).strftime("%Y-%m-%d %H:%M:%S")) # CTIME
        if JMP_IDX != 7:
            BTIME.append(getTimeStamp(lines[i+7].split()[1:]).strftime("%Y-%m-%d %H:%M:%S")) # BTIME

    df = pandas.DataFrame(FILE, columns=['File Full Path'])
    df['File Path'] = FILE_PATH
    df['File Name'] = FILE_NAME
    df['Size'] = SIZE
    df['Inode'] = INODE
    df['Acess Control'] = ACESS
    df['Uid'] = UID
    df['Gid'] = GID
    df['Acess Time'] = ATIME
    df['Modify Time'] = MTIME
    df['Change Time'] = CTIME
    if JMP_IDX != 7:
        df['Birth Time'] = BTIME
    
    df.to_csv(OUTPUT_FILE, index=False)


if __name__ == "__main__":
    main()
