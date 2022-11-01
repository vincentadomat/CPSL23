import model

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

scenario_list = [set_o, set_m, set_t, set_c, b, k, h, d, w, f, p, g, u, e]

solution = model.solve(scenario_list)

print(solution[0])
print(solution[1])