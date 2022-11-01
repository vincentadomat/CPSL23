import pulp as pl
from prettytable import PrettyTable

path_to_cbc = '/opt/homebrew/opt/cbc/bin/cbc'
solver = pl.COIN_CMD(path=path_to_cbc, keepFiles=False, msg=False)

def solve(scenario_list):
    # Handling of scenario data
    set_o, set_m, set_t, set_c, b, k, h, d, w, f, p, g, e, timestamps = scenario_list

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
    lp_problem += pl.lpSum((e[o] - b[o][m] * k[t] - d[o][c] * w[c] - p[m]) * decision_x[o][m][t]
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
    table_meta = PrettyTable()
    names = ['Name', 'Solution Status', 'Solution Time [s]', 'Objective Value']
    table_meta.field_names = names
    table_meta.add_row([lp_problem.name, lp_problem.sol_status, lp_problem.solutionTime, lp_problem.objective.value()])
    #print(table)

    # Print solution's pretty table
    table = PrettyTable()
    names = ['period']
    names.extend(set_t)
    table.field_names = names
    table.add_row(['date'] + list(stamp.split('-')[0] for stamp in timestamps))
    table.add_row(['time'] + list(stamp.split('-')[1] for stamp in timestamps))
    table.add_row(['energy cost'] + list(k[t] for t in set_t))
    for m in set_m:
        row_list = [m]
        for t in set_t:
            element = ''
            for o in set_o:
                if decision_x[o][m][t].varValue == 1:
                    element = o
            row_list.append(element)
        table.add_row(row_list)
    #print(table)

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

    return [table_meta, table]
