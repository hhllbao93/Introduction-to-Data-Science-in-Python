# ### Question 1 (20%)
# Load the energy data from the file `Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **energy**.
# 
# Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
# 
# `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']`
# 
# Convert `Energy Supply` to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.
# 
# Rename the following list of countries (for use in later questions):
# 
# ```"Republic of Korea": "South Korea",
# "United States of America": "United States",
# "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
# "China, Hong Kong Special Administrative Region": "Hong Kong"```
# 
# There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, 
# 
# 
# `'Bolivia (Plurinational State of)'` should be `'Bolivia'`, 
# 
# `'Switzerland17'` should be `'Switzerland'`.
# 
# 
# Next, load the GDP data from the file `world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 
# 
# Make sure to skip the header, and rename the following list of countries:
# 
# ```"Korea, Rep.": "South Korea", 
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"```
# 
# Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102) from the file `scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.
# 
# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 
# 
# The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
#        'Citations per document', 'H index', 'Energy Supply',
#        'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
#        '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
# 
# *This function should return a DataFrame with 20 columns and 15 entries.*


import pandas as pd
import numpy as np
def answer_one():
    a = pd.read_excel('Energy Indicators.xls',sheetname='Energy',index_col=2,skiprows=16,header=0,skipfooter=38)
    a = a.drop(['Unnamed: 0','Unnamed: 1'],axis=1)
    global energy, GDP, ScimEn, SciEn
    energy = a.reset_index()
    energy = energy.drop([0],axis=0)
    energy.columns=['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    energy.replace(to_replace="...",value=np.NaN,inplace=True)
    energy['Energy Supply']=energy['Energy Supply']*1000000
    energy['Country'] = energy['Country'].str.replace(r" \(.*\)","")
    energy['Country'] = energy['Country'].str.replace("[0-9()]+$", "")
    energy.replace('Republic of Korea','South Korea', inplace = True)
    energy.replace('United States of America','United States', inplace = True)
    energy.replace('United Kingdom of Great Britain and Northern Ireland','United Kingdom', inplace = True)
    energy.replace('China, Hong Kong Special Administrative Region','Hong Kong', inplace = True)
    print(energy.head())
    GDP = pd.read_csv('world_bank.csv',skiprows=4)
    GDP.replace('Korea, Rep.','South Korea', inplace = True)
    GDP.replace('Iran, Islamic Rep.', 'Iran', inplace = True)
    GDP.replace('Hong Kong SAR, China', 'Hong Kong', inplace = True)
    GDP.rename(columns={'Country Name': 'Country'},inplace=True)
    print(GDP.head())
    ScimEn=pd.read_excel('scimagojr-3.xlsx')
    print(ScimEn)
    col=['Country','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']
    GDP_tmp = GDP[col]
    SciEn=pd.merge(ScimEn.iloc[0:15], energy, how='inner', on='Country')
    SciEnGDP=pd.merge(SciEn, GDP_tmp, how='inner', on='Country')  
    SciEnGDP.index=SciEnGDP['Country']
    SciEnGDP.drop(['Country'], axis=1, inplace=True)
    print(SciEnGDP.columns)
    return SciEnGDP
answer_one()


# 
# ### Question 2 (6.6%)
# The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
# 
# *This function should return a single number.*
#    



get_ipython().run_cell_magic('HTML', '', '<svg width="800" height="300">\n  <circle cx="150" cy="180" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="blue" />\n  <circle cx="200" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="red" />\n  <circle cx="100" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="green" />\n  <line x1="150" y1="125" x2="300" y2="150" stroke="black" stroke-width="2" fill="black" stroke-dasharray="5,3"/>\n  <text  x="300" y="165" font-family="Verdana" font-size="35">Everything but this!</text>\n</svg>')



def answer_two():
    Top15 = answer_one() 
    col=['Country','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']
    GDP_tmp = GDP[col]
    SciEn=pd.merge(ScimEn, energy, how='inner', on='Country')  
    SciEn.index=SciEn['Country']
    SciEnGDP=pd.merge(SciEn, GDP_tmp, how='inner', on='Country')  
    print(SciEnGDP.head())
    SciEn2=pd.merge(ScimEn, energy, how='outer', on='Country')  
    SciEn2.index=SciEn2['Country']
    SciEnGDP2=pd.merge(SciEn2, GDP_tmp, how='outer', on='Country')  
    print(SciEnGDP2.head())
    loss_country = (len(SciEnGDP2.index))-(len(SciEnGDP.index))
    return loss_country
answer_two()


# ## Answer the following questions in the context of only the top 15 countries by Scimagojr Rank (aka the DataFrame returned by `answer_one()`)

# ### Question 3 (6.6%)
# What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)
# 
# *This function should return a Series named `avgGDP` with 15 countries and their average GDP sorted in descending order.*



def answer_three():
    Top15 = answer_one()
    col=['2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']
    avgGDP = (Top15[col].mean(axis=1))
    avgGDP.sort(ascending=False, inplace=True)
    return avgGDP
answer_three()


# ### Question 4 (6.6%)
# By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
# 
# *This function should return a single number.*



def answer_four():
    Top15 = answer_one()
    col=['2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']
    Top15["AvgGDP"] = answer_three()
    Top15.sort_values("AvgGDP", ascending=False, inplace=True)
    print(Top15.iloc[5,10:21])
    minv  = Top15.iloc[5,10:21].min()
    maxv  = Top15.iloc[5,10:21].max()
#    print(minv)
#    print(maxv)
    return maxv-minv
answer_four()


# ### Question 5 (6.6%)
# What is the mean `Energy Supply per Capita`?
# 
# *This function should return a single number.*



def answer_five():
    Top15 = answer_one()
    return Top15['Energy Supply per Capita'].mean()
answer_five()


# ### Question 6 (6.6%)
# What country has the maximum % Renewable and what is the percentage?
# 
# *This function should return a tuple with the name of the country and the percentage.*


def answer_six():
    Top15 = answer_one()
    value = Top15['% Renewable'].idxmax(), Top15['% Renewable'].max()
    return value
answer_six()


# ### Question 7 (6.6%)
# Create a new column that is the ratio of Self-Citations to Total Citations. 
# What is the maximum value for this new column, and what country has the highest ratio?
# 
# *This function should return a tuple with the name of the country and the ratio.*



def answer_seven():
    Top15 = answer_one()
    Top15['Self_total']=Top15['Self-citations']/Top15['Citations']
    return Top15['Self_total'].idxmax(), Top15['Self_total'].max()
answer_seven()


# ### Question 8 (6.6%)
# 
# Create a column that estimates the population using Energy Supply and Energy Supply per capita. 
# What is the third most populous country according to this estimate?
# 
# *This function should return a single string value.*

# In[108]:


def answer_eight():
    Top15 = answer_one()
    Top15['Population'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']
    Third = Top15['Population'].nlargest(3).index[2] 
    return Third
answer_eight()


# ### Question 9 (6.6%)
# Create a column that estimates the number of citable documents per person. 
# What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the `.corr()` method, (Pearson's correlation).
# 
# *This function should return a single number.*
# 
# *(Optional: Use the built-in function `plot9()` to visualize the relationship between Energy Supply per Capita vs. Citable docs per Capita)*



def answer_nine():
    Top15 = answer_one()
    Top15['Population'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['Population']
    Col2 = Top15[['Citable docs per Capita', 'Energy Supply per Capita']]
    corr = Col2.corr(method='pearson')
    return corr.iloc[0,1]
answer_nine()




def plot9():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    Top15.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])




#plot9() # Be sure to comment out plot9() before submitting the assignment!


# ### Question 10 (6.6%)
# Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
# 
# *This function should return a series named `HighRenew` whose index is the country name sorted in ascending order of rank.*



def answer_ten():
    Top15 = answer_one()
    data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    HighRenew = pd.Series(data,index=Top15.index)
    HighRenew[Top15['% Renewable']>=Top15['% Renewable'].median()]=1
    HighRenew.sort_index(ascending=True, inplace=True)
    return HighRenew
answer_ten()


# ### Question 11 (6.6%)
# Use the following dictionary to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
# 
# ```python
# ContinentDict  = {'China':'Asia', 
#                   'United States':'North America', 
#                   'Japan':'Asia', 
#                   'United Kingdom':'Europe', 
#                   'Russian Federation':'Europe', 
#                   'Canada':'North America', 
#                   'Germany':'Europe', 
#                   'India':'Asia',
#                   'France':'Europe', 
#                   'South Korea':'Asia', 
#                   'Italy':'Europe', 
#                   'Spain':'Europe', 
#                   'Iran':'Asia',
#                   'Australia':'Australia', 
#                   'Brazil':'South America'}
# ```
# 
# *This function should return a DataFrame with index named Continent `['Asia', 'Australia', 'Europe', 'North America', 'South America']` and columns `['size', 'sum', 'mean', 'std']`*



def answer_eleven():
    Top15 = answer_one()
    Top15['Population'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    Top15['Continent'] = pd.Series(ContinentDict)
    tmp = Top15[['Population','Continent']]
    sizev = tmp.groupby(['Continent']).count().astype(float)
    sumv = tmp.groupby(['Continent']).sum()
    meanv = tmp.groupby(['Continent']).mean()
    stdv = tmp.groupby(['Continent']).std()
    Group1= pd.merge(sizev,sumv,left_index=True, right_index=True)
    Group2= pd.merge(meanv,stdv,left_index=True, right_index=True)
    Group = pd.merge(Group1,Group2,left_index=True, right_index=True)
    Group.columns= ['size', 'sum', 'mean', 'std']
    print(Group)
    return Group
answer_eleven()


# ### Question 12 (6.6%)
# Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?
# 
# *This function should return a __Series__ with a MultiIndex of `Continent`, then the bins for `% Renewable`. Do not include groups with no countries.*

def answer_twelve():
    Top15 = answer_one()
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    Top15['Continent'] = pd.Series(ContinentDict)    
    Top15['bins']=(pd.cut(Top15['% Renewable'], 5))
    tmp = Top15[['Continent','bins']]
    tmp1 = tmp.groupby([tmp['Continent'],tmp['bins']]).size()
    return tmp1
answer_twelve()


# ### Question 13 (6.6%)
# Convert the Population Estimate series to a string with thousands separator (using commas). Do not round the results.
# 
# e.g. 317615384.61538464 -> 317,615,384.61538464
# 
# *This function should return a Series `PopEst` whose index is the country name and whose values are the population estimate string.*


def answer_thirteen():
    Top15 = answer_one()
    Top15['Population'] = Top15['Energy Supply']/Top15['Energy Supply per Capita'] 
    print (Top15['Population'])
    Top15['PopEst'] = Top15['Population'].apply(lambda x: "{:,}".format(x))
    print(type(Top15['PopEst']))
    return Top15['PopEst']
answer_thirteen()


# ### Optional
# 
# Use the built in function `plot_optional()` to see an example visualization.

def plot_optional():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    Top15 = answer_one()
    ax = Top15.plot(x='Rank', y='% Renewable', kind='scatter', 
                    c=['#e41a1c','#377eb8','#e41a1c','#4daf4a','#4daf4a','#377eb8','#4daf4a','#e41a1c',
                       '#4daf4a','#e41a1c','#4daf4a','#4daf4a','#e41a1c','#dede00','#ff7f00'], 
                    xticks=range(1,16), s=6*Top15['2014']/10**10, alpha=.75, figsize=[16,6]);

    for i, txt in enumerate(Top15.index):
        ax.annotate(txt, [Top15['Rank'][i], Top15['% Renewable'][i]], ha='center')

    print("This is an example of a visualization that can be created to help understand the data. This is a bubble chart showing % Renewable vs. Rank. The size of the bubble corresponds to the countries' 2014 GDP, and the color corresponds to the continent.")

#plot_optional() # Be sure to comment out plot_optional() before submitting the assignment!





