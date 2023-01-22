import argparse
import sys
import datetime
import re
import pandas as pd


class LinueMetaData(object):
    def __init__(self, infile):
        
        self.fileName = []
        self.size = []
        self.inode = []
        self.permission = []
        self.owner = []
        self.group = []
        self.atime = []
        self.mtime = []
        self.ctime = []
        
        with open(infile, 'r', encoding='utf-8') as infile:
            self.lines = [l.rstrip() for l in infile.readlines()]
            self.utc = self.lines[4].split()[-1]
            if 'Birth' not in self.lines[7]: # Birth 정보가 있는 파일
                JMP_IDX = 7 # Birth: 가 존재하면 step 8
            else: # Birth 정보가 없는 파일
                JMP_IDX = 8 # Birth: 가 존재하지 않으면 step  7
            
            data = []
            for i in range(0, len(self.lines), JMP_IDX):
                elements = []
                for j in range(i, i+7):
                    elements.append(self.lines[j])
                self.cleanning(elements)

                
    def cleanning(self, data: list):
        data = list(map(lambda s: s.split(), data))
        self.fileName.append(self.get_filename(data))
        self.size.append(self.get_size(data))
        self.inode.append(self.get_inode(data))
        self.permission.append(self.get_permission(data))
        (uid, gid) = self.get_owner(data)
        self.owner.append(uid)
        self.group.append(gid)
        self.atime.append(self.get_timestamp(data, 4))
        self.mtime.append(self.get_timestamp(data, 5))
        self.ctime.append(self.get_timestamp(data, 6))

    def get_filename(self, data: list):
        return data[0][1].replace('‘', '').replace('’', '')

    def get_size(self, data: list):
        return data[1][1]

    def get_inode(self, data: list):
        return data[2][3]
    
    def get_permission(self, data: list):
        return data[3][1].replace('(', '').replace(')', '').split('/')[0]
    
    def get_owner(self, data: list):
        data = data[3][:]
        uid_gid = []
        
        for i in data:
            if re.match(r"\d+/.*\)", i):
                uid_gid.append(self.get_user(i))
            elif re.match(r"\d+/", i):
                index = data.index(i)
                uid_gid.append(data[index+1].replace(')', ''))
        
        return uid_gid
            
    def get_user(self, data: str):
        return data.split('/')[1].replace(')', '')
    
    # TODO: AMC 시간 업데이트
    def get_timestamp(self, data: list, mode: int):
        timestamp = data[mode][1] + " " + data[mode][2]
        return timestamp


def main():
    p = argparse.ArgumentParser(sys.argv[1:])
    p.add_argument('-f', '--file', help="Result file of stat command", dest='stat_file')
    p.add_argument('-o', '--out', help="Specify output file name", dest='output_file')
    args = p.parse_args()
    
    # input file verify
    if args.stat_file is None:
        print(f"stat 명령어 결과 파일에 대한 경로를 입력하세요!")
        print(f"옵션: '-f' 또는 '--file'")
        exit(0)
    else:
        STAT_FILE = args.stat_file
        
        if args.output_file is None:
            OUTPUT_FILE = "stat.csv" # default output file name: "stat.csv"
        else:
            OUTPUT_FILE = args.output_file
    
        p = LinueMetaData(STAT_FILE)
        
        # make csv file
        df = pd.DataFrame({"File Name": p.fileName, "Size": p.size, "inode": p.inode, "Permission": p.permission, "User": p.owner, "Group": p.group, "Access Time": p.atime, "Modify Time": p.mtime, "Change Time": p.ctime})

        print("======================================================")
        print("[!] Current UTC is " + p.utc + "!!!")
        
        df.to_csv(OUTPUT_FILE, index=False)

if __name__ == "__main__":
    main()
