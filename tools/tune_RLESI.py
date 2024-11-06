import json
import itertools
import time

def generate_combinations_as_map(parameters, key_names):
    # Extract parameter values based on provided key names
    values = [parameters[key] for key in key_names if key in parameters]
    
    # Generate combinations
    combinations = list(itertools.product(*values))
    
    # Convert each combination into a dictionary with key-value pairs using key names
    combination_maps = [
        {key_names[i]: value for i, value in enumerate(combo)} for combo in combinations
    ]
    
    return combination_maps

def run_index(combination):
    start_time = time.time()

    # learn
    # build
    query_cost = 0
    return query_cost, time.time() - start_time

def index_tuning(index_name, key_names=[]):

    config_file_path = f"data/tuning/{index_name}/parameters.json"

    print(config_file_path)
    
    time_cost_total = 0
    with open(config_file_path, "r") as json_file:
        parameters = json.load(json_file)


        print(parameters)

        build_threshold = parameters['build_threshold']
        total_threshold = parameters['total_threshold']
        query_threshold = parameters['query_threshold']

        combination_maps = generate_combinations_as_map(parameters, key_names)


        for combination_map in combination_maps:
            print(combination_map)


            query_cost, time_cost = run_index(combination_map)

            time_cost_total += time_cost

            # if query_cost < query_threshold:
            #      break

            # if time_cost_total > total_threshold:
            #      break
            
            # if time_cost > build_threshold:
            #     # delete this combination
            #     continue


index_key_names_map = {"rlrtree": ["sampling", "episode"],
                       "qdtree": ["sampling_ratio", "episode", "action_sampling_size"],
                       "bmtree": ["sampling", "tree_depth", "bit_num"]}

def main():
    index_tuning("rlrtree", key_names=index_key_names_map["rlrtree"])
    index_tuning("qdtree", key_names=index_key_names_map["qdtree"])
    index_tuning("bmtree", key_names=index_key_names_map["bmtree"])


if __name__ == "__main__":

    main()