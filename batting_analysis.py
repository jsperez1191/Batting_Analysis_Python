import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# displaying all columns on shell
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)
pd.set_option('display.width', 1000)

# reading the csv file
batting = pd.read_csv('/Users/juanperez/Downloads/Batting.csv')
print(batting.head(5))

# filtering out players who had 0 at bats
active_players = batting[batting['AB'] > 0]
print(active_players.describe())

# homerun leaders in dataset
sum_homeruns = batting.groupby('playerID')['HR'].sum().sort_values(ascending=False)
print(sum_homeruns)

# comparing babe ruth to hitters in the years he played
babe_ruth = batting[batting['playerID'] == 'ruthba01']
print(babe_ruth)

start_year = babe_ruth['yearID'].min()
end_year = babe_ruth['yearID'].max()

print(start_year, end_year)

ruth_years = batting[(batting['yearID'] >= start_year) & (batting['yearID'] <= end_year)]
print(ruth_years)

ruth_years_leaders = ruth_years.groupby('playerID')['HR'].sum().sort_values(ascending=False)
print(ruth_years_leaders)

# homeruns year over year
total_hr_by_year = batting.groupby('yearID')['HR'].sum()
print(total_hr_by_year)

# visualizing homeruns over the years
plt.plot(total_hr_by_year.index, total_hr_by_year.values)
plt.title('Total HR per Season Over Time')
plt.xlabel('Year')
plt.ylabel('Total HR')
plt.show()

# grouping homeruns by year and team
team_hr_per_year = (
    batting
    .groupby(['yearID', 'teamID'])['HR']
    .sum()
    .reset_index()
)
print(team_hr_per_year)
# only taking LAN(dodgers) homeruns
dodgers_hr = (
    team_hr_per_year
    [team_hr_per_year['teamID'] == 'LAN']
    .set_index('yearID')['HR']
)
dodgers_hr = dodgers_hr[dodgers_hr.index >= 2005]
print(dodgers_hr)

# taking league average homeruns per year
league_avg_hr = (
    team_hr_per_year
    .groupby('yearID')['HR']
    .mean()
)
league_avg_hr = league_avg_hr[league_avg_hr.index >= 2005]
print(league_avg_hr)

# plotting results league average vs nationals homeruns per year
plt.plot(
    league_avg_hr.index,
    league_avg_hr.values,
    label = 'League Average',
    linestyle = '--'
)

plt.plot(
    dodgers_hr.index,
    dodgers_hr.values,
    label = 'Dodgers HR'
)

plt.title('Dodgers HR vs League Average')
plt.xlabel('Year')
plt.xticks(np.arange(2005, 2025, 1))
plt.xticks(rotation=90)
plt.ylabel('Home Runs')
plt.legend()
plt.show()

# adding OBP to dataset
batting[['BB', 'HBP', 'SF']] = batting[['BB', 'HBP', 'SF']].fillna(0)

batting['OBP'] = (
    (batting['H'] + batting['BB'] + batting['HBP']) /
    (batting['AB'] + batting['BB'] + batting['HBP'] + batting['SF'])
)
batting['OBP'] = batting['OBP'].fillna(0)
print(batting.head(5))

# bring in salaries dataset and merge with batting dataset
salaries = pd.read_csv('/Users/juanperez/Downloads/Salaries.csv')

batting_with_salary = batting.merge(
    salaries,
    on = ['playerID', 'yearID', 'teamID'],
    how = 'left'
)
print(batting_with_salary.head(5))

value_df = batting_with_salary[
    (batting_with_salary['salary'] > 0) &
    (batting_with_salary['OBP'] > 0) &
    (batting_with_salary['AB'] >= 200)
].copy()

print(value_df.head(5))

value_df['OBP_per_dollar'] = value_df['OBP'] / value_df['salary']

value_df_sorted = value_df.sort_values(
    by='OBP_per_dollar',
    ascending=False
)

print(value_df_sorted[value_df_sorted['yearID'] == 2015] [[
    'playerID',
    'yearID',
    'teamID',
    'OBP',
    'salary',
    'OBP_per_dollar'
]].head(5))