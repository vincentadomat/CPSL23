import pulp as pl

path_to_cbc = '/opt/homebrew/opt/cbc/bin/cbc'
solver = pl.COIN_CMD(path=path_to_cbc, keepFiles=True)

# Declaration of sets
set_j = ['job_1', 'job_2']
set_o = {'job_1': ['operation_11', 'operation_12'],
         'job_2': ['operation_21', 'operation_22']}
set_m = ['machine_1', 'machine_2']
set_t = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
set_c = ['competence_1', 'competence_2']

# Declaration of parameters
# Energy demand
b = {j:
         {o:
              {m:
                   123
               for m in set_m}
          for o in set_o[j]}
     for j in set_j}

# Energy cost
k = {t: 123 for t in set_t}

# Energy capacity
h = {t: 123 for t in set_t}

# Employee demand
d = {j:
         {o:
              {c:
                   123
               for c in set_c}
          for o in set_o[j]}
     for j in set_j}

# employee cost
w = {c: 123 for c in set_c}

# Employee capacity
f = {c:
         {t:
              123
          for t in set_t}
     for c in set_c}

# Machine cost
p = {m: 123 for m in set_m}

# Machine capacity
g = {m: 123 for m in set_m}

# Operational duration
u = dict()
for j in set_j:
    for o in set_o[j]:
        u[o] = 123

# Initialize problem and declare problem type
lp_problem = pl.LpProblem('energy_opt_prod_scheduling', pl.LpMinimize)

# Decision variable
decision_x = dict()
for j in set_j:
    decision_x[j] = dict()
    for o in set_o[j]:
        decision_x[j][o] = dict()
        for m in set_m:
            decision_x[j][o][m] = dict()
            for t in set_t:
                decision_x[j][o][m][t] = pl.LpVariable(name='%s %s %s %s' % (j, o, m, t), cat='Binary')

# Objective function
lp_problem += pl.lpSum((
                               b[j][o][m] * k[t]
                               + d[j][o][c] * w[c]
                               + p[m]
                       ) * decision_x[j][o][m][t]
                       for j in set_j
                       for o in set_o[j]
                       for m in set_m
                       for c in set_c
                       for t in set_t)

# Constraint 1
for j in set_j:
    lp_problem =+ pl.lpSum(decision_x[j][o][m][t] / u[o]
                           for o in set_o[j]
                           for m in set_m
                           for t in set_t) / len(set_o[j]) == 'NOT FINISHED'

