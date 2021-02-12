from os import listdir, mkdir
from os.path import isfile, join, isdir

import nestedtext as nt

from utils import capitalize, sqlalchemy_column_types


def create_model_file(output_folder, model):
    indent = '    '
    if not isdir(join(output_folder, 'models')):
        mkdir(join(output_folder, 'models'))
    with open(join(output_folder, 'models', model+'.py'), 'w+') as f:
        f.write('# This file was generated by sapiens\n')
        f.write('from sqlalchemy import Column, Integer, String\n\n')
        f.write('from engine import Base\n\n\n')
        f.write(f'Class {capitalize(model)}(Base):\n')
        f.write(f'{indent}__tablename__ = {model}\n\n')

def create_properties(output_folder, model, fields):
    # fields are received as a list [field_name: some parameters separated by commas, ...]
    indent = '    '
    with open(join(output_folder, 'models', model+'.py'), 'a') as f:
        for field in fields:
            field_name = field.split(':')[0]
            field_props = field.split(':')[1]
            field_type = field_props.split(',')[0]
            f.write(f'{indent}{field_name} = Column({sqlalchemy_column_types(field_type)})\n')

def create_models(design_folder, output_folder):
    for f in [f for f in listdir(design_folder) 
              if isfile(join(design_folder, f))
              and f[-3:] == '.nt'
              and f[:5] == 'model']:
        models = nt.load(join(design_folder, f), 'dict')
        for model in models:
            create_model_file(output_folder, model)
            for k in models[model]:
                if k == 'fields':
                    create_properties(output_folder, model, models[model][k])

def create_engine(design_folder, output_folder, engine):
    if not isdir(join(output_folder, 'models')):
        mkdir(join(output_folder, 'models'))
    with open(join(output_folder, 'models', 'engine.py'), 'w+') as f:
        f.write('# This file was generated by sapiens\n')
        f.write('from sqlalchemy import create_engine\n')
        f.write('from sqlalchemy.ext.declarative import declarative_base\n\n\n')
        f.write(f"engine = create_engine({engine}, echo=True)\n")
        f.write('Base = declarative_base()\n')
