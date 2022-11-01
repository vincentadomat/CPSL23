import csv
from random import seed, randint

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

# Scenario definition
scenarios = {'scenario 1':
                 {'num_o': 10,          # Number of operations in scenario
                  'num_m': 10,          # Number of machines in scenario
                  'range_t': [57, 65],  # Monday, January 3rd 2022, 08:00 am till 06:00 pm, first workday of the year
                  'num_c': 5,           # Number of competencies in scenario
                  'energy_demand': [1, 25], # Ranges to draw from for random demand, capacity and cost values
                  'energy_capacity': [1000, 1000],
                  'employee_demand': [1, 5],
                  'employee_cost': [80, 160],
                  'employee_capacity': [0, 20],
                  'machine_cost': [80, 160],
                  'machine_capacity': [1, 1],
                  'operation_revenue': [500, 1500]},
             'scenario 2':
                 {}
             }

scenario = scenarios['scenario 1']

# Set seed for random number calculations
seed(1000)

# Declaration of sets
set_o = list('operation %s' % (i, ) for i in range(1, scenario['num_o'] + 1))
set_m = list('machine %s' % (i, ) for i in range(1, scenario['num_m'] + 1))
set_t = list(range(scenario['range_t'][0], scenario['range_t'][1] + 1))
set_c = list('competence %s' % (i, ) for i in range(1, scenario['num_c'] + 1))

# Declaration of parameters
# Energy demand
min = scenario['energy_demand'][0]
max = scenario['energy_demand'][1]
b = {o:
         {m:
              randint(min, max)
          for m in set_m}
     for o in set_o}

# Energy cost
k = {t: energy_data[t]['value'] for t in set_t}

# Energy capacity
min = scenario['energy_capacity'][0]
max = scenario['energy_capacity'][1]
h = {t: randint(min, max) for t in set_t}

# Employee demand
min = scenario['employee_demand'][0]
max = scenario['employee_demand'][1]
d = {o:
         {c:
              randint(min, max)
          for c in set_c}
     for o in set_o}

# employee cost
min = scenario['employee_cost'][0]
max = scenario['employee_cost'][1]
w = {c: 10 * randint(int(min / 10), int(max / 10)) for c in set_c}

# Employee capacity
min = scenario['employee_capacity'][0]
max = scenario['employee_capacity'][1]
f = {c:
         {t:
              randint(min, max)
          for t in set_t}
     for c in set_c}

# Machine cost
min = scenario['machine_cost'][0]
max = scenario['machine_cost'][1]
p = {m: 10 * randint(int(min / 10), int(max / 10)) for m in set_m}

# Machine capacity
min = scenario['machine_capacity'][0]
max = scenario['machine_capacity'][1]
g = {m: randint(min, max) for m in set_m}

# Operation's revenue
min = scenario['operation_revenue'][0]
max = scenario['operation_revenue'][1]
e = {o: 10 * randint(int(min / 10), int(max / 10)) for o in set_o}

# List of timestamps for periods
timestamps = list(energy_data[t]['time'] for t in set_t)

scenario_list = [set_o, set_m, set_t, set_c, b, k, h, d, w, f, p, g, e, timestamps]
