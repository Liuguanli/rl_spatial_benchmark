import sys
import os
import json
import shutil


# Define p_opt as a global variable
p_opt = None
p_opt_config = None
acc_build = 0
min_query_cost = 0

key_map = {
    "qdtree": ["min_query_cost", "total_build", "query", "sampling"],
    "rlrtree": ["min_query_cost", "total_build", "epoch", "sampling"],
    "bmtree": ["min_query_cost", "total_build", "tree_depth", "sampling"]
}

real_build_cost_path = {
    "bmtree": "./result/libspatialindex/HDD/4K/bmtree/build/{dataset1}_100000000_{dataset2}_100000000_range_1000_2_uniform_1_0.001x0.001_bits_32_depth_{key1}_sample_{key2}.txt",
    "qdtree": "./result/libspatialindex/HDD/4K/qdtree/build/{dataset1}_100000000_{dataset2}_100000000_range_1000_2_uniform_1_0.001x0.001_episode_10_sampling_ratio_{key2}_action_space_{key1}.txt",
    "rlrtree": "./result/libspatialindex/HDD/4K/rlrtree/build/{dataset1}_100000000_{dataset2}_100000000_range_1000_2_uniform_1_0.001x0.001_rlrtree_epoch_{key1}_sample_{key2}.txt"
}

synthetic_build_cost_path = {
    "bmtree": "./result/libspatialindex/HDD/4K/bmtree/build/data_100000000_2_{distribution}_{skewness}_range_1000_2_uniform_1_0.001x0.001_bits_32_depth_{key1}_sample_{key2}.txt",
    "qdtree": "./result/libspatialindex/HDD/4K/qdtree/build/data_100000000_2_{distribution}_{skewness}_range_1000_2_uniform_1_0.001x0.001_episode_10_sampling_ratio_{key2}_action_space_{key1}.txt",
    "rlrtree": "./result/libspatialindex/HDD/4K/rlrtree/build/data_100000000_2_{distribution}_{skewness}_range_1000_2_uniform_1_0.001x0.001_rlrtree_epoch_{key1}_sample_{key2}.txt"
}

real_query_cost_path = {
    "bmtree": "./result/libspatialindex/HDD/4K/bmtree/range/{dataset1}_100000000_{dataset2}_100000000_range_1000_2_uniform_1_0.001x0.001_bits_32_depth_{key1}_sample_{key2}.txt",
    "qdtree": "./result/libspatialindex/HDD/4K/qdtree/range/{dataset1}_100000000_{dataset2}_100000000_range_1000_2_uniform_1_0.001x0.001_episode_10_sampling_ratio_{key2}_action_space_{key1}.txt",
    "rlrtree": "./result/libspatialindex/HDD/4K/rlrtree/range/{dataset1}_100000000_{dataset2}_100000000_range_1000_2_uniform_1_0.001x0.001_rlrtree_epoch_{key1}_sample_{key2}.txt"
}

synthetic_query_cost_path = {
    "bmtree": "./result/libspatialindex/HDD/4K/bmtree/range/data_100000000_2_{distribution}_{skewness}_range_1000_2_uniform_1_0.001x0.001_bits_32_depth_{key1}_sample_{key2}.txt",
    "qdtree": "./result/libspatialindex/HDD/4K/qdtree/range/data_100000000_2_{distribution}_{skewness}_range_1000_2_uniform_1_0.001x0.001_episode_10_sampling_ratio_{key2}_action_space_{key1}.txt",
    "rlrtree": "./result/libspatialindex/HDD/4K/rlrtree/range/data_100000000_2_{distribution}_{skewness}_range_1000_2_uniform_1_0.001x0.001_rlrtree_epoch_{key1}_sample_{key2}.txt"
}

def modify_json(data, modifications):
    """Modify specific fields in the JSON data."""
    for experiment in data.get("experiments", []):
        # Modify the 'distribution' field
        if "data" in experiment and "distribution" in experiment["data"]:
            experiment["data"]["distribution"] = modifications.get("distribution", experiment["data"]["distribution"])
            experiment["data"]["skewness"] = modifications.get("skewness", experiment["data"]["skewness"])
        
        # Modify bmtree-specific fields
        for baseline in experiment.get("baseline", []):
            config = baseline.get("config", {})
            if baseline.get("name") == "bmtree":
                config["tree_depth"] = modifications.get("tree_depth", config["tree_depth"])
                config["sampling"] = modifications.get("sampling", config["sampling"])
            if baseline.get("name") == "qdtree":
                modifications["sampling"] = modifications.get("sampling", 10000) /  100000000
                config["action_sampling_size"] = modifications.get("query", config["action_sampling_size"])
                config["sampling_ratio"] = modifications.get("sampling", config["sampling_ratio"])
            if baseline.get("name") == "rlrtree":
                config["epoch"] = modifications.get("epoch", config["epoch"])
                config["sample_size"] = modifications.get("sampling", config["sample_size"])                

    return data

def save_json(data, file_path):
    """Save the modified JSON data back to a file."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


def is_build_required(p):
    global p_opt
    if not p_opt:
        p_opt = p
        return True
    if p_opt['key1'] < p['key1'] and p_opt['key2'] < p['key2']:
        return False
    else:
        return True
    
def extract_build_time_from_txt(file_path):
    """Extract Elapsed Learn Time and Elapsed Build Time from a text file."""
    with open(file_path, 'r') as f:
        lines = f.readlines()

    elapsed_learn_time = None
    elapsed_build_time = None

    for line in lines:
        if "Elapsed Learn Time" in line:
            elapsed_learn_time = float(line.split(":")[-1].strip())
        if "Elapsed Build Time" in line:
            elapsed_build_time = float(line.split(":")[-1].strip())

    return (elapsed_learn_time +  elapsed_build_time) / (1e9 * 3600)

def extract_query_time_from_txt(file_path):
    """Extract Elapsed Learn Time and Elapsed Build Time from a text file."""
    with open(file_path, 'r') as f:
        lines = f.readlines()

    query_time = None

    for line in lines:
        if "Query mean" in line:
            query_time = float(line.split(":")[-1].strip())

    return query_time


def exec(config_file, modifications, tree_type, total_build):
    global acc_build
    global p_opt
    global min_query_cost

    if tree_type == 'qdtree':
        p = {'key1': modifications['query'], 'key2': modifications['sampling']} 
    elif tree_type == 'rlrtree':
        p = {'key1': modifications['epoch'], 'key2': modifications['sampling']}
    elif tree_type == 'bmtree':
        p = {'key1': modifications['tree_depth'], 'key2': modifications['sampling']}
    
    if is_build_required(p):
        # os.system(f"python run_exp_from_config.py {config_file}")
        dataset = modifications['distribution']
        if dataset in ["uniform", "normal", "skewed"]:
            build_cost_path = synthetic_build_cost_path[tree_type].format(
                distribution=modifications['distribution'],
                skewness=modifications['skewness'],
                key1=p['key1'],
                key2=p['key2']
            )
            query_cost_path = synthetic_query_cost_path[tree_type].format(
                distribution=modifications['distribution'],
                skewness=modifications['skewness'],
                key1=p['key1'],
                key2=p['key2']
            )
        else:
            build_cost_path = real_build_cost_path[tree_type].format(
                dataset1=modifications['distribution'],
                dataset2=modifications['distribution'],
                key1=p['key1'],
                key2=p['key2']
            )
            query_cost_path = real_query_cost_path[tree_type].format(
                dataset1=modifications['distribution'],
                dataset2=modifications['distribution'],
                key1=p['key1'],
                key2=p['key2']
            )
        

        if not os.path.exists(build_cost_path):
            return
        if not os.path.exists(query_cost_path):
            return
        
        build_cost = extract_build_time_from_txt(build_cost_path)

        query_cost = extract_query_time_from_txt(query_cost_path)

        if acc_build + build_cost < total_build:
            acc_build += build_cost

        if query_cost < min_query_cost:
            min_query_cost = query_cost
            p_opt = p
            optimal_config_file = config_file.replace(".json", f"_optimal_{modifications['distribution']}.json")
            shutil.copyfile(config_file, optimal_config_file)

def main():
    global p_opt
    global acc_build
    global min_query_cost
    # Define tree types and datasets
    tree_types = ["qdtree", "rlrtree", "bmtree"]
    datasets = ["us", "india", "australia", "uniform", "normal", "skewed"]

    for tree in tree_types:
        config_file = f"exp_config/index_tuning/{tree}_parameters.json"
        with open(config_file, 'r') as f:
            data = json.load(f)
            keys = key_map.get(tree, [])
            extracted = {key: data.get(key, None) for key in keys}
            # print(extracted)
        for dataset in datasets:
            template_file = f"exp_config/index_tuning/{tree}_template.json"
            with open(template_file, 'r') as f:
                template_data = json.load(f)
            
            modifications = {"distribution": dataset, "skewness": 4 if dataset == 'skewed' else 1}
            min_query_cost = extracted["min_query_cost"]
            if tree == 'qdtree':
                querys = extracted["query"]
                samplings = extracted["sampling"]
                for query in querys:
                    for sampling in samplings:
                        modifications["query"] = query
                        modifications["sampling"] = sampling
                        res = modify_json(template_data, modifications)
                        # print(tree, dataset, modifications)
                        save_json(res, f"exp_config/index_tuning/{tree}_tune_item.json")
                        exec(f"exp_config/index_tuning/{tree}_tune_item.json", modifications, tree, extracted["total_build"])

            elif tree == 'rlrtree':
                epochs = extracted["epoch"]
                samplings = extracted["sampling"]
                for epoch in epochs:
                    for sampling in samplings:
                        modifications["epoch"] = epoch
                        modifications["sampling"] = sampling
                        res = modify_json(template_data, modifications)
                        # print(tree, dataset, modifications)
                        save_json(res, f"exp_config/index_tuning/{tree}_tune_item.json")
                        exec(f"exp_config/index_tuning/{tree}_tune_item.json", modifications, tree, extracted["total_build"])

            elif tree == 'bmtree':
                tree_depths = extracted["tree_depth"]
                samplings = extracted["sampling"]
                for tree_depth in tree_depths:
                    for sampling in samplings:
                        modifications["tree_depth"] = tree_depth
                        modifications["sampling"] = sampling
                        res = modify_json(template_data, modifications)
                        # print(tree, dataset, modifications)
                        save_json(res, f"exp_config/index_tuning/{tree}_tune_item.json")
                        exec(f"exp_config/index_tuning/{tree}_tune_item.json", modifications, tree, extracted["total_build"])

            else:
                print(f"{tree} type is not supported!")

            print("dataset:", dataset, " p_opt:", p_opt)

            
            p_opt = None
            acc_build = 0



# def main():
#     # Define tree types and datasets
#     tree_types = ["qdtree", "rlrtree", "bmtree"]
#     datasets = ["us", "india", "australia", "uniform", "normal", "skewed"]

    # # Iterate over tree types and datasets
    # for tree in tree_types:
    #     for dataset in datasets:
    #         print(f"Running experiment for {tree} on {dataset}")
    #         config_file = f"exp_config/index_tuning/{tree}_{dataset}.json"
    #         # Run the experiment command
    #         os.system(f"python run_exp_from_config.py {config_file}")
    #         # TODO capture time 

if __name__ == "__main__":
    main()

# python run_index_tuning.py exp_config/index_tuning/bmtree_australia.json


