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
import numpy as np
import matplotlib.pyplot as plt
import datetime
from statedata import StateData

mystate = StateData('FL')

positive = mystate.getColumn('positive')
dates = mystate.getSparseDates(4)
xs = range(len(positive))

fig = plt.figure(figsize=(10,20))
plt.subplot(412)
# plt.subplots_adjust(hspace=0.01)
pos_rate = mystate.getColumn('delta_positive')
pos_rate_sma = death_rate = mystate.get_column_sma('delta_positive', 7)

xs = range(len(pos_rate))
plt.bar(xs, pos_rate, color='#CfCfff')
plt.plot(xs,pos_rate_sma, color='r')
plt.xticks(xs, dates[len(dates)-len(pos_rate):], rotation=45)
plt.title('Daily New Positives (Blue), 7 Day Average (Red)')
plt.tight_layout()


# plt.savefig(last_date+'-PosRate.png', dpi=300)
# plt.clf()


deaths = mystate.getColumn('delta_death')
death_rate = mystate.get_column_sma('delta_death', 7)
xs = range(len(deaths))

plt.subplot(414)
plt.bar(xs, deaths, color='#cfcfff')
plt.plot(xs,death_rate, color='r')
plt.xticks(xs, dates, rotation=45)
plt.title('Daily COVID-19 Deaths (Blue), 7 Day Average (Red)')
plt.tight_layout()

# plt.savefig(last_date+'-Deaths.png', dpi=300)
# plt.clf()


#   ##################################################################
#   Plot Total Tests
#   ##################################################################

totals = mystate.getColumn('delta_total')
total_rate = mystate.get_column_sma('delta_total', 7)
xs = range(len(totals))

plt.subplot(411)
plt.bar(xs, totals, color='#CfCfff')
plt.plot(xs,total_rate, color='r')
plt.xticks(xs, dates, rotation=45)
plt.title('Daily COVID-19 Tests (Blue), 7 Day Average (Red)')
plt.tight_layout()

#   ##################################################################
#   Plot Hospitalizations
#   ##################################################################

totals = mystate.getColumn('delta_hospitalizedCumulative')
total_rate = mystate.get_column_sma('delta_hospitalizedCumulative', 7)
xs = range(len(totals))

plt.subplot(413)
plt.bar(xs, totals, color='#CfCfff')
plt.plot(xs,total_rate, color='r')
plt.xticks(xs, dates, rotation=45)
plt.title('Daily New Hospitalizations (Blue), 7 Day Average (Red)')
plt.tight_layout()

plt.suptitle("COVID-19 Tracking Data for " + mystate.get_state_name() + " on " + mystate.getLastDate(), fontsize=16)
plt.figtext(0.5, 0.02, "Chart prepared by Charles McGuinness using data from covidtracking.com", ha="center", fontsize=10)
fig.subplots_adjust(top=0.95, bottom=0.075)

# plt.subplot_tool()
# plt.show()

# plt.savefig(last_date+'-DeathRate.png', dpi=300)

plt.savefig('images/' + mystate.getLastDate()+'-'+mystate.getstate()+'.png', dpi=150)

print("Generated chart for "+mystate.getLastDate()+" for "+ mystate.getstate())
