'''
Data Website: https://data.cdc.gov/Public-Health-Surveillance/NWSS-Public-SARS-CoV-2-Wastewater-Metric-Data/2ew6-ywp6/about_data

'''


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import prophet
from statsmodels.tsa.seasonal import STL
from sklearn.metrics import mean_squared_error
import mlflow
import json


if __name__ == '__main__':
    mlflow.create_experiment(name='forecasting_wastewater', tags={'data': 'wastewater'})
    mlflow.set_experiment(experiment_name='forecasting_wastewater')
    
    with mlflow.start_run():
    
        sars_cov2 = pd.read_csv('SARS-CoV-2_Wastewater_Metric_Data_20240529.csv')
        sars_cov2 = sars_cov2.iloc[2:598,:] #remove first few and last few rows with NaN values
        sars_cov2['date_start'] = pd.to_datetime(sars_cov2['date_start'])
        sars_cov2['date_end'] = pd.to_datetime(sars_cov2['date_end'])
        sars_cov2['ds'] = pd.to_datetime(sars_cov2['date_start'] + (sars_cov2['date_end'] - sars_cov2['date_start']) / 2)
        sars_cov2 = sars_cov2[['ds', 'ptc_15d']]
        sars_cov2.set_index('ds', inplace=True)
        sars_cov2 = sars_cov2.asfreq('D')

        # plot and log wasterwater data
        plt.figure(figsize=(10, 5))
        plt.plot(sars_cov2, marker='.', linestyle='none', label='Daily Observations')
        plt.title("SARS-CoV-2 Wastewater Data")
        plt.legend()
        plt.savefig('wastewater_data_plot.png')
        mlflow.log_artifact('wastewater_data_plot.png')

        # decompose time series and plot
        decompose = STL(sars_cov2['ptc_15d']).fit()
        fig = decompose.plot()
        fig.set_size_inches(10, 5)
        plt.savefig('timeseries_decomposition.png')
        mlflow.log_artifact('timeseries_decomposition.png')

        # prepare train and test data
        split_date = '2024-01-01'
        sars_cov2_train = sars_cov2.loc[sars_cov2.index <= split_date]
        sars_cov2_test = sars_cov2.loc[sars_cov2.index > split_date]

        # Plot train and test so you can see where we have split
        sars_cov2_test \
            .rename(columns={'ptc_15d': 'TEST SET'}) \
            .join(sars_cov2_train.rename(columns={'ptc_15d': 'TRAINING SET'}),
                how='outer') \
            .plot(figsize=(10, 5), title='Traing/Tet Split', style='.')
        plt.savefig('train_test_split.png')
        mlflow.log_artifact('train_test_split.png')

        sars_cov2_train_prophet = sars_cov2_train.reset_index().rename(columns={'Datetime':'ds', 'ptc_15d':'y'})
        sars_cov2_test_prophet = sars_cov2_test.reset_index().rename(columns={'Datetime':'ds','ptc_15d':'y'})

        # train prophet model
        model = prophet.Prophet()
        model.fit(sars_cov2_train_prophet)
        mlflow.log_param("growth", model.growth)
        model_params = model.params
        params_path = 'model_params.json'
        with open(params_path, 'w') as f:
            json.dump({k: v.tolist() for k, v in model_params.items()}, f)  # convert numpy arrays to lists
        mlflow.log_artifact(params_path)

        # forecasting
        sars_cov2_test_fcst = model.predict(sars_cov2_test_prophet)

        fig, ax = plt.subplots(figsize=(10, 5))
        fig = model.plot(sars_cov2_test_fcst, ax=ax)
        ax.set_title('Prophet Forecast')
        plt.title('Prophet Forecast')
        plt.savefig('prophet_forecast.png')
        mlflow.log_artifact('prophet_forecast.png')

        # plot components learnt by the model
        fig = model.plot_components(sars_cov2_test_fcst)
        plt.title('Model Components')
        plt.savefig('model_components.png')
        mlflow.log_artifact('model_components.png')


        # Plot the forecast with the actuals
        f, ax = plt.subplots(figsize=(15, 5))
        ax.scatter(sars_cov2_test.index, sars_cov2_test['ptc_15d'], color='g', label='actual')
        fig = model.plot(sars_cov2_test_fcst, ax=ax)
        a = prophet.plot.add_changepoints_to_plot(fig.gca(), model, sars_cov2_test_fcst)
        ax.legend()
        plt.title('Prophet Forecast with observed data')
        plt.savefig('prophet_forecast_obs.png')
        mlflow.log_artifact('prophet_forecast_obs.png')

        # calculate and log rmse
        rmse = np.sqrt(mean_squared_error(y_true=sars_cov2_test['ptc_15d'],y_pred=sars_cov2_test_fcst['yhat']))
        mlflow.log_metric("rmse", rmse)

        # log and save model
        mlflow.prophet.log_model(model, "model", pip_requirements="requirements.txt")

