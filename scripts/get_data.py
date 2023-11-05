from subprocess import Popen
import os
import zipfile
import logging

logger = logging.getLogger('get_data')

logger.info('Start loading dataset')
os.system('cd ~/repos/mlops4/datasets && kaggle datasets download -d rkiattisak/mobile-phone-price')

logger.info('Loaded dataset')
with zipfile.ZipFile('/home/pyretttt/repos/mlops4/datasets/mobile-phone-price.zip', 'r') as zip_ref:
        zip_ref.extractall('/home/pyretttt/repos/mlops4/datasets/raw_data')
        logger.info('Extracted zip files')
