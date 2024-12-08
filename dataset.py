import pandas as pd

df = pd.read_csv('weight_change_dataset.csv')
spaces = pd.DataFrame({'Column': list(df.columns), 'Number of spaces': [df[i].isna().sum() for i in df.columns]})

columns = ['Age', 'Current Weight (lbs)', 'BMR (Calories)', 'Daily Calories Consumed', 'Daily Caloric Surplus/Deficit', 'Weight Change (lbs)', 'Duration (weeks)', 'Final Weight (lbs)']
mnc = [min(df[i]) for i in columns]
mxc = [max(df[i]) for i in columns]
meanc = [df[i].mean() for i in columns]
medianc = [df[i].median() for i in columns]
devc = [df[i].std() for i in columns]
stat = pd.DataFrame({'Column': columns, 'Minimum': mnc, 'Maximum': mxc, 'Mean': meanc, 'Median': medianc, 'Standard Deviation': devc})

mx = []
mn = []
for i in sorted(df['Duration (weeks)'].unique()):
    ansn = 1000
    ansx = -1000
    for j in range(len(df)):
        if df['Duration (weeks)'][j] == i:
            if df['Weight Change (lbs)'][j] > ansx:
                ansx = df['Weight Change (lbs)'][j]
            if df['Weight Change (lbs)'][j] < ansn:
                ansn = df['Weight Change (lbs)'][j]
    mx.append(ansx)
    mn.append(ansn*(-1))
dweightweek = pd.DataFrame({'Duration (weeks)': sorted([int(i) for i in df['Duration (weeks)'].unique()]), 'Max Weight Loss': mn, 'Max Weight Gain': mx})

ans = []
for i in ['Sedentary', 'Lightly Active', 'Moderately Active', 'Very Active']:
    mx = 100
    for j in range(len(df)):
        if df['Physical Activity Level'][j] == i:
            if df['Weight Change (lbs)'][j] < mx:
                mx = df['Weight Change (lbs)'][j]
    ans.append(mx*(-1))
dweightphys = pd.DataFrame({'Physical Activity Level': ['Sedentary', 'Lightly Active', 'Moderately Active', 'Very Active'], 'Max Weight Loss': ans})