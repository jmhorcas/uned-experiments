# Table of Contents
- [Table of Contents](#table-of-contents)
- [uned-experiments](#uned-experiments)
  - [How to use it](#how-to-use-it)
    - [Requirements](#requirements)
    - [Download and install](#download-and-install)
    - [Execution](#execution)
  
# uned-experiments
Experiments with SAT in Flama

## How to use it

### Requirements
- Linux
- [Python 3.9+](https://www.python.org/)
- antlr4
- [Flama](https://flamapy.github.io/)

### Download and install
1. Install [Python 3.9+](https://www.python.org/)
2. Clone this repository and enter into the main directory:

    `git clone https://github.com/jmhorcas/uned-experiments.git`

    `cd fm_solver`

3. Create a virtual environment: `python3 -m venv env`

4. Activate the environment: 
   
   `source env/bin/activate`
   
5. Install the dependencies: 

    5.1. Install Flama core and Flama for FM:
        `pip install flamapy flamapy-fm`

    5.2. Install UVL Parser from sources:
         `pip uninstall uvlparser`

         `git clone https://github.com/jmhorcas/uvlparser.git`

         `cd uvlparser`

         `pip install antlr4-python3-runtime`

         `antlr4 -Dlanguage=Python3 -no-listener UVL.g4`

         `pip install -e .`

    5.2. Install Flama SAT from sources:
         `git clone https://github.com/jmhorcas/pysat_metamodel.git`

         `cd pysat_metamodel`
         
         `pip install -e .`


### Execution
- To run only one analysis: 
    
    `python main_sat_analysis.py -fm FEATURE_MODEL [-s] SOLVER_NAME`

    The `FEATURE_MODEL` parameter is mandatory and specifies the file path of the feature model in UVL format.
    
    The `-s` argument is optional, if provided, the specified solver is used. The list of available solver are:
            
        cadical     = ('cd', 'cdl', 'cadical')
        gluecard3   = ('gc3', 'gc30', 'gluecard3', 'gluecard30')
        gluecard41  = ('gc3', 'gc41', 'gluecard4', 'gluecard41')
        glucose3    = ('g3', 'g30', 'glucose3', 'glucose30')
        glucose4    = ('g4', 'g41', 'glucose4', 'glucose41')
        lingeling   = ('lgl', 'lingeling')
        maplechrono = ('mcb', 'chrono', 'maplechrono')
        maplecm     = ('mcm', 'maplecm')
        maplesat    = ('mpl', 'maple', 'maplesat')
        mergesat3   = ('mg3', 'mgs3', 'mergesat3', 'mergesat30')
        minicard    = ('mc', 'mcard', 'minicard')
        minisat22   = ('m22', 'msat22', 'minisat22')
        minisatgh   = ('mgh', 'msat-gh', 'minisat-gh')


- To analyze a feature model running X executions and generate the result in a .csv file, execute:
    `./script.sh FEATURE_MODEL SOLVER_NAME RUNS`
    