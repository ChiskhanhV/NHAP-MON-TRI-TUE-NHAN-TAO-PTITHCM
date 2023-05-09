
def cost(chromosome):
    
    prof_cost = 0
    classrooms_cost = 0
    groups_cost = 0
    subjects_cost = 0
    cost_matrix_prof = 0
    #cost_matrix_class = 0
    

    for idx, single_class in enumerate(chromosome[0]):
        time_class = single_class['Assigned_time']
        class_len = single_class['Duration']
        
        
        for i in range(time_class, time_class + int(class_len)):
            if chromosome[1][single_class['Professor']][i] > 1: 
                prof_cost += 1
            # if matrix_prof.loc[single_class['Professor']]['Period'][i] == 1:
            #     cost_matrix_prof += 5
            if chromosome[2][single_class['Assigned_classroom']][i] > 1:
                classrooms_cost += 1
            for group in single_class['Groups']:
                if chromosome[3][group][i] > 1:
                    groups_cost += 1

    
    for single_class in chromosome[4]:
        for lab in chromosome[4][single_class]['L']:
            for practice in chromosome[4][single_class]['V']:
                for group in lab[1]:
                    if group in practice[1] and lab[0] < practice[0]: # If lab is before practical
                        subjects_cost += 0.05
            for lecture in chromosome[4][single_class]['P']:
                for group in lab[1]:
                    if group in lecture[1] and lab[0] < lecture[0]: # If lab is before lecture
                        subjects_cost += 0.05
        for practice in chromosome[4][single_class]['V']:
            for lecture in chromosome[4][single_class]['P']:
                for group in practice[1]:
                    if group in lecture[1] and practice[0] < lecture[0]: # If practical is before lecture
                        subjects_cost += 0.05
    

    return prof_cost + classrooms_cost  + groups_cost + round(subjects_cost, 4) 

