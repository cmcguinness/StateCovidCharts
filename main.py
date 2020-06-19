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

import argparse
import matplotlib.pyplot as plt
import numpy as np
from statedata import StateData

def do_subplot(title, state: StateData, subplot_num, data_name, data_label):
    plt.subplot(subplot_num)
    # plt.yscale('log')
    bar_data = state.getColumn(data_name)
    line_data = state.get_column_sma(data_name, 7)
    dates = state.getSparseDates(4)
    fulldates = state.getSparseDates(1)
    xs = range(len(bar_data))
    plt.bar(xs, bar_data, color='#CfCfff')
    plt.plot(xs,line_data, color='r')
    plt.xticks(xs, dates[len(dates)-len(line_data):], rotation=45)
    plt.title(title)
    plt.tight_layout()
    max_index = np.nanargmax(line_data)
    print('Maximum {} occured on {} with value {:.0f}'.format(data_label, (fulldates[len(dates)-len(line_data):])[max_index], line_data[max_index]))
    last = line_data[-1]
    for i in range(len(line_data)-2,-1,-1):
        if line_data[i]*2 <= last:
            print("{} doubles in {} days".format(data_label, len(line_data)-(i+1)))
            break



def plot_state(state_short,mystate):


    fig = plt.figure(figsize=(10,20))

    do_subplot('Daily COVID-19 Tests (Blue), 7 Day Average (Red)', mystate, 411, 'delta_total', 'Tests')
    do_subplot('Daily New Positives (Blue), 7 Day Average (Red)', mystate, 412, 'delta_positive', 'Positivies')

    # Texas does not have hospitalization data
    if (state_short != 'TX'):
        do_subplot('Daily New Hospitalizations (Blue), 7 Day Average (Red)', mystate, 413, 'delta_hospitalizedCumulative', 'Hospitalizations')
    do_subplot('Daily COVID-19 Deaths (Blue), 7 Day Average (Red)', mystate, 414, 'delta_death', 'Deaths')


    plt.suptitle("COVID-19 Tracking Data for " + mystate.get_state_name() + " on " + mystate.getLastDate(), fontsize=16)
    plt.figtext(0.5, 0.02, "Chart prepared by Charles McGuinness using data from covidtracking.com", ha="center", fontsize=10)
    fig.subplots_adjust(top=0.95, bottom=0.075)

    plt.savefig('images/' + mystate.getLastDate()+'-'+mystate.getstate()+'.png', dpi=150)

    print("Generated chart for "+mystate.getLastDate()+" for "+ mystate.get_state_name())

def do_doubles(title, state: StateData):
    plt.clf()
    # plt.yscale('log')
    fig = plt.figure(figsize=(10,5))

    line_data = state.get_column_sma('delta_positive', 7)
    dates = state.getSparseDates(4)
    xs = range(len(line_data))
    bar_data = []
    for i in range(len(line_data)):
        last_half = 0
        for j in range(i):
            if line_data[i] > 2*line_data[j]:
                last_half = i-j
        bar_data.append(last_half)
    plt.bar(xs, bar_data, color='#CfCfff')
    plt.xticks(xs, dates[len(dates)-len(line_data):], rotation=45)
    plt.title(title)
    plt.figtext(0.5, 0.02, "Chart prepared by Charles McGuinness @socialseercom using data from covidtracking.com", ha="center", fontsize=10)
    fig.subplots_adjust(top=0.95, bottom=0.225)

    # plt.tight_layout()
    plt.savefig('images/' + mystate.getLastDate()+'-doubles-'+mystate.getstate()+'.png', dpi=150)


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description="Generate a state's Covid-19 charts")
    # parser.add_argument('state', type=str, help='two letter abbreviation of the state (default FL)', default='FL')
    # args = parser.parse_args()
    # plot_state(args.state)
    state_short = 'FL'
    mystate = StateData(state_short)
    plot_state(state_short,mystate)
    do_doubles('Number of days to double daily positivies in '+mystate.get_state_name(), mystate)