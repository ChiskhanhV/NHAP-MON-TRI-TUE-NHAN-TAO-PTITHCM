import json
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def load_data(path):
    with open(path, 'r') as read_file:
        data = json.load(read_file)
    for cls in data['Classes']:
        classroom = cls['Classroom']
        cls['Classroom'] = data['Classrooms'][classroom]

    data = data['Classes']
    return data # return list of classes

def generate_chromosome(data, Number_of_lessons = 60):
    
    Professors = {}
    classrooms = {}
    groups = {}
    subjects = {}
    new_data = []

    for single_class in data:
        Professors[single_class['Professor']] = [0] * Number_of_lessons
        for classroom in single_class['Classroom']:
            classrooms[classroom] = [0] * Number_of_lessons
        for group in single_class['Groups']:
            groups[group] = [0] * Number_of_lessons
        subjects[single_class['Subject']] = {'P' : [], 'V' : [], 'L' : []}

    for single_class in data:
        new_single_class = single_class.copy()
        classroom = random.choice(single_class['Classroom'])
        day = random.randrange(0, 5)

        if day == 4:
            period = random.randrange(0, 12 - int(single_class['Duration']))
        else:
            period = random.randrange(0, 13 - int(single_class['Duration']))

        new_single_class['Assigned_classroom'] = classroom
        time = 12 * day + period
        new_single_class['Assigned_time'] = time

        for i in range(time, time + int(single_class['Duration'])):
            Professors[new_single_class['Professor']][i] += 1
            classrooms[classroom][i] += 1
            for group in new_single_class['Groups']:
                groups[group][i] += 1
        subjects[new_single_class['Subject']][new_single_class['Type']].append((time, new_single_class['Groups']))

        new_data.append(new_single_class)
    
    return (new_data, Professors, classrooms, groups, subjects)



def write_data(data, path):
    with open(path, 'w') as write_file:
        json.dump(data, write_file, indent=4)


# def load_matrix_constraints(data):
#     return create_matrix_constraints(data)

def info_input(data:list[dict]):

    file_name = 'info_input.txt'
    data_df = pd.DataFrame(data)

    groups = []
    for gr in data_df['Groups']:
        groups.extend(gr)
    groups = list(set(groups))

    profs = list(data_df['Professor'].unique())
    subjs = list(data_df['Subject'].unique())

    print("Profs Size: {} prof".format(len(profs)))
    print("Profs     : {}".format(profs))
    print("Group Size:  {} group".format(len(groups)))
    print("Group     :  {}".format(groups))
    print("Subjects Size:  {} subjs".format(len(subjs)))
    print("Subjects     :  {}".format(subjs))

def create_dataFrame(data):
    columns = ["Subject", "Professor", "Type", "Groups", "Duration", "Assigned_time", "Assigned_classroom"]
    lst_subs = list()
    for i, sub in enumerate(data):
        lst = []
        for ele in columns:
            lst.append(sub[ele])
        lst_subs.append(lst)
    
    df_table = pd.DataFrame(lst_subs, columns=columns)
    return df_table

def visualize_table(table: pd.DataFrame):
    plt.axis('off')
    
    clus_data = table.values
    collabel = table.columns
    time_table = plt.table(cellText=clus_data, colLabels=collabel, loc='center')

    plt.show()
