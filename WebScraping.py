#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 13:59:35 2020

@author: christopher
"""

# Imports 
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import os
import pymysql
from sqlalchemy import create_engine


def link_acquisition():
    # Get soup - and define url of genre website
    url = 'https://www.game.co.uk/en/games/?attributeName1=Release%20Date&sortColumn=popular&sortTypeStr=DESC&inStockOnly=true&listerOnly=true&attributeValue1=4294965823&sortBy='
    html = requests.get(url).content
    soup = BeautifulSoup(html,'lxml')
    # Get only genre list and #
    # div.genre a to select genre div. a has text of genre and span contains the number of games in that genre
    genre_list=[i.text.strip().replace('\xa0','.') for i in soup.select('div.genre a')]
    # To find website forward links, save all numbers in url linked to genre page
    genre_web_page = [re.findall(r'2=(\d+)',i['href']) for i in soup.select('div.genre a')]
    genre_web_page_flat = []
    # Turn web page numbers into ints
    for i in genre_web_page:
        for x in i:
            genre_web_page_flat.append(int(x))
    # Create a dataframe from genre, with columns = genre, rows = number of games in genre
    df = pd.DataFrame([i.split('.') for i in genre_list], columns=['Genre','Number'])
    # Clean number colums
    df.Number = df.Number.str.strip(')(')
    df.Number = df.Number.str.replace(',','')
    df.Number = pd.to_numeric(df.Number)
    # add Genre web link to df
    df['Web'] = genre_web_page_flat
    # Export database to mysql
    engine = create_engine('mysql+pymysql://root:{}')
    df.to_sql(name='Genre', con=engine, if_exists = 'append')
    return df

def link_wrangling(df):
    # Sort df by most popular genre
    df.sort_values(by='Number', ascending=False, inplace=True)
    # New database with only top 10 most popular genres to scrape
    df = df.head(10)
    return df

def data_acquisition(df):
    # Create df of games
    Game_df = pd.DataFrame()
    # Combine genre and web link and loop through it via zip
    for genre,web in zip(df.Genre, df.Web):
        # loop through top 10 genre, and scrape 
        for k in range(1,len(df)):
            url = f'https://www.game.co.uk/en/games/?attributeName1=Release%20Date&sortColumn=popular&sortTypeStr=DESC&inStockOnly=true&listerOnly=true&attributeValue2={web}&attributeValue1=4294965823&sortBy=&attributeName2=Genre&pageSize=96&pageNumber={k}'
            html = requests.get(url).content
            soup = BeautifulSoup(html,'lxml')
            # Create lists of each item on page
            Name = [i.text for i in soup.select('article.product h2>a')]
            New_Price = [0 if i.find('div', {'class':'priceContainer'}).find('a',{'class':'mintPrice'}) is None else float(i.find('div', {'class':'priceContainer'}).find('a',{'class':'mintPrice'}).find('span').text[1:].replace(',','')) for i in soup.find_all('article',{'class': 'product'})]
            Preowned_Price = [0 if i.find('div', {'class':'priceContainer'}).find('a',{'class':'preownedPrice'}) is None else float(i.find('div', {'class':'priceContainer'}).find('a',{'class':'preownedPrice'}).find('span').text[1:].replace(',','')) for i in soup.find_all('article',{'class': 'product'})]
            Download_Price = [0 if i.find('div', {'class':'priceContainer'}).find('a',{'class':['preownedPrice','downloadPrice']}) is None else float(i.find('div', {'class':'priceContainer'}).find('a',{'class':['preownedPrice','downloadPrice']}).find('span').text[1:].replace(',','')) for i in soup.find_all('article',{'class': 'product'})]
            Other_Price = [0 if i.find('div', {'class':'priceContainer'}).find('a',{'class':'other'}) is None else float(i.find('div', {'class':'priceContainer'}).find('a',{'class':'other'}).find('span').text[1:].replace(',','')) for i in soup.find_all('article',{'class': 'product'})]
            Console = [i.text.strip() for i in soup.select('article.product>div.productHeader>span.platformLogo')]
            # Create temp df to store information of page
            df2 = pd.DataFrame()
            # Assign values into columns
            df2['Name'] = Name
            df2['New_Price'] = New_Price
            df2['Preowned_Price'] = Preowned_Price
            df2['Download_Price'] = Download_Price
            df2['Other_Price'] = Other_Price
            df2['Console'] = Console
            df2['Genre'] = genre
            # Append to game list df
            Game_df = Game_df.append(df2)
    return Game_df

def data_wrangling(Game_df):
    # clean up Console column 
    Game_df.Console = Game_df.Console.str.strip(')(')
    # Reset index if needed, inplace =save and drop = drops old index
    Game_df.reset_index(inplace=True, drop=True)
    # Import to mysql database
    engine = create_engine('mysql+pymysql://root:{}')
    Game_df.to_sql(name='Game', con=engine, if_exists = 'append')
    # save to csv
    Game_df.to_csv('Game_df.csv', sep=' ', index=False)

def analysis():
    # Read database from MySQL
    engine = create_engine('mysql+pymysql://root:{}')
    # Select avg New/Preowned Sale price for each genre
    data = pd.read_sql_query('SELECT avg(New_Price) as New, avg(Preowned_Price) as Preowned, Genre FROM Game GROUP BY Genre;', engine)
    # Find difference between new and preowned sale price/new price per genre
    data2 = pd.read_sql_query('select round(((New - Preowned)/New *100),2) as Loss, Genre from (select avg(New_Price) as New, avg(Preowned_Price) as Preowned, Genre from Game group by Genre) x group by Genre order by Loss DESC;', engine)
    #Find post popular consoles
    data3 = pd.read_sql_query('select count(Name) as titles, Console from Game group by Console order by titles DESC limit 5;', engine)
    data3.set_index('Console', inplace = True)
    data3.rename(columns={'titles':'Titles'}, inplace=True)
    return data,data2,data3

def report(data,data2,data3):
    # Set color scheme
    colors = ["#b64040", "#ffc002", "#de4223", "#ffad2c", "#e69138"]
    # Create plot for genre
    plot =data.plot.bar(x='Genre', color =colors,figsize=(10,5))
    fig = plot.get_figure()
    fig.savefig('Genre.png',dpi=600,bbox_inches = "tight")
    # Create plot for profit loss
    plot2 = data2.plot.bar(x='Genre', color=colors)
    fig2 = plot2.get_figure()
    fig2.savefig('Loss.png',dpi=600,bbox_inches = "tight")
    # Create plot for console
    plot3 =data3.plot.pie(y='Titles',autopct='%1.0f%%',explode=(0.15, 0, 0, 0, 0), colors = colors)
    plot3.legend(loc='center left', bbox_to_anchor=(1, 0.7))
    fig3= plot3.get_figure()
    fig3.savefig('console.png',dpi=600,bbox_inches = "tight")
    
def pipeline():
    link_acquisition().pipe(link_wrangling).pipe(data_acquisition).pipe(data_wrangling).pipe(analysis).pipe(report)
    
pipeline()


