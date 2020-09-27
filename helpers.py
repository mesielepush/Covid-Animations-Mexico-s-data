import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import joblib
import seaborn as sns
import calendar
import os
from numpy import genfromtxt
from datetime import datetime, timedelta
from collections import OrderedDict
from constants import *

def csvToNumpy(file_names,raw_data_url):
    for file in file_names:
        name = file[0:-4] +'.npy'
        if name not in data_files:
            data = pd.read_csv(os.path.join(raw_data_url,file), encoding='ANSI')
            data.to_numpy(dtype=None, copy=False)
            np.save(os.path.join(data_base_url,file[:-4]), data, allow_pickle=True, fix_imports=True)

def getStateData(data,state):
    state_code = inverse_dict_for_name_states[state]
    return np.array([data[x] for x in range(len(data)) if data[x][7] == state_code])

def getConfirmed(data):
    return np.array([data[x] for x in range(len(data)) if data[x][30] == 1])

def getSuspicious(data):
    return np.array([data[x] for x in range(len(data)) if data[x][30] == 3])

def getDeathData(data):
    data = getConfirmed(data)
    return np.array([data[x] for x in range(len(data)) if data[x][12] != '9999-99-99'])

def getAliveData(data):
    data = getConfirmed(data)
    return np.array([data[x] for x in range(len(data)) if data[x][12] == '9999-99-99'])

def getNegativesData(data):
    return np.array([data[x] for x in range(len(data)) if data[x][30] == 2])

def getHospitalized(data):
    data = getConfirmed(data)
    return np.array([data[x] for x in range(len(data)) if data[x][9] == 2])

def getOngoing(data):
    data = getConfirmed(data)
    return np.array([data[x] for x in range(len(data)) if data[x][9] == 1])

def getAgeData(data,age):
    data = getConfirmed(data)
    return np.array([data[x] for x in range(len(data)) if data[x][15] == age])

def getMenData(data):
    data = getConfirmed(data)
    return np.array([data[x] for x in range(len(data)) if data[x][5] == 2])
    
def getWomenData(data):
    data = getConfirmed(data)
    return np.array([data[x] for x in range(len(data)) if data[x][5] == 1])

def getSectorData(data,sector):
    data = getConfirmed(data)
    return np.array([data[x] for x in range(len(data)) if data[x][3] == inverse_dict_for_sector_states[sector]])

def data_actives(data,state,window=14):  
    if state.lower() not in ['nacional','all']:
        data = getStateData(data,state)

    data = getConfirmed(data)
    onset_symptoms = pd.to_datetime(data[:,11])
    set_dates = set(onset_symptoms)
    timeline = pd.date_range(start=min(set_dates), end = data[0][0])
    result = {key:0 for key in timeline}

    for ind, day_active in enumerate(onset_symptoms):
        for day in range(window):
            if day_active not in timeline:
                break
            elif data[ind][12] != '9999-99-99' and day_active > pd.to_datetime(data[ind][12]):
                break
            else:
                result[day_active] +=1
                day_active = day_active + timedelta(days=1)

    dates = timeline
    data =  np.array(list(result.values()))
    return [dates,data]

def getDataType(data,distribution,target_dates):
    set_dates = set(target_dates)
    
    timeline = pd.date_range(start=min(set_dates), end = data[0][0])
    
    result = {key:list(target_dates).count(key) for key in timeline}
    
    dates = timeline
    if distribution == 'discrete':
        data =  np.array(list(result.values()))
    else:
        data = np.array(list(result.values())).cumsum()
    return dates, data

def data_distribution(data, state, dist_type, distribution,window =14):
    
    if state.lower() not in ['nacional','all']:
        data = getStateData(data,state)    
    if dist_type == 'confirmed':
        data = getConfirmed(data)
        target_dates = pd.to_datetime(data[:,11])
    elif dist_type == 'suspicious':
        data = getSuspicious(data)
        target_dates = pd.to_datetime(data[:,11])
    elif dist_type == 'deaths':
        data = getDeathData(data)
        target_dates = pd.to_datetime(data[:,12])
    elif dist_type == 'negatives':
        data = getNegativesData(data)
        target_dates = pd.to_datetime(data[:,11])
    elif dist_type == 'hospitalized':
        data = getHospitalized(data)
        target_dates = pd.to_datetime(data[:,10])
    elif dist_type == 'ongoing':
        data = getOngoing(data)
        target_dates = pd.to_datetime(data[:,10])
    elif dist_type == 'actives':
        return data_actives(data,state,window)
    
    dates, data = getDataType(data,distribution,target_dates)
    return [dates,data]

def plotCummulative(data, state, data_types):
    plotting_data = []
    for data_type in data_types:
        dates, processed_data = data_distribution(data, state, data_type, 'cummulative')
        plotting_data.append([dates, processed_data, data_type])
    
    plt.close('all')
    plt.rcParams["figure.figsize"] = (15,6)

    for plot_data in plotting_data:
        dates = plot_data[0]
        cummulative_data = plot_data[1]
        data_type = plot_data[2]
        if data_type == 'deaths':
            plt.plot(dates, cummulative_data, label= data_type, color='r')
        else:
            plt.plot(dates, cummulative_data, label= data_type)
        plt.scatter(dates[-1], cummulative_data[-1])
        plt.text(dates[-1], cummulative_data[-1],str(int(cummulative_data[-1])) , fontsize=14)

    if state in ['nacional','all']:
        state = 'Mexico'
    today = str(plotting_data[0][0][-1])[:10]
    today = today[:5] + str(calendar.month_name[int(today[5:7])]) + today[7:]

    plt.title(''.join(data_type.capitalize() + ' ' for data_type in data_types) + state.capitalize(), fontsize=18)
    plt.suptitle(today, fontsize= 18)
    plt.ylabel('Number of Patients', fontsize=16)
    plt.xlabel('Dates', fontsize=16)
    plt.xticks(rotation=75)
    plt.legend(loc='upper left',fontsize=14)
    plt.show()

def plotDiscrete(data, state, data_types):
    plotting_data = []
    for data_type in data_types:
        dates, processed_data = data_distribution(data, state, data_type, 'discrete')
        plotting_data.append([dates, processed_data, data_type])
    
    plt.close('all')
    plt.rcParams["figure.figsize"] = (15,6)

    for plot_data in plotting_data:
        dates = plot_data[0]
        discrete_data = plot_data[1]
        data_type = plot_data[2]
        if data_type == 'deaths':
            plt.bar(dates, discrete_data, label= data_type, color='r')
        else:
            plt.bar(dates, discrete_data, label= data_type, alpha = 0.7)
    if state in ['nacional','all']:
        state = 'Mexico'
    today = str(plotting_data[0][0][-1])[:10]
    today = today[:5] + str(calendar.month_name[int(today[5:7])]) + today[7:]       

    plt.title(''.join(data_type.capitalize() + ' ' for data_type in data_types) + state.capitalize(), fontsize=18)
    plt.suptitle(today, fontsize= 18)
    plt.ylabel('Number of Patients', fontsize=16)
    plt.xlabel('Dates', fontsize=16)
    plt.xticks(rotation=75)
    plt.legend(loc='upper left',fontsize=14)
    plt.show()

def plotActives(data, states, window = 14):
    plotting_data = []
    for state in states:
        dates, processed_data = data_distribution(data, state, 'actives', window)
        plotting_data.append([dates, processed_data, state])
    
    plt.close('all')
    plt.rcParams["figure.figsize"] = (15,6)

    for plot_data in plotting_data:
        dates = plot_data[0]
        actives = plot_data[1]
        state = plot_data[2]

        if state in ['nacional','all']:
            state = 'Mexico'
        
        plt.plot(dates, actives, label = state.capitalize())
        plt.scatter(dates[-1], actives[-1])
        plt.text(dates[-1], actives[-1],str(int(actives[-1])) , fontsize=14)
    
    today = str(plotting_data[0][0][-1])[:10]
    today = today[:5] + str(calendar.month_name[int(today[5:7])]) + today[7:]

    plt.title(''.join(state.capitalize() + ', ' for state in states) + '- Actives Patients -', fontsize=18)
    plt.suptitle(today, fontsize= 18)
    plt.ylabel('Active Patients', fontsize=16)
    plt.xlabel('Dates', fontsize=16)
    plt.xticks(rotation=75)
    plt.legend(loc='upper left',fontsize=14)
    plt.show()

def sectors(data):
    plt.close('all')
    plt.rcParams["figure.figsize"] = (15,25)
    
    sector_bins = {patients_codes['sector'][key]:list(data[:,3]).count(key) for key in set(data[:,3])}
    ordered = OrderedDict(sorted(sector_bins.items(), key=lambda t: t[1],reverse=True))
    top = list(ordered.keys())[:2]
    others= list(ordered.keys())[2:]
    
    fig, axs = plt.subplots(3)
    plt.subplots_adjust(left=None, bottom=None, right=None, top=0.8, wspace=0.5, hspace=0.6)
    
    axs[0].bar(top,[sector_bins[x] for x in top], alpha=0.5)
    axs[0].text(-.05, sector_bins[top[0]] + (sector_bins[top[0]]*0.06), str(round((sector_bins[top[0]]/sum(ordered.values())*100),2))+'%', color='black',fontsize=20)
    axs[0].text(.95, sector_bins[top[1]] + (sector_bins[top[1]]*0.06), str(round((sector_bins[top[1]]/sum(ordered.values())*100),2))+'%', color='black',fontsize=20)
    axs[0].set_title('Sectors with more patients',fontsize=20, pad=30)
    axs[0].set_ylim(0,(max(sector_bins[top[0]],sector_bins[top[1]])+ 100000))
    axs[0].set_ylabel('Number of Patients', fontsize=18)

    axs[1].bar(others,[sector_bins[x] for x in others],alpha = 0.6)
    axs[1].set_title('Other sectors',fontsize=20, pad=30)
    axs[1].set_ylabel('Number of Patients', fontsize=18)

    for ind,sector in enumerate(others):
        axs[1].text(ind-0.3, sector_bins[sector] + (sector_bins[sector]*0.05), str(round((sector_bins[sector]/sum(ordered.values())*100),2))+'%', color='black',fontsize=16)

    proportions = []
    for sector in ordered.keys():
        sector_data = getSectorData(data,sector)
        
        try:
            deaths_by_sector = (len(getDeathData(sector_data))/len(sector_data))*100
        except:
            deaths_by_sector = 0
        proportions.append(deaths_by_sector)

    axs[2].bar([x for x in ordered.keys()],proportions,alpha = 0.6, color ='r')
    axs[2].set_title('Death rate for sector', fontsize=23)
    axs[2].set_ylabel('Percentage of Patients', fontsize=18)
    axs[2].set_ylim(0,(max(proportions)+ 10))

    for ind,sector in enumerate(ordered.keys()):
        axs[2].text(ind-0.3, proportions[ind] +1.5, str(round(proportions[ind],2))+'%', color='black',fontsize=14)

    for ax in fig.axes:
        plt.sca(ax)
        plt.xticks(rotation=65,fontsize=16)

    plt.show()