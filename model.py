import pulp as pl
from prettytable import PrettyTable

path_to_cbc = '/opt/homebrew/opt/cbc/bin/cbc'
solver = pl.COIN_CMD(path=path_to_cbc, keepFiles=True)

# Declaration of sets
set_o = ['operation_11', 'operation_12', 'operation_21', 'operation_22', '1', '2', '3', '4', '5', '6', '7']
set_m = ['machine_1', 'machine_2']
set_t = [1, 2, 3, 4, 5]
set_c = ['competence_1', 'competence_2']

# Declaration of parameters
# Energy demand
b = {o:
         {m:
              1
          for m in set_m}
     for o in set_o}

# Energy cost
k = {t: 150 for t in set_t}

# Energy capacity
h = {t: 100 for t in set_t}

# Employee demand
d = {o:
         {c:
              1
          for c in set_c}
     for o in set_o}

# employee cost
w = {c: 100 for c in set_c}

# Employee capacity
f = {c:
         {t:
              100000
          for t in set_t}
     for c in set_c}

# Machine cost
p = {m: 90 for m in set_m}

# Machine capacity
g = {m: 100000 for m in set_m}

# Operational duration
u = dict()
for o in set_o:
    u[o] = 2

# Operation revenue
e = {o: 10000 for o in set_o}

# Initialize problem and declare problem type
lp_problem = pl.LpProblem('energy_opt_prod_scheduling', pl.LpMaximize)

# Decision variable X
decision_x = {o:
                  {m:
                       {t:
                            pl.LpVariable(name='x %s %s %s' % (o, m, t), cat=pl.LpInteger, lowBound=0, upBound=1)
                        for t in set_t}
                   for m in set_m}
              for o in set_o}

# Objective function
lp_problem += pl.lpSum((e[o] - b[o][m] * k[t] + d[o][c] * w[c] + p[m]) * decision_x[o][m][t]
                       for o in set_o
                       for m in set_m
                       for c in set_c
                       for t in set_t)

# Constraint 1
for o in set_o:
    lp_problem += pl.lpSum(decision_x[o][m][t] for m in set_m for t in set_t) <= 1

# Constraint 2
for m in set_m:
    for t in set_t:
        lp_problem += pl.lpSum(decision_x[o][m][t] for o in set_o) <= 1

# Constraint 6
for m in set_m:
    for t in set_t:
        lp_problem += pl.lpSum(decision_x[o][m][t] for o in set_o) <= g[m]

# Constraint 7
for t in set_t:
    for c in set_c:
        lp_problem += pl.lpSum(decision_x[o][m][t] * d[o][c] for o in set_o for m in set_m) <= f[c][t]

# Constraint 8
for t in set_t:
    lp_problem += pl.lpSum(decision_x[o][m][t] * b[o][m] for o in set_o for m in set_m) <= h[t]

# Write model to MPS file
# lp_problem.writeMPS('model.mps')

# Solve model
lp_problem.solve(solver)

# Print solution info
table = PrettyTable()
names = ['Name', 'Solution Status', 'Solution Time [s]', 'Objective Value']
table.field_names = names
table.add_row([lp_problem.name, lp_problem.sol_status, lp_problem.solutionTime, lp_problem.objective.value()])
print(table)

# Print solution's pretty table
table = PrettyTable()
names = ['machine']
names.extend(set_t)
table.field_names = names
for m in set_m:
    row_list = [m]
    for t in set_t:
        element = ''
        for o in set_o:
            if decision_x[o][m][t].varValue == 1:
                element = o
        row_list.append(element)
    table.add_row(row_list)
print(table)

# Print full set of variable values
"""
for variable in lp_problem.variables():
    if variable.varValue == 0:
        pass
    elif variable.varValue == 1:
        print(variable.getName())
        print(variable.varValue)
    else:
        print('something is wrong with var %s' % (variable, ))
"""
