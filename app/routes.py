from app import app
import pandas as pd
import json
from datetime import datetime
import re
import matplotlib.pyplot as plt
import numpy as np
import calendar
from matplotlib.figure import Figure
import base64
from io import BytesIO

df = pd.read_excel('Tick Sightings.xlsx', dtype={'id':str, 'date':str, 'location':str, 'species':str, 'latinName':str})
df['date'] = pd.to_datetime(df['date'])
global_monthly_max_sightings = df.groupby([df['date'].dt.year, df['date'].dt.month]).size().max()
monthly_y_limit = global_monthly_max_sightings + 10

global_weekly_max_sightings = df.groupby([df['date'].dt.year, df['date'].dt.isocalendar().week]).size()
weekly_y_limit = global_weekly_max_sightings.max() + 10

@app.errorhandler(400)
def bad_request(error):
    return error, 400

@app.route('/')
def index():
    return df.to_json(orient='records', date_format='iso')

@app.route('/city', defaults={'item': None})
@app.route('/city/<city>')
def city(city):
    def use_regex(input_item):
        pattern = re.compile(r"[A-Z][a-z]+")
        return pattern.match(input_item)
    
    if city:
        if use_regex(city):
            sightings = df[df['location'] == city]

            total_entries = len(sightings)
            result = {'total_entries': total_entries, 'data': sightings.to_dict(orient='records')}
    
            return json.dumps(result, default=str)
        else:
            return bad_request('Invalid input (The first letter of the city must be capitalised)')
    else:
        return df.to_json(orient='records',date_format='iso')

@app.route('/date', defaults={'after': None, 'before': None})
@app.route('/date/after=<after>', defaults={'before': None})
@app.route('/date/before=<before>', defaults={'after': None})
@app.route('/date/after=<after>before=<before>')
def date(after, before):
    def use_regex(input_item):
        pattern = re.compile(r"^([0-9]+-(0[1-9]|1[0,1,2])-(0[1-9]|[12][0-9]|3[01])T(0?[0-9]|1[0-9]|2[0-3]):(0?[0-9]|[1-5][0-9]):(0?[0-9]|[1-5][0-9]){19})$")
        return pattern.match(input_item)

    if after and before:
        if use_regex(after) and use_regex(before):
            after = pd.to_datetime(after)
            before = pd.to_datetime(before)

            temp = df[df['date'] > after]
            sightings = temp[temp['date'] < before]
            return sightings.to_json(orient='records', date_format='iso')
        
        else:
            return bad_request('Invalid input (Dates must be in the format YYYY-MM-ddThh:mm:ss)')
    elif after:
        if use_regex(after):
            after = pd.to_datetime(after)

            sightings = df[df['date'] > after]
            return sightings.to_json(orient='records', date_format='iso')
        
        else:
            return bad_request('Invalid input (Dates must be in the format YYYY-MM-ddThh:mm:ss)')
    elif before:
        if use_regex(before):
            before = pd.to_datetime(before)

            sightings = df[df['date'] < before]
            return sightings.to_json(orient='records', date_format='iso')
        
        else:
            return bad_request('Invalid input (Dates must be in the format YYYY-MM-ddThh:mm:ss)')
    else:
        return df.to_json(orient='records', date_format='iso')

@app.route('/trend/monthly', defaults={'year':None, 'city':None}) 
@app.route('/trend/monthly/year=<year>', defaults={'city':None})
@app.route('/trend/monthly/year=<year>city=<city>')
def monthly(year, city):
    def year_regex(input_item):
        pattern = re.compile(r"^[0-9]{4}$")
        return pattern.match(input_item)
    
    def city_regex(input_item):
        pattern = re.compile(r"[A-Z][a-z]+")
        return pattern.match(input_item)

    if year and city:
        if year_regex(year) and city_regex(city):
            year = int(year)
            temp = df[df['date'].dt.year == year]
            sightings = temp[temp['location']== city]
            monthly_counts = sightings.groupby(sightings['date'].dt.month).size()
            monthly_counts = monthly_counts.reindex(range(1, 13), fill_value=0)
            monthly_counts.index = [calendar.month_abbr[x] for x in monthly_counts.index]

            fig, ax = plt.subplots()
            monthly_counts.plot(kind='bar', ax=ax, title=f'Monthly trend for {year} in {city}', rot=0)
            ax.set_xlabel("Month")
            ax.set_ylabel("Sightings")
            ax.set_ylim(0, monthly_y_limit)

            buf = BytesIO()
            fig.savefig(buf, format='png')
    
            plot_url = base64.b64encode(buf.getbuffer()).decode()
    
            plt.close(fig) 
            return f'<img src="data:image/png;base64,{plot_url}"/>'
        
        else:
            return bad_request('Please input a valid year and, if you would like to filter results further, a valid city (City names must be capitalised)')
        
    elif year:
        if year_regex(year):
            year = int(year)
            sightings = df[df['date'].dt.year == year]
            monthly_counts = sightings.groupby(sightings['date'].dt.month).size()
            monthly_counts = monthly_counts.reindex(range(1, 13), fill_value=0)
            monthly_counts.index = [calendar.month_abbr[x] for x in monthly_counts.index]

            fig, ax = plt.subplots()
            monthly_counts.plot(kind='bar', ax=ax, title=f'Monthly trend for {year}', rot=0)
            ax.set_xlabel("Month")
            ax.set_ylabel("Sightings")
            ax.set_ylim(0, monthly_y_limit)

            buf = BytesIO()
            fig.savefig(buf, format='png')
    
            plot_url = base64.b64encode(buf.getbuffer()).decode()
    
            plt.close(fig) 
            return f'<img src="data:image/png;base64,{plot_url}"/>'
        else:
            return bad_request('Please input a valid year and (optional) a valid city (City names must be capitalised)')
        
    else:
        return bad_request('Please input a valid year and (optional) a valid city (City names must be capitalised)')
    
@app.route('/trend/weekly', defaults={'year':None, 'month':None, 'city':None})
@app.route('/trend/weekly/year=<year>month=<month>', defaults={'city':None})
@app.route('/trend/weekly/year=<year>month=<month>city=<city>')
def weekly(year, month, city):
    def year_regex(input_item):
        pattern = re.compile(r"^[0-9]{4}$")
        return pattern.match(input_item)
    
    def month_regex(input_item):
        pattern = re.compile(r"^[0-9]{2}$")
        return pattern.match(input_item)
    
    def city_regex(input_item):
        pattern = re.compile(r"[A-Z][a-z]+")
        return pattern.match(input_item)
    
    if year and month and city:
        if year_regex(year) and month_regex(month) and city_regex(city):
            year = int(year)
            month = int(month)
            temp1 = df[df['date'].dt.year == year]
            temp2 = temp1[temp1['date'].dt.month == month]
            sightings = temp2[temp2['location']== city]

            start_date = pd.Timestamp(year, month, 1)
            end_date = start_date + pd.offsets.MonthEnd()
            weeks_in_month = pd.date_range(start=start_date, end=end_date).isocalendar().week.unique()

            weekly_counts = sightings.groupby(sightings['date'].dt.isocalendar().week).size()
            weekly_counts = weekly_counts.reindex(weeks_in_month, fill_value=0)

            fig, ax = plt.subplots()
            weekly_counts.plot(kind='bar', ax=ax, title=f'Weekly Trend for {month}/{year} in {city}', rot=0)
    
            ax.set_xlabel("Week")
            ax.set_ylabel("Sightings")
            ax.set_ylim(0, weekly_y_limit)

            img = BytesIO()
            fig.savefig(img, format='png')
            plt.close(fig)

            plot_url = base64.b64encode(img.getvalue()).decode()
            return f'<img src="data:image/png;base64,{plot_url}"/>'
        
        else:
            return bad_request('Please input a valid year, month, and (optional) a city (City names must be capitalised)')
        
    elif year and month:
        if year_regex(year) and month_regex(month):
            year = int(year)
            month = int(month)
            temp = df[df['date'].dt.year == year]
            sightings = temp[temp['date'].dt.month == month]

            start_date = pd.Timestamp(year, month, 1)
            end_date = start_date + pd.offsets.MonthEnd()
            weeks_in_month = pd.date_range(start=start_date, end=end_date).isocalendar().week.unique()

            weekly_counts = sightings.groupby(sightings['date'].dt.isocalendar().week).size()
            weekly_counts = weekly_counts.reindex(weeks_in_month, fill_value=0)

            fig, ax = plt.subplots()
            weekly_counts.plot(kind='bar', ax=ax, title=f'Weekly Trend for {month}/{year}', rot=0)
    
            ax.set_xlabel("Week number")
            ax.set_ylabel("Sightings")
            ax.set_ylim(0, weekly_y_limit)

            img = BytesIO()
            fig.savefig(img, format='png')
            plt.close(fig)

            plot_url = base64.b64encode(img.getvalue()).decode()
            return f'<img src="data:image/png;base64,{plot_url}"/>'
        
        else:
            return bad_request('Please input a valid year, month, and (optional) a city (City names must be capitalised)')
    
    else:
        return bad_request('Please input a valid year, month, and (optional) a city (City names must be capitalised)')