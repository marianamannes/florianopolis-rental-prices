# Importing libraries
import numpy as np
import statsmodels.api as sm
from traintestsplit import x_train, x_test, y_train, y_test
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score

# Adding constant
x_train_c = sm.add_constant(x_train)
ols_lr = sm.OLS(y_train, x_train_c, hasconst=True).fit()
ols_lr.summary()

# Removing non significant features
x_train = x_train[:, [0, 1, 2, 3, 4, 6, 7]]
x_test = x_test[:, [0, 1, 2, 3, 4, 6, 7]]
x_train_c = sm.add_constant(x_train)
ols_lr = sm.OLS(y_train, x_train_c, hasconst=True).fit()
ols_lr.summary()

# Model fitting
ols_lr = LinearRegression()
ols_lr.fit(x_train, y_train)

# Model predicting
ols_lr_y_pred = ols_lr.predict(x_test)

# Model scores with cross validation
ols_lr_r2 = np.mean(cross_val_score(ols_lr, x_test, y_test, scoring='r2')).round(2)
ols_lr_mae = -np.mean(cross_val_score(ols_lr, x_test, y_test, scoring='neg_mean_absolute_error')).round(2)
ols_lr_mse = -np.mean(cross_val_score(ols_lr, x_test, y_test, scoring='neg_mean_squared_error')).round(2)