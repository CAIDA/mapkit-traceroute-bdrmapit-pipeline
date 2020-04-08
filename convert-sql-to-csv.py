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
#convert sql output of bdrmapit to csv

sqlFile = outDir + 'bdrmapit_output.sql'
csvFile = outDir + 'bdrmapit_output.csv'
command = '''sqlite3 -header -csv ''' + sqlFile + ''' "select * from annotation;" > ''' + csvFile
os.system(command) 

