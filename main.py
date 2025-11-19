from app import app
import pandas as pd
import datetime

table = pd.read_excel('Tick Sightings.xlsx', dtype={'id':str, 'date':str, 'location':str, 'species':str, 'latinName':str})

print(table)