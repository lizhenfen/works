#!/usr/bin/env python
# coding: utf-8
import sys
import os

class HandlerLog(object):
    def __init__(self, path='./access.log'):
        try:
            self.fp = open(path)
        except:
            print
            "{path} not exists.".format(path=path)
            sys.exit()
        self.fp.seek(0, os.SEEK_END)
        self.size = self.fp.tell()
        self.fp.seek(0, os.SEEK_SET)

    def __del__(self):
        try:
            self.fp.close()
        except:
            pass

    def seekLineHead(self):
        while self.fp.tell() > 0:
            self.fp.seek(-1, os.SEEK_CUR)
            value = self.fp.read(1)
            if value == "\n":
                break
            # print value
            self.fp.seek(-1, os.SEEK_CUR)

    def logCompare(self, timestamp, line):
        # return line.startswith(timestamp)  #此方式不能使用,无法定位
        log_datetime = '\t'.join(line.split()[:2])
        return cmp(timestamp, log_datetime)

    def searchTimeStamp(self, timestamp, start_pos=0):
        '''
            二分查找日志的实现
        '''
        pos_start, pos_end = start_pos, self.size
        while pos_start < pos_end:
            pos_mid = pos_start + (pos_start + pos_end) / 2
            self.fp.seek(pos_mid, os.SEEK_SET)
            # 定位中间位置的行首
            self.seekLineHead()
            line = self.fp.readline()
            # 匹配时间戳
            compare_val = logCompare(timestamp, line)
            if compare_val == 0:
                print
                line
                return True
            elif compare_val > 0:
                pos_start = self.fp.tell()
            else:
                pos_end = pos_mid
            return False

    def searchFirstTimeStamp(self, timestamp, start_pos=0):
        first_pos = -1
        ifexisttime = self.searchTimeStamp(timestamp, start_pos)
        if ifexisttime:
            line_cur_pos = self.fp.tell()
            while line_cur_pos > 0:
                self.fp.seek(-1, os.SEEK_CUR)
                self.seekLineHead()
                line_cur_pos = self.fp.tell()
                line = self.fp.readline()
                if line.startswith(timestamp):
                    self.fp.seek(line_cur_pos)
                    continue
                first_pos = self.fp.tell()
                break
        return ifexisttime

    def searchFirstTimeStamp(self, timestamp, start_pos=0):
        last_pos = -1
        ifexisttime = self.searchTimeStamp(timestamp, start_pos)
        '''if self.fp.tell() > 0:
            self.fp.seek(-1, os.SEEK_CUR)
            self.seekLineHead()'''
        if ifexisttime:
            last_pos = self.fp.tell()
            while last_pos < self.size:
                line = self.fp.readline()
                if line.startswith(timestamp):
                    last_pos = self.fp.tell()
                    continue
                '''self.fp.seek(-1, os.SEEK_CUR)
                self.seekLineHead()'''
                self.fp.seek(last_pos, os.SEEK_CUR)
            return last_pos


if __name__ == "__main__":
    loghandler = HandlerLog()
    loghandler.searchTimeStamp("2016-07-06 10:56:22")