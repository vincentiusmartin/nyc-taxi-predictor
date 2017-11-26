import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.regressionplots import abline_plot
from scipy.stats.stats import pearsonr

def time_to_int(dt):
    input_time = list(reversed(dt.split(":")))
    return sum(int(input_time[i]) * 60**i for i in range(0,3))

def date_to_int(dt):
    input_date = list(reversed(dt.split("-")))
    return int(input_date[2])

def preprocess(filename):
    # "lpep_pickup_datetime","lpep_dropoff_datetime","PULocationID","DOLocationID","trip_distance","fare_amount"
    df = pd.read_csv(filename,usecols=["trip_distance","fare_amount"],index_col=False,sep=',')

    '''dt = df["lpep_pickup_datetime"].apply(lambda x: x.split(' ')).tolist()
    df["pu_date"] = pd.DataFrame([date_to_int(x[0]) for x in dt])
    df["pu_time"] = pd.DataFrame([time_to_int(x[1]) for x in dt])
    df = df.drop("lpep_pickup_datetime",axis=1)

    dt = df["lpep_dropoff_datetime"].apply(lambda x: x.split(' ')).tolist()
    df["do_date"] = pd.DataFrame([date_to_int(x[0]) for x in dt])
    df["do_time"] = pd.DataFrame([time_to_int(x[1]) for x in dt])
    df = df.drop("lpep_dropoff_datetime",axis=1)
    '''

    df[['trip_distance','fare_amount']].apply(pd.to_numeric)
    df = sm.add_constant(df) # need to manually add intercept term

    df = df.drop(df[df.fare_amount <= 0].index)
    df = df.drop(df[df.trip_distance <= 0].index)

    return df

if __name__ == "__main__":
    training_file = "green_tripdata_2017-01.csv"
    testing_file = "green_tripdata_2017-06.csv"
    
    df_train = preprocess(training_file)
    lm = sm.OLS(df_train['fare_amount'],df_train.drop('fare_amount',axis=1)).fit()

    y_train = lm.predict(df_train.drop('fare_amount',axis=1))
    rtrain = pearsonr(y_train,df_train['fare_amount'])

    df_test = preprocess(testing_file)
    y_test = lm.predict(df_test.drop('fare_amount',axis=1))
    rtest = pearsonr(y_test,df_test['fare_amount'])
    
    print(lm.summary())    
    print("rtrain: {:.4f} , rtest: {:.4f}".format(rtrain[0],rtest[0]))
    
    # scatter-plot data
    ax = df_train.plot(x='trip_distance', y='fare_amount', kind='scatter', s=1)
    ax.set_ylim(0, 250)
    ax.set_xlim(0, 80)

    # plot regression line
    abline_plot(model_results=lm, ax=ax,markersize=1)

    plt.show()
