import model
import json

select = 'avg' # Switch to 'avg' for average prices

scenario_json_files = ['data/scenario_1_%s_price.json' % (select, ),
                       'data/scenario_2_%s_price.json' % (select, ),
                       'data/scenario_3_%s_price.json' % (select, )]

# Loop through scenario data sets
for data_set in scenario_json_files:
    # Load scenario data set from file
    with open(data_set, 'r', encoding='utf-8') as f:
        scenario_list = json.load(f)

    # Call model and generate solution for scenario
    solution = model.solve(scenario_list)

    # Print solution
    print(solution[0])
    print(solution[1])
