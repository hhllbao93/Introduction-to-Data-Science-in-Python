import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.



# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


def get_list_of_university_towns():
# Use this dictionary to map state names to two letter acronyms
    states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}
    mapping_states = pd.DataFrame({
      "State": list(states.values()),
      "StateAcronyms": list(states.keys())
    })
    Town_data = pd.DataFrame(); Town_list=pd.DataFrame()
    with open('university_towns.txt', 'r') as f:
        for line in f:
            Town_data = pd.concat( [Town_data, pd.DataFrame([tuple(line.strip().split(')'))])], ignore_index=True )
    Town_list=Town_data.iloc[:,0].copy().to_frame()
#    print(Town_data)
    Town_list.columns=['RegionName']#
#    print(Town_list)
    Town_list['RegionName'] = Town_list['RegionName'].str.replace(r"\(.*","")
    Town_list['RegionName'] = Town_list['RegionName'].str.replace(r"\s+$","")
    Town_list['StateFlag'] = Town_list['RegionName'].str.contains(pat=r'\[edit\]')
    States_list = Town_list[Town_list['StateFlag'] == True]
#    print(Town_list)
#find the states with different 
    States = States_list['RegionName'].str.replace(pat=r'\[edit\]', repl='').unique()
#    print(States)
    StateFlags = Town_list['StateFlag'].values
#    print(StateFlags)
    k = 0
    StateMatchRegion = [States[k]]
# assign states name to each city
    for i in range(1, len(StateFlags)):
        if StateFlags[i] == True:
            k += 1
        else:
            k += 0
        StateMatchRegion.append(States[k])
# data clearance -------------
    Town_list['StateMatchRegion'] = StateMatchRegion
    Town_list1=Town_list[Town_list['StateFlag'] == False]
    Town_list1 = Town_list1.drop(['StateFlag'], axis=1)
    Town_list1.columns = ['CityName','State']
    Town_list2 = pd.merge(Town_list1, mapping_states, how='left')
    Town_list3 = Town_list2[['State','CityName','StateAcronyms']]
    Town_list3.columns = ['State','RegionName','StateAcronyms']
#    Town_list2.index =Town_list1[['State','CityName']]
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    return Town_list3[['State','RegionName']]
get_list_of_university_towns()



def get_recession_start():
    global GDP_quarter
    GDP_data = pd.read_excel('gdplev.xls',index_col=4,skiprows=7,header=0)
    GDP_quarter = GDP_data[['Unnamed: 6']].iloc[212:,:]
    GDP_quarter.columns = ['GDP']
    GDP_quarter.index.name = 'date'
    recession_date = GDP_quarter.copy()
    recession_date.iloc[:,0]=0.0
#    print(GDP_quarter[30:])
    #    print(GDP_quarter.iloc[1])
    for j in range(1,len(GDP_quarter)-1):
#        print(GDP_quarter.iloc[j+1,0],GDP_quarter.iloc[j,0],GDP_quarter.iloc[j-1,0])
        if GDP_quarter.iloc[j,0]<GDP_quarter.iloc[j-1,0] and GDP_quarter.iloc[j+1,0]<GDP_quarter.iloc[j,0]:
            recession_date.iloc[j,0] = 1.0
#            print(GDP_quarter.iloc[j,0])
        else:
            recession_date.iloc[j,0] = 0.0
    recession_date.iloc[0,0] = 0.0
    recession_date.iloc[65,0] = 0.0
#    print(recession_date.iloc[20:,0])
    for j in range(1,len(GDP_quarter)-1):
         if (recession_date.iloc[len(GDP_quarter)-1-j,0]==1.0) and (recession_date.iloc[len(GDP_quarter)-2-j,0]==1.0):
                 recession_date.iloc[len(GDP_quarter)-1-j,0] = 0.0
#    print(recession_date.iloc[20:,0])
    recession_start = pd.Series(recession_date[recession_date['GDP']==1.0].index)
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''

    return recession_start[0]
get_recession_start()


def get_recession_end():
    start_date=get_recession_start()
    start_date=start_date
    start_date = pd.to_datetime(start_date)
#    print(start_date)  
    n=0
    recover_date = GDP_quarter.copy()
    GDP_quarter['date'] = pd.to_datetime(GDP_quarter.index)
#    print(GDP_quarter.iloc[0,1])
#    print(start_date.iloc[0,0])
    for j in range(2,len(GDP_quarter)):
#        print(GDP_quarter.iloc[j+1,1] )
        if GDP_quarter.iloc[j,1] >= start_date:
#            print(GDP_quarter.iloc[j+1,0],GDP_quarter.iloc[j,0],GDP_quarter.iloc[j-1,0])
            if GDP_quarter.iloc[j,0]>GDP_quarter.iloc[j-1,0] and GDP_quarter.iloc[j-1,0]>GDP_quarter.iloc[j-2,0]:
                recover_date.iloc[j,0] = 1.0
                n+=1
                if n >=1:
                    break
#                print(GDP_quarter.iloc[j,0])
            else:
                recover_date.iloc[j,0] = 0.0
        else:
            recover_date.iloc[j,0] = 0.0
    recover_date.iloc[j+1:,0] = 0.0
#    print(recover_date)
    recession_end = pd.Series(recover_date[recover_date['GDP']==1.0].index)
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
       
    return recession_end[0]
get_recession_end()

def get_recession_bottom():
    start_date=get_recession_start()
    end_date=get_recession_end()
    GDP_tmp1=GDP_quarter[GDP_quarter['date']>=pd.to_datetime(start_date)]
    GDP_tmp2=GDP_tmp1[(GDP_tmp1['date']<=pd.to_datetime(end_date))]
#    print(GDP_tmp2)
    GDP_bottom=GDP_tmp2[GDP_tmp2['GDP']==GDP_tmp2['GDP'].min()]
#    print(GDP_bottom)
    bottom_date=GDP_bottom.index
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    
    return bottom_date[0]
get_recession_bottom()



def convert_housing_data_to_quarters():
    states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}

    house_price = pd.read_csv('City_Zhvi_AllHomes.csv')
    mapping_states = pd.DataFrame({
      "State": list(states.values()),
      "StateAcronyms": list(states.keys())
    })
#    print(mapping_states)
    house_price1 = pd.merge(house_price, mapping_states, left_on='State', right_on='StateAcronyms')
#    house_price1.drop(['State_x'],axis=1)
#    print(house_price1)
    house_price1.set_index(['State_y','RegionName'],inplace=True)
    house_price2=house_price1.iloc[:,50:249]
#    print(house_price2)
    house_price2.sort_index(level=0,ascending=True, inplace=True)
    house_price2=house_price2.groupby(pd.PeriodIndex(house_price2.columns, freq='Q'), axis=1).mean()
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    
    return house_price2

convert_housing_data_to_quarters()


from scipy import stats
def run_ttest():
    start_date = get_recession_start()
    bottom_date = get_recession_bottom()
    date1 = start_date.index 
    start_date1=pd.Period(start_date,freq='Q-DEC')
    bottom_date1=pd.Period(bottom_date,freq='Q-DEC')
    house_price= convert_housing_data_to_quarters()
    Univ_list=get_list_of_university_towns()
    Univ_list.index=Univ_list[['State','RegionName']]
#    print(house_price.columns)
#    diff_price=pd.DataFrame()
#    diff_price['price_ratio']=house_price[start_date1].divide(house_price[bottom_date1])
    diff_price=house_price[start_date1-1]/(house_price[bottom_date])
#    print(Univ_list)

#    print(diff_price[list(Univ_list.index)])
#    diff_price.reset_index(inplace=True)
#    diff_price.dropna(inplace=True)
#    diff_price.sort_index(ascending=True, inplace=True)
    diff_college = diff_price[list(Univ_list.index)].dropna(axis=0)
    print(diff_college)
    diff_not_college_indices = set(diff_price.index) - set(diff_college.index)
    print(len(diff_not_college_indices))
    diff_not_college = diff_price.loc[list(diff_not_college_indices)]#.dropna()
    alpha = stats.ttest_ind(diff_college, diff_not_college,nan_policy='omit')
    print(diff_college.shape)
    print(diff_not_college.shape)
    mean1=(diff_college.mean())
    mean2=(diff_not_college.mean()) 
#    print(mean1,mean2)

    null_hypothesis=False
    if alpha[1] < 0.01:
        null_hypothesis = True
    if (mean1<mean2):
        better='university town'
    else:
        better='non-university town' 
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    return null_hypothesis, alpha[1], better

run_ttest()
