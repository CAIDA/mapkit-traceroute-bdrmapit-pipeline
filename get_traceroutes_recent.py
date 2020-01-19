from sys import argv,exit
from datetime import date
import datetime
from os.path import exists
from os import mkdir
import urllib.request
from multiprocessing import Process
import time
#import wget


# ------------------------------------------------------ #
def date_from_iso(isoformat_str, fail_object=None):
    """
    date_from_iso(isoformat_str[, fail_object]) -> datetime.date()

        Returns a datetime.date() instance using the date
    written in isoformat.
    """
    isoformat_parts = isoformat_str.split("-")
    if len(isoformat_parts) != 3:
        print("Error: date must be in isoformat -- YYYY-MM-DD")
        return fail_object

    year, month, day = [int(part) for part in isoformat_parts]
    new_date = date(year, month, day)

    return new_date

# ------------------------------------------------------ #
def date_range(start_date, end_date, fail_object=None):
    """
    daterange() -> datetime.date (generator)

    Iterates over the range of the given date span.
    """
    if start_date <= end_date:
        for n in range((end_date - start_date).days):
            yield start_date + datetime.timedelta(n)
        yield end_date
    else:
        for n in range((start_date - end_date).days):
            yield start_date - datetime.timedelta(n)
        yield end_date

# ------------------------------------------------------ #
def getURL(url, output_dir):

    urllib.request.urlretrieve(url, output_dir + "/" + filename)
    #wget.download(url, output_dir + "/" + filename, bar=None)
# ------------------------------------------------------ #

if(len(argv) != 4):
    print("python get_traceroutes_recent.py <begin_date> <end_date> <output_dir>")
    exit()

LIMIT = 5
base_output_dir = argv[3]
if(not exists(base_output_dir)):
    mkdir(base_output_dir)

base_url = "https://data-store.ripe.net/datasets/atlas-daily-dumps/"

#https://data-store.ripe.net/datasets/atlas-daily-dumps/2019-11-01/traceroute-2019-11-01T0800.bz2

processes = list()
for date in date_range(date_from_iso(argv[1]), date_from_iso(argv[2])):

    date = str(date)

    output_dir = base_output_dir + "/" + str(date) + "/"
    if(not exists(output_dir)):
        mkdir(output_dir)

    for hour in range(24):
        hour_padded = str(hour).zfill(2)
        print("Processing: ", date, "hour: ", hour_padded)

        filename = "traceroute-" + date + "T" + hour_padded + "00.bz2"
        url = base_url + date + "/" + filename

        print(url)
        # Blocks until a process finish
        while(len(processes) >= LIMIT):
            time.sleep(5)
            processes = list(filter(lambda x: x.is_alive(), processes))

        # Add another node to process
        p = Process(name=filename, target=getURL, args=(url, output_dir, ))
        p.start()
        processes.append(p)

# Wait the remaining processes finish
for process in processes:
     process.join()
