"""
Example of execution:
    python execute_Xruns.py -r 30 -s main_sat_analysis.py -a "-fm fm_models/fms/Pizzas_complex.uvl -s g3"
"""
import os
import argparse
import subprocess
import locale


TOOL_NAME = 'Flama'
OUTPUT_FILE = 'result.csv'
SCRIPT = 'main_sat_analysis.py'
COLUMNS_VALUES = [3]
TIMEOUT = 2

def get_fm_filepath_models(dir: str) -> list[str]:
    """Get all models from the given directory."""
    models = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            filepath = os.path.join(root, file)
            models.append(filepath)
    return models


def main(runs: int, filepath: str, solver_name: str) -> tuple[str, list[str]]:
    # Get path and filename
    path, filename = os.path.split(filepath)
    filename = filename.split('.')[0]

    results = []
    print(f'Executing {runs} runs for model {filepath} with solver {solver_name}:')
    for i in range(1, runs + 1):
        print(f'{i} ', end='', flush=True)
        try:
            process = subprocess.run(args=['python', SCRIPT, '-fm', filepath, '-s', solver_name], stdout=subprocess.PIPE, timeout=TIMEOUT) #, stderr=subprocess.DEVNULL)
            result = process.stdout.decode(locale.getdefaultlocale()[1])
        except subprocess.TimeoutExpired as e:
            print(f'Timeout for model: {filepath}')
            return ('', [';'.join([filename, TOOL_NAME, solver_name, 'timeout'])])
    
        # Parse result:
        result_split = [l for l in result.split(os.linesep) if l]
        header = result_split[-2]
        res = result_split[-1]
        results.append(res)

    print()
    results_str = os.linesep.join(results)
    print(results_str)

    return (header, results)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Execute X runs the given script with its arguments.')
    parser.add_argument('-r', '--runs', dest='runs', type=int, required=False, default=1, help='Number of executions (default 1).')
    parser.add_argument('-d', '--dir', dest='dir', type=str, required=True, help='Folder with the models in Dimacs (.cnf).')
    args = parser.parse_args()


    n_runs = args.runs
    all_models = get_fm_filepath_models(args.dir)
    n_models = len(all_models)
    header_file = None
    for i, filepath in enumerate(all_models, 1):
        print(f'FM {i}/{n_models} ({round(i/n_models*100, 2)}%): {filepath}')
        try:
            # Glucose4 solver
            header, result = main(n_runs, filepath, 'glucose4')
            if header_file is None:
                header_file = header
                with open(OUTPUT_FILE, 'w+', encoding='utf8') as file:
                    file.write(f'{header_file}{os.linesep}')
            with open(OUTPUT_FILE, 'a', encoding='utf8') as file:
                    file.write(f'{os.linesep.join(result)}{os.linesep}')
            
            # lingeling solver
            _, result = main(n_runs, filepath, 'lingeling')
            with open(OUTPUT_FILE, 'a', encoding='utf8') as file:
                    file.write(f'{os.linesep.join(result)}{os.linesep}')

            # minisat22 solver
            _, result = main(n_runs, filepath, 'minisat22')
            with open(OUTPUT_FILE, 'a', encoding='utf8') as file:
                file.write(f'{os.linesep.join(result)}{os.linesep}')


        except Exception as e:
            print(f'Error in model: {filepath}')
    