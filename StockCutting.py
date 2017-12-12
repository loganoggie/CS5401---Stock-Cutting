# Logan Nielsen
# CS5401 - Evolutionary Computing
# Assignment-1d

# vvvvv    FOR TESTING    vvvvv
# PYTHONHASHSEED=0 python3 StockCutting.py instances/50Shapes.txt -st ea -es comma -s 1234 -e 10000 -r 1 -m 100 -l 20 -ps tournament -pk 10 -ss truncate -mr 100 -pc 0

import mainFile
import argparse
import random
import time

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('instance_filename',
                            help = "filename and location containing data for the program.")

    parser.add_argument('-lf', '--log_filename', default = "logs/log",
                            help = "filename / location for logging every program run.")

    parser.add_argument('-sf', '--solution_filename', default = "solutions/solution",
                            help = "filename / location for recording the best-run result.")

    parser.add_argument('-es', '--evolutionary_strategy', default = 0, type = str,
                            help = "Type of evolutionary strategy. 'plus' for a (μ + λ)-EA or 'comma' for a (μ , λ)-EA ")

    parser.add_argument('-s', '--seed', default = "None",
                            help = "Seed for randomization. 'None' for time based randomization.")

    parser.add_argument('-e', '--evaluations', default = 10000, type = int,
                            help = "Number of fitness evaluations. Default value is 1000.")

    parser.add_argument('-r', '--runs', default = 30, type = int,
                            help = 'Number of times the program will run the evalations.')

    parser.add_argument('-m', '--mu', default = 10, type = int,
                            help = 'μ value - size of parent population')

    parser.add_argument('-l', '--lam', default = 10, type = int,
                            help = 'λ value - size of offspring population/generation size')

    parser.add_argument('-ps', '--parent_selection', default = "tournament", type = str,
                            help = "'rand' for Uniform Random selection. 'fps' for Fitness Proportional Selection. 'tournament' k-Tournament Selection with replacement'.")

    parser.add_argument('-pk', '--parent_k_val', default = 5, type = int,
                            help = "integer value represents the number of competition in k-tournament parent selection" )

    parser.add_argument('-ss', '--survival_selection', default = "truncate", type = str,
                            help = "'rand' for Uniform Random selection. 'fps' for Fitness Proportional Selection. 'tournament' k-Tournament Selection with replacement'. 'truncate' for truncation method.")

    parser.add_argument('-sk', '--survival_k_val', default = 5, type = int,
                            help = "integer value represents the number of competition in k-tournament survival selection" )

    parser.add_argument('-mr', '--mutation_rate', default = 2000, type = int,
                            help = 'value between 0 and 99. Represents the percent-chance of a mutation in an offspring')

    parser.add_argument('-t', '--termination', default = 0, type = int,
                            help = "0 for termination after all evaluations have been completed. 1 for termination after no change in average population fitness for n generations. 2 for termination after no change in best fitness in population for n generations.")

    parser.add_argument('-n', '--n_value', default = 50, type = int,
                            help = "value for termination convergence criterion")

    parser.add_argument('-pc', '--penalty_coefficient', default = 0, type = float,
                            help = "this coefficient manipulates the fitness of invalid solutions.")

    parser.add_argument('-sa', '--self_adaptive', default = 0, type = int,
                            help = "set this parameter to 1 to enable the self-adapting mutation rate parameter.")

    parser.add_argument('-i', '--initialize_parent_population', default = "None", type = str,
                            help = "determines if starting parent population is initialiezed randomly (0) or with a set of starting solution (1)")

    args = parser.parse_args() # creates the argument variables -- ex: args.instance_filename, args.seed, etc


    if args.seed == "None":
        args.seed = time.time()

    mainFile.Program(args.instance_filename, args.log_filename, args.solution_filename, args.evolutionary_strategy, args.seed, args.evaluations,
                        args.runs, args.mu, args.lam, args.parent_selection, args.parent_k_val, args.survival_selection, args.survival_k_val,
                        args.mutation_rate, args.termination, args.n_value, args.penalty_coefficient, args.self_adaptive, args.initialize_parent_population)


if __name__ == "__main__" :
    main()


    #els = [ <element> for <loop_variable> in <collection> if <condition>]
    #els = []
    #for <loop_variable> in <collection>:
    #    if <condition>:
    #        els.append(<element>)
