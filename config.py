#This configuration file contains all the variables to run bdrmapit on RIPE traceroutes
#change-me Base and output directory
baseDir = "/project/mapkit/bdrmapit_pipeline/"
outDir = baseDir + "output/"

#change-me-inputs Year and Month 
#This is the month used for all datasets except as2org and peeringDB

year = "2020"
month = "03"

#change-me-inputs AS2Org Month (this dataset is not produced monthly https://www.caida.org/research/topology/as2org/)
as2orgYear = "2020"
as2orgMonth = "01"

#change-me-inputs
peeringDBYear = "2020"
peeringDBMonth = "03"

#change-me-inputs maximum iterations (depth) of bdrmapIT, and number of parallel processes to run
#parallelization is only used for the traceroute parsing portion
processes = 5
maxIterations = "5"

#change-me-external If you're on CAIDA's server (e.g., beamer.caida.org), these directories 
#already have the required input files; 
#if running elsewhere, follow the URLs next to each input file,
#download the files (you may have to fill out a request form) and 
#modify the directories below to point towards your downloaded files
dateString = year + month + "01"
as2orgString = as2orgYear + as2orgMonth + "01"

#http://data.caida.org/datasets/as-relationships/serial-1/
asRel = "/data/external/as-rank-ribs/" + dateString + "/" + dateString + ".as-rel.txt.bz2"

#http://data.caida.org/datasets/as-relationships/serial-1/
custCone = "/data/external/as-rank-ribs/" + dateString + "/" + dateString + ".ppdc-ases.txt.bz2"

# https://www.caida.org/research/topology/as2org/
as2org = "/data/external/topology-asdata/as-organizations/" + as2orgString + ".as-org2info.txt.gz"

#change-me-inputs the "-1200" suffix might be for a different hour below
# https://www.caida.org/data/routing/routeviews-prefix2as.xml
pfx2as = "/data/routing/routeviews-prefix2as/" + year + "/" + month + "/" + "routeviews-rv2-" + dateString + "-1200.pfx2as.gz"

#change-me-external if you're not using the shared installation,
#The following will be the input start and end
#dates of script to download traceroutes 
#directly from RIPE (README step 3.2)
#end dates below, as well as a directory to save them to (each day takes about 21G of disk)
downloadStart = "2020-03-20" #AGG TODO remane these to downloadStart ?
downloadFinish = "2020-03-22" 

#change-me-traceroutes: specify the directory where the RIPE atlas traceroutes are stored *in subdirectories* (see README step 4.2)
ripeInput = "/scratch/mapkit/dlripetraces/2020_mar20/"

#ip2as file (generated before running bdrmapIT)
ip2asFile = baseDir + "ip2as/" + dateString + ".ip2as"
