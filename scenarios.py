import model
import csv

# Import energy cost and number of periods from CSV file
csv_path = 'Gro_handelspreise_202201010000_202201072359.csv'
energy_data = dict()
with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for counter, row in enumerate(reader):
        t = counter + 1
        row_date = row['Datum']
        row_time = row['Uhrzeit']
        row_value = row['Deutschland/Luxemburg[€/MWh]']
        energy_data[t] = {'value': float(row_value.replace(',', '.')), 'time': '%s-%s' % (row_date, row_time)}

# Declaration of sets
set_o = list('operation %s' % (i, ) for i in range(1, 11))
set_m = list('machine %s' % (i, ) for i in range(1, 11))
set_t = list(energy_data.keys())
set_c = list('competence %s' % (i, ) for i in range(1, 6))

# Declaration of parameters
# Energy demand
b = {o:
         {m:
              1
          for m in set_m}
     for o in set_o}

# Energy cost
k = {t: energy_data[t]['value'] for t in set_t}

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