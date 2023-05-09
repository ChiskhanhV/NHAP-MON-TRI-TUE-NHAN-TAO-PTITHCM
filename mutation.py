import random

def neighbour(chromosome):

    candidates = []
    for k in range(len(chromosome[0])):     
        for j in range(len(chromosome[2][chromosome[0][k]['Assigned_classroom']])):
            if chromosome[2][chromosome[0][k]['Assigned_classroom']][j] >= 2:
                candidates.append(k)
        for j in range(len(chromosome[1][chromosome[0][k]['Professor']])):
            if chromosome[1][chromosome[0][k]['Professor']][j] >= 2:
                candidates.append(k)
        for group in chromosome[0][k]['Groups']:
            for j in range(len(chromosome[3][group])):
                if chromosome[3][group][j] >= 2:
                    candidates.append(k)

    if not candidates:
        i = random.randrange(len(chromosome[0]))
    else:
        i = random.choice(candidates)
    
    # Remove that class from its time frame and classroom
    for j in range(chromosome[0][i]['Assigned_time'], chromosome[0][i]['Assigned_time'] + int(chromosome[0][i]['Duration'])):
        chromosome[1][chromosome[0][i]['Professor']][j] -= 1
        chromosome[2][chromosome[0][i]['Assigned_classroom']][j] -= 1
        for group in chromosome[0][i]['Groups']:
            chromosome[3][group][j] -= 1
    chromosome[4][chromosome[0][i]['Subject']][chromosome[0][i]['Type']].remove((chromosome[0][i]['Assigned_time'], chromosome[0][i]['Groups']))

    # Find a free time and place
    length = int(chromosome[0][i]['Duration'])
    found = False
    pairs = []
    for classroom in chromosome[2]:
        c = 0
        if classroom not in chromosome[0][i]['Classroom']:
            continue
        for k in range(len(chromosome[2][classroom])):
            if chromosome[2][classroom][k] == 0 and k % 12 + length <= 12:
                c += 1
                # If we found x consecutive hours where x is length of our class
                if c == length:
                    time = k + 1 - c
                    # Friday 8pm is reserved for free hour
                    if k != 59:
                        pairs.append((time, classroom))
                        found = True
                    c = 0
            else:
                c = 0
    if not found:
        classroom = random.choice(chromosome[0][i]['Classroom'])
        day = random.randrange(0, 5)
        # Friday 8pm is reserved for free hour
        if day == 4:
            period = random.randrange(0, 12 - int(chromosome[0][i]['Duration']))
        else:
            period = random.randrange(0, 13 - int(chromosome[0][i]['Duration']))
        time = 12 * day + period

        chromosome[0][i]['Assigned_classroom'] = classroom
        chromosome[0][i]['Assigned_time'] = time

    # Set that class to a new time and place
    if found:
        novo = random.choice(pairs)
        chromosome[0][i]['Assigned_classroom'] = novo[1]
        chromosome[0][i]['Assigned_time'] = novo[0]

    for j in range(chromosome[0][i]['Assigned_time'], chromosome[0][i]['Assigned_time'] + int(chromosome[0][i]['Duration'])):
        chromosome[1][chromosome[0][i]['Professor']][j] += 1
        chromosome[2][chromosome[0][i]['Assigned_classroom']][j] += 1
        for group in chromosome[0][i]['Groups']:
            chromosome[3][group][j] += 1
    chromosome[4][chromosome[0][i]['Subject']][chromosome[0][i]['Type']].append((chromosome[0][i]['Assigned_time'], chromosome[0][i]['Groups']))

    return chromosome