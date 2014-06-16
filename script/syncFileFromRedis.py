import redis
import re
import os, sys
import ConfigParser

cf = ConfigParser.ConfigParser()
cf.read("config.conf")
REDIS_DB                   = cf.get("key", "REDIS_DB")

# your sync config
server = '23.226.79.61'
user = 'chappyhome'
password = ''
port = ''
source = '/home/data/NEWBOOK/'
target = 'download'
options = "-rtvuC --delete  --password-file=/etc/rsync.password"

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

pool = redis.ConnectionPool(host='127.0.0.1', password='qazwsxedc', db=REDIS_DB)
redis_conn = redis.Redis(connection_pool=pool)
pubsub_ins = redis_conn.pubsub()
pubsub_ins.subscribe('channel_1')
listen2 =  pubsub_ins.listen()
while True:
    if listen2.next():
    	sync()