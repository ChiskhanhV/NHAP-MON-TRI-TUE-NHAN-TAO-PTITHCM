import data as dt
import cost_function
import mutation
from copy import deepcopy


path_file_result = 'result.txt'

def evolutionary_algorithm(output_file, data, num_runs = 1, max_generations = 0):

    best_timetable = None
    neighbour = mutation.neighbour
    cost_func = cost_function.cost

    for i in range(num_runs):
        chromosome = dt.generate_chromosome(data)
        print(f"Epochs  {i + 1}/{num_runs}")

        for j in range(max_generations):
            new_chromosome = neighbour(deepcopy(chromosome))
            ft = cost_func(chromosome)
            if ft == 0:
                print("Stop Iteration Early Because cost = 0!")
                break
            ftn = cost_func(new_chromosome)
            if ftn <= ft:
                chromosome = new_chromosome
            if j % 200 == 0:
                print('[Iteration', j, '] ===>  [cost]', cost_func(chromosome))
        if best_timetable is None:
            best_timetable = deepcopy(chromosome)

    chromosome = best_timetable
    check_constraints(chromosome)
    dt.write_data(chromosome, output_file)
    # table = dt.create_dataFrame(chromosome[0])
    # print(table[['Professor', 'Assigned_time', 'Duration']])
    #dt.visualize_table(table)


def check_constraints(chromosome):
    output_file_result = open(path_file_result, 'w')

    professor_hard = True 
    classroom_hard = True
    group_hard = True
    allowed_classrooms = True

    for single_class in chromosome[0]:
        if single_class['Assigned_classroom'] not in single_class['Classroom']:
            allowed_classrooms = False
    for profesor in chromosome[1]:
        for i in range(len(chromosome[1][profesor])):
            if chromosome[1][profesor][i] > 1:
                professor_hard = False
    for Classroom in chromosome[2]:
        for i in range(len(chromosome[2][Classroom])):
            if chromosome[2][Classroom][i] > 1:
                classroom_hard = False
    for group in chromosome[3]:
        for i in range(len(chromosome[3][group])):
            if chromosome[3][group][i] > 1:
                group_hard = False
    

    output_file_result.write("============================================================\n")
    output_file_result.write(f'Are hard restrictions for professors satisfied: {professor_hard}\n')
    output_file_result.write(f'Are hard restrictions for classrooms satisfied:: {classroom_hard}\n')
    output_file_result.write(f'Are hard restrictions for groups satisfied: {group_hard}\n')
    output_file_result.write(f'Are hard restrictions for allowed classrooms satisfied: {allowed_classrooms}\n')
    output_file_result.write("============================================================\n")



    # Check preferred order statistics
    # P -> V -> L
    subjects_cost = 0
    for single_class in chromosome[4]:
        subject_cost = 0
        for lab in chromosome[4][single_class]['L']:
            for practice in chromosome[4][single_class]['V']:
                for group in lab[1]:
                    if group in practice[1] and lab[0] < practice[0]:
                        subject_cost += 1
            for lecture in chromosome[4][single_class]['P']:
                for group in lab[1]:
                    if group in lecture[1] and lab[0] < lecture[0]:
                        subject_cost += 1
                        
        for practice in chromosome[4][single_class]['V']:
            for lecture in chromosome[4][single_class]['P']:
                for group in practice[1]:
                    if group in lecture[1] and practice[0] < lecture[0]:
                        subject_cost += 1
        subjects_cost += subject_cost
        output_file_result.write(f'Subject cost for subject {single_class} is: {subject_cost}\n')

    output_file_result.write(f'Total subject cost: {subjects_cost}\n')
    output_file_result.write('============================================================\n')
    output_file_result.write('============================================================\n')

    

    output_file_result.close()

  