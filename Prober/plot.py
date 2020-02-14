import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('data_GH.csv')
# df = df.iloc[288:432]
df['Time of the day'] = pd.to_datetime(df['Time of the day'])
df = df.set_index('Time of the day')
df.plot()