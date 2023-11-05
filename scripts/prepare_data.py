import re
import logging

import numpy as np
import pandas as pd

from airflow.decorators import task

@task(task_id='prepare_data')
def run(**kwargs):
    '''Data preparation step'''
    logger = logging.getLogger('prepare_data')
    data = pd.read_csv('/home/pyretttt/repos/mlops4/datasets/raw_data/Mobile phone price.csv', sep=',')

    logger.info('Data preparation started')

    data.rename({'Storage ': 'Storage', 'RAM ': 'RAM'}, axis=1, inplace=True)
    data['Storage'] = data['Storage'].apply(lambda x: re.sub('\s?GB', '', x, flags=re.I)).astype(int)
    data['RAM'] = data['RAM'].apply(lambda x: re.sub('\s?GB', '', x, flags=re.I)).astype(int)
    data['Screen Size (inches)'] = data['Screen Size (inches)'].apply(lambda x: x.split()[0]) \
            .astype(np.float16).apply(lambda x: round(x, 1))
    data['Price ($)'] = data['Price ($)'] \
        .apply(lambda x: re.sub('\$', '', x, flags=re.I)) \
        .apply(lambda x: re.sub('\,', '', x, flags=re.I).strip()) \
        .astype(int)
    data['n_cameras'] = data['Camera (MP)'].apply(lambda x: len(x.strip().split('+')))
    data['is_pro'] = data['Model'].apply(lambda x: 1 if 'pro' in x.lower() else 0)
    data['is_ultra'] = data['Model'].apply(lambda x: 1 if 'ultra' in x.lower() else 0)
    data['is_max'] = data['Model'].apply(lambda x: 1 if 'max' in x.lower() else 0)
    data = pd.concat((pd.get_dummies(data['Brand']).astype(np.int8), data), axis=1)
    data.drop(['Camera (MP)', 'Model', 'Brand'], axis=1, inplace=True)


    logger.info('Data preparation succeed')
    logger.info(f'Data description\n shape: {data.shape}\ncolumns: {data.columns}')
    data.to_csv('/home/pyretttt/repos/mlops4/datasets/prepared.csv', index=False)
    return 'Data prepared succesfully'

task = run()
