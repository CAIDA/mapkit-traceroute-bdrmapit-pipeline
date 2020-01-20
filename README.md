This script downloads and prepares all the inputs required to run BdrmapIT on a set of recent traceroutes from RIPE. 
Developed by Alexander Gamero-Garrido, CAIDA - UC San Diego.

Development greatly benefitted from a previous version by Elverton Carvalho Fazzion and Rafael Almeida.

# First time installation

## Step 1. Clone the repo

`git clone https://github.com/CAIDA/mapkit-traceroute-bdrmapit-pipeline`

### 1.1. [Optional] You may remove our installation of bdrmapit and ip2as (fetched and built in Dec. 2019) and install your own.

#### 1.1.1. Installing bdrmapit

`git clone https://github.com/alexmarder/bdrmapit`

To create your own installation, you may follow the instructions here:

https://alexmarder.github.io/bdrmapit/

In subsequent steps, make sure to replace "bdrmapit/" with your installation directory.

#### 1.1.2. Installing ip2as

`git clone https://github.com/alexmarder/ip2as/`

### 1.2. It's probably a good idea to run subsequent steps on a screen

`screen -S pipeline`

## Step 2. Create a virtual environment pointing to the bdrmapit subdirectory

See https://virtualenv.pypa.io/en/latest/ if you are unfamiliar with virtualenv. Create the virtual environment:

`virtualenv --python=/usr/bin/python3 bdrmapit/`

And set the virtual environment as the active development environment:

`source bdrmapit/bin/activate`

## Step 3. Install requirement libraries:

`pip install Cython`

`pip install traceutils`

`pip install requests`

#Running bdrmapit. 
Start here on subsequent runs after first-time installation.
Update the fields labeled "change-me" in the config.py with the correct dates and directories. 
If you are using RIPE traceroutes, this is the only file you should need to modify. 

## Step 4. Preparing input data files

bdrmapit takes several input from CAIDA, PeeringDB and RIRs. Additionally, you'll need a set of traceroutes to use as input. 

The following two sub-steps (4.1. and 4.2.) may be executed in parallel for efficiency (on separate screens).

### 4.1. Produce ip2as file 

See https://alexmarder.github.io/ip2as/ for a description of this intermediary input.



#### 4.1.1. Download RIR files (and save list of downloaded files to an RIR file itself, which is an input to ip2as later on), AS Relationships file, Customer Cone file, PeeringDB file, then run ip2as; the below script does all of this:

`python ip2as-prepare-inputs-and-run.py`

### 4.2. You may now download a subset of all RIPE traceroutes from the last month:
Note: the below script is a wrapper for a previous script written by Elverton and Rafael.

`python download_ripe_traces.py`

## Step 5. Running bdrmapit.

### 5.1. It's probably a good idea to run this on a screen:

`screen -S pipeline`

### 5.2. Configure and run bdrmapit:

`python create-json-config-and-run-bdrmapit.py`

### 5.3 Convert SQL output to csv:

`python convert-sql-to-csv.py`

The final output of bdrmapIT is in `output/bdrmapit_output.csv`; the last two columns are for internal debugging and should be ignored.

# Parallel Execution Note 
Any of the above steps may be concatenated to run in sequence by separating them with a semicolon. For instance, to run steps 5.2 - 5.3:

`python create-json-config-and-run-bdrmapit.py; python convert-sql-to-csv.py`

