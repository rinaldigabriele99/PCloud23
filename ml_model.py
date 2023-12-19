import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np


print('inizio')
data = pd.read_csv('MiningProcess_Flotation_Plant_Database.csv')
df = pd.DataFrame(data)
print('file letto')

# Verifico se nel dataset sono presenti dei valori nulli
total = df.isnull().sum()
percent = (df.isnull().sum()/df.isnull().count())
missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
missing_data

# Verifico se nel dataset sono presenti valori duplicati ed elimino quelli presenti
df.duplicated().sum()
df.drop_duplicates()
#elimino il campo date
df = df.drop('date', axis=1)

'''
# Action1: Select only the possible features, drop other column
df.columns
droplist=['% Iron Feed','% Silica Feed','Starch Flow',\
          'Ore Pulp Flow', 'Ore Pulp Density', 'Flotation Column 04 Air Flow',\
          'Flotation Column 05 Air Flow', 'Flotation Column 06 Air Flow',\
          'Flotation Column 07 Air Flow', 'Flotation Column 01 Level',
          'Flotation Column 02 Level', 'Flotation Column 03 Level', ]

df=df.drop(droplist,axis=1)
df.shape

# Action2 : Polynomial Feature Engineering for 
#df['% Iron Concentrate_power2']=df['% Iron Concentrate']**2
'''

# Sostituisci le virgole con i punti e converti le colonne in float
df = df.replace(',', '.', regex=True).astype(float)

#splitto i dati in feature x e target y
X = df.drop('% Silica Concentrate', axis=1)
y = df['% Silica Concentrate']

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

#[59.38, 8.1, 3048.97, 586.568, 398.277, 9.80542, 1.72575, 305.64, 302.641, 298.715, 300.99, 297.24, 300.331, 305.973, 407.719, 420.253, 400.138, 417.728,  346.601, 346.133, 359.425, 64.62]
Y_real = 2.83
X_new = np.array([[59.38, 8.1, 3048.97, 586.568, 398.277, 9.80542, 1.72575, 305.64, 302.641, 298.715, 300.99, 297.24, 300.331, 305.973, 407.719, 420.253, 400.138, 417.728,  346.601, 346.133, 359.425, 64.62]])
prediction = model.predict(X_new)

print('PREDIZIONE:', prediction)

#salva il modello
joblib.dump(model, 'modello_regressione.joblib')
