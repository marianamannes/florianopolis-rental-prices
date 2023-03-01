# Importing libraries
import numpy as np
from traintestsplit import x_train, x_test, y_train, y_test
from sklearn.linear_model import SGDRegressor
from sklearn.model_selection import cross_val_score

# Removing non significant features
x_train = x_train[:, [0, 1, 2, 3, 4, 6, 7]]
x_test = x_test[:, [0, 1, 2, 3, 4, 6, 7]]

# Model fitting
sgdr = SGDRegressor(random_state=123)
sgdr.fit(x_train, y_train)

# Model predicting
sgdr_y_pred = sgdr.predict(x_test)

# Model scores with cross validation
sgdr_r2 = np.mean(cross_val_score(sgdr, x_test, y_test, scoring='r2')).round(2)
sgdr_mae = -np.mean(cross_val_score(sgdr, x_test, y_test, scoring='neg_mean_absolute_error')).round(2)
sgdr_mse = -np.mean(cross_val_score(sgdr, x_test, y_test, scoring='neg_mean_squared_error')).round(2)
