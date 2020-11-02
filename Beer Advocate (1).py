#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import datetime
import re
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import matplotlib.pyplot as plt
# Python program to convert a list to string 
    
# Function to convert   
def listToString(s):  
    
    # initialize an empty string 
    str1 = ""  
    
    # traverse in the string   
    for ele in s:  
        str1 += ele   
    
    # return string   
    return str1  







# In[2]:


# Importing production data from directory
import glob
import os
path = r"C:\Users\mmotd\OneDrive\Documents\Boot Camp Files\Beer Production"
all_files = glob.glob(path + "/*.xlsx")
production = pd.DataFrame()
for f in all_files:
    data = pd.read_excel(f)
    data = data[7:19]
    data = data[1:]
    date = re.findall('\d+', f)
    date = listToString(date)
    
    data['Year'] = date
    production = production.append(data)                                


# In[3]:


# Configuring columns and cleaning data
production = production.drop('Unnamed: 5', axis=1)    
production.columns = ['Barrels', 'Number of Breweries', 'Total Barrels', 'Taxable Removals', 'Total Exported', 'Year']
production.index = range(0,132)

production = production[production['Barrels'] != 'Barrels (31 gallons) (2)']
production = production[production['Barrels'] != 'Total']
production['Barrels'] = production['Barrels'].str.strip()


# In[4]:


production.describe


# In[5]:


# Converting columns to numeric type
cols = production.iloc[:,1:5].columns

production[cols] = production[cols].apply(pd.to_numeric, errors='coerce')
yearly_production = production.sort_values(by=["Year","Total Barrels"])
yearly_production.index  = range(0,130)
yearly_production.head(15)


# In[6]:



from matplotlib import pyplot
import seaborn as sns
import plotly.express as px
import plotly

num_breweries = px.line(yearly_production, x='Year', y='Number of Breweries', color='Barrels', 
                        title = 'Number of Brewery Trend by Production Capacity')

num_breweries.show()


# In[7]:


barrels = px.line(yearly_production, x='Year', y='Total Barrels', color='Barrels')
barrels.show()


# In[8]:


# Distinguishing craft brewery production range from macro
craft_beers = list(yearly_production["Barrels"][0:10])
other = ['1,000,000 to 6,000,000 Barrels (5)', '1,000,001 to 1,999,999 Barrels', '2,000,000 to 6,000,000 Barrels']
craft_beers = craft_beers + other
Classification = ['Craft' if i in craft_beers else "Macro" for i in yearly_production["Barrels"]]
yearly_production['Classification'] = Classification
craft_macro = pd.DataFrame(yearly_production.groupby(["Year", "Classification"]).agg("sum")).reset_index()
craft_macro.head()


# In[9]:


comparison_production = px.line(craft_macro, x='Year', y='Total Barrels', color='Classification', 
                                title = 'Craft and Macro Production over Time' )
comparison_production.show()


# In[10]:


# Calculating the yearly proportions of craft and macro production
yearly_total = craft_macro.groupby(["Year", "Classification"])["Total Barrels"].sum().reset_index()

yearly_prop = pd.DataFrame(yearly_total.groupby("Year")["Total Barrels"].apply(lambda x: 100 * x / float(x.sum())))

years = [i for i in yearly_total["Year"]]
yearly_prop["Year"] = years
yearly_prop["Classification"] = [i for i in yearly_total["Classification"]]
yearly_prop = yearly_prop.rename(columns = {'Total Barrels':"Percentage of Production"})
yearly_prop.head()


# In[11]:


import plotly.graph_objects as go

class_percentage = go.Figure()

class_percentage.add_trace(go.Bar(x=yearly_prop[yearly_prop['Classification'] == 'Craft']['Year'],
                y= yearly_prop[yearly_prop['Classification'] == 'Craft']['Percentage of Production'] ,
                name='Craft',
                marker_color='rgb(55, 83, 109)'
                ))
class_percentage.add_trace(go.Bar(x=yearly_prop[yearly_prop['Classification'] == 'Macro']['Year'],
                y= yearly_prop[yearly_prop['Classification'] == 'Macro']['Percentage of Production'],
                name='Macro',
                marker_color='rgb(26, 118, 255)'
                ))
class_percentage.update_layout(
    title='Brewery Classification Percentages',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title= 'Percentage',
        titlefont_size=16
    ),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)')),

class_percentage.show()


# In[12]:


# Reading in beer advocate data
beer_advocate = pd.read_csv("advocate_data.csv")
beer_advocate.head()


# In[13]:


# Data cleaning
beer_advocate = beer_advocate.dropna(subset = ['avg_rating'])
beer_advocate['total_rank'] = beer_advocate['total_rank'].filter(regex = '\d+')
beer_advocate.head()
beer_advocate['total_rank'] = beer_advocate['total_rank'].str.replace('<a href="/beer/top-rated/" class="Tooltip" title="Ranking against all beers. Click to view the Top 250 Rated Beers.">Ranked #',"")
beer_advocate['total_rank'] = beer_advocate['total_rank'].str.replace('</a>', '')
beer_advocate['total_rank'] = beer_advocate['total_rank'].str.replace(',', '')
beer_advocate['total_rank'] = beer_advocate['total_rank'].astype(float)
beer_advocate['style_rank'] = beer_advocate['style_rank'].str.replace('Ranked #',"")
beer_advocate['style_rank'] = beer_advocate['style_rank'].str.replace(',',"")
beer_advocate['style_rank'] = beer_advocate['style_rank'].astype(float)
beer_advocate['num_ratings'] = beer_advocate['num_ratings'].str.replace(',',"")
beer_advocate['num_ratings'] = beer_advocate['num_ratings'].astype(float)

beer_advocate['beer_desc'] = beer_advocate['beer_desc'].str.strip(',\n')


# In[14]:


beer_advocate.head()


# In[15]:


beer_advocate.describe()


# In[16]:


beer_advocate['beer_type'].unique()


# In[17]:


# Adding grading system for beer advocate score
beer_grade = ['A' if i >= 90 else 'B' if (i >= 80)
 and (i < 90) else 'C' if (i >= 70) and 
 (i < 80) else 'F' for i in beer_advocate['adv_score']]

beer_advocate['beer_grade'] = beer_grade
beer_advocate.head()


# In[18]:


# Aggregating beer_advocate data frame by beer_type and sorting by the mean of the avg rating column
style_agg = beer_advocate.groupby('beer_type').agg(['mean','min', 'max', 'count']).reset_index()
avg_rating_agg = style_agg.sort_values( [('avg_rating',  'mean')], ascending = False)
# Converting column names from tuples into single elements separated by "_"
avg_rating_agg.columns = ["_".join(x) for x in avg_rating_agg.columns.ravel()]


# In[19]:


# Creating a dataframe of the top 20 and bottom 20 beer styles by average rating
top_20_rating = avg_rating_agg.head(20)
bottom_20_rating = avg_rating_agg.tail(20)


# In[20]:


# Creating a dataframe consisting of the 20 highest rated beer styles for visualization aesthetics
top_20_styles = top_20_rating['beer_type_']
top_20_styles_df = beer_advocate[beer_advocate['beer_type'].isin(top_20_styles)]


# In[21]:


rating_dist = px.box().update_xaxes(categoryorder = 'total descending')
rating_dist.update_layout(
    title="Rating Distributions by Style",
    xaxis_title="Beer Style",
    yaxis_title="Average Rating"
    )
rating_dist.add_trace(go.Box(x = top_20_styles_df['beer_type'],
    y= top_20_styles_df['avg_rating'],
    name='Mean & SD',
    marker_color='royalblue',
    boxmean='sd' # represent mean and standard deviation
))
rating_dist.show()


# In[22]:


numrating_dist = px.box().update_xaxes(categoryorder = 'total descending')
numrating_dist.update_layout(
    title="Number of Ratings Distributions by Style",
    xaxis_title="Beer Style",
    yaxis_title="Number of Ratings"
    )
numrating_dist.add_trace(go.Box(x = top_20_styles_df['beer_type'],
    y= top_20_styles_df['num_ratings'],
    name='Mean & SD',
    marker_color='royalblue',
    boxmean='sd' # represent mean and standard deviation
))
numrating_dist.show()


# In[23]:


import plotly.graph_objects as go

rating_bar = px.bar(top_20_rating, x='beer_type_', y= 'avg_rating_mean',
             hover_data= ['num_ratings_mean', 'total_rank_mean'], 
             color= 'adv_score_mean')
rating_bar.update_layout(
    title="Average Rating for Top 20 Beer Styles",
    xaxis_title="Beer Style",
    yaxis_title="Average Rating",
    legend_title="Beer Advocate Score"
    
    )

rating_bar.show()


# In[24]:


bottom_bar = rating_bar = px.bar(bottom_20_rating, x='beer_type_', y= 'avg_rating_mean',
             hover_data= ['num_ratings_mean', 'total_rank_mean'], 
             color= 'adv_score_mean')
bottom_bar.update_layout(
    title="Average Rating for Bottom 20 Beer Styles",
    xaxis_title="Beer Style",
    yaxis_title="Average Rating",
    legend_title="Beer Advocate Score"
    
    )

bottom_bar.show()


# In[25]:


avg_pie = px.pie(top_20_rating, values='avg_rating_mean', 
                    names='beer_type_', title='Pie Chart of Beer Styles by Average Rating')
avg_pie.show()


# In[26]:


# Beer advocate has a ranking system for the beers on their website. Sorting beer_advocate by total rank
sorted_rank = beer_advocate.sort_values(by='total_rank').reset_index()
top_ranks_100 = sorted_rank.head(100)
top_ranks_50 = sorted_rank.head(50)


# In[27]:



style_hist = px.histogram(top_ranks_100, y="beer_type",
                         title = 'Beer Style Counts in Top 100').update_yaxes(categoryorder = 'total ascending')
style_hist.show()


# In[28]:


brewery_hist = px.histogram(top_ranks_50, y="brewery",
                         title = 'Brewery Counts in Top 50').update_yaxes(categoryorder = 'total ascending')
brewery_hist.show()


# In[29]:


# Aggregating top 100 beers by beer type to count the frequency of each beer type
style_counts = top_ranks_100.groupby("beer_type").agg({'beer_type' : ['count']}).reset_index()
style_counts.columns = ["_".join(x) for x in style_counts.columns.ravel()]
style_counts.columns
rating_pie = px.pie(style_counts, values='beer_type_count', names='beer_type_', title='Pie Chart of Beer Styles Counts in Top 100')
rating_pie.show()


# In[30]:


text = " ".join(review for review in top_ranks_100['beer_desc'])
stopwords = set(STOPWORDS)
stopwords.update(["Release","flavor", "beer", "glass", "amount", "drink"])
top_100_word_cloud = WordCloud(max_font_size=100, max_words=100, background_color="black").generate(text)

# Display the generated image:
plt.imshow(top_100_word_cloud, interpolation='bilinear')
plt.axis("off")
plt.show()


# A word cloud in this case can illuminate some of the primary characteristics of popular beers. Double IPA occurs frequently in the top 500 beers. It would appear that barrel aged beers, particularly bourbon barrel aged beers are very highly rated. 
