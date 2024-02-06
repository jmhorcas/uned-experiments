import os
import argparse

from flamapy.metamodels.fm_metamodel.transformations import UVLReader

from flamapy.metamodels.pysat_metamodel.transformations import FmToPysat, DimacsWriter, DimacsReader


def get_fm_filepath_models(dir: str) -> list[str]:
    """Get all models from the given directory."""
    models = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            filepath = os.path.join(root, file)
            models.append(filepath)
    return models

    
def main(dir: str):
    models_filepaths = get_fm_filepath_models(dir)
    n_models = len(models_filepaths)
    
    for i, fm_filepath in enumerate(models_filepaths, 1):
        try:
            print(f'FM {i}/{n_models} ({round(i/n_models*100, 2)}%): {fm_filepath}')
            if fm_filepath.endswith('.uvl'):
                # Get FM name
                fm_name = '.'.join(os.path.basename(fm_filepath).split('.')[:-1])

                # Load the feature model
                feature_model = UVLReader(fm_filepath).transform()
                print(f'  |-> |F| = {len(feature_model.get_features())}, |CTCs| = {len(feature_model.get_constraints())}')
                
            elif fm_filepath.endswith('.cnf') or fm_filepath.endswith('.dimacs'):
                sat_model = DimacsReader(fm_filepath).transform()
                print(f'  |-> |F| = {len(sat_model.variables)}, |Clauses| = {len(sat_model.get_all_clauses().clauses)}')
        except Exception as e:
            print(e)
            print(f'Error in model: {fm_filepath}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert all FMs in .uvl from the given folder to dimacs (.cnf).')
    parser.add_argument(dest='dir', type=str, help='Folder with the models.')
    args = parser.parse_args()

    main(args.dir)
