# Importing libraries
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Importing the data set
df = pd.read_csv('florianópolis_rental_prices.csv')

# Selecting columns
df = df[['price', 'region', 'square_meters', 'condominium_fee', 'bathrooms', 'garages']]

# Removing rental prices > 7000
for i in range(df.shape[0]):
    if df['price'][i] > 7000:
        df = df.drop(index=i)
df = df.reset_index(drop=True)

# Filling condominium_fee NA with median
df['condominium_fee'] = df['condominium_fee'].fillna(np.nanmedian(df['condominium_fee']))

# Creating dummies
df = pd.get_dummies(df)

# Attributing columns to x and y
x = df.drop(columns=['price', 'region_continent'])
y = df['price']

# Splitting into train and test
x_train, x_test, y_train, y_test = train_test_split(x,
                                                    y,
                                                    test_size=0.3,
                                                    random_state=123,
                                                    stratify=x[['region_downtown',
                                                                'region_south',
                                                                'region_north',
                                                                'region_east']])

# Feature scaling x train and test
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.fit_transform(x_test)
