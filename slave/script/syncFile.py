import os
import sys
import pyinotify
import re

# your sync config
server = '59.188.87.61'
user = 'chappyhome'
password = ''
port = ''
source = '/data/htdocs/static/epub_content/'
target = 'books_data'
options = "-rtvuC --delete  --password-file=/etc/rsyncd/rsync.password"

#custom regular expression
rulers = (r"[#~.][\s\S]*", r"[\s\S]*[#~]", r"[\s\S]*_flymake.[\s\S]*")

if port != '':
    port = "-e 'ssh -p %d'" % (port)

def runCmd(cmd):
    os.system(cmd)

def sync():
    global server, user, port, source, target, option
    cmd = "rsync %s %s %s %s@%s::%s" % (port, options, source, user, server, target)
    #print cmd
    runCmd(cmd)


class OnChangeHandler(pyinotify.ProcessEvent):
    def checkFileName(self, fileName):
        global rulers
        for ruler in rulers:
            p = re.compile(ruler)
            if p.match(fileName) != None:
                return False
        return True

    def syncFile(self, fileName):
        if self.checkFileName(fileName):
            sync()

    def process_IN_CREATE(self, event):
        #print "Create file: %s " % os.path.join(event.path,event.name)
        self.syncFile(event.name)

    def process_IN_DELETE(self, event):
        #print "Delete file: %s " % os.path.join(event.path,event.name)
        self.syncFile(event.name)

    def process_IN_MOVED_TO(self, event):
        #print "Delete file: %s " % os.path.join(event.path,event.name)
        self.syncFile(event.name)

    # def process_IN_MODIFY(self, event):
    #     #print "Modify file: %s " % os.path.join(event.path,event.name)
    #     self.syncFile(event.name)

def auto_sync():
    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_MOVED_TO | pyinotify.IN_CLOSE_WRITE | pyinotify.IN_CREATE | pyinotify.IN_DELETE | pyinotify.IN_MODIFY
    notifier = pyinotify.Notifier(wm, OnChangeHandler())
    wm.add_watch(source, mask, rec=True, auto_add=True)
    notifier.loop()


def main():
    auto_sync()


# main
if __name__ == "__main__":
    main()