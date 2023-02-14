import os
import argparse

from flamapy.metamodels.fm_metamodel.transformations import UVLReader

from flamapy.metamodels.pysat_metamodel.transformations import FmToPysat, DimacsWriter


def get_fm_filepath_models(dir: str) -> list[str]:
    """Get all models from the given directory."""
    models = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            filepath = os.path.join(root, file)
            models.append(filepath)
    return models

    
def main(dir: str, output_dir: str):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    models_filepaths = get_fm_filepath_models(dir)
    n_models = len(models_filepaths)
    
    for i, fm_filepath in enumerate(models_filepaths, 1):
        try:
            print(f'FM {i}/{n_models} ({round(i/n_models*100, 2)}%): {fm_filepath}')
            if fm_filepath.endswith('.uvl'):
                # Get FM name
                fm_name = '.'.join(os.path.basename(fm_filepath).split('.')[:-1])
                output_filepath = f'{os.path.join(output_dir,fm_name)}.cnf'

                if not os.path.exists(output_filepath):
                    # Load the feature model
                    feature_model = UVLReader(fm_filepath).transform()

                    # Convert to CNF (throught the PySAT metamodel)
                    sat_model = FmToPysat(feature_model).transform()

                    # Convert to dimacs (.cnf)
                    DimacsWriter(path=output_filepath, source_model=sat_model).transform()
        except Exception as e:
            print(e)
            print(f'Error in model: {fm_filepath}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert all FMs in .uvl from the given folder to dimacs (.cnf).')
    parser.add_argument(dest='dir', type=str, help='Folder with the models.')
    parser.add_argument('-o', dest='output', type=str, required=False, default='.', help='Destination folder (default .).')
    args = parser.parse_args()

    main(args.dir, args.output)
