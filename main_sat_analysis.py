import os
import argparse

from flamapy.metamodels.fm_metamodel.transformations import UVLReader

from flamapy.metamodels.pysat_metamodel.transformations import FmToPysat, DimacsReader
from flamapy.metamodels.pysat_metamodel.operations import SATCoreDeadFeatures

from utils import timer, memory_profiler


SOLVER_NAMES = """
            cadical     = ('cd', 'cdl', 'cadical')
            gluecard3   = ('gc3', 'gc30', 'gluecard3', 'gluecard30')
            gluecard41  = ('gc3', 'gc41', 'gluecard4', 'gluecard41')
            glucose3    = ('g3', 'g30', 'glucose3', 'glucose30')
            glucose4    = ('g4', 'g41', 'glucose4', 'glucose41')
            lingeling   = ('lgl', 'lingeling')
            maplechrono = ('mcb', 'chrono', 'maplechrono')
            maplecm     = ('mcm', 'maplecm')
            maplesat    = ('mpl', 'maple', 'maplesat')
            mergesat3   = ('mg3', 'mgs3', 'mergesat3', 'mergesat30')
            minicard    = ('mc', 'mcard', 'minicard')
            minisat22   = ('m22', 'msat22', 'minisat22')
            minisatgh   = ('mgh', 'msat-gh', 'minisat-gh')
"""

HEADER = ['Model', 'Tool', 'SAT-solver', 'Seconds']
TOOL_NAME = 'Flama'


def main(fm_filepath: str, solver_name: str) -> None:
    # Get feature model name
    path, filename = os.path.split(fm_filepath)
    filename = '.'.join(filename.split('.')[:-1])

    # Load the feature model
    if fm_filepath.endswith('.uvl'):
        feature_model = UVLReader(fm_filepath).transform()

        # Create the BDD from the FM
        sat_model = FmToPysat(feature_model).transform()
    else:
        sat_model = DimacsReader(fm_filepath).transform()

    # Core features
    with timer.Timer(name='Time', logger=None):
        core_features, dead_features = SATCoreDeadFeatures(solver_name).execute(sat_model).get_result()
    print(f'Core features: {len(core_features)} {core_features}')
    print(f'Dead features: {len(dead_features)} {dead_features}')
    
    time_seconds = str(round(timer.Timer.timers['Time'], 4))

    print()
    header = ';'.join(HEADER)
    values = ';'.join([filename, TOOL_NAME, solver_name, time_seconds])
    print(header)
    print(values)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyze an FM using the SAT Solver.')
    parser.add_argument('-fm', '--featuremodel', dest='feature_model', type=str, required=True, help='Input feature model. Supported formats: .uvl (UVL), .dimacs (Dimacs).')
    parser.add_argument('-s', '--solver', dest='solver', type=str, required=False, default='glucose3', help='Solver to use (default "glucose3").' + SOLVER_NAMES)
    args = parser.parse_args()

    main(args.feature_model, args.solver)
    