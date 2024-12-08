import pandas as pd
import seaborn as sns
import numpy as np
import json
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from front import dft


def predict_weight(test_data: json, model: LinearRegression, enc: OneHotEncoder) -> float:
    df_pr = pd.read_json(test_data, orient='index')
    print(df_pr)
    arr = df_pr.values.reshape(-1)
    print()
    arr[0], arr[1] = arr[1], arr[0]
    arr[1], arr[6] = arr[6], arr[1]
    arr[2], arr[6] = arr[6], arr[2]
    arr[3], arr[6] = arr[6], arr[3]
    arr[4], arr[6] = arr[6], arr[4]
    arr[5], arr[6] = arr[6], arr[5]
    print(arr)
    arr = np.concatenate([coder.transform([arr[:2]]).toarray()[0], arr[2:]])
    return model.predict([arr])[0]


linr = LinearRegression()
coder = OneHotEncoder()
cat = coder.fit_transform(dft[['Gender', 'Physical_Activity_Level']]).toarray()
X = np.concatenate([cat, dft[['Age', 'Current_Weight_kg', 'BMR_Calories', 'Daily_Calories_Consumed', 'Duration_weeks']]], axis=1)
y = dft['Weight Change (kg)']
linr.fit(X, y)

if __name__ == '__main__':
    aboba = json.dumps({
        'Gender': "M",
        'Physical_Activity_Level': 'Lightly Active',
        'Age': 30,
        'Current_Weight_kg': 60,
        'BMR_Calories': 1000,
        'Daily_Calories_Consumed': 1000,
        'Duration_weeks': 5
    })
    print()
    print(predict_weight(aboba, linr, coder))
    print()