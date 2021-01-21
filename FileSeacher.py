import os, sys
import re

class FileVisitor:

    def __init__(self, context=None, trace=0):
        self.fcount   = 0
        self.dcount   = 0
        self.context  = context
        self.trace    = trace

    def run(self, startDir=os.curdir, reset=True):
        if reset: self.reset()
        for (thisDir, dirsHere, filesHere) in os.walk(startDir):
            self.visitdir(thisDir)
            for fname in filesHere:                          # for non-dir files
                fpath = os.path.join(thisDir, fname)         # fnames have no path
                self.visitfile(fpath)
 
    def reset(self):                                         # to reuse walker
        self.fcount = self.dcount = 0                        # for independent walks

    def visitdir(self, dirpath):                             # called for each dir
        self.dcount += 1                                     # override or extend me
        if self.trace > 0: print(dirpath, '文件夹...')

    def visitfile(self, filepath):                           # called for each file
        self.fcount += 1                                     # override or extend me
        if self.trace > 1: print(self.fcount, '=>', filepath)


class SearchVisitor(FileVisitor):

    def __init__(self, searchkey, trace=2):
        FileVisitor.__init__(self, searchkey, trace)
        self.scount = 0

    def reset(self):                                         # on independent walks
        self.scount = 0
    
    def visitdir(self, dirpath):                             # called for each dir
        FileVisitor.visitdir
        if re.search(self.context,dirpath):
            print('找到文件夹：%s' % dirpath)

         
    def visitfile(self,fname):      
        FileVisitor.visitfile(self, fname) 
        filename=os.path.split(fname)[1]                        # test for a match
        if re.search(self.context,filename):
            self.visitmatch(fname)
            self.scount += 1 

    def visitmatch(self, fname):                       # process a match
        print('找到文件：%s' % fname)                   # override me lower


if __name__ == '__main__':
    # self-test logic
    dolist   = 1
    dosearch = 2    # 3=do list and search
    donext   = 4    # when next test added
    
    def selftest(testmask):
        if testmask & dolist:
           visitor = FileVisitor(trace=2)
           visitor.run(sys.argv[2])
           print('Visited %d files and %d dirs' % (visitor.fcount, visitor.dcount))

        if testmask & dosearch:
           visitor = SearchVisitor(sys.argv[3], trace=0)
           visitor.run(sys.argv[2])
           print('Found in %d files, visited %d' % (visitor.scount, visitor.fcount))

    selftest(int(sys.argv[1]))    # e.g., 3 = dolist | dosearch
