import json
import logging
import os
import shutil
import subprocess
import time

logger = None
is_range_query = True

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
        safe_remove("./benchmark/a")
        safe_remove("./benchmark/b")
        safe_remove("./benchmark/.t")
        safe_remove("./benchmark/res2")

    safe_remove("./benchmark/res")
    safe_remove('./benchmark/tree.dat')
    safe_remove('./benchmark/tree.idx')

    safe_remove('./benchmark/zorder.dat')
    safe_remove('./benchmark/zorder.idx')

    safe_remove('./benchmark/rtree.dat')
    safe_remove('./benchmark/rtree.idx')

    safe_remove('./benchmark/kdtree.dat')
    safe_remove('./benchmark/kdtree.idx')

    safe_remove('./benchmark/rankspace.dat')
    safe_remove('./benchmark/rankspace.idx')

    safe_remove('./benchmark/rstar.dat')
    safe_remove('./benchmark/rstar.idx')

    safe_remove('./benchmark/kdgreedy.dat')
    safe_remove('./benchmark/kdgreedy.idx')

    safe_remove('./benchmark/bmtree.dat')
    safe_remove('./benchmark/bmtree.idx')

    safe_remove('./benchmark/rlrtree.dat')
    safe_remove('./benchmark/rlrtree.idx')

    safe_remove('./benchmark/qdtree.dat')
    safe_remove('./benchmark/qdtree.idx')

    safe_remove(Z_ORDER_OUTPUT)
    safe_remove(RANK_SPACE_Z_ORDER_OUTPUT)
    safe_remove(BMTREE_INPUT)
    safe_remove(CHOOSE_SUBTREE_MODEL_NAME)
    safe_remove(SPLIT_MODEL_NAME)
    safe_remove(QDTREE_MODEL_NAME)

    logger.info(f"finish cleanup_intermediate_files")


def copy_and_rename(source_filename, new_filename):

    global logger
    logger.info(f"copy_and_rename: {source_filename} {new_filename}")
    # directory = os.path.dirname(source_filename)

    # destination_filename = os.path.join(directory, new_filename)

    shutil.copyfile(source_filename, new_filename)
    logger.info(f"finish copy_and_rename")


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
        subprocess.run("test-rtree-Exhaustive ./benchmark/.t intersection > ./benchmark/res2", shell=True, check=True)
    else:
        if k:
            subprocess.run(f"test-rtree-Exhaustive ./benchmark/.t {k}NN > ./benchmark/res2", shell=True, check=True)

    logger.info("Comparing results")
    subprocess.run("sort -n ./benchmark/res > ./benchmark/a", shell=True)
    subprocess.run("sort -n ./benchmark/res2 > ./benchmark/b", shell=True)

    diff_result = subprocess.run("diff a b", shell=True)
    if diff_result.returncode == 0:
        logger.info("Same results with exhaustive search. Everything seems fine.")
    else:
        logger.info("PROBLEM! We got different results from exhaustive search!")

    wc_result = subprocess.run("wc -l a", shell=True, capture_output=True, text=True)
    logger.info(f"Results: {wc_result.stdout}")


def execute_range_query(data_file, query_file, range_query_output_path, test_file="test-rtree-RTreeQuery", index_name="tree"):

    global logger

    logger.info(f"execute_range_query: data_file:{data_file} query_file:{query_file} range_query_output_path:{range_query_output_path} test_file:{test_file}")

    if RUN_EXHAUSTIVE_SEARCH:
        command = f"{test_file} {query_file} ./benchmark/{index_name} intersection {BUFFER} > ./benchmark/res"
    else:
        command = f"{test_file} {query_file} ./benchmark/{index_name} intersection {BUFFER}"

    logger.info(f"execute_range_query: {command}")

    # result = subprocess.run(command, shell=True, check=True, stderr=subprocess.PIPE, text=True)
    result, elapsed_time_ns_range = execute_command_with_err(command)
    
    os.makedirs(os.path.dirname(range_query_output_path), exist_ok=True)

    with open(range_query_output_path, "w") as f:
        if result:
            f.write(result.stderr)
        f.write(f"Elapsed Time: {elapsed_time_ns_range}\n")

    if RUN_EXHAUSTIVE_SEARCH:
        run_exhaustive_search(data_file, query_file, query_type="range")
    
    logger.info("Finish range query")


def execute_knn_query(k, query_file, data_file, knn_query_output_path, test_file="test-rtree-RTreeQuery", index_name="tree"):

    global logger
    logger.info(f"execute_knn_query: data_file:{data_file} query_file:{query_file} knn_query_output_path:{knn_query_output_path} test_file:{test_file}")

    if RUN_EXHAUSTIVE_SEARCH:
        command = f"{test_file} {query_file} ./benchmark/{index_name} {k}NN {BUFFER}> res"
    else:
        command = f"{test_file} {query_file} ./benchmark/{index_name} {k}NN {BUFFER}"
    
    result, elapsed_time_ns_knn = execute_command_with_err(command)

    os.makedirs(os.path.dirname(knn_query_output_path), exist_ok=True)

    with open(knn_query_output_path, "w") as f:
        if result:
            f.write(result.stderr)
        f.write(f"Elapsed Time: {elapsed_time_ns_knn}\n")

    if RUN_EXHAUSTIVE_SEARCH:
        run_exhaustive_search(data_file, query_file, query_type="knn", k=k)

    logger.info("Finish knn query")


def execute_point_query(query_file, data_file, point_query_output_path, test_file="test-rtree-RTreeQuery", index_name="tree"):

    global logger
    logger.info(f"execute_point_query: data_file:{data_file} query_file:{query_file} point_query_output_path:{point_query_output_path} test_file:{test_file}")

    if RUN_EXHAUSTIVE_SEARCH:
        command = f"{test_file} {query_file} ./benchmark/{index_name} intersection {BUFFER} > res"
    else:
        command = f"{test_file} {query_file} ./benchmark/{index_name} intersection {BUFFER}"
    
    result, elapsed_time_ns_point = execute_command_with_err(command)

    os.makedirs(os.path.dirname(point_query_output_path), exist_ok=True)

    with open(point_query_output_path, "w") as f:
        if result:
            f.write(result.stderr)
        f.write(f"Elapsed Time: {elapsed_time_ns_point}\n")

    if RUN_EXHAUSTIVE_SEARCH:
        run_exhaustive_search(data_file, query_file, query_type="range")

    logger.info("Finish point query")
    

def execute_insert(query_file, insert_output_path, test_file="test-rtree-RTreeQuery", index_name="tree"):

    global logger
    logger.info(f"execute_insert: query_file:{query_file} insert_output_path:{insert_output_path} test_file:{test_file}")

    command = f"{test_file} {query_file} ./benchmark/{index_name} intersection {BUFFER}"
    
    result, elapsed_time_ns_point = execute_command_with_err(command)

    os.makedirs(os.path.dirname(insert_output_path), exist_ok=True)

    with open(insert_output_path, "w") as f:
        if result:
            f.write(result.stderr)
        f.write(f"Elapsed Time: {elapsed_time_ns_point}\n")

    logger.info("Finish insert")
    

def execute_insert_point(query_file, insert_point_output_path, test_file="test-rtree-RTreeQuery", index_name="tree"):

    global logger
    logger.info(f"execute_insert_point: query_file:{query_file} insert_point_output_path:{insert_point_output_path} test_file:{test_file}")

    command = f"{test_file} {query_file} ./benchmark/{index_name} intersection {BUFFER}"
    
    result, elapsed_time_ns_point = execute_command_with_err(command)

    os.makedirs(os.path.dirname(insert_point_output_path), exist_ok=True)

    with open(insert_point_output_path, "w") as f:
        if result:
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

        z_order_output_default = Z_ORDER_SORTED_DEFAULT.format(
            data_file_prefix=data_file_prefix,
            bit_num=bit_num
        )

        data_file = Z_ORDER_SORTED_OUTPUT

        if not os.path.exists(z_order_output_default):
            logger.info(f"{z_order_output_default} NOT exists")

            transform_command = f"python tools/zorder.py {ablosute_data_file_name} {Z_ORDER_OUTPUT} {bit_num}"
            elapsed_time_ns_order = execute_command(transform_command)

            format_data_command = f"python tools/libspatialindex_data_adapter.py --type data --input {Z_ORDER_OUTPUT} --output {data_file}"
            execute_command(format_data_command)

            copy_and_rename(data_file, z_order_output_default)
        else:
            copy_and_rename(z_order_output_default, data_file)

            elapsed_time_ns_order = 0

        logger.info(f"Starting SFC Rtree bulk load using sorted data: {data_file}")
        
        command = f"test-rtree-SFCRTreeBulkLoad {data_file} ./benchmark/zorder {page_size} {fill_factor} {PAGE_SIZE} {BUFFER}"

        result, elapsed_time_ns_build = execute_command_with_err(command)

        # save build information when executing point or knn queries. range query is not considered becuase
        # we put default query every time. We do this because some models are saved to avoid training again,
        # so the build time is not accurate. But for point and knn queries, they are executed when index is built 
        # for the first time.
        if point_queries or knn_queries:
            build_output_path = Z_BUILD_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                bit_num=bit_num
            )

            os.makedirs(os.path.dirname(build_output_path), exist_ok=True)

            with open(build_output_path, "w") as f:
                if result:
                    f.write(result.stderr)
                f.write(f"Elapsed Time: {elapsed_time_ns_order + elapsed_time_ns_build}\n")
                f.write(f"Tree.dat Size: {os.path.getsize('./benchmark/zorder.dat')}\n")
                f.write(f"Tree.idx Size: {os.path.getsize('./benchmark/zorder.idx')}\n")

        for file_name in range_queries:
            file_name_prefix = file_name.rstrip('.csv')
            range_query_output_path = Z_RANGE_QUERY_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                range_query_prefix=file_name_prefix,
                bit_num=bit_num,
            )
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            execute_range_query(data_file, query_file, range_query_output_path, "test-rtree-RTreeQuery", index_name="zorder")

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
                execute_knn_query(k, query_file, data_file, knn_query_output_path, index_name="zorder")

        for file_name in point_queries:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            point_query_output_path = Z_POINT_QUERY_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                point_query_prefix=file_name_prefix,
                bit_num=bit_num,
            )
            execute_point_query(query_file, data_file, point_query_output_path, index_name="zorder")

        for file_name in insertions:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            insert_output_path = Z_INSERT_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                insert_prefix=file_name_prefix,
                bit_num=bit_num,
            )
            execute_insert(query_file, insert_output_path, index_name="zorder")

        for file_name in insert_points:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            insert_point_output_path = Z_INSERT_POINT_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                insert_point_prefix=file_name_prefix,
                bit_num=bit_num,
            )
            execute_insert_point(query_file, insert_point_output_path, index_name="zorder")

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

        data_file = RANK_SPACE_Z_ORDER_SORTED_OUTPUT

        rank_space_z_order_output_default = RANK_SPACE_Z_ORDER_SORTED_DEFAULT.format(
            data_file_prefix=data_file_prefix,
            bit_num=bit_num
        )

        if not os.path.exists(rank_space_z_order_output_default):
            logger.info(f"{rank_space_z_order_output_default} NOT exists")

            transform_command = f"python tools/rank_space_z.py {ablosute_data_file_name} {RANK_SPACE_Z_ORDER_OUTPUT} {bit_num}"
            elapsed_time_ns_order = execute_command(transform_command)

            format_data_command = f"python tools/libspatialindex_data_adapter.py --type data --input {RANK_SPACE_Z_ORDER_OUTPUT} --output {data_file}"
            execute_command(format_data_command)
            copy_and_rename(data_file, rank_space_z_order_output_default)
        else:
            copy_and_rename(rank_space_z_order_output_default, data_file)

            elapsed_time_ns_order = 0

        logger.info(f"Starting SFC Rtree bulk load using sorted data: {data_file}")
        
        command = f"test-rtree-SFCRTreeBulkLoad {data_file} ./benchmark/rankspace {page_size} {fill_factor} {PAGE_SIZE} {BUFFER}"

        result, elapsed_time_ns_build = execute_command_with_err(command)

        if point_queries or knn_queries:
            build_output_path = RANK_SPACE_Z_BUILD_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                bit_num=bit_num,
            )

            os.makedirs(os.path.dirname(build_output_path), exist_ok=True)

            with open(build_output_path, "w") as f:
                if result:
                    f.write(result.stderr)
                f.write(f"Elapsed Time: {elapsed_time_ns_order + elapsed_time_ns_build}\n")
                f.write(f"Tree.dat Size: {os.path.getsize('./benchmark/rankspace.dat')}\n")
                f.write(f"Tree.idx Size: {os.path.getsize('./benchmark/rankspace.idx')}\n")

        for file_name in range_queries:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            range_query_output_path = RANK_SPACE_Z_RANGE_QUERY_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                range_query_prefix=file_name_prefix,
                bit_num=bit_num,
            )
            execute_range_query(data_file, query_file, range_query_output_path, index_name="rankspace")

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
                execute_knn_query(k, query_file, data_file, knn_query_output_path, index_name="rankspace")

        for file_name in point_queries:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            point_query_output_path = RANK_SPACE_Z_POINT_QUERY_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                point_query_prefix=file_name_prefix,
                bit_num=bit_num,
            )
            execute_point_query(query_file, data_file, point_query_output_path, index_name="rankspace")

        for file_name in insertions:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            insert_output_path = RANK_SPACE_Z_INSERT_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                insert_prefix=file_name_prefix,
                bit_num=bit_num,
            )
            execute_insert(query_file, insert_output_path, index_name="rankspace")

        for file_name in insert_points:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            insert_point_output_path = RANK_SPACE_Z_INSERT_POINT_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                insert_point_prefix=file_name_prefix,
                bit_num=bit_num,
            )
            execute_insert_point(query_file, insert_point_output_path, index_name="rankspace")

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

            bmtree_output_default = BMTREE_OUTPUT_DEFAULT.format(
                data_file_prefix=data_file_prefix,
                query=file_name_prefix,
                bit_num=bit_num,
                tree_depth=tree_depth,
                sample_size=sample_size,
            )

            # if not os.path.exists(bmtree_output_default):
            # logger.info(f"{bmtree_output_default} NOT exists")
        
            data_transfer_command = f"python rl_baseline/bmtree_data_transfer.py {ablosute_data_file_name} {ablosute_query_file_name}"
            execute_command(data_transfer_command)

            learn_bmtree_command = f"bash rl_baseline/learn_bmtree.sh {data_file_prefix} {file_name_prefix} {tree_depth} {sample_size} {bit_num} {ablosute_data_file_name}"
            elapsed_time_ns_learn = execute_command(learn_bmtree_command)

            data_adapter_command = f"python tools/libspatialindex_data_adapter.py --type data --is_scaled --input {BMTREE_INPUT} --output {BMTREE_OUTPUT}"
            execute_command(data_adapter_command)

            copy_and_rename(BMTREE_OUTPUT, bmtree_output_default)
            # else:
            #     copy_and_rename(bmtree_output_default, BMTREE_OUTPUT)
                # elapsed_time_ns_learn = 0

            # build bmtree sfcrtree
            command = f"test-rtree-SFCRTreeBulkLoad {BMTREE_OUTPUT} ./benchmark/bmtree {page_size} {fill_factor} {PAGE_SIZE} {BUFFER}"
            result, elapsed_time_ns_build = execute_command_with_err(command)

            if point_queries or knn_queries:
                build_output_path = BMTREE_BUILD_OUTPUT_PATH.format(
                    data_file_prefix=data_file_prefix,
                    query=file_name_prefix,
                    bit_num=bit_num,
                    tree_depth=tree_depth,
                    sample_size=sample_size,
                )

                os.makedirs(os.path.dirname(build_output_path), exist_ok=True)

                with open(build_output_path, "w") as f:
                    if result:
                        f.write(result.stderr)
                    f.write(f"Elapsed Learn Time: {elapsed_time_ns_learn}\n")
                    f.write(f"Elapsed Build Time: {elapsed_time_ns_build}\n")
                    f.write(f"Tree.dat Size: {os.path.getsize('./benchmark/bmtree.dat')}\n")
                    f.write(f"Tree.idx Size: {os.path.getsize('./benchmark/bmtree.idx')}\n")

            data_file = BMTREE_OUTPUT

            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            range_query_output_path = BMTREE_RANGE_QUERY_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                range_query_prefix=file_name_prefix,
                bit_num=bit_num,
                tree_depth=tree_depth,
                sample_size=sample_size,
            )
            execute_range_query(data_file, query_file, range_query_output_path, index_name="bmtree")

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
                    execute_knn_query(k, knn_query_file, data_file, knn_query_output_path, index_name="bmtree")

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
                execute_point_query(query_file, data_file, point_query_output_path, index_name="bmtree")

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
                execute_insert(query_file, insert_output_path, index_name="bmtree")

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
                execute_insert_point(query_file, insert_point_output_path, index_name="bmtree")

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
        
        command = f"test-rtree-RTreeLoad {data_file} ./benchmark/rtree {page_size} {fill_factor} {rtree_variant} {PAGE_SIZE} {BUFFER}"

        result, elapsed_time_ns_build = execute_command_with_err(command)

        if point_queries or knn_queries:
            build_output_path = RTREE_BUILD_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                variant=rtree_variant
            )
                    
            os.makedirs(os.path.dirname(build_output_path), exist_ok=True)

            with open(build_output_path, "w") as f:
                if result:
                    f.write(result.stderr)
                f.write(f"Elapsed Time: {elapsed_time_ns_build}\n")
                f.write(f"Tree.dat Size: {os.path.getsize('./benchmark/rtree.dat')}\n")
                f.write(f"Tree.idx Size: {os.path.getsize('./benchmark/rtree.idx')}\n")

        for file_name in range_queries:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            range_query_output_path = RTREE_RANGE_QUERY_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                range_query_prefix=file_name_prefix,
                variant=rtree_variant
            )
            execute_range_query(data_file, query_file, range_query_output_path, index_name="rtree")

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
                execute_knn_query(k, query_file, data_file, knn_query_output_path, index_name="rtree")

        for file_name in point_queries:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            point_query_output_path = RTREE_POINT_QUERY_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                point_query_prefix=file_name_prefix,
                variant=rtree_variant
            )
            execute_point_query(query_file, data_file, point_query_output_path, index_name="rtree")

        for file_name in insertions:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            insert_output_path = RTREE_INSERT_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                insert_prefix=file_name_prefix,
                variant=rtree_variant
            )
            execute_insert(query_file, insert_output_path, index_name="rtree")

        for file_name in insert_points:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            insert_point_output_path = RTREE_INSERT_POINT_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                insert_point_prefix=file_name_prefix,
                variant=rtree_variant
            )
            execute_insert_point(query_file, insert_point_output_path, index_name="rtree")

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
        
        command = f"test-rtree-RTreeLoad {data_file} ./benchmark/rstar {page_size} {fill_factor} {rtree_variant} {PAGE_SIZE} {BUFFER}"

        result, elapsed_time_ns_build = execute_command_with_err(command)

        if point_queries or knn_queries:
            build_output_path = R_STAR_TREE_BUILD_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                variant=rtree_variant
            )

            os.makedirs(os.path.dirname(build_output_path), exist_ok=True)

            with open(build_output_path, "w") as f:
                if result:
                    f.write(result.stderr)
                f.write(f"Elapsed Time: {elapsed_time_ns_build}\n")
                f.write(f"Tree.dat Size: {os.path.getsize('./benchmark/rstar.dat')}\n")
                f.write(f"Tree.idx Size: {os.path.getsize('./benchmark/rstar.idx')}\n")

        for file_name in range_queries:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            range_query_output_path = R_STAR_TREE_RANGE_QUERY_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                range_query_prefix=file_name_prefix,
                variant=rtree_variant
            )
            execute_range_query(data_file, query_file, range_query_output_path, index_name="rstar")

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
                execute_knn_query(k, query_file, data_file, knn_query_output_path, index_name="rstar")

        for file_name in point_queries:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            point_query_output_path = R_STAR_TREE_POINT_QUERY_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                point_query_prefix=file_name_prefix,
                variant=rtree_variant
            )
            execute_point_query(query_file, data_file, point_query_output_path, index_name="rstar")

        for file_name in insertions:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            insert_output_path = R_STAR_TREE_INSERT_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                insert_prefix=file_name_prefix,
                variant=rtree_variant
            )
            execute_insert(query_file, insert_output_path, index_name="rstar")

        for file_name in insert_points:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            insert_point_output_path = R_STAR_TREE_INSERT_POINT_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                insert_point_prefix=file_name_prefix,
                variant=rtree_variant
            )
            execute_insert_point(query_file, insert_point_output_path, index_name="rstar")

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

            split_model_name_default = SPLIT_MODEL_NAME_DEFAULT.format(
                data_file_prefix=data_file_prefix,
                range_query_prefix=file_name_prefix,
                variant=rtree_variant,
                epoch=epoch,
                sample_size=sample_size
            )

            choose_subtree_model_name_default = CHOOSE_SUBTREE_MODEL_NAME_DEFAULT.format(
                data_file_prefix=data_file_prefix,
                range_query_prefix=file_name_prefix,
                variant=rtree_variant,
                epoch=epoch,
                sample_size=sample_size
            )

            if not os.path.exists(split_model_name_default) or not os.path.exists(choose_subtree_model_name_default):
                logger.info(f"{split_model_name_default} NOT exists")
                logger.info(f"{choose_subtree_model_name_default} NOT exists")
                
                learn_rlrtree_command = f"bash rl_baseline/learn_rlrtree.sh {ablosute_data_file_name} {ablosute_query_file_name} {epoch} {sample_size}"
                elapsed_time_ns_learn = execute_command(learn_rlrtree_command)

                copy_and_rename(SPLIT_MODEL_NAME, split_model_name_default)
                copy_and_rename(CHOOSE_SUBTREE_MODEL_NAME, choose_subtree_model_name_default)
            else:
                copy_and_rename(split_model_name_default, SPLIT_MODEL_NAME)
                copy_and_rename(choose_subtree_model_name_default, CHOOSE_SUBTREE_MODEL_NAME)

                elapsed_time_ns_learn = 0

            command = f"test-rtree-RTreeLoad {data_file} ./benchmark/rlrtree {page_size} {fill_factor} {rtree_variant} {model_path} {PAGE_SIZE} {BUFFER}"
            result, elapsed_time_ns_build = execute_command_with_err(command)

            if point_queries or knn_queries:
                build_output_path = RLRTREE_BUILD_OUTPUT_PATH.format(
                    data_file_prefix=data_file_prefix,
                    range_query_prefix=file_name_prefix,
                    variant=rtree_variant,
                    epoch=epoch,
                    sample_size=sample_size
                )

                os.makedirs(os.path.dirname(build_output_path), exist_ok=True)

                with open(build_output_path, "w") as f:
                    if result:
                        f.write(result.stderr)
                    f.write(f"Elapsed Learn Time: {elapsed_time_ns_learn}\n")
                    f.write(f"Elapsed Build Time: {elapsed_time_ns_build}\n")
                    f.write(f"Tree.dat Size: {os.path.getsize('./benchmark/rlrtree.dat')}\n")
                    f.write(f"Tree.idx Size: {os.path.getsize('./benchmark/rlrtree.idx')}\n")

            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            range_query_output_path = RLRTREE_RANGE_QUERY_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                range_query_prefix=file_name_prefix,
                variant=rtree_variant,
                epoch=epoch,
                sample_size=sample_size
            )
            execute_range_query(data_file, query_file, range_query_output_path, index_name="rlrtree")

            for file_name in point_queries:
                point_file_name_prefix = file_name.rstrip('.csv')
                query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, point_file_name_prefix)
                point_query_output_path = RLRTREE_POINT_QUERY_OUTPUT_PATH.format(
                    data_file_prefix=data_file_prefix,
                    range_query_prefix=file_name_prefix,
                    point_query_prefix=point_file_name_prefix,
                    epoch=epoch,
                    variant=rtree_variant,
                    sample_size=sample_size
                )
                execute_point_query(query_file, data_file, point_query_output_path, index_name="rlrtree")

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
                        variant=rtree_variant,
                        sample_size=sample_size
                    )
                    execute_knn_query(k, knn_query_file, data_file, knn_query_output_path, index_name="rlrtree")

            for file_name in insertions:
                insert_file_name_prefix = file_name.rstrip('.csv')
                query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, insert_file_name_prefix)
                insert_output_path = RLRTREE_INSERT_OUTPUT_PATH.format(
                    data_file_prefix=data_file_prefix,
                    range_query_prefix=file_name_prefix,
                    insert_prefix=insert_file_name_prefix,
                    epoch=epoch,
                    variant=rtree_variant,
                    sample_size=sample_size
                )
                execute_insert(query_file, insert_output_path, index_name="rlrtree")

            for file_name in insert_points:
                insert_point_file_name_prefix = file_name.rstrip('.csv')
                query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, insert_point_file_name_prefix)
                insert_point_output_path = RLRTREE_INSERT_POINT_OUTPUT_PATH.format(
                    data_file_prefix=data_file_prefix,
                    range_query_prefix=file_name_prefix,
                    insert_point_prefix=insert_point_file_name_prefix,
                    epoch=epoch,
                    variant=rtree_variant,
                    sample_size=sample_size
                )
                execute_insert_point(query_file, insert_point_output_path, index_name="rlrtree")


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
        command = f"test-kdtree-KDTreeBulkLoad kdtree {data_file} path ./benchmark/kdtree {page_size} 1.0 {PAGE_SIZE} {BUFFER}"  

        logger.info(f"Start building kdtree: {command}")

        result, elapsed_time_ns_build = execute_command_with_err(command)

        if point_queries or knn_queries:
            build_output_path = KDTREE_BUILD_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix
            )

            os.makedirs(os.path.dirname(build_output_path), exist_ok=True)

            with open(build_output_path, "w") as f:
                if result:
                    f.write(result.stderr)
                f.write(f"Elapsed Time: {elapsed_time_ns_build}\n")
                f.write(f"Tree.dat Size: {os.path.getsize('./benchmark/kdtree.dat')}\n")
                f.write(f"Tree.idx Size: {os.path.getsize('./benchmark/kdtree.idx')}\n")

        for file_name in range_queries:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            range_query_output_path = KDTREE_RANGE_QUERY_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                range_query_prefix=file_name_prefix
            )
            execute_range_query(data_file, query_file, range_query_output_path, "test-kdtree-KDTreeQuery", index_name="kdtree")


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
                execute_knn_query(k, query_file, data_file, knn_query_output_path, "test-kdtree-KDTreeQuery", index_name="kdtree")

        for file_name in point_queries:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            point_query_output_path = KDTREE_POINT_QUERY_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                point_query_prefix=file_name_prefix,
            )
            execute_point_query(query_file, data_file, point_query_output_path, "test-kdtree-KDTreeQuery", index_name="kdtree")

        for file_name in insertions:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            insert_output_path = KDTREE_INSERT_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                insert_prefix=file_name_prefix,
            )
            execute_insert(query_file, insert_output_path, "test-kdtree-KDTreeQuery", index_name="kdtree")

        for file_name in insert_points:
            file_name_prefix = file_name.rstrip('.csv')
            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)
            insert_point_output_path = KDTREE_INSERT_POINT_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                insert_point_prefix=file_name_prefix,
            )
            execute_insert_point(query_file, insert_point_output_path, "test-kdtree-KDTreeQuery", index_name="kdtree")

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

            command = f"test-kdtree-KDTreeBulkLoad greedy_kdtree {data_file} {query_file} ./benchmark/kdgreedy {page_size} 1.0 {PAGE_SIZE} {BUFFER}"  

            logger.info(f"Start building kdtree: {command}")

            result, elapsed_time_ns_build = execute_command_with_err(command)

            if point_queries or knn_queries:
                build_output_path = KDTREE_GREEDY_BUILD_OUTPUT_PATH.format(
                    data_file_prefix=data_file_prefix,
                    range_query_prefix=file_name_prefix
                )

                os.makedirs(os.path.dirname(build_output_path), exist_ok=True)

                with open(build_output_path, "w") as f:
                    if result:
                        f.write(result.stderr)
                    f.write(f"Elapsed Time: {elapsed_time_ns_build}\n")
                    f.write(f"Tree.dat Size: {os.path.getsize('./benchmark/kdgreedy.dat')}\n")
                    f.write(f"Tree.idx Size: {os.path.getsize('./benchmark/kdgreedy.idx')}\n")

            range_query_output_path = KDTREE_GREEDY_RANGE_QUERY_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                range_query_prefix=file_name_prefix
            )
            execute_range_query(data_file, query_file, range_query_output_path, "test-kdtree-KDTreeQuery", index_name="kdgreedy")

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
                    execute_knn_query(k, query_file, data_file, knn_query_output_path, "test-kdtree-KDTreeQuery", index_name="kdgreedy")

            for file_name in point_queries:
                point_file_name_prefix = file_name.rstrip('.csv')
                query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, point_file_name_prefix)
                point_query_output_path = KDTREE_GREEDY_POINT_QUERY_OUTPUT_PATH.format(
                    data_file_prefix=data_file_prefix,
                    range_query_prefix=file_name_prefix,
                    point_query_prefix=point_file_name_prefix,
                )
                execute_point_query(query_file, data_file, point_query_output_path, "test-kdtree-KDTreeQuery", index_name="kdgreedy")

            for file_name in insertions:
                insert_file_name_prefix = file_name.rstrip('.csv')
                query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, insert_file_name_prefix)
                insert_output_path = KDTREE_GREEDY_INSERT_OUTPUT_PATH.format(
                    data_file_prefix=data_file_prefix,
                    range_query_prefix=file_name_prefix,
                    insert_prefix=insert_file_name_prefix,
                )
                execute_insert(query_file, insert_output_path, "test-kdtree-KDTreeQuery", index_name="kdgreedy")

            for file_name in insert_points:
                insert_point_file_name_prefix = file_name.rstrip('.csv')
                query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, insert_point_file_name_prefix)
                insert_point_output_path = KDTREE_GREEDY_INSERT_POINT_OUTPUT_PATH.format(
                    data_file_prefix=data_file_prefix,
                    range_query_prefix=file_name_prefix,
                    insert_point_prefix=insert_point_file_name_prefix,
                )
                execute_insert_point(query_file, insert_point_output_path, "test-kdtree-KDTreeQuery", index_name="kdgreedy")

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

            qdtree_model_name_default = QDTREE_MODEL_NAME_DEFAULT.format(
                data_file_prefix=data_file_prefix,
                range_query_prefix=file_name_prefix,
                episode=episode,
                sampling_ratio=sampling_ratio,
                action_sampling_size=action_sampling_size,
            )

            if not os.path.exists(qdtree_model_name_default):
                logger.info(f"{qdtree_model_name_default} NOT exists") 

                learn_qdtree_command = f"bash rl_baseline/learn_qdtree.sh {ablosute_data_file_name} {ablosute_query_file_name} {episode} {sampling_ratio} {action_sampling_size}"
                elapsed_time_ns_learn = execute_command(learn_qdtree_command)

                copy_and_rename(QDTREE_MODEL_NAME, qdtree_model_name_default)
            else:
                copy_and_rename(qdtree_model_name_default, QDTREE_MODEL_NAME)

                elapsed_time_ns_learn = 0

            logger.info(f"Start building qdtree: {data_file}")
            
            command = f"test-kdtree-QDTreeBulkLoad qdtree {data_file} {query_file} ./benchmark/qdtree {page_size} 1.0 {model_path} {action_sampling_size} {PAGE_SIZE} {BUFFER}"  

            logger.info(f"Start building qdtree: {command}")

            result, elapsed_time_ns_build = execute_command_with_err(command)

            if point_queries or knn_queries:
                build_output_path = QDTREE_BUILD_OUTPUT_PATH.format(
                    data_file_prefix=data_file_prefix,
                    range_query_prefix=file_name_prefix,
                    episode=episode,
                    sampling_ratio=sampling_ratio,
                    action_sampling_size=action_sampling_size,
                )

                os.makedirs(os.path.dirname(build_output_path), exist_ok=True)

                with open(build_output_path, "w") as f:
                    if result:
                        f.write(result.stderr)
                    f.write(f"Elapsed Learn Time: {elapsed_time_ns_learn}\n")
                    f.write(f"Elapsed Build Time: {elapsed_time_ns_build}\n")
                    f.write(f"Tree.dat Size: {os.path.getsize('./benchmark/qdtree.dat')}\n")
                    f.write(f"Tree.idx Size: {os.path.getsize('./benchmark/qdtree.idx')}\n")

            query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, file_name_prefix)

            range_query_output_path = QDTREE_RANGE_QUERY_OUTPUT_PATH.format(
                data_file_prefix=data_file_prefix,
                range_query_prefix=file_name_prefix,
                episode=episode,
                sampling_ratio=sampling_ratio,
                action_sampling_size=action_sampling_size,
            )
            execute_range_query(data_file, query_file, range_query_output_path, "test-kdtree-KDTreeQuery", index_name="qdtree")

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
                    execute_knn_query(k, query_file, data_file, knn_query_output_path, "test-kdtree-KDTreeQuery", index_name="qdtree")

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
                execute_point_query(query_file, data_file, point_query_output_path, "test-kdtree-KDTreeQuery", index_name="qdtree")

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
                execute_insert(query_file, insert_output_path, "test-kdtree-KDTreeQuery", index_name="qdtree")

            for file_name in insert_points:
                insert_point_file_name_prefix = file_name.rstrip('.csv')
                query_file = os.path.join(BENCHMARK_LIBSPATIALINDEX, insert_point_file_name_prefix)
                insert_point_output_path = QDTREE_INSERT_POINT_OUTPUT_PATH.format(
                    data_file_prefix=data_file_prefix,
                    range_query_prefix=file_name_prefix,
                    insert_point_prefix=insert_point_file_name_prefix,
                    episode=episode,
                    sampling_ratio=sampling_ratio,
                    action_sampling_size=action_sampling_size,
                )
                execute_insert_point(query_file, insert_point_output_path, "test-kdtree-KDTreeQuery", index_name="qdtree")

    except subprocess.CalledProcessError as e:
        logger.error(f"fail: {e}")
    
    finally:
        # clean up intermediate files
        cleanup_intermediate_files()
        safe_remove(QDTREE_DATA)
        # save_remove(QDTREE_QUERY)

def process_experiment(experiment):

    global logger

    # if not experiment['available']:
    if not experiment.get('available', True):
        logger.info(f"experiment not available")
        return

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

    workload_suffix = "_small" if RUN_EXAMPLE else ""

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

            with open(os.path.join(SYNTHETIC_WORKLOAD_PATH + workload_suffix, workload), "r") as json_file:
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
        
        if len(range_queries) == 0:
            logger.info("No queries in range_queries (synthetic)")
            if os.path.exists(os.path.join(SYNTHETIC_QUERY_PATH, RANGE_QUERY_FILENAME_DEFAULT)):
                query_command = f"python tools/synthetic_query_generator.py --query_type range --n_queries 1000 --dimensions 2 --distribution uniform --skewness 1 --bounds 0 1 --bounds 0 1 --query_range 0.001 0.001"
                execute_command(query_command)
            is_range_query = False
            range_queries.append(RANGE_QUERY_FILENAME_DEFAULT)

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

            with open(os.path.join(REAL_WORKLOAD_PATH + workload_suffix, workload), "r") as json_file:
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
        
        if len(range_queries) == 0:
            logger.info("No queries in range_queries (real)")
            if not os.path.exists(os.path.join(REAL_QUERY_PATH, REAL_RANGE_QUERY_FILENAME_DEFAULT.format(data=base_name))):
                query_command = f"python tools/real_query_generator.py --data {absolute_data_file_name} --query_type range --n_queries 1000 --dimensions 2 --distribution uniform --skewness 1 --query_range 0.001 0.001"
                execute_command(query_command)
            is_range_query = False
            range_queries.append(REAL_RANGE_QUERY_FILENAME_DEFAULT.format(data=base_name))    

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

        if not baseline.get('available', True):
            logger.info(f"{baseline_name} is not available")
            continue


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
            configs = ["example_config_all_baselines.json",
                       "example_config_all_baselines_insert.json",
                       "example_config_all_baselines_read_heavy.json",
                       "example_config_all_baselines_write_heavy.json"]
            configs = ["example_config_all_baselines_point_rank_space_100m.json"]
        else: # for debug specific index
            configs = ["example_config_debug_bmtree.json"]
    else:
        directory = CONFIG_DIR
        # First run point_range_knn_queries to make sure queries are generated first for RL based.
        special_candidate = "point_range_knn_queries"
        for root, dirs, files in os.walk(directory):
            if root.split("/")[-1] == special_candidate:
                for file in files:
                    if file.endswith(".json"):
                        config_file_path = os.path.join(root, file)
                        configs.append(config_file_path)

        # # candidates = ["write_only", "balance_only", "write_heavy_only", "read_heavy_only"]
        candidates = ["write_only", "read_heavy_only", "write_heavy_only"]
        for root, dirs, files in os.walk(directory):
            if root.split("/")[-1] not in candidates:
                continue
            for file in files:
                if file.endswith(".json"):
                    config_file_path = os.path.join(root, file)
                    configs.append(config_file_path)
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
# python tools/libspatialindex_data_adapter.py --type data --input data/real/dataset/us_10000.csv --output benchmark/libspatialindex/kdtree_data
# test-kdtree-KDTreeBulkLoad kdtree benchmark/libspatialindex/kdtree_data path ./benchmark/tree 100 1.0 4096 0
# test-kdtree-KDTreeQuery benchmark/libspatialindex/us_10000_insert_10000_2_uniform_1 ./benchmark/tree intersection 0