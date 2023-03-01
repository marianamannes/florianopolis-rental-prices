# 🏠 Florianópolis Rental Prices 

An end-to-end data science project starting from the project planning to the model evaluation, all in Python.

## Project Overview

- Web scraping over 1000 apartments for rent information from olx.com.br using URLLIB, BeautifulSoup and data wrangling concepts with Pandas and Numpy;

- Analysing the data collected and drawing some important conclusions to the model building with Seaborn and Matplotlib;

- Creating models that predicts the rental price by the properties information with Sklearn and Statsmodel;

- Evaluating models to select the best model using Cross Validation;

## Project Steps

1. <a href="#step1"> Project Planning </a> <br>
2. <a href="#step2"> Data collection and data wrangling </a> <br>
3. <a href="#step3"> Exploratory Data Analysis </a> <br>
4. <a href="#step4"> Model Building </a> <br>
5. <a href="#step5"> Reaching the best model </a> <br>

<h2 id="step1">
  1. Project Planning
</h2>

Florianópolis, the capital of the state of Santa Catarina in southern Brazil, is famous for its beaches and many natural beauties. Thus, the rental price varies greatly according to each region of the city.

For this project, data was collected on rental prices in the city of Florianópolis through web scraping and the [OLX website](https://www.olx.com.br/), a popular marketplace that also has listings for rental properties. This database was then used to draw conclusions about the distribution of prices according to regions, number of rooms, square meters, etc., as well as to create models using Machine Learning techniques to estimate the rent value according to the property's attributes.

<h2 id="step2">
  2. Data collection and data wrangling
</h2>

A [data scrapper](https://github.com/marianamannes/florianopolis-rental-prices/blob/main/data_scrapper.py) was created for the OLX website using a Python class that returned the following information for each apartment, using the URLLIB and BeautifulSoup libraries:

- Ad text;
- Region (downtown, continent, east, north, or south);
- District;
- Square meters;
- Condominium fee;
- Number of bedrooms;
- Number of bathrooms;
- Garages
- Price.

During the creation of the class, functions were also placed to bring a more accurate dataset, removing apartments from the database that had null information about price, number of rooms, etc. Other non-apartment property types were also removed from the database via REGEX, such as houses, guest rooms, commercial properties, and summer-only rental properties. Next, the [data collection](https://github.com/marianamannes/florianopolis-rental-prices/blob/main/data_collection.py) was done.

<h2 id="step3">
  3. Exploratory Data Analysis
</h2>

In the [EDA](https://github.com/marianamannes/florianopolis-rental-prices/blob/main/data_eda.ipynb), the distribution of rental prices was verified, as well as its correlation with the number of square meters, bedrooms and bathrooms. The difference in prices between regions was also analyzed. Below are a few highlights:

<p align="center">
<img src="https://i.ibb.co/s1XjTzm/download.png" width=100% height=70%>

<p align="center">
<img src="https://i.ibb.co/0ByHRfG/download-1.png" width=100% height=70%>

<p align="center">
<img src="https://i.ibb.co/ysMksL2/download-2.png" width=100% height=70%>

<h2 id="step4">
  4. Model Building
</h2>

After selecting the main columns, creating dummys and replacing null values, the data set was splitted into [training and testing X and Y sets](https://github.com/marianamannes/florianopolis-rental-prices/blob/main/traintestsplit.py) and padronized with StandardScaler. Since there's a lack of data for rental prices over R$ 7.000,00, only apartments below this price were selected, constraining but improving the model. 

To predict rental prices, four types of algorithms were tested:

- [Ordinary Least Squares Linear Regression (OLS)](https://github.com/marianamannes/florianopolis-rental-prices/blob/main/ols_lr.py)
- [Stochastic Gradient Descent Regression (SDGR)](https://github.com/marianamannes/florianopolis-rental-prices/blob/main/sgdr.py)
- [Random Forest Regression (RF)](https://github.com/marianamannes/florianopolis-rental-prices/blob/main/rf_reg.py)
- [Support Vector Regression (SVR)](https://github.com/marianamannes/florianopolis-rental-prices/blob/main/svr.py)

Supervised machine learning models were chosen since rent values were already collected and the goal was to predict new values from the information of each apartment.

<h2 id="step5">
  5. Reaching the best model
</h2>

The mean absolute error (MAE) was chosen to evaluate the models since it gives the mean of absolute difference between model prediction and target value, and the goal was to minimize this error with cross validation.

Between the four models tested, Random Forest perfomed better, as can be seen below:

|Regressor|MAE|
|-----|-----|
|RF|798.54|
|SGDR|966.34|
|OLS|967.70|
|SVR|1172.55|
