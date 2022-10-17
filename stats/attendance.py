from cProfile import label
from statistics import mean
from turtle import color
import pandas as pd
import matplotlib.pyplot as plt
from data import games

attendance = games.loc[((games['type'] == 'info') &
                       (games['multi2'] == 'attendance')), ['year', 'multi3']]

attendance.columns = ['year', 'attendance']
# print(attendance.head())

attendance.loc[:, 'attendance'] = pd.to_numeric(
    attendance.loc[:, 'attendance'])

attendance.plot(x='year', y='attendance', figsize=(15, 7), kind='bar')
plt.xlabel('Year')
plt.ylabel('Attendance')
attendance['attendance'].mean()
plt.axhline(label='mean', color='green', ls='dashed')
plt.show()
