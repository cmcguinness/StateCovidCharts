#
#   State Charts for Covid-19
#
#   This is a simple application that downloads state by state data and
#   generates charts to visualize what's happening with the various
#   key indicators
#
#   It uses data from https://covidtracking.com
#
#   @author Charles McGuinness <covid@mcguinness.us>
#

import requests
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
import datetime
from statedata import StateData

mystate = StateData('FL')

positive = mystate.getColumn('positive')
dates = mystate.getSparseDates(4)
xs = range(len(positive))
plt.figure(figsize=(10,15))
plt.subplot(321)
plt.yscale('log')
plt.plot(xs, positive)
plt.xticks(xs, dates, rotation='vertical')
plt.title('Cumulative Positive Tests in ' + mystate.get_state_name())
plt.tight_layout()
# plt.savefig(last_date+'-Positive.png', dpi=300)
# plt.clf()

plt.subplot(322)
pos_rate = mystate.get_column_sma('delta_positive', 7)
xs = range(len(pos_rate))
plt.plot(xs,pos_rate)
plt.xticks(xs, dates[len(dates)-len(pos_rate):], rotation='vertical')
plt.title('Rolling 7 Day Mean of New Positives in ' + mystate.get_state_name())
plt.tight_layout()

# plt.savefig(last_date+'-PosRate.png', dpi=300)
# plt.clf()


deaths = mystate.getColumn('death')
xs = range(len(deaths))

plt.subplot(323)
plt.yscale('log')
plt.plot(xs, deaths)
plt.xticks(xs, dates, rotation='vertical')
plt.title('Cumulative COVID-19 Deaths in ' + mystate.get_state_name())
plt.tight_layout()

# plt.savefig(last_date+'-Deaths.png', dpi=300)
# plt.clf()

death_rate = mystate.get_column_sma('delta_death', 7)
xs = range(len(death_rate))
plt.subplot(324)
plt.plot(xs,death_rate)
plt.xticks(xs, dates[len(dates)-len(pos_rate):], rotation='vertical')
plt.title('Rolling 7 Day Mean of Daily New Deaths in ' + mystate.get_state_name())
plt.tight_layout()

#   ##################################################################
#   Plot Total Tests
#   ##################################################################

totals = mystate.getColumn('total')
xs = range(len(totals))

plt.subplot(325)
plt.yscale('log')
plt.plot(xs, totals)
plt.xticks(xs, dates, rotation='vertical')
plt.title('Cumulative COVID-19 Tests in ' + mystate.get_state_name())
plt.tight_layout()

# plt.savefig(last_date+'-Deaths.png', dpi=300)
# plt.clf()

total_rate = mystate.get_column_sma('delta_total', 7)
xs = range(len(total_rate))
plt.subplot(326)
plt.plot(xs,total_rate)
plt.xticks(xs, dates[len(dates)-len(total_rate):], rotation='vertical')
plt.title('Rolling 7 Day Mean of Daily New Tests in ' + mystate.get_state_name())
plt.tight_layout()



# plt.savefig(last_date+'-DeathRate.png', dpi=300)

plt.savefig(mystate.getLastDate()+'-'+mystate.getstate()+'.png', dpi=300)
