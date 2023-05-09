from algorithm import evolutionary_algorithm
import data as dt
import argparse
import pandas as pd
import os

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--Input', help = "Name of file Input")
    parser.add_argument('-o', '--Output', help = "Name of file Output")
    parser.add_argument('-e', "--Epochs", help = "The numbers of epochs", default=1)
    parser.add_argument('-g', "--MaxGenerations", help = "Max Generations", default=5000)
    ags = parser.parse_args()
    
    folder_dataset = 'dataset'
    folder_output = 'output'

    input_file = os.path.join(folder_dataset,ags.Input)
    output_file = os.path.join(folder_output,ags.Output)
    epochs = int(ags.Epochs)
    max_gen = int(ags.MaxGenerations)

    data = dt.load_data(input_file)

    #matrix_class_prof, matrix_prof = dt.load_matrix_constraints(data)
    
    print(max_gen)
    evolutionary_algorithm(output_file ,data, num_runs=epochs, max_generations=max_gen)


