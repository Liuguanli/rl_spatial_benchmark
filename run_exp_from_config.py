import json
import subprocess
import os
import time
import shutil

import logging

logger = None

from constants import *

def execute_command(command):

    global logger
    logger.info(f"execute_command: {command}")

    start_time_ns = time.perf_counter_ns()

    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {e}")

    end_time_ns = time.perf_counter_ns()

    logger.info(f"finish execute_command")

    return end_time_ns - start_time_ns


def execute_command_with_err(command):

    global logger
    logger.info(f"execute_command_with_err: {command}")

    start_time_ns = time.perf_counter_ns()

    try:
        retult = subprocess.run(command, shell=True, check=True, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {e}")
        retult = None

    end_time_ns = time.perf_counter_ns()

    logger.info(f"finish execute_command_with_err")

    return retult, end_time_ns - start_time_ns

def safe_remove(file_name):

    global logger
    logger.info(f"safe_remove: {file_name}")

    if os.path.exists(file_name):
        os.remove(file_name)
    logger.info(f"finish safe_remove")
    

def cleanup_intermediate_files():

    global logger
    logger.info(f"cleanup_intermediate_files")

    if RUN_EXHAUSTIVE_SEARCH:
        safe_remove("a")
        safe_remove("b")
        safe_remove(".t")
        safe_remove("res2")

    safe_remove("res")
    safe_remove("tree.dat")
    safe_remove("tree.idx")

    safe_remove(Z_ORDER_OUTPUT)
    safe_remove(BMTREE_INPUT)
    logger.info(f"finish cleanup_intermediate_files")



def run_exhaustive_search(data_file, query_file, query_type="range", k=None):

    global logger
    logger.info(f"run_exhaustive_search: {data_file} {query_file} {query_type} {k}")
    
    with open('.t', 'w') as t_file:
        with open(data_file, 'r') as data:
            t_file.write(data.read())
        with open(query_file, 'r') as queries:
            t_file.write(queries.read())

    logger.info(f"Running exhaustive search: {query_type}")
    if query_type == "range":
        subprocess.run("test-rtree-Exhaustive .t intersection > res2", shell=True, check=True)
    else:
        if k:
            subprocess.run(f"test-rtree-Exhaustive .t {k}NN > res2", shell=True, check=True)

    logger.info("Comparing results")
    subprocess.run("sort -n res > a", shell=True)
    subprocess.run("sort -n res2 > b", shell=True)

    diff_result = subprocess.run("diff a b", shell=True)
    if diff_result.returncode == 0:
        logger.info("Same results with exhaustive search. Everything seems fine.")
    else:
        logger.info("PROBLEM! We got different results from exhaustive search!")

    wc_result = subprocess.run("wc -l a", shell=True, capture_output=True, text=True)
    logger.info(f"Results: {wc_result.stdout}")


def execute_range_query(data_file, query_file, range_query_output_path, test_file="test-rtree-RTreeQuery"):

    global logger

    logger.info(f"execute_range_query: data_file:{data_file} query_file:{query_file} range_query_output_path:{range_query_output_path} test_file:{test_file}")

    if RUN_EXHAUSTIVE_SEARCH:
        command = f"{test_file} {query_file} tree intersection {BUFFER} > res"
    else:
        command = f"{test_file} {query_file} tree intersection {BUFFER}"

    logger.info(f"execute_range_query: {command}")

    # result = subprocess.run(command, shell=True, check=True, stderr=subprocess.PIPE, text=True)
    result, elapsed_time_ns_range = execute_command_with_err(command)
    
    os.makedirs(os.path.dirname(range_query_output_path), exist_ok=True)

    with open(range_query_output_path, "w") as f:
        f.write(result.stderr)
        f.write(f"Elapsed Time: {elapsed_time_ns_range}\n")

    if RUN_EXHAUSTIVE_SEARCH:
        run_exhaustive_search(data_file, query_file, query_type="range")
    
    logger.info("Finish range query")


def execute_knn_query(k, query_file, data_file, knn_query_output_path, test_file="test-rtree-RTreeQuery"):

    global logger
    logger.info(f"execute_knn_query: data_file:{data_file} query_file:{query_file} knn_query_output_path:{knn_query_output_path} test_file:{test_file}")

    if RUN_EXHAUSTIVE_SEARCH:
        command = f"{test_file} {query_file} tree {k}NN {BUFFER}> res"
    else:
        command = f"{test_file} {query_file} tree {k}NN {BUFFER}"
    
    result, elapsed_time_ns_knn = execute_command_with_err(command)

    os.makedirs(os.path.dirname(knn_query_output_path), exist_ok=True)

    with open(knn_query_output_path, "w") as f:
        f.write(result.stderr)
        f.write(f"Elapsed Time: {elapsed_time_ns_knn}\n")

    if RUN_EXHAUSTIVE_SEARCH:
        run_exhaustive_search(data_file, query_file, query_type="knn", k=k)

    logger.info("Finish knn query")


def execute_point_query(query_file, data_file, point_query_output_path, test_file="test-rtree-RTreeQuery"):

    global logger
    logger.info(f"execute_point_query: data_file:{data_file} query_file:{query_file} point_query_output_path:{point_query_output_path} test_file:{test_file}")

    if RUN_EXHAUSTIVE_SEARCH:
        command = f"{test_file} {query_file} tree intersection {BUFFER} > res"
    else:
        command = f"{test_file} {query_file} tree intersection {BUFFER}"
    
    result, elapsed_time_ns_point = execute_command_with_err(command)

    os.makedirs(os.path.dirname(point_query_output_path), exist_ok=True)

    with open(point_query_output_path, "w") as f:
        f.write(result.stderr)
        f.write(f"Elapsed Time: {elapsed_time_ns_point}\n")

    if RUN_EXHAUSTIVE_SEARCH:
        run_exhaustive_search(data_file, query_file, query_type="range")

    logger.info("Finish point query")
    

def execute_insert(query_file, insert_output_path, test_file="test-rtree-RTreeQuery"):

    global logger
    logger.info(f"execute_insert: query_file:{query_file} insert_output_path:{insert_output_path} test_file:{test_file}")

    command = f"{test_file} {query_file} tree intersection {BUFFER}"
    
    result, elapsed_time_ns_point = execute_command_with_err(command)

    os.makedirs(os.path.dirname(insert_output_path), exist_ok=True)

    with open(insert_output_path, "w") as f:
        f.write(result.stderr)
        f.write(f"Elapsed Time: {elapsed_time_ns_point}\n")

    logger.info("Finish insert")
    

def execute_insert_point(query_file, insert_point_output_path, test_file="test-rtree-RTreeQuery"):

    global logger
    logger.info(f"execute_insert_point: query_file:{query_file} insert_point_output_path:{insert_point_output_path} test_file:{test_file}")

    command = f"{test_file} {query_file} tree intersection {BUFFER}"
    
    result, elapsed_time_ns_point = execute_command_with_err(command)

    os.makedirs(os.path.dirname(insert_point_output_path), exist_ok=True)

    with open(insert_point_output_path, "w") as f:
        f.write(result.stderr)
        f.write(f"Elapsed Time: {elapsed_time_ns_point}\n")

    logger.info("Finish insert_point")
    

def run_zorder(data_file_name, point_queries, range_queries, knn_queries, ks_map, insertions, insert_points, baseline_config):

    global logger
    logger.info(f"run_zorder: data_file_name:{data_file_name} baseline_config:{baseline_config}")
    try:

        if data_file_name.startswith("data"):
            ablosute_data_file_name = os.path.join(SYNTHETIC_DATA_PATH, data_file_name)
        else:
            ablosute_data_file_name = os.path.join(REAL_DATA_PATH, data_file_name)
        data_file_prefix = data_file_name.rstrip('.csv')

        page_size = baseline_config.get("page_size", 100)
        fill_factor = baseline_config.get("fill_factor", 1.0)
        bit_num = baseline_config.get("bit_num", 20)

        transform_command = f"python tools/zorder.py {ablosute_data_file_name} {Z_ORDER_OUTPUT} {bit_num}"
        elapsed_time_ns_order = execute_command(transform_command)

        data_file = Z_ORDER_SORTED_OUTPUT

        format_data_command = f"python tools/libspatialindex_data_adapter.py --type data --input {Z_ORDER_OUTPUT} --output {data_file}"
        execute_command(format_data_command)

        logger.info(f"Starting SFC Rtree bulk load using sorted data: {data_file}")
        
        command = f"test-rtree-SFCRTreeBulkLoad {data_file} tree {page_size} {fill_factor} {PAGE_SIZE} {BUFFER}"

        result, elapsed_time_ns_build = execute_command_with_err(command)

        build_output_path = Z_BUILD_OUTPUT_PATH.format(
            data_file_prefix=data_file_prefix,
            bit_num=bit_num
        )

        os.makedirs(os.path.dirname(build_output_path), exist_ok=True)

        with open(build_output_path, "w") as f:
            f.write(result.stderr)
            f.write(f"Elapsed Time: {elapsed_time_ns_order + elapsed_time_ns_build}\n")

        for file_name in range_queries:
            file_name_prefix = file_name.rstrip('.csv')
            range_query_output_path = Z_RANGE_QUERY_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                range_query_prefix=file_name_prefix,
                bit_num=bit_num,
            )
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            execute_range_query(data_file, query_file, range_query_output_path, "test-rtree-RTreeQuery")

        for file_name in knn_queries:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            ks = ks_map.get(file_name)
            for k in ks:
                knn_query_output_path = Z_KNN_QUERY_OUTPUT_PATH.format(
                    data_file_prefix=data_file_prefix,
                    knn_query_prefix=file_name_prefix,
                    bit_num=bit_num,
                    k=k
                )
                execute_knn_query(k, query_file, data_file, knn_query_output_path)

        for file_name in point_queries:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            point_query_output_path = Z_POINT_QUERY_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                point_query_prefix=file_name_prefix,
                bit_num=bit_num,
            )
            execute_point_query(query_file, data_file, point_query_output_path)

        for file_name in insertions:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            insert_output_path = Z_INSERT_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                insert_prefix=file_name_prefix,
                bit_num=bit_num,
            )
            execute_insert(query_file, insert_output_path)

        for file_name in insert_points:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            insert_point_output_path = Z_INSERT_POINT_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                insert_point_prefix=file_name_prefix,
                bit_num=bit_num,
            )
            execute_insert_point(query_file, insert_point_output_path)

    except subprocess.CalledProcessError as e:
        logger.error(f"fail: {e}")
    
    finally:
        # clean up intermediate files
        cleanup_intermediate_files()
        safe_remove(Z_ORDER_SORTED_OUTPUT)

def run_rankspace(data_file_name, point_queries, range_queries, knn_queries, ks_map, insertions, insert_points, baseline_config):

    global logger
    logger.info(f"run_rankspace: data_file_name:{data_file_name} baseline_config:{baseline_config}")
    try:
        if data_file_name.startswith("data"):
            ablosute_data_file_name = os.path.join(SYNTHETIC_DATA_PATH, data_file_name)
        else:
            ablosute_data_file_name = os.path.join(REAL_DATA_PATH, data_file_name)
        data_file_prefix = data_file_name.rstrip('.csv')

        page_size = baseline_config.get("page_size", 100)
        fill_factor = baseline_config.get("fill_factor", 1.0)
        bit_num = baseline_config.get("bit_num", 20)

        transform_command = f"python tools/rank_space_z.py {ablosute_data_file_name} {RANK_SPACE_Z_ORDER_OUTPUT} {bit_num}"
        elapsed_time_ns_order = execute_command(transform_command)

        data_file = RANK_SPACE_Z_ORDER_SORTED_OUTPUT

        format_data_command = f"python tools/libspatialindex_data_adapter.py --type data --input {RANK_SPACE_Z_ORDER_OUTPUT} --output {data_file}"
        execute_command(format_data_command)

        logger.info(f"Starting SFC Rtree bulk load using sorted data: {data_file}")
        
        command = f"test-rtree-SFCRTreeBulkLoad {data_file} tree {page_size} {fill_factor} {PAGE_SIZE} {BUFFER}"

        result, elapsed_time_ns_build = execute_command_with_err(command)

        build_output_path = RANK_SPACE_Z_BUILD_OUTPUT_PATH.format(
            data_file_prefix=data_file_prefix,
            bit_num=bit_num,
        )

        os.makedirs(os.path.dirname(build_output_path), exist_ok=True)

        with open(build_output_path, "w") as f:
            f.write(result.stderr)
            f.write(f"Elapsed Time: {elapsed_time_ns_order + elapsed_time_ns_build}\n")

        for file_name in range_queries:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            range_query_output_path = RANK_SPACE_Z_RANGE_QUERY_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                range_query_prefix=file_name_prefix,
                bit_num=bit_num,
            )
            execute_range_query(data_file, query_file, range_query_output_path)

        for file_name in knn_queries:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            ks = ks_map.get(file_name)
            for k in ks:
                knn_query_output_path = RANK_SPACE_Z_KNN_QUERY_OUTPUT_PATH.format(
                    data_file_prefix=data_file_prefix,
                    knn_query_prefix=file_name_prefix,
                    bit_num=bit_num,
                    k=k
                )
                execute_knn_query(k, query_file, data_file, knn_query_output_path)

        for file_name in point_queries:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            point_query_output_path = RANK_SPACE_Z_POINT_QUERY_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                point_query_prefix=file_name_prefix,
                bit_num=bit_num,
            )
            execute_point_query(query_file, data_file, point_query_output_path)

        for file_name in insertions:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            insert_output_path = RANK_SPACE_Z_INSERT_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                insert_prefix=file_name_prefix,
                bit_num=bit_num,
            )
            execute_insert(query_file, insert_output_path)

        for file_name in insert_points:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            insert_point_output_path = RANK_SPACE_Z_INSERT_POINT_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                insert_point_prefix=file_name_prefix,
                bit_num=bit_num,
            )
            execute_insert_point(query_file, insert_point_output_path)

    except subprocess.CalledProcessError as e:
        logger.error(f"fail: {e}")
    
    finally:
        # clean up intermediate files
        cleanup_intermediate_files()
        safe_remove(RANK_SPACE_Z_ORDER_SORTED_OUTPUT)

def run_bmtree(data_file_name, point_queries, range_queries, knn_queries, ks_map, insertions, insert_points, baseline_config):

    global logger
    logger.info(f"run_bmtree: data_file_name:{data_file_name} baseline_config:{baseline_config}")
    try:
        is_real_data = data_file_name.startswith("data")
        if is_real_data:
            ablosute_data_file_name = os.path.join(SYNTHETIC_DATA_PATH, data_file_name)
        else:
            ablosute_data_file_name = os.path.join(REAL_DATA_PATH, data_file_name)
        data_file_prefix = data_file_name.rstrip('.csv')

        page_size = baseline_config.get("page_size", 100)
        fill_factor = baseline_config.get("fill_factor", 1.0)
        tree_depth = baseline_config.get("tree_depth", 1)
        sample_size = baseline_config.get("sampling", 10000)
        bit_num = baseline_config.get("bit_num", 20)

        for range_file_name in range_queries:
            file_name_prefix = range_file_name.rstrip('.csv')
            if is_real_data:
                ablosute_query_file_name = f"data/synthetic/query/{range_file_name}"
            else:
                ablosute_query_file_name = f"data/real/query/{range_file_name}"

            logger.info("Prepare BMTree")
            
            data_transfer_command = f"python rl_baseline/bmtree_data_transfer.py {ablosute_data_file_name} {ablosute_query_file_name}"
            execute_command(data_transfer_command)

            learn_bmtree_command = f"bash rl_baseline/learn_bmtree.sh {data_file_prefix} {file_name_prefix} {tree_depth} {sample_size} {bit_num}"
            elapsed_time_ns_learn = execute_command(learn_bmtree_command)

            data_adapter_command = f"python tools/libspatialindex_data_adapter.py --type data --is_scaled --input {BMTREE_INPUT} --output {BMTREE_OUTPUT}"
            execute_command(data_adapter_command)

            # build bmtree sfcrtree
            command = f"test-rtree-SFCRTreeBulkLoad {BMTREE_OUTPUT} tree {page_size} {fill_factor} {PAGE_SIZE} {BUFFER}"
            result, elapsed_time_ns_build = execute_command_with_err(command)

            build_output_path = BMTREE_BUILD_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                query=file_name_prefix,
                bit_num=bit_num,
                tree_depth=tree_depth,
                sample_size=sample_size,
            )

            os.makedirs(os.path.dirname(build_output_path), exist_ok=True)

            with open(build_output_path, "w") as f:
                f.write(result.stderr)
                f.write(f"Elapsed Learn Time: {elapsed_time_ns_learn}\n")
                f.write(f"Elapsed Build Time: {elapsed_time_ns_build}\n")

            data_file = BMTREE_OUTPUT

            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            range_query_output_path = BMTREE_RANGE_QUERY_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                range_query_prefix=file_name_prefix,
                bit_num=bit_num,
                tree_depth=tree_depth,
                sample_size=sample_size,
            )
            execute_range_query(data_file, query_file, range_query_output_path)

            for knn_file_name in knn_queries:
                knn_file_name_prefix = knn_file_name.rstrip('.csv')
                knn_query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, knn_file_name_prefix)

                ks = ks_map.get(knn_file_name)
                for k in ks:
                    knn_query_output_path = BMTREE_KNN_QUERY_OUTPUT_PATH.format(
                        data_file_prefix=data_file_prefix,
                        range_query_prefix=file_name_prefix,
                        bit_num=bit_num,
                        tree_depth=tree_depth,
                        sample_size=sample_size,
                        knn_query_prefix=knn_file_name_prefix,
                        k=k
                    )
                    execute_knn_query(k, knn_query_file, data_file, knn_query_output_path)

            for file_name in point_queries:
                point_file_name_prefix = file_name.rstrip('.csv')
                query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, point_file_name_prefix)
                point_query_output_path = BMTREE_POINT_QUERY_OUTPUT_PATH.format(
                    data_file_prefix=data_file_prefix,
                    range_query_prefix=file_name_prefix,
                    point_query_prefix=point_file_name_prefix,
                    bit_num=bit_num,
                    tree_depth=tree_depth,
                    sample_size=sample_size
                )
                execute_point_query(query_file, data_file, point_query_output_path)

            for file_name in insertions:
                insert_file_name_prefix = file_name.rstrip('.csv')
                query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, insert_file_name_prefix)
                insert_output_path = BMTREE_INSERT_OUTPUT_PATH.format(
                    data_file_prefix=data_file_prefix,
                    range_query_prefix=file_name_prefix,
                    insert_prefix=insert_file_name_prefix,
                    bit_num=bit_num,
                    tree_depth=tree_depth,
                    sample_size=sample_size
                )
                execute_insert(query_file, insert_output_path)

            for file_name in insert_points:
                insert_point_file_name_prefix = file_name.rstrip('.csv')
                query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, insert_point_file_name_prefix)
                insert_point_output_path = BMTREE_INSERT_POINT_OUTPUT_PATH.format(
                    data_file_prefix=data_file_prefix,
                    range_query_prefix=file_name_prefix,
                    insert_point_prefix=insert_point_file_name_prefix,
                    bit_num=bit_num,
                    tree_depth=tree_depth,
                    sample_size=sample_size
                )
                execute_insert_point(query_file, insert_point_output_path)

    except subprocess.CalledProcessError as e:
        logger.error(f"fail: {e}")
    
    finally:
        # clean up intermediate files
        cleanup_intermediate_files()
        safe_remove(BMTREE_OUTPUT)

def run_rtree(data_file_name, point_queries, range_queries, knn_queries, ks_map, insertions, insert_points, baseline_config):

    global logger
    logger.info(f"run_rtree: data_file_name:{data_file_name} baseline_config:{baseline_config}")
    try:
        if data_file_name.startswith("data"):
            ablosute_data_file_name = os.path.join(SYNTHETIC_DATA_PATH, data_file_name)
        else:
            ablosute_data_file_name = os.path.join(REAL_DATA_PATH, data_file_name)
        data_file_prefix = data_file_name.rstrip('.csv')

        page_size = baseline_config.get("page_size", 100)
        fill_factor = baseline_config.get("fill_factor", 0.4)
        rtree_variant = baseline_config.get("rtree_variant", "quadratic")
        data_file = RTREE_DATA

        format_data_command = f"python tools/libspatialindex_data_adapter.py --type data --input {ablosute_data_file_name} --output {data_file}"
        execute_command(format_data_command)

        logger.info(f"Start building rtree ({rtree_variant}): {data_file}")
        
        command = f"test-rtree-RTreeLoad {data_file} tree {page_size} {fill_factor} {rtree_variant} {PAGE_SIZE} {BUFFER}"

        result, elapsed_time_ns_build = execute_command_with_err(command)

        build_output_path = RTREE_BUILD_OUTPUT_PATH.format(
            data_file_prefix=data_file_prefix,
            variant=rtree_variant
        )
                
        os.makedirs(os.path.dirname(build_output_path), exist_ok=True)

        with open(build_output_path, "w") as f:
            f.write(result.stderr)
            f.write(f"Elapsed Time: {elapsed_time_ns_build}\n")

        for file_name in range_queries:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            range_query_output_path = RTREE_RANGE_QUERY_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                range_query_prefix=file_name_prefix,
                variant=rtree_variant
            )
            execute_range_query(data_file, query_file, range_query_output_path)

        for file_name in knn_queries:
            ks = ks_map.get(file_name)
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            for k in ks:
                knn_query_output_path = RTREE_KNN_QUERY_OUTPUT_PATH.format(
                    data_file_prefix=data_file_prefix,
                    knn_query_prefix=file_name_prefix,
                    k=k,
                    variant=rtree_variant
                )
                execute_knn_query(k, query_file, data_file, knn_query_output_path)

        for file_name in point_queries:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            point_query_output_path = RTREE_POINT_QUERY_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                point_query_prefix=file_name_prefix,
                variant=rtree_variant
            )
            execute_point_query(query_file, data_file, point_query_output_path)

        for file_name in insertions:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            insert_output_path = RTREE_INSERT_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                insert_prefix=file_name_prefix,
                variant=rtree_variant
            )
            execute_insert(query_file, insert_output_path)

        for file_name in insert_points:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            insert_point_output_path = RTREE_INSERT_POINT_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                insert_point_prefix=file_name_prefix,
                variant=rtree_variant
            )
            execute_insert_point(query_file, insert_point_output_path)

    except subprocess.CalledProcessError as e:
        logger.error(f"fail: {e}")
    finally:
        # clean up intermediate files
        cleanup_intermediate_files()
        safe_remove(RTREE_DATA)

def run_rstartree(data_file_name, point_queries, range_queries, knn_queries, ks_map, insertions, insert_points, baseline_config):
    
    global logger
    logger.info(f"run_rstartree: data_file_name:{data_file_name} baseline_config:{baseline_config}")

    try:
        if data_file_name.startswith("data"):
            ablosute_data_file_name = os.path.join(SYNTHETIC_DATA_PATH, data_file_name)
        else:
            ablosute_data_file_name = os.path.join(REAL_DATA_PATH, data_file_name)
        data_file_prefix = data_file_name.rstrip('.csv')

        page_size = baseline_config.get("page_size", 100)
        fill_factor = baseline_config.get("fill_factor", 0.4)
        
        rtree_variant = baseline_config.get("rtree_variant", "rstar")
        data_file = R_STAR_TREE_DATA

        format_data_command = f"python tools/libspatialindex_data_adapter.py --type data --input {ablosute_data_file_name} --output {data_file}"
        execute_command(format_data_command)

        logger.info(f"Start building rstartree ({rtree_variant}): {data_file}")
        
        command = f"test-rtree-RTreeLoad {data_file} tree {page_size} {fill_factor} {rtree_variant} {PAGE_SIZE} {BUFFER}"

        result, elapsed_time_ns_build = execute_command_with_err(command)

        build_output_path = R_STAR_TREE_BUILD_OUTPUT_PATH.format(
            data_file_prefix=data_file_prefix,
            variant=rtree_variant
        )

        os.makedirs(os.path.dirname(build_output_path), exist_ok=True)

        with open(build_output_path, "w") as f:
            f.write(result.stderr)
            f.write(f"Elapsed Time: {elapsed_time_ns_build}\n")

        for file_name in range_queries:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            range_query_output_path = R_STAR_TREE_RANGE_QUERY_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                range_query_prefix=file_name_prefix,
                variant=rtree_variant
            )
            execute_range_query(data_file, query_file, range_query_output_path)

        for file_name in knn_queries:
            ks = ks_map.get(file_name)
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            for k in ks:
                knn_query_output_path = R_STAR_TREE_KNN_QUERY_OUTPUT_PATH.format(
                    data_file_prefix=data_file_prefix,
                    knn_query_prefix=file_name_prefix,
                    k=k,
                    variant=rtree_variant
                )
                execute_knn_query(k, query_file, data_file, knn_query_output_path)

        for file_name in point_queries:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            point_query_output_path = R_STAR_TREE_POINT_QUERY_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                point_query_prefix=file_name_prefix,
                variant=rtree_variant
            )
            execute_point_query(query_file, data_file, point_query_output_path)

        for file_name in insertions:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            insert_output_path = R_STAR_TREE_INSERT_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                insert_prefix=file_name_prefix,
                variant=rtree_variant
            )
            execute_insert(query_file, insert_output_path)

        for file_name in insert_points:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            insert_point_output_path = R_STAR_TREE_INSERT_POINT_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                insert_point_prefix=file_name_prefix,
                variant=rtree_variant
            )
            execute_insert_point(query_file, insert_point_output_path)

    except subprocess.CalledProcessError as e:
        logger.error(f"fail: {e}")
    finally:
        # clean up intermediate files
        cleanup_intermediate_files()
        safe_remove(RTREE_DATA)

def run_rlrtree(data_file_name, point_queries, range_queries, knn_queries, ks_map, insertions, insert_points, baseline_config):

    global logger
    logger.info(f"run_rlrtree: data_file_name:{data_file_name} baseline_config:{baseline_config}")

    try:
        is_real_data = data_file_name.startswith("data")
        if is_real_data:
            ablosute_data_file_name = os.path.join(SYNTHETIC_DATA_PATH, data_file_name)
        else:
            ablosute_data_file_name = os.path.join(REAL_DATA_PATH, data_file_name)
        data_file_prefix = data_file_name.rstrip('.csv')

        page_size = baseline_config.get("page_size", 100)
        fill_factor = baseline_config.get("fill_factor", 0.4)
        epoch = baseline_config.get("epoch", 10)
        rtree_variant = baseline_config.get("rtree_variant", "rlrtree")
        sample_size = baseline_config.get("sample_size", 10000)
        model_path = baseline_config.get("model_path", RLRTREE_MODEL_PATH)

        data_file = RLRTREE_DATA

        format_data_command = f"python tools/libspatialindex_data_adapter.py --type data --input {ablosute_data_file_name} --output {data_file}"
        execute_command(format_data_command)

        for range_file_name in range_queries:

            file_name_prefix = range_file_name.rstrip('.csv')
            
            if is_real_data:
                ablosute_query_file_name = f"data/synthetic/query/{range_file_name}"
            else:
                ablosute_query_file_name = f"data/real/query/{range_file_name}"

            logger.info("Prepare RLRTree")
            
            # data_transfer_command = f"cp {ablosute_data_file_name} {ablosute_query_file_name}"
            # execute_command(data_transfer_command)

            learn_rlrtree_command = f"bash rl_baseline/learn_rlrtree.sh {ablosute_data_file_name} {ablosute_query_file_name} {epoch} {sample_size}"
            elapsed_time_ns_learn = execute_command(learn_rlrtree_command)

            command = f"test-rtree-RTreeLoad {data_file} tree {page_size} {fill_factor} {rtree_variant} {model_path} {PAGE_SIZE} {BUFFER}"
            result, elapsed_time_ns_build = execute_command_with_err(command)

            build_output_path = RLRTREE_BUILD_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                variant=rtree_variant,
                epoch=epoch,
            )

            os.makedirs(os.path.dirname(build_output_path), exist_ok=True)

            with open(build_output_path, "w") as f:
                f.write(result.stderr)
                f.write(f"Elapsed Learn Time: {elapsed_time_ns_learn}\n")
                f.write(f"Elapsed Build Time: {elapsed_time_ns_build}\n")

            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            range_query_output_path = RLRTREE_RANGE_QUERY_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                range_query_prefix=file_name_prefix,
                variant=rtree_variant,
                epoch=epoch,
            )
            execute_range_query(data_file, query_file, range_query_output_path)

            for file_name in knn_queries:
                ks = ks_map.get(file_name)
                knn_file_name_prefix = file_name.rstrip('.csv')
                knn_query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, knn_file_name_prefix)
                for k in ks:
                    knn_query_output_path = RLRTREE_KNN_QUERY_OUTPUT_PATH.format(
                        data_file_prefix=data_file_prefix,
                        range_query_prefix=file_name_prefix,
                        knn_query_prefix=knn_file_name_prefix,
                        epoch=epoch,
                        k=k,
                        variant=rtree_variant
                    )
                    execute_knn_query(k, knn_query_file, data_file, knn_query_output_path)

            for file_name in point_queries:
                point_file_name_prefix = file_name.rstrip('.csv')
                query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, point_file_name_prefix)
                point_query_output_path = RLRTREE_POINT_QUERY_OUTPUT_PATH.format(
                    data_file_prefix=data_file_prefix,
                    range_query_prefix=file_name_prefix,
                    point_query_prefix=point_file_name_prefix,
                    epoch=epoch,
                    variant=rtree_variant
                )
                execute_point_query(query_file, data_file, point_query_output_path)

            for file_name in insertions:
                insert_file_name_prefix = file_name.rstrip('.csv')
                query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, insert_file_name_prefix)
                insert_output_path = RLRTREE_INSERT_OUTPUT_PATH.format(
                    data_file_prefix=data_file_prefix,
                    range_query_prefix=file_name_prefix,
                    insert_prefix=insert_file_name_prefix,
                    epoch=epoch,
                    variant=rtree_variant
                )
                execute_insert(query_file, insert_output_path)

            for file_name in insert_points:
                insert_point_file_name_prefix = file_name.rstrip('.csv')
                query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, insert_point_file_name_prefix)
                insert_point_output_path = RLRTREE_INSERT_POINT_OUTPUT_PATH.format(
                    data_file_prefix=data_file_prefix,
                    range_query_prefix=file_name_prefix,
                    insert_point_prefix=insert_point_file_name_prefix,
                    epoch=epoch,
                    variant=rtree_variant
                )
                execute_insert_point(query_file, insert_point_output_path)


    except subprocess.CalledProcessError as e:
        logger.error(f"fail: {e}")
    
    finally:
        # clean up intermediate files
        cleanup_intermediate_files()
        safe_remove(RLRTREE_DATA)

def run_kdtree(data_file_name, point_queries, range_queries, knn_queries, ks_map, insertions, insert_points, baseline_config):

    global logger
    logger.info(f"run_kdtree: data_file_name:{data_file_name} baseline_config:{baseline_config}")

    try:
        if data_file_name.startswith("data"):
            ablosute_data_file_name = os.path.join(SYNTHETIC_DATA_PATH, data_file_name)
        else:
            ablosute_data_file_name = os.path.join(REAL_DATA_PATH, data_file_name)
        data_file_prefix = data_file_name.rstrip('.csv')

        page_size = baseline_config.get("page_size", 100)
        # fill_factor = baseline_config.get("fill_factor", None)
        # rtree_variant = baseline_config.get("rtree_variant", None)
        data_file = KDTREE_DATA

        format_data_command = f"python tools/libspatialindex_data_adapter.py --type data --input {ablosute_data_file_name} --output {data_file}"
        execute_command(format_data_command)

        logger.info(f"Start building kdtree: {data_file}")
        
        # The second parameter path is not used and 1.0 is also not used. They are for greedy kdtree. 
        # Here, they are placeholders.
        command = f"test-kdtree-KDTreeBulkLoad kdtree {data_file} path tree {page_size} 1.0 {PAGE_SIZE} {BUFFER}"  

        logger.info(f"Start building kdtree: {command}")

        result, elapsed_time_ns_build = execute_command_with_err(command)

        build_output_path = KDTREE_BUILD_OUTPUT_PATH.format(
            data_file_prefix=data_file_prefix
        )

        os.makedirs(os.path.dirname(build_output_path), exist_ok=True)

        with open(build_output_path, "w") as f:
            f.write(result.stderr)
            f.write(f"Elapsed Time: {elapsed_time_ns_build}\n")

        for file_name in range_queries:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            range_query_output_path = KDTREE_RANGE_QUERY_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                range_query_prefix=file_name_prefix
            )
            execute_range_query(data_file, query_file, range_query_output_path, "test-kdtree-KDTreeQuery")


        for file_name in knn_queries:
            ks = ks_map.get(file_name)
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            for k in ks:
                knn_query_output_path = KDTREE_KNN_QUERY_OUTPUT_PATH.format(
                    data_file_prefix=data_file_prefix,
                    knn_query_prefix=file_name_prefix,
                    k=k
                )
                execute_knn_query(k, query_file, data_file, knn_query_output_path, "test-kdtree-KDTreeQuery")

        for file_name in point_queries:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            point_query_output_path = KDTREE_POINT_QUERY_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                point_query_prefix=file_name_prefix,
            )
            execute_point_query(query_file, data_file, point_query_output_path, "test-kdtree-KDTreeQuery")

        for file_name in insertions:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            insert_output_path = KDTREE_INSERT_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                insert_prefix=file_name_prefix,
            )
            execute_insert(query_file, insert_output_path, "test-kdtree-KDTreeQuery")

        for file_name in insertions:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            insert_point_output_path = KDTREE_INSERT_POINT_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                insert_point_prefix=file_name_prefix,
            )
            execute_insert_point(query_file, insert_point_output_path, "test-kdtree-KDTreeQuery")

    except subprocess.CalledProcessError as e:
        logger.error(f"fail: {e}")
    
    finally:
        # clean up intermediate files
        cleanup_intermediate_files()
        safe_remove(KDTREE_DATA)


def run_kdtree_greedy(data_file_name, point_queries, range_queries, knn_queries, ks_map, insertions, insert_points, baseline_config):
    
    global logger
    logger.info(f"run_kdtree_greedy: data_file_name:{data_file_name} baseline_config:{baseline_config}")
    try:
        is_real_data = data_file_name.startswith("data")
        if is_real_data:
            ablosute_data_file_name = os.path.join(SYNTHETIC_DATA_PATH, data_file_name)
        else:
            ablosute_data_file_name = os.path.join(REAL_DATA_PATH, data_file_name)
        data_file_prefix = data_file_name.rstrip('.csv')

        page_size = baseline_config.get("page_size", 100)
        data_file = KDTREE_GREEDY_DATA

        format_data_command = f"python tools/libspatialindex_data_adapter.py --type data --input {ablosute_data_file_name} --output {data_file}"
        execute_command(format_data_command)

        for range_file_name in range_queries:

            file_name_prefix = range_file_name.rstrip('.csv')

            logger.info(f"Start building greedy_kdtree: {data_file}")
            
            # query_adapter_command = f"python tools/libspatialindex_data_adapter.py --type range --input {ablosute_query_file_name} --output {KDTREE_GREEDY_QUERY}"
            # execute_command(query_adapter_command)

            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)

            command = f"test-kdtree-KDTreeBulkLoad greedy_kdtree {data_file} {query_file} tree {page_size} 1.0 {PAGE_SIZE} {BUFFER}"  

            logger.info(f"Start building kdtree: {command}")

            result, elapsed_time_ns_build = execute_command_with_err(command)

            build_output_path = KDTREE_GREEDY_BUILD_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                range_query_prefix=file_name_prefix
            )

            os.makedirs(os.path.dirname(build_output_path), exist_ok=True)

            with open(build_output_path, "w") as f:
                f.write(result.stderr)
                f.write(f"Elapsed Time: {elapsed_time_ns_build}\n")

            range_query_output_path = KDTREE_GREEDY_RANGE_QUERY_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                range_query_prefix=file_name_prefix
            )
            execute_range_query(data_file, query_file, range_query_output_path, "test-kdtree-KDTreeQuery")

            for file_name in knn_queries:
                ks = ks_map.get(file_name)
                knn_file_name_prefix = file_name.rstrip('.csv')
                query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, knn_file_name_prefix)
                for k in ks:
                    knn_query_output_path = KDTREE_GREEDY_KNN_QUERY_OUTPUT_PATH.format(
                        data_file_prefix=data_file_prefix,
                        range_query_prefix=file_name_prefix,
                        knn_query_prefix=knn_file_name_prefix,
                        k=k
                    )
                    execute_knn_query(k, query_file, data_file, knn_query_output_path, "test-kdtree-KDTreeQuery")

            for file_name in point_queries:
                point_file_name_prefix = file_name.rstrip('.csv')
                query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, point_file_name_prefix)
                point_query_output_path = KDTREE_GREEDY_POINT_QUERY_OUTPUT_PATH.format(
                    data_file_prefix=data_file_prefix,
                    range_query_prefix=file_name_prefix,
                    point_query_prefix=point_file_name_prefix,
                )
                execute_point_query(query_file, data_file, point_query_output_path, "test-kdtree-KDTreeQuery")

            for file_name in insertions:
                insert_file_name_prefix = file_name.rstrip('.csv')
                query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, insert_file_name_prefix)
                insert_output_path = KDTREE_GREEDY_INSERT_OUTPUT_PATH.format(
                    data_file_prefix=data_file_prefix,
                    range_query_prefix=file_name_prefix,
                    insert_prefix=insert_file_name_prefix,
                )
                execute_insert(query_file, insert_output_path, "test-kdtree-KDTreeQuery")

            for file_name in insert_points:
                insert_point_file_name_prefix = file_name.rstrip('.csv')
                query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, insert_point_file_name_prefix)
                insert_point_output_path = KDTREE_GREEDY_INSERT_POINT_OUTPUT_PATH.format(
                    data_file_prefix=data_file_prefix,
                    range_query_prefix=file_name_prefix,
                    insert_point_prefix=insert_file_name_prefix,
                )
                execute_insert_point(query_file, insert_point_output_path, "test-kdtree-KDTreeQuery")

    except subprocess.CalledProcessError as e:
        logger.info(f"fail: {e}")
    
    finally:
        # clean up intermediate files
        cleanup_intermediate_files()
        safe_remove(KDTREE_GREEDY_DATA)
        # save_remove(KDTREE_GREEDY_QUERY)


def run_qdtree_rl(data_file_name, point_queries, range_queries, knn_queries, ks_map, insertions, insert_points, baseline_config):
    
    global logger
    logger.info(f"run_qdtree_rl: data_file_name:{data_file_name} baseline_config:{baseline_config}")
    try:
        is_real_data = data_file_name.startswith("data")
        if is_real_data:
            ablosute_data_file_name = os.path.join(SYNTHETIC_DATA_PATH, data_file_name)
        else:
            ablosute_data_file_name = os.path.join(REAL_DATA_PATH, data_file_name)
        data_file_prefix = data_file_name.rstrip('.csv')

        page_size = baseline_config.get("page_size", 100)
        episode = baseline_config.get("episode", 10)
        sampling_ratio = baseline_config.get("sampling_ratio", 0.01)
        model_path = baseline_config.get("model_path", QDTREE_MODEL_PATH)
        action_sampling_size = baseline_config.get("action_sampling_size", None)
        data_file = QDTREE_DATA

        format_data_command = f"python tools/libspatialindex_data_adapter.py --type data --input {ablosute_data_file_name} --output {data_file}"
        execute_command(format_data_command)

        for range_file_name in range_queries:

            file_name_prefix = range_file_name.rstrip('.csv')

            if is_real_data:
                ablosute_query_file_name = f"data/synthetic/query/{range_file_name}"
            else:
                ablosute_query_file_name = f"data/real/query/{range_file_name}"

            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)

            learn_qdtree_command = f"bash rl_baseline/learn_qdtree.sh {ablosute_data_file_name} {ablosute_query_file_name} {episode} {sampling_ratio} {action_sampling_size}"
            elapsed_time_ns_learn = execute_command(learn_qdtree_command)

            logger.info(f"Start building qdtree: {data_file}")
            
            command = f"test-kdtree-QDTreeBulkLoad qdtree {data_file} {query_file} tree {page_size} 1.0 {model_path} {action_sampling_size} {PAGE_SIZE} {BUFFER}"  

            logger.info(f"Start building qdtree: {command}")

            result, elapsed_time_ns_build = execute_command_with_err(command)

            build_output_path = QDTREE_BUILD_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                range_query_prefix=file_name_prefix,
                episode=episode,
                sampling_ratio=sampling_ratio,
                action_sampling_size=action_sampling_size,
            )

            os.makedirs(os.path.dirname(build_output_path), exist_ok=True)

            with open(build_output_path, "w") as f:
                f.write(result.stderr)
                f.write(f"Elapsed Learn Time: {elapsed_time_ns_learn}\n")
                f.write(f"Elapsed Build Time: {elapsed_time_ns_build}\n")

            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)

            range_query_output_path = QDTREE_RANGE_QUERY_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                range_query_prefix=file_name_prefix,
                episode=episode,
                sampling_ratio=sampling_ratio,
                action_sampling_size=action_sampling_size,
            )
            execute_range_query(data_file, query_file, range_query_output_path, "test-kdtree-KDTreeQuery")

            for file_name in knn_queries:
                ks = ks_map.get(file_name)
                knn_file_name_prefix = file_name.rstrip('.csv')
                query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, knn_file_name_prefix)
                for k in ks:
                    knn_query_output_path = QDTREE_KNN_QUERY_OUTPUT_PATH.format(
                        data_file_prefix=data_file_prefix,
                        range_query_prefix=file_name_prefix,
                        knn_query_prefix=knn_file_name_prefix,
                        episode=episode,
                        sampling_ratio=sampling_ratio,
                        action_sampling_size=action_sampling_size,
                        k=k
                    )
                    execute_knn_query(k, query_file, data_file, knn_query_output_path, "test-kdtree-KDTreeQuery")

            for file_name in point_queries:
                point_file_name_prefix = file_name.rstrip('.csv')
                query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, point_file_name_prefix)
                point_query_output_path = QDTREE_POINT_QUERY_OUTPUT_PATH.format(
                    data_file_prefix=data_file_prefix,
                    range_query_prefix=file_name_prefix,
                    point_query_prefix=point_file_name_prefix,
                    episode=episode,
                    sampling_ratio=sampling_ratio,
                    action_sampling_size=action_sampling_size,
                )
                execute_point_query(query_file, data_file, point_query_output_path, "test-kdtree-KDTreeQuery")

            for file_name in insertions:
                insert_file_name_prefix = file_name.rstrip('.csv')
                query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, insert_file_name_prefix)
                insert_output_path = QDTREE_INSERT_OUTPUT_PATH.format(
                    data_file_prefix=data_file_prefix,
                    range_query_prefix=file_name_prefix,
                    insert_prefix=insert_file_name_prefix,
                    episode=episode,
                    sampling_ratio=sampling_ratio,
                    action_sampling_size=action_sampling_size,
                )
                execute_insert(query_file, insert_output_path, "test-kdtree-KDTreeQuery")

            for file_name in insert_points:
                insert_point_file_name_prefix = file_name.rstrip('.csv')
                query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, insert_point_file_name_prefix)
                insert_point_output_path = QDTREE_INSERT_POINT_OUTPUT_PATH.format(
                    data_file_prefix=data_file_prefix,
                    range_query_prefix=file_name_prefix,
                    insert_point_prefix=insert_file_name_prefix,
                    episode=episode,
                    sampling_ratio=sampling_ratio,
                    action_sampling_size=action_sampling_size,
                )
                execute_insert_point(query_file, insert_point_output_path, "test-kdtree-KDTreeQuery")

    except subprocess.CalledProcessError as e:
        logger.error(f"fail: {e}")
    
    finally:
        # clean up intermediate files
        cleanup_intermediate_files()
        safe_remove(QDTREE_DATA)
        # save_remove(QDTREE_QUERY)


def process_experiment(experiment):

    global logger

    range_queries = []
    knn_queries = []
    point_queries = []
    insertions = []
    insert_points = []
    ks_map = {}
    # Data Section
    data_size = experiment['data'].get('size', '')
    data_dimensions = experiment['data'].get('dimensions', '')
    data_distribution = experiment['data'].get('distribution', '')
    data_skewness = experiment['data'].get('skewness', '')
    data_bounds = experiment['data'].get('bounds', [[]])
    data_bounds_params = ' '.join([f"--range {' '.join(map(str, bound))}" for bound in data_bounds])

    logger.info(f"data distribution: {data_distribution}")

    is_real_data = True

    if data_distribution in ["uniform", "normal", "skewed"]:

        is_real_data = False

        data_file_name = SYNTHETIC_DATA_FILENAME_TEMPLATE.format(
            size=data_size,
            dimensions=data_dimensions,
            distribution=data_distribution,
            skewness=data_skewness
        )

        if os.path.exists(os.path.join(SYNTHETIC_DATA_PATH, data_file_name)):
            logger.info(f"File {data_file_name} already exists. Skipping command execution.")
        else:
            data_command = f"python tools/synthetic_data_generator.py --size {data_size} --dimensions {data_dimensions} --distribution {data_distribution} --skewness {data_skewness} {data_bounds_params}"
            logger.info(data_command)
            execute_command(data_command)

        # Workloads Section:
        for workload in experiment['workloads']:

            with open(os.path.join(SYNTHETIC_WORKLOAD_PATH, workload), "r") as json_file:
                workload = json.load(json_file)

                # Operation Section
                for query in workload['operations']:
                    query_type = query['type']
                    query_size = query['size']
                    query_dimensions = query['dimensions']
                    query_distribution = query['distribution']
                    query_skewness = query.get('skewness', 1)
                    frequency = query.get('frequency', [1])
                    query_bounds_params = ' '.join([f"--bounds {' '.join(map(str, bound))}" for bound in query['bounds']])
                    
                    if query_type == "range":

                        query_ranges = query['query_range']

                        for query_range in query_ranges:

                            query_range_params = ' '.join([str(val) for val in query_range])
                            range_str = "x".join([str(_) for _ in query_range])

                            file_name = RANGE_QUERY_FILENAME_TEMPLATE.format(
                                query_type=query_type,
                                n_queries=query_size,
                                dimensions=query_dimensions,
                                distribution=query_distribution,
                                skewness=query_skewness,
                                range_str=range_str
                            )

                            range_queries.append(file_name)
                                            
                            if os.path.exists(os.path.join(SYNTHETIC_QUERY_PATH, file_name)):
                                logger.info(f"File {file_name} already exists. Skipping command execution.")
                            else:
                                query_command = f"python tools/synthetic_query_generator.py --query_type {query_type} --n_queries {query_size} --dimensions {query_dimensions} --distribution {query_distribution} --skewness {query_skewness} {query_bounds_params} --query_range {query_range_params}"
                                execute_command(query_command)

                    elif query_type == "knn":
                        ks = [int(k) for k in query['k']]

                        file_name = KNN_QUERY_FILENAME_TEMPLATE.format(
                            query_type=query_type,
                            n_queries=query_size,
                            dimensions=query_dimensions,
                            distribution=query_distribution,
                            skewness=query_skewness
                        )

                        knn_queries.append(file_name)
                        ks_map[file_name] = ks

                        if os.path.exists(os.path.join(SYNTHETIC_QUERY_PATH, file_name)):
                            logger.info(f"File {file_name} already exists. Skipping command execution.")
                        else:
                            query_command = f"python tools/synthetic_query_generator.py --query_type {query_type} --n_queries {query_size} --dimensions {query_dimensions} --distribution {query_distribution} --skewness {query_skewness} {query_bounds_params}"
                            execute_command(query_command)

                    elif query_type == "point":
                        base_name, extension = os.path.splitext(os.path.basename(data_file_name))
                        file_name = POINT_QUERY_FILENAME_TEMPLATE.format(
                            query_type=query_type,
                            n_queries=query_size,
                            data=base_name,
                            dimensions=query_dimensions,
                            distribution=query_distribution,
                            skewness=query_skewness
                        )
                        point_queries.append(file_name)

                        if os.path.exists(os.path.join(SYNTHETIC_QUERY_PATH, file_name)):
                            logger.info(f"File {file_name} already exists. Skipping command execution.")
                        else:
                            if os.path.exists(os.path.join(SYNTHETIC_DATA_PATH, data_file_name)):
                                query_command = f"python tools/synthetic_query_generator.py --query_type {query_type} --n_queries {query_size} --dimensions {query_dimensions} --distribution {query_distribution} --skewness {query_skewness} --data_file_name {data_file_name}"
                                execute_command(query_command)
                            else:
                                raise ValueError(f"File {data_file_name} does not exist.")

                    elif query_type == "insert":
                        file_name = INSERT_FILENAME_TEMPLATE.format(
                            query_type=query_type,
                            n_queries=query_size,
                            dimensions=query_dimensions,
                            distribution=query_distribution,
                            skewness=query_skewness
                        )
                        insertions.append(file_name)

                        if os.path.exists(os.path.join(SYNTHETIC_QUERY_PATH, file_name)):
                            logger.info(f"File {file_name} already exists. Skipping command execution.")
                        else:
                            query_command = f"python tools/synthetic_query_generator.py --query_type {query_type} --n_queries {query_size} --dimensions {query_dimensions} --distribution {query_distribution} --skewness {query_skewness} {query_bounds_params}"
                            execute_command(query_command)
                    elif query_type == "insert_point":
                        base_name, extension = os.path.splitext(os.path.basename(data_file_name))
                        frequency_str = "_".join([str(_) for _ in frequency])
                        file_name = INSERT_POINT_FILENAME_TEMPLATE.format(
                            query_type=query_type,
                            n_queries=query_size,
                            data=base_name,
                            dimensions=query_dimensions,
                            distribution=query_distribution,
                            skewness=query_skewness,
                            frequency=frequency_str
                        )
                        insert_points.append(file_name)
                        if os.path.exists(os.path.join(SYNTHETIC_QUERY_PATH, file_name)):
                            logger.info(f"File {file_name} already exists. Skipping command execution.")
                        else:
                            if os.path.exists(os.path.join(SYNTHETIC_DATA_PATH, data_file_name)):
                                frequency_params = " ".join([str(_) for _ in frequency])
                                query_command = f"python tools/synthetic_query_generator.py --query_type {query_type} --n_queries {query_size} --dimensions {query_dimensions} --distribution {query_distribution} --skewness {query_skewness} --frequency {frequency_params} --data_file_name {data_file_name} {query_bounds_params}"
                                execute_command(query_command)
                            else:
                                raise ValueError(f"File {data_file_name} does not exist.")

    else:
        data_file_name = RELATIVE_REAL_DATA_FILENAME.format(
            data_distribution=data_distribution,
            data_size=data_size
        )

        absolute_data_file_name = os.path.join(REAL_DATA_PATH, data_file_name)
        if not os.path.exists(absolute_data_file_name):
            # copy to project data directory
            shutil.copy(os.path.join("/home/research/datasets/", data_file_name), absolute_data_file_name)

        base_name, extension = os.path.splitext(os.path.basename(absolute_data_file_name))

        # Workloads Section:
        for workload in experiment['workloads']:

            with open(os.path.join(REAL_WORKLOAD_PATH, workload), "r") as json_file:
                workload = json.load(json_file)
                # Queries Section
                for query in workload['operations']:
                    query_type = query['type']
                    query_size = query['size']
                    query_dimensions = query['dimensions']
                    query_distribution = query['distribution']
                    query_skewness = query.get('skewness', '')
                    frequency = query.get('frequency', [1])

                    if query_type == "range":

                        query_ranges = query['query_range']

                        for query_range in query_ranges:

                            query_range_params = ' '.join([str(val) for val in query_range])
                            range_str = "x".join([str(_) for _ in query_range])

                            file_name = REAL_RANGE_QUERY_FILENAME_TEMPLATE.format(
                                data=base_name,
                                query_type=query_type,
                                n_queries=query_size,
                                dimensions=query_dimensions,
                                distribution=query_distribution,
                                skewness=query_skewness,
                                range_str=range_str
                            )
                            
                            range_queries.append(file_name)

                            if os.path.exists(os.path.join(REAL_QUERY_PATH, file_name)):
                                logger.info(f"File {file_name} already exists. Skipping command execution.")
                            else:
                                query_command = f"python tools/real_query_generator.py --data {absolute_data_file_name} --query_type {query_type} --n_queries {query_size} --dimensions {query_dimensions} --distribution {query_distribution} --skewness {query_skewness} --query_range {query_range_params}"
                                execute_command(query_command)

                    elif query_type == "knn":
                        ks = [int(k) for k in query['k']]

                        file_name = REAL_KNN_QUERY_FILENAME_TEMPLATE.format(
                            data=base_name,
                            query_type=query_type,
                            n_queries=query_size,
                            dimensions=query_dimensions,
                            distribution=query_distribution,
                            skewness=query_skewness
                        )

                        knn_queries.append(file_name)
                        ks_map[file_name] = ks

                        if os.path.exists(os.path.join(REAL_QUERY_PATH, file_name)):
                            logger.info(f"File {file_name} already exists. Skipping command execution.")
                        else:
                            if os.path.exists(absolute_data_file_name):
                                query_command = f"python tools/real_query_generator.py --data {absolute_data_file_name} --query_type {query_type} --n_queries {query_size} --dimensions {query_dimensions} --distribution {query_distribution} --skewness {query_skewness}"
                                execute_command(query_command)
                            else:
                                raise ValueError(f"File {absolute_data_file_name} does not exist.")
                    
                    elif query_type == "point":
                        file_name = REAL_POINT_QUERY_FILENAME_TEMPLATE.format(
                            data=base_name,
                            query_type=query_type,
                            n_queries=query_size,
                            dimensions=query_dimensions,
                            distribution=query_distribution,
                            skewness=query_skewness
                        )
                        point_queries.append(file_name)

                        if os.path.exists(os.path.join(REAL_QUERY_PATH, file_name)):
                            logger.info(f"File {file_name} already exists. Skipping command execution.")
                        else:
                            if os.path.exists(absolute_data_file_name):
                                query_command = f"python tools/real_query_generator.py --data {absolute_data_file_name} --query_type {query_type} --n_queries {query_size} --dimensions {query_dimensions} --distribution {query_distribution} --skewness {query_skewness}"
                                execute_command(query_command)
                            else:
                                raise ValueError(f"File {data_file_name} does not exist.")

                    elif query_type == "insert":
                        file_name = REAL_INSERT_FILENAME_TEMPLATE.format(
                            data=base_name,
                            query_type=query_type,
                            n_queries=query_size,
                            dimensions=query_dimensions,
                            distribution=query_distribution,
                            skewness=query_skewness
                        )
                        insertions.append(file_name)

                        if os.path.exists(os.path.join(REAL_QUERY_PATH, file_name)):
                            logger.info(f"File {file_name} already exists. Skipping command execution.")
                        else:
                            if os.path.exists(absolute_data_file_name):
                                query_command = f"python tools/real_query_generator.py --data {absolute_data_file_name} --query_type {query_type} --n_queries {query_size} --dimensions {query_dimensions} --distribution {query_distribution} --skewness {query_skewness}"
                                execute_command(query_command)
                            else:
                                raise ValueError(f"File {data_file_name} does not exist.")
                            
                    elif query_type == "insert_point":
                        frequency_str = "_".join([str(_) for _ in frequency])
                        file_name = REAL_INSERT_POINT_FILENAME_TEMPLATE.format(
                            data=base_name,
                            query_type=query_type,
                            n_queries=query_size,
                            dimensions=query_dimensions,
                            distribution=query_distribution,
                            skewness=query_skewness,
                            frequency=frequency_str
                        )
                        insert_points.append(file_name)

                        if os.path.exists(os.path.join(REAL_QUERY_PATH, file_name)):
                            logger.info(f"File {file_name} already exists. Skipping command execution.")
                        else:
                            if os.path.exists(absolute_data_file_name):
                                frequency_params = " ".join([str(_) for _ in frequency])
                                query_command = f"python tools/real_query_generator.py --data {absolute_data_file_name} --query_type {query_type} --n_queries {query_size} --dimensions {query_dimensions} --distribution {query_distribution} --skewness {query_skewness} --frequency {frequency_params}"
                                execute_command(query_command)
                            else:
                                raise ValueError(f"File {data_file_name} does not exist.")
             

    query_path = REAL_QUERY_PATH if is_real_data else SYNTHETIC_QUERY_PATH

    query_maps = {"range_query": range_queries, "knn_query": knn_queries, "point_query": point_queries
                  , "insert": insertions, "insert_point": insert_points}
    
    for query_type, file_names in query_maps.items():
        for file_name in file_names:
            file_name_prefix = file_name.rstrip('.csv')
            file_name = os.path.join(query_path, file_name)

            logger.info(f"File: {file_name}")
            
            if os.path.exists(os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)):
                logger.info(f"File {file_name_prefix} already exists. Skipping command execution.")
            else:
                format_query_command = f"python tools/libspatialindex_data_adapter.py --type {query_type} --input {file_name} --output {BENCHMARK_LIBSPATIALINDEX}/{file_name_prefix}"
                execute_command(format_query_command)

    # Baselines Section
    for baseline in experiment['baseline']:
        baseline_name = baseline['name']
        # config of a specific baseline
        baseline_config = baseline["config"]

        logger.info(f"-----------------Baseline name: {baseline_name}-----------------")
        logger.info(f"-----------------Baseline config: {baseline_config}-----------------")

        if baseline_name == "zorder":
            run_zorder(data_file_name, point_queries, range_queries, knn_queries, ks_map, insertions, insert_points, baseline_config)
        elif baseline_name == "bmtree":
            run_bmtree(data_file_name, point_queries, range_queries, knn_queries, ks_map, insertions, insert_points, baseline_config)
        elif baseline_name == "rankspace":
            run_rankspace(data_file_name, point_queries, range_queries, knn_queries, ks_map, insertions, insert_points, baseline_config)
        elif baseline_name == "rtree":
            run_rtree(data_file_name, point_queries, range_queries, knn_queries, ks_map, insertions, insert_points, baseline_config)
        elif baseline_name == "rstar":
            run_rstartree(data_file_name, point_queries, range_queries, knn_queries, ks_map, insertions, insert_points, baseline_config)
        elif baseline_name == "rlrtree":
            run_rlrtree(data_file_name, point_queries, range_queries, knn_queries, ks_map, insertions, insert_points, baseline_config)
        elif baseline_name == "kdtree":
            run_kdtree(data_file_name, point_queries, range_queries, knn_queries, ks_map, insertions, insert_points, baseline_config)
        elif baseline_name == "kdgreedy":
            run_kdtree_greedy(data_file_name, point_queries, range_queries, knn_queries, ks_map, insertions, insert_points, baseline_config)
        elif baseline_name == "qdtree":
            run_qdtree_rl(data_file_name, point_queries, range_queries, knn_queries, ks_map, insertions, insert_points, baseline_config)
       

def remove_and_create_directory(directory_path):

    global logger
    logger.info(f"remove_and_create_directory: {directory_path}")
    try:
        shutil.rmtree(directory_path)
    except FileNotFoundError:
        pass
    os.makedirs(directory_path)

def main():

    global logger
    configs = []
    if RUN_EXAMPLE:
        if RUN_ALL_BASELINE_EXAMPLE:
            configs = ["example_config_all_baselines.json"]
        else:
            # configs = ["example_config.json"]
            configs = ["verify_qdtree.json"]
    else:
        directory = CONFIG_DIR
        # candidates = ["overall"]
        candidates = ["point_range_knn_queries", "write_only", "write_heavy_only"]
        for root, dirs, files in os.walk(directory):
            if root.split("/")[-1] not in candidates:
                continue
            for file in files:
                if file.endswith(".json"):
                    config_file_path = os.path.join(root, file)
                    configs.append(config_file_path)
                    # print(config_file_path)
    
    counter = 0

    for config_file_path in configs:
        with open(config_file_path, "r") as json_file:
            config = json.load(json_file)
        
        logger = setup_logger(config_file_path)

        logger.info(f"-----------------Run config {config_file_path}-----------------")

        for experiment in config['experiments']:
            counter += 1
            logger.info(f"-----------------Processing experiment #{counter}-----------------")
            process_experiment(experiment)
            logger.info(f"-----------------Finish experiment #{counter}-----------------")

            if SAVE_SPACE:
                remove_and_create_directory(SYNTHETIC_PATH)
                remove_and_create_directory(BENCHMARK_LIBSPATIALINDEX)

        logger.info(f"-----------------Finish config {config_file_path}-----------------")
        
def setup_logger(config_file_path):
    log_filename = f'./log/{config_file_path.rsplit(".", 1)[0].replace("/", "_")}.log'
    
    logger = logging.getLogger(config_file_path)
    logger.setLevel(logging.INFO)

    if logger.hasHandlers():
        logger.handlers.clear()
    
    file_handler = logging.FileHandler(log_filename, mode='w')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)

    return logger

if __name__ == "__main__":
    main()