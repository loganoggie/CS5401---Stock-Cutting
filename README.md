use with ./run.sh <config_file> <problem_instance.txt>

All internal program paramters are labeled wth RAND or EA.
This label suggests whether or not the paramter is required for EA or RAND search types

# location for logs and solutions
log=logs/log
solution=solutions/solution

# set to "rand" for a completely random solution search, set to "ea" for an evolutionary algorithm that  
searchType=<string "ea" or "rand" including quotes>

# Seed value for the random number generator -- <"None"> initializes time-stamp based randomization
seed=<string "None" including quotes, or float number>

# evolutionary strategy type... 'plus' enables a (μ + λ)-EA  while  'comma' enables a (μ , λ)-EA
strategy=<integer value of 0 or 1>

# number of evaluations
evaluations=<integer value greater than 0>

# number of program run-throughs
runs=<integer value greater than 0>

# EA -- mu represents the number of parents
mu=<integer value greater than 0>

# EA -- lambda represents the number of offspring
lambda=<integer value greater than 0>

# parent selection type:
# 'rand' for Uniform Random selection.
# 'fps' for Fitness Proportional Selection.
# 'tournament' k-Tournament Selection with replacement'
parentSelection=<string "rand", "fps", or "tournament" including quotes>

# integer value represents the number of competition in k-tournament parent selection
pkval=<integer greater than 0 and less than or equal to mu>

# survival selection type:
# 'rand' for Uniform Random selection.
# 'fps' for Fitness Proportional Selection.
# 'tournament' k-Tournament Selection with replacement'.
# 'truncate' for truncation method
survivalSelection=<integer between -1 and lam>

# integer value represents the number of competition in k-tournament survival selection
skval=<integer greater than 0 and less than or equal to lambda>

# value between 0 and 10,000, representing the chance that an offspring will be mutated during gene crossover
mRate=<integer between 0 and 10000>

# 0 represents termination after all of the evaluations have been completed
# 1 terminates if no change in top non-dominated level of population for n generations
term=<integer value of 0 or 1>

# value for termination convergence criterion
nVal=<integer value>

# value for penalty coefficient. this float value is multipled by the number of overlapping points in an invalid solution and added to the fitness number of the solution. 0 for no penalty.
pCoefficient=<integer value grater than or equal to 0>

# flag to turn self adaptivity on(1) or off(0). This feature sets the initial mutation rate at 80% and gradually
selfAdaptive=<set to 1 for on, 0 for off>

# pass in solution seed file name/location here, or put "None" to issue a random initial starting population
initSeed=<"None" or location/filename of solution seed>


------------------------------------------------------------------------------


usage: StockCutting.py [-h] [-lf LOG_FILENAME] [-sf SOLUTION_FILENAME]
                       [-es EVOLUTIONARY_STRATEGY] [-s SEED] [-e EVALUATIONS]
                       [-r RUNS] [-m MU] [-l LAM] [-ps PARENT_SELECTION]
                       [-pk PARENT_K_VAL] [-ss SURVIVAL_SELECTION]
                       [-sk SURVIVAL_K_VAL] [-mr MUTATION_RATE]
                       [-t TERMINATION] [-n N_VALUE] [-pc PENALTY_COEFFICIENT]
                       [-sa SELF_ADAPTIVE] [-i INITIALIZE_PARENT_POPULATION]
                       instance_filename

positional arguments:
  instance_filename     filename and location containing data for the program.

optional arguments:
  -h, --help            show this help message and exit
  -lf LOG_FILENAME, --log_filename LOG_FILENAME
                        filename / location for logging every program run.
  -sf SOLUTION_FILENAME, --solution_filename SOLUTION_FILENAME
                        filename / location for recording the best-run result.
  -es EVOLUTIONARY_STRATEGY, --evolutionary_strategy EVOLUTIONARY_STRATEGY
                        Type of evolutionary strategy. 'plus' for a (μ + λ)-EA
                        or 'comma' for a (μ , λ)-EA
  -s SEED, --seed SEED  Seed for randomization. 'None' for time based
                        randomization.
  -e EVALUATIONS, --evaluations EVALUATIONS
                        Number of fitness evaluations. Default value is 1000.
  -r RUNS, --runs RUNS  Number of times the program will run the evalations.
  -m MU, --mu MU        μ value - size of parent population
  -l LAM, --lam LAM     λ value - size of offspring population/generation size
  -ps PARENT_SELECTION, --parent_selection PARENT_SELECTION
                        'rand' for Uniform Random selection. 'fps' for Fitness
                        Proportional Selection. 'tournament' k-Tournament
                        Selection with replacement'.
  -pk PARENT_K_VAL, --parent_k_val PARENT_K_VAL
                        integer value represents the number of competition in
                        k-tournament parent selection
  -ss SURVIVAL_SELECTION, --survival_selection SURVIVAL_SELECTION
                        'rand' for Uniform Random selection. 'fps' for Fitness
                        Proportional Selection. 'tournament' k-Tournament
                        Selection with replacement'. 'truncate' for truncation
                        method.
  -sk SURVIVAL_K_VAL, --survival_k_val SURVIVAL_K_VAL
                        integer value represents the number of competition in
                        k-tournament survival selection
  -mr MUTATION_RATE, --mutation_rate MUTATION_RATE
                        value between 0 and 99. Represents the percent-chance
                        of a mutation in an offspring
  -t TERMINATION, --termination TERMINATION
                        0 for termination after all evaluations have been
                        completed. 1 for termination after no change in
                        average population fitness for n generations. 2 for
                        termination after no change in best fitness in
                        population for n generations.
  -n N_VALUE, --n_value N_VALUE
                        value for termination convergence criterion
  -pc PENALTY_COEFFICIENT, --penalty_coefficient PENALTY_COEFFICIENT
                        this coefficient manipulates the fitness of invalid
                        solutions.
  -sa SELF_ADAPTIVE, --self_adaptive SELF_ADAPTIVE
                        set this parameter to 1 to enable the self-adapting
                        mutation rate parameter.
  -i INITIALIZE_PARENT_POPULATION, --initialize_parent_population INITIALIZE_PARENT_POPULATION
                        determines if starting parent population is
                        initialiezed randomly (0) or with a set of starting
                        solution (1)
