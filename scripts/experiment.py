import logging

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import AdaBoostRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error

from airflow.decorators import task

@task(task_id='experiment')
def run(**kwargs):
    '''Experiment step'''

    logger = logging.getLogger('experiment')

    data = pd.read_csv('/home/pyretttt/repos/mlops4/datasets/prepared.csv', sep=',', index_col=None)

    lr = LinearRegression(fit_intercept=True)
    lasso = Lasso(alpha=0.5)
    ridge = Ridge(alpha=0.5)
    knn = KNeighborsRegressor(n_neighbors=3, weights='distance')
    ada = AdaBoostRegressor(n_estimators=20)
    gbr = GradientBoostingRegressor(n_estimators=200)

    X_train, X_test, y_train, y_test = train_test_split(data.drop(['Price ($)'], axis=1), data['Price ($)'], test_size=0.3, random_state=42)

    best_mse = np.inf
    best_estimator = None

    for model in [lr, lasso, ridge, knn, ada, gbr]:
        logger.info(f'{model} is about to start training')
        model.fit(X_train, y_train)
        logger.info(f'{model} training is finished')
        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        logger.info(f'{model} mse: ', mse)
        mae = mean_absolute_error(y_test, predictions)
        logger.info(f'{model} mae: ', mae)                            
        if mse < best_mse:
            best_mse = mse
            best_estimator = model


    logger.info(f'best_estimator: {best_estimator}')
    logger.info(f'best_mse: {best_mse}')

    return 'Experiment finished successfully'

task = run()
