import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

dataset = pd.read_csv('MiningProcess_Flotation_Plant_Database.csv', 
    parse_dates=['date'],
    infer_datetime_format=True,
    decimal=',')
print('file letto')

# Verifico se nel dataset sono presenti dei valori nulli
total = dataset.isnull().sum()
percent = (dataset.isnull().sum()/dataset.isnull().count())
missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])

# Verifico se nel dataset sono presenti valori duplicati
dataset.duplicated().sum()
dataset.drop_duplicates()

#creo una nuova colonne con data splittata
dataset['Data'] = dataset['date'].dt.date

#elimino la vecchia colonna data-ora
dataset = dataset.drop('date', axis=1)

#elimino tutte le righe da una certa soglia(data) in poi
data_soglia = pd.to_datetime('2017-07-15')
dataset = dataset.loc[dataset['Data'] < data_soglia]

# Convertire la colonna 'Date' in formato datetime
dataset['Data'] = pd.to_datetime(dataset['Data'], format='%Y-%m-%d')

# Convertire la colonna 'Date' in un numero intero nel formato 'YYYYMMDD'
dataset['Data'] = dataset['Data'].dt.strftime('%Y%m%d').astype(int)

#ML model
#splitto i dati in feature x e target y
X = dataset.drop('% Silica Concentrate', axis=1)
y = dataset['% Silica Concentrate']

#creazione modello (Regressione Lineare)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)
print('fine addestramento')

#valuto la prestazione del modello tra una y_pred e la sua X_test
y_pred = model.predict(X_test)

# Valuta le prestazioni del modello
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error (MSE): {mse:.2f}')
print(f'R-squared (R2): {r2:.2f}')

'''
Mean Squared Error (MSE): 0.40
R-squared (R2): 0.69
'''

#[59.38, 8.1, 3048.97, 586.568, 398.277, 9.80542, 1.72575, 305.64, 302.641, 298.715, 300.99, 297.24, 300.331, 305.973, 407.719, 420.253, 400.138, 417.728,  346.601, 346.133, 359.425, 64.62, 20170715]
Y_real = 2.83
X_new = np.array([[59.38, 8.1, 3048.97, 586.568, 398.277, 9.80542, 1.72575, 305.64, 302.641, 298.715, 300.99, 297.24, 300.331, 305.973, 407.719, 420.253, 400.138, 417.728,  346.601, 346.133, 359.425, 64.62, 20170715]])
prediction = model.predict(X_new)

print('PREDIZIONE:', prediction)

#salva il modello
joblib.dump(model, 'modello_regressione_facoltativo.joblib')