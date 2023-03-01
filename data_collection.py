# Importing the DataScrapper class
from data_scrapper import DataScrapper

# Calling the DataScrapper class
dataset = DataScrapper(size=1000)
df = dataset.df

# Exporting the database to a csv file
df.to_csv('florianópolis_rental_prices.csv', index=False)
