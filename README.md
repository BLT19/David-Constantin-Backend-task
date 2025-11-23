# David-Constantin-Backend-task

Submission of the backend task for the second round interview

## Project Outline

### What the project does

This is the backend of a web app that processes provided data about tick sightings in the UK. Data can be filtered by city and date. Furthermore, both weekly and monthly trends for all of the data can be seen easily through the created app routes.

### Why the project is useful

This app allows for the quick processing of tick sighting data dating back over a decade ago. This means that the app can both help keep track of old records and very clearly view the change in the amount of tick sightings over the year. This makes studying the data significantly easier as it takes far less time to go through it all to find the specific parts you might ahve been looking for.

## How to run the project

1. Download and extract the zip file

2. Create a venv in the same directory you cloned the repo

3. Activate the venv with the command "source venv/bin/activate" on linux or just "venv/scripts/activate" on windows

4. Run "pip install -r requirements.txt" to install all the dependencies

5. Now you can use the command "flask run" in order to run the project

6. Open the localhost link to start using the app. Routes are as follows:
    - "/" will display the whole dataset

    - "/city/**CITYNAME**" will filter the data by the provided city. If no city is provided the whole dataset will be presented.

    - "/date/after=**AFTER**before=**BEFORE**" will filter the data by the provided dates. If only the "after" is provided then the app will display all data with dates after the provided one. Same with "before" but data with dates before the provided one will be shown. If both "after" and "before" are provided, the app will display all data within the provided time range. (Date format is YYYY-MM-ddThh:mm:ss)

    - "/trend/monthly/year=**YEAR**city=**CITY**" will display a graph of the monthly data trends within a given year and in a specified city. The "city" is optional and does not need to be provided. If "city" is not provided, the app will display the monthly trend for the entirety of the UK.

    - "/trend/weekly/year=**YEAR**month=**MONTH**city=**CITY**" will display a graph of the weekly data trends within a given month of a given year. The "city" is once again optional and does not need to be provided. If it is not provided, the weekly trend for the month in the given year for the entirety of the UK will be displayed.

7. Once finished with the app, press Shift+C in the command line to close the app.

## Documentation and Thought Process

### Frameworks and architecture

The framework that I decided to use for this project was **Flask**. This is because Flask is a lightweight and easy to use framework. The project was not particularly large or complicated, and so I thought that Flask was fitting as it would hepl me complete the project within the specified deadline as Flask is very easy to learn and easy to use with plenty of documentation on it to help learn it. Flask would also make scaling the project up easy if it was required.

### How the app consumes and presents data

At present, the app uses the **Pandas** library to read the provided excel file for all of the data contained within it. It then reads through the created DataFrame and filters out data as specified. This is because of the size of the project and the limited time I had to complete it. Due to these limitations, I opted for a simple solution to reading the data rather than building a database, to ensure that the functionality of the backend was completed.

On the actual web pages, the data presented is mostly formatted to be JSON strings from the DataFrames. The only exception to this are the trends which instead render the graphs directly on the page. This is all done so that in the scenario where a frontend half of this app is created, the data is readily accessible and hasn't been altered to allow it to be easily formatted however is necessary in the frontend. 

### Handling large datasets, duplicates, and incomplete data

To handle large datasets, I would opt to swap the framework from Flask to something that doesn't utilise Python as Python can take quite a bit longer than other languages. I would likely swap to either Express or Ruby on Rails as they would make SQL queries and handling a database more efficient that Flask

Duplicate data would be handled at data creation. The data would be compared by location, date and tick species. If a sighting of the same species happens within a few hours in the same location, there's a good chance it would be the same sighting.

Incomplete data would also be handled at data creation by the database schema, as any data that doesn't fit the schema would be invalid.

### Things I could have done better if I had more time

- Creating an actual database. At present data is directly read from a single excel file which makes scaling this data somewhat cumbersome and difficult to do. If I had more time and the resources to do it, I would've opted for designed a database schema for this task and implementing the data into it

- Making data slightly easier to read in the weekly trends. At present, the x-axis which is the different weeks, shows the week number from the whole year rather than the date the week started on. This can be confusing in later months as the week numbers get very high. With more time, I would've opted to have each week be displayed with the date it started on

- Adding the AI insights. By the time I finished the trends and could move on to the actual AI insights extension task, it was getting very close to the submission date. The project did take me all the time provided as I did need to learn many new things and improve my existing skill sets further in order to complete. Thus, while researching how to add the AI insights, I realised that this feature would likely take me time I no longer had as the rest of the app already took all the possible time I could allocate it in between my university studies and part time job.