from subprocess import Popen
import os
import zipfile

os.system('cd ~/repos/mlops4/datasets && kaggle datasets download -d rkiattisak/mobile-phone-price')

with zipfile.ZipFile('/home/pyretttt/repos/mlops4/datasets/mobile-phone-price.zip', 'r') as zip_ref:
        zip_ref.extractall('/home/pyretttt/repos/mlops4/datasets/raw_data')
