"""
Example of execution:
    python execute_Xruns.py -r 30 -s main_sat_analysis.py -a "-fm fm_models/fms/Pizzas_complex.uvl -s g3"
"""
import os
import traceback
import argparse
import subprocess
import locale


PYTHON = 'python3'
TOOL_NAME = 'Flama'
OUTPUT_FILE = 'result_2024.csv'
ALREADY_ANALYZED_RESULTS = 'result_analyzed_2024.csv'
SCRIPT_PYTHON = 'main_sat_analysis.py'
SCRIPT_JAVA = 'fide_sat_analysis.jar'
COLUMNS_VALUES = [3]
TIMEOUT = 3600

def get_fm_filepath_models(dir: str) -> list[str]:
    """Get all models from the given directory."""
    models = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            filepath = os.path.join(root, file)
            models.append(filepath)
    return sorted(models)


def main(runs: int, filepath: str, solver_name: str, command: list[str]) -> None:
    # Get path and filename
    path, filename = os.path.split(filepath)
    filename = '.'.join(filename.split('.')[:-1])

    #results = []
    print(f'Executing {runs} runs for model {filepath} with solver {solver_name}:')
    for i in range(1, runs + 1):
        print(f'{i} ', end='', flush=True)
        try:
            process = subprocess.run(args=command, stdout=subprocess.PIPE, timeout=TIMEOUT) #, stderr=subprocess.DEVNULL)
            result = process.stdout.decode(locale.getlocale()[1])
            print(result)
            # Parse result:
            result_split = [l for l in result.split(os.linesep) if l]
            header = result_split[-2]
            res = result_split[-1]

            with open(OUTPUT_FILE, 'a', encoding='utf8') as file:
                file.write(f'{res}{os.linesep}')

        except subprocess.TimeoutExpired as e:
            print(f'Timeout for model: {filepath}')
            with open(OUTPUT_FILE, 'a', encoding='utf8') as file:
                res = [';'.join([filename, TOOL_NAME, solver_name, '-1', '-1', 'timeout'])]
                file.write(f"{res}{os.linesep}")
            return None
        except Exception as e:
            print(f'Other exception: {e}')
            return None
    
        # Parse result:
        # result_split = [l for l in result.split(os.linesep) if l]
        # header = result_split[-2]
        # res = result_split[-1]
        # if i == 1:
        #     header_file = header
        #     with open(OUTPUT_FILE, 'w+', encoding='utf8') as file:
        #         file.write(f'{header_file}{os.linesep}')
        # else:
        #     with open(OUTPUT_FILE, 'a', encoding='utf8') as file:
        #         file.write(f'{res}{os.linesep}')

    # print()
    # results_str = os.linesep.join(results)
    # print(results_str)

    # return (header, results)
    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Execute X runs the given script with its arguments.')
    parser.add_argument('-r', '--runs', dest='runs', type=int, required=False, default=1, help='Number of executions (default 1).')
    parser.add_argument('-d', '--dir', dest='dir', type=str, required=True, help='Folder with the models in Dimacs (.cnf).')
    args = parser.parse_args()

    analyzed_models = []
    # to avoid already analyzed models
    with open(ALREADY_ANALYZED_RESULTS, 'r') as f:
        analyzed_models = f.read()

    n_runs = args.runs
    all_models = get_fm_filepath_models(args.dir)
    n_models = len(all_models)
    header_file = None
    for i, filepath in enumerate(all_models, 1):
        print(f'FM {i}/{n_models} ({round(i/n_models*100, 2)}%): {filepath}')

        # Avoid already analyzed models
        path, filename = os.path.split(filepath)
        filename = '.'.join(filename.split('.')[:-1])
        if filename in analyzed_models:
            print(f'Skypped model.')
        else:
            try:
                # cadical solver
                solver_name = 'cadical153'
                main(n_runs, filepath, solver_name, [PYTHON, SCRIPT_PYTHON, '-fm', filepath, '-s', solver_name])
                
                # Glucose4 solver
                #solver_name = 'glucose4'
                #main(n_runs, filepath, solver_name, [PYTHON, SCRIPT_PYTHON, '-fm', filepath, '-s', solver_name])
                # header, result = main(n_runs, filepath, solver_name, ['python', SCRIPT_PYTHON, '-fm', filepath, '-s', solver_name])
                # if header_file is None:
                #     header_file = header
                #     with open(OUTPUT_FILE, 'w+', encoding='utf8') as file:
                #         file.write(f'{header_file}{os.linesep}')
                # with open(OUTPUT_FILE, 'a', encoding='utf8') as file:
                #         file.write(f'{os.linesep.join(result)}{os.linesep}')
                
                # lingeling solver
                #solver_name = 'lingeling'
                #main(n_runs, filepath, solver_name, [PYTHON, SCRIPT_PYTHON, '-fm', filepath, '-s', solver_name])
                # _, result = main(n_runs, filepath, solver_name, ['python', SCRIPT_PYTHON, '-fm', filepath, '-s', solver_name])
                # with open(OUTPUT_FILE, 'a', encoding='utf8') as file:
                #         file.write(f'{os.linesep.join(result)}{os.linesep}')

                # minisat22 solver
                solver_name = 'minisat22'
                main(n_runs, filepath, solver_name, [PYTHON, SCRIPT_PYTHON, '-fm', filepath, '-s', solver_name])
                # _, result = main(n_runs, filepath, solver_name, ['python', SCRIPT_PYTHON, '-fm', filepath, '-s', solver_name])
                # with open(OUTPUT_FILE, 'a', encoding='utf8') as file:
                #     file.write(f'{os.linesep.join(result)}{os.linesep}')

                # sat4j solver (FeatureIDE)
                #path, filename = os.path.split(filepath)
                #filename = '.'.join(filename.split('.')[:-1])
                #filepath_dimacs = os.path.join(path, filename + '.dimacs')
                #print(f'DIMACS file: {filepath_dimacs}')
                solver_name = 'sat4j'
                #main(n_runs, filepath_dimacs, solver_name, ['java', '-jar', SCRIPT_JAVA, filepath_dimacs])
                main(n_runs, filepath, solver_name, ['java', '-jar', SCRIPT_JAVA, filepath])
                #_, result = main(n_runs, filepath_dimacs, solver_name, ['java', '-jar', SCRIPT_JAVA, filepath_dimacs])
                # with open(OUTPUT_FILE, 'a', encoding='utf8') as file:
                #     file.write(f'{os.linesep.join(result)}{os.linesep}')


            except Exception as e:
                print(f'Error in model: {filepath}')
                print(e)
            #    traceback.print_exc()
    print(f'Finished all.')