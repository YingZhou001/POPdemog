# POPdemog
POPdemog is a R package to visualize demographic history from coalescent simulation script. 
Currently, this POPdemog package does not check the simulation program input for correctness, but assumes the simulation program input has been validated by the simulation program.

We have verified the POPdemog package can be installed on R of version 2.15.0, 2.15.1, 3.0.0, 3.0.2, 3.1.0, 3.1.2, 3.2.0, 3.2.2, 3.3.0, 3.3.2, 3.4.1, and 3.4.3; but not all examples in the tutorial file can run on all these versions. We suggest user to use R (>= 3.3.0) to install and run this package.
   

Who to blame: Ying Zhou (yz001(at)uw(dot)edu)

## Installation
We are working on submitting this package to the CRAN.
Before that, user can [download](https://github.com/YingZhou001/POPdemog/raw/master/POPdemog_1.0.3.tar.gz) and then install it as

        install.package("POPdemog_1.0.3.tar.gz", repos=NULL, source=TRUE)

For R version >= 3.3.0, package POPdemog can be installed from the source file

        install.packages("https://github.com/YingZhou001/POPdemog/raw/master/POPdemog_1.0.3.tar.gz", repos=NULL)

then loaded it with

        library(POPdemog)

**Note:** Safari may automatically unzip the gz file when download the package source. Please see this [page](https://apple.stackexchange.com/questions/961/how-to-stop-safari-from-unzipping-files-after-download) for how to download files with Safari without unzipping files.

This package applies to R of version later than ..

## Docs and materials: doc/

User can start with the [tutorial](doc/POPdemog-tutorial.md), and check function details with the [manual](doc/POPdemog-manual.pdf)
   
## Tools: tools/

### msprime2ms.py
Convert the demographic model specified in msprime to the ms-compatible format.

Usage:   
> python msprime2ms.py [demofile] [population_configurations] [migration_matrix] [demographic_events]   
  
>   [demofile] = input python file which specified the demographic model in msprime format   
>   [population_configurations] = name of the variable for population_configurations in msprime   
>   [migration_matrix] = name of the variable for migration_matrix in msprime   
>   [demographic_events] = name of the variable for demographic_events in msprime   

**Notes:**   
  + The python version should be the same as you use to install msprime.   
  + The reference effective population size is set as `Ne=10,000`, for the followed plot, `N4=4*Ne=40,000`.  
  + The sample size for each subpopulation is set as 1 since it is irrelevant here.   


An example:

python [tools/msprime2ms.py](tools/msprime2ms.py) [doc/demo1.py](doc/demo1.py) population_configurations migration_matrix demographic_events > msprime.demo.cmd
