# popdemog
Demographic history visualization from coalescent simulation script

Who to blame: Ying Zhou (yz001(at)uw.edu)

Copyright: 

## Docs:

Function manu: popdemog-manual.pdf

Tutorial: popdemog-tutorial.html

## Installation:

  install.packages("https://github.com/YingZhou001/popdemog/raw/master/popdemog_1.1.tar.gz", repos = NULL)
   
## Other tools

### msprime2ms.py
Convert the demographic model specified in msprime to the ms-compatible format.

Usage:   
> python msprime2ms.py [demofile] [population_configurations] [migration_matrix] [demographic_events]   
  
>   [demofile] = input python file which specified the demographic model in msprime format   
>   [population_configurations] = name of the variable for population_configurations in msprime   
>   [migration_matrix] = name of the variable for migration_matrix in msprime   
>   [demographic_events] = name of the variable for demographic_events in msprime   

**Notes:**   
  + the python version should be the same as you use to install msprime.   
  + The reference effective population size is set as 10,000.  
  + The sample size for each subpopulation is set as 1 since it is irrelevant here.   


An example:

python msprime2ms.py demo1.py population_configurations migration_matrix demographic_events > msprime.demo.cmd
