import requests
# from bs4 import BeautifulSoup
import json
import numpy as np
import datetime
import pandas as pd
import us_state_abbrev

class StateData:
    #   Initialize by fetching the data from the web site,
    #   parsing it, and putting into an appropriate data frame
    def __init__(self, state: str):
        self.state = state.lower()
        self.headers = []
        self.columns = []

        # Fetch the data from the web site
        # url = 'https://covidtracking.com/data/state/' + self.state
        url = 'https://covidtracking.com/api/v1/states/' + self.state + '/daily.json'
        page = requests.get(url)

        if not page.ok:
            page.raise_for_status()

        self.json_data = json.loads(page.content)

        self.data_frame = pd.DataFrame(self.json_data)

        # Because the data is given with most recent date first, we sort it
        self.data_frame.sort_values(by=['date'], inplace=True)

        self.data_frame['date'] = self.data_frame['date'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))

        self.last_date = self.data_frame['date'].array[-1].strftime("%Y-%m-%d")

    # Get columns, including computed ones
    def get_col(self, name: str):
        if name.startswith('delta_'):
            return self.data_frame[name[6:]].diff(1)

        return self.data_frame[name]

    # Get the column with the specified name
    def getColumn(self, colname: str):
        return self.get_col(colname).to_numpy()

    def get_column_sma(self, colname: str, days: int):
        return self.get_col(colname).rolling(days).mean().to_numpy()

    # Because the xticks of our graphs would be too dense if every date is shown,
    # we can return an array with just every x dates
    def getSparseDates(self, sparseness):
        sparseDates = self.data_frame['date'].apply(lambda x: x.strftime("%Y-%m-%d"))
        for i in range(sparseness-1):
            sparseDates[len(sparseDates)-(i+2)::-sparseness] = ""
        return sparseDates.array

    # The last date in the table
    def getLastDate(self):
        return self.last_date

    def getstate(self):
        return self.state

    def get_state_name(self):
        return us_state_abbrev.abbrev_us_state[self.state.upper()]
