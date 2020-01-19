#This configuration file contains all the variables to run bdrmapit on RIPE traceroutes
#change-me Base and output directory
baseDir = "/project/mapkit/agamerog/country_asn_analysis/pipeline/"
outDir = baseDir + "output/"
#change-me Year and Month 
year = "2019"
month = "12"

#change-me AS2Org Month (this dataset is not produced monthly https://www.caida.org/research/topology/as2org/)
as2orgMonth = "10"

#change-me maximum iterations (depth) of bdrmapIT, and number of parallel processes to run
processes = "4" 
maxIterations = "5"

#change-me on beamer.caida.org, these directories 
#already have the required input files; 
#if running elsewhere, follow the URLs next to each input file,
#download the files (you may have to fill out a request form) and 
#modify the directories below to point towards your downloaded files
dateString = year + month + "01"
as2orgString = year + as2orgMonth + "01"
#http://data.caida.org/datasets/as-relationships/serial-1/
asRel = "/data/external/as-rank-ribs/" + dateString + "/" + dateString + ".as-rel.txt.bz2"

#http://data.caida.org/datasets/as-relationships/serial-1/
custCone = "/data/external/as-rank-ribs/" + dateString + "/" + dateString + ".ppdc-ases.txt.bz2"

# https://www.caida.org/research/topology/as2org/
as2org = "/data/external/topology-asdata/as-organizations/" + as2orgString + ".as-org2info.txt.gz"

# https://www.caida.org/data/routing/routeviews-prefix2as.xml
pfx2as = "/data/external/as-rank-ribs/" + dateString + "/" + dateString + ".prefix2as.bz2"

#change-me if you wish to download RIPE traceroutes from the last month, set the start and
#end dates below, as well as a directory to save them to (each day takes about 21G of disk)
ripeStart = "2019-12-30"
ripeFinish = "2019-12-31"
ripeOutput = "/scratch/mapkit/dlripetraces/"

#ip2as file (generated before running bdrmapIT)
ip2asFile = baseDir + "ip2as/" + dateString + ".ip2as"
