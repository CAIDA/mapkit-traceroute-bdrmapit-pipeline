import os
import config as cfg

#import base dir and dates
baseDir = cfg.baseDir
year = cfg.year
month = cfg.month
as2orgMonth = cfg.as2orgMonth
pfx2as = cfg.pfx2as
#Download ip2as inputs
#Download and decompress RIR delegation files
os.system("cd ./ip2as")
dateString = year + month + "01" #first day of the month

os.system("wget https://ftp.apnic.net/stats/afrinic/2019/delegated-afrinic-extended-" + dateString)
os.system("wget https://ftp.apnic.net/stats/lacnic/delegated-lacnic-extended-" + dateString)
os.system("wget https://ftp.apnic.net/stats/arin/delegated-arin-extended-" + dateString)
os.system("wget https://ftp.apnic.net/stats/apnic/2019/delegated-apnic-extended-" + dateString + ".gz")
os.system("wget https://ftp.ripe.net/pub/stats/ripencc/2019/delegated-ripencc-extended-" + dateString + ".bz2")

#Download PeeringDB file
os.system("wget http://data.caida.org/datasets/peeringdb-v2/" + year + "/" + month + "/peeringdb_2_dump_" + year + "_" + month + "_01.json")
pdbFile = baseDir + "/ip2as/" + "peeringdb_2_dump_" + year + "_" + month + "_01.json"

#Move downloaded files to ip2as directory
os.system("gunzip delegated-apnic-extended-" + dateString+ ".gz")
os.system("bunzip2 delegated-ripencc-extended-" + dateString + ".bz2")
os.system("mv delegated* ip2as")
os.system("mv peeringdb* ip2as")
ip2asDir = baseDir + '/ip2as/'

with open('./ip2as/rir.files', 'w+') as f: #create list of above downloaded files
    f.write(ip2asDir + "delegated-lacnic-extended-" + dateString + "\n" + \
        ip2asDir + "delegated-afrinic-extended-" + dateString + "\n" + \
        ip2asDir + "delegated-arin-extended-" + dateString + "\n" + \
        ip2asDir + "delegated-apnic-extended-" + dateString + "\n" + \
        ip2asDir + "delegated-ripencc-extended-" + dateString)

#Now run ip2as
command = "cd ip2as; ./rir_delegations.py -f rir.files -r " + cfg.asRel + " -c " + cfg.custCone + " -o rir.prefixes"
os.system(command)

command = "cd ip2as; ./ip2as.py -p " + pfx2as + " -r rir.prefixes -R " + cfg.asRel + " -c " + cfg.custCone + " -a " + cfg.as2org + " -P " + " " + pdbFile + " -o " + dateString + ".ip2as"
os.system(command)
