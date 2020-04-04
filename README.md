This set of scripts download and prepare all the inputs required to run BdrmapIT on a set of recent traceroutes from RIPE. 
Developed by Alexander Gamero-Garrido, CAIDA - UC San Diego.

Development greatly benefitted from a previous version by Elverton Carvalho Fazzion and Rafael Almeida.

**Note: if you are using CAIDA's shared installation at beamer.caida.org, proceed to step 4.**

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

## Step 3. Install requirement libraries 

(make sure you have the latest version as there are frequent updates with fixes)

`pip install Cython`

`pip install traceutils`

`pip install requests`

# Running bdrmapit

## Step 4. Preparing config and input data files

### 4.0.0 Accessing CAIDA's shared installation (if applicable)
CAIDA's shared installation is located at `beamer.caida.org:/project/mapkit/bdrmapit_pipeline`
To activate the virtual environment there, run:
`cd /project/mapkit/bdrmapit_pipeline`
`source bdrmapit/bin/activate`

### 4.0.1 Change Config File
Start here on subsequent runs after first-time installation.
Update the fields labeled `change-me` in the `config.py` file with the correct dates and directories. 
If you are using RIPE traceroutes, this is the only `.py` file you need to modify. 

### 4.0.2 Prepare Input Files
bdrmapit takes several input from CAIDA, PeeringDB and RIRs. Additionally, you'll need a set of traceroutes to use as input. 

The following two sub-steps (4.1. and 4.2.) may be executed in parallel for efficiency (on separate screens).

### 4.1. Produce ip2as file 

See https://alexmarder.github.io/ip2as/ for a description of this intermediary input.

#### 4.1.1. Download: RIR files (and save list of downloaded files to an RIR file itself, which is an input to ip2as later on), AS Relationships file, Customer Cone file, PeeringDB file. Then, run ip2as. The below script does all of this:

`python ip2as-prepare-inputs-and-run.py`

### 4.2. Copy or download the RIPE traceroutes you want to use:
Put any traceroutes you want to use as an input for BdrmapIT in a **subdirectory** of the directory listed in the `config.py` file with variable name `ripeOutput`.

In the default config file, `ripeOutput` points to `/scratch/mapkit/dlripetraces/` which has a set of all publically available RIPE traceroutes in subdirectories as follows:
`/scratch/mapkit/dlripetraces/2020-03-20/traceroute-2020-03-20T**00.bz2`
where ** is the time of day.

If you are planning on using a large number of traceroutes (i.e., over 5GB), please put the input files in `/scratch/mapkit/<your_subdirectory>` or elsewhere where you have been allocated disk space if that directory is full. **This is to ensure that our production directory at /project/mapkit/ does not run out of space.**

We at CAIDA are _currently_ (April 2020) downloading and keeping copies of all public RIPE traceroutes in the following directory:
`/data/external/ripe-atlas-dumps/`. You may copy these files into your input directory, or create symbolic link subdirectories (see https://kb.iu.edu/d/abbe) in your input directory to the specific dates you want to use from `/data/external/ripe-atlas-dumps/`. 

If you are using non-public measurements from RIPE, you will have to download those.

## Step 5. Running bdrmapit.

### 5.1. It's probably a good idea to run this on a screen:

`screen -S pipeline`

### 5.2. Configure and run bdrmapit:

`python create-json-config-and-run-bdrmapit.py`

### 5.3 Convert SQL output to csv:

`python convert-sql-to-csv.py`

The final output of bdrmapIT is in `output/bdrmapit_output.csv`; the last two columns are for internal debugging and should be ignored.

# Parallel Execution Note 
Any of the above steps (except for screen creation) may be concatenated 
to run in sequence by separating them with a semicolon. For instance, to run steps 5.2 - 5.3:

`python create-json-config-and-run-bdrmapit.py; python convert-sql-to-csv.py`

