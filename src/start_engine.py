import os, sys
import argparse
import shutil

from modeler import create_engine, create_models


def check_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--design", help="design folder location")
    parser.add_argument("-o", "--output", help="output folder location")
    args = parser.parse_args()
    design =args.design if args.design else 'design'
    output =args.output if args.output else 'output'
    return design, output

def check_design_folder(dir):
    if not os.path.isdir(dir):
        print(f'>>> Could not find {dir} folder. Exiting...')
        sys.exit(-1)
    if not os.path.isfile(os.path.join(dir, 'settings.nt')):
        print(f'>>> Could not find settings file. Exiting...')
        sys.exit(-1)
    return True

def create_output_folder(dir):
    try:
        if os.path.isdir(dir):
            shutil.rmtree(dir)
        os.mkdir(dir)
    except OSError as e:
        print(f">>> Error {e} occurred. Exiting...")
        sys.exit(-1)


design_folder, output_folder = check_arguments()
print('>>> Launching engine ...')
if check_design_folder(design_folder):
    print('>>> Found valid design folder')
create_output_folder(output_folder)
print('>>> Output folder created')
print('>>> Starting writing files')
create_engine(design_folder, output_folder)
create_models(design_folder, output_folder)
print('>>> All files written')

    