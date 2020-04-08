import os
import config as cfg

#import base dir and dates
baseDir = cfg.baseDir
year = cfg.year
month = cfg.month
as2orgMonth = cfg.as2orgMonth
ip2asFile = cfg.ip2asFile
trDir = cfg.ripeInput
asRelFile = cfg.asRel
coneFile = cfg.custCone
orgFile = cfg.as2org
proc = cfg.processes
iterations = cfg.maxIterations
outDir = cfg.outDir
#list traceroute files, save list to temp file and parse that file, 
#generate json file, then run bdrmapit

#get list of traceroutes
print ("ls " + trDir + "*/* > tmpFiles.txt")
os.system("ls " + trDir + "*/* > tmpFiles.txt") 
#CHANGE BACK AGG
trList = []
with open('tmpFiles.txt', 'r') as f:
    rows = f.readlines()
    for i in range(len(rows)):
        row = rows[i].strip('\n')
        trList.append(row)

#generate bdrmapit json file
with open('bdrmapit/config_bdrmapit.json','w+') as f:
    f.write('''{"$schema": "schema.json", "ip2as": "''')
    f.write(ip2asFile)
    f.write('''", "as2org": {"as2org": "''')
    f.write(orgFile)
    f.write('''"}, "as-rels": {"rels": "''')
    f.write(asRelFile)
    f.write('''", "cone": "''')
    f.write(coneFile)
    f.write('''"}, "processes":''')
    f.write(str(proc))
    f.write(''', "max_iterations":''')
    f.write(iterations)
    f.write(''', "atlas": {"files-list": [''')
    for i in range(len(trList)):
        if i < len(trList) - 1: #all but the last element
            f.write('''"''' + trList[i] + '''", ''')
        else:
            f.write('''"''' + trList[i] + '''"]}}''')
            
#Download ip2as inputs
#Download and decompress RIR delegation files
os.system("cd ./ip2as")
dateString = year + month + "01" #first day of the month

#Now run ip2as
command = "cd bdrmapit; ./bdrmapit.py -c config_bdrmapit.json -o " + outDir + "bdrmapit_output.sql"
print(command)
os.system(command)


