import pandas as pd
import random
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


df=pd.read_csv("C:/Users/anilp/Project_Files/BVP.csv")

#print(df.head())

df.rename(columns = {'64.000000':'Blood Pressure'}, inplace = True)
df.index.names = ['Time(ms)']
#df.column.names = ['Blood Pressure']
df["exercise"]=""
df.fillna(0)

def fun1(x):
  if x>400:
    x=400
  elif x<-400:
    x=400
  else:
    pass
  return x

def fun2(x):
  x=random.random()
  if x>-200 and x<200:
    x="Resting Blood Pressure"
  else:
    x="Active Blood Presssure"
  return x


df['Blood Pressure'] = df['Blood Pressure'].map(lambda x:fun1(x))

df['exercise'] = df['exercise'].map(lambda x:fun2(x))
print(df)
#meanData = np.mean(df)
#medianData = np.median()
#modeData = np.mode()
#print(meanData)
#print(medianData)
#print(modeData)



# lineplot creation

palette = sns.color_palette("rocket_r")
sns.lineplot(data=df, palette="tab10", linewidth=2.5)
sns.set_theme(style="ticks")
plt.grid(True)

#search subplot (maybe find outliers woth boxplot)
f, ax = plt.subplots(figsize=(7, 5))
sns.despine(f)

# histplot creation

sns.histplot(
    df,
    x="Blood Pressure",
    hue="exercise",
    palette="light:m_r",
    edgecolor=".3",
    linewidth=.5,
)
ax.xaxis.set_major_formatter(mpl.ticker.ScalarFormatter())
ax.set_xticks([-400, -200, 0, 200, 400])