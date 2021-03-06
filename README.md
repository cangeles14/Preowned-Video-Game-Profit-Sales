# Web Scraping Game.co.uk for Preowned Video Game Profit Sales

Web scraping is the process of automatically extracting data from websites and saving that data collected into a dataset allowing you to use that data to extract information. It’s one of the most efficient ways to get data from the web. Some practices inlcude 

- Research for web content or business intelligence
- Pricing for travel booker sites/price comparison sites
- Finding sales leads/conducting market research by crawling public data sources
- Sending product data from an e-commerce site to another online vendor

## Purpose

In this project I will create a pipeline that will web scrap a video game sales website using Python, Pandas, and BeautifulSoup. I will collect the data recieved and create a dataset utilizing Pandas and Python, and MySQL. Using this dataset, I will make a general analysis on the data collected. And finally, report this dataset analysis using visuals made in python and with matplotlib library. 

## Getting Started

Finding a website to scrape - in this case I used an online market for video games

- [Game.co.uk](https://game.co.uk)

## Examining The Website 

There are two major techniqes used in web scraping. Using HTML to target web page tags, or using an API to extract data. In this case, I will use HTML tags and BeautifulSoup library to target key web page tags, and retrieve the speceific information.

BeautifulSoup will get the URL and the element tags of that web page, and extract the elements you specify. Using this, I am able to collect sale prices for each video game per genre of video games.

By creating function that can loop through all the URls for each genre webapge and save them, I am able to create a dataset with just the URLs of websites I want to scrape. This will allow me to loop through the webpages and collect the data thats associated with each genre, rather than all the game titles at once.

![URLs](https://github.com/cangeles14/VideoGameSalesWebScrapping/blob/master/Images/urls.png)

Next is to scrape the URL contents for the game titles, and various data associated with each title; new price, preowned price, or the console its on. I then created a dataset with each titles per genre

![Dataset](https://github.com/cangeles14/VideoGameSalesWebScrapping/blob/master/Images/dataset.png)

## Cleaning The Data & Creating the Dataset

Cleaning data is one of the most important factors to accuratly analyzing and describing your data. In this case, some data was cleaned before it was stored into the dataset, allowing for little cleaning after creating the dataset.

<img src="https://github.com/cangeles14/VideoGameSalesWebScrapping/blob/master/Images/datacleaning.png" width="50%" height="50%">

We can also save the our dataset into MySQL for future queries.

## Analysing Data with MySQL

MySQL is a powerful tool to analyze datasets. Here I will show a simple query to take a look at my dataset. Exploration of data is important for determining what insights you can extract from your dataset.

<img src="https://github.com/cangeles14/VideoGameSalesWebScrapping/blob/master/Images/MySQL%20Genre%20Avg%20Prices.png" width="50%" height="50%">

## Analysing Data with MatPlotLib

Next I will transform the information found in the dataset into  powerful visuals that will help me explain the information I found. Here I will demonstate this using MatPlotLib library in Python. 

<img src="https://github.com/cangeles14/VideoGameSalesWebScrapping/blob/master/Images/MatPlotLib.png" width="50%" height="50%">

## Storytelling of Data in a Presentation

For this project, Ironhack tasked me in presenting my project in a real life senario to simulate the process of collecting, cleaning, and presenting my analysis. For this project I assume my client was a French Video Game Shop looking to increase their inventory in pre-owned games. They wanted to know which titles they should purchase as pre-owned to resell at their shop with the most profit.

To do this I collected data, and found which titles sell higher than new titles, thus profitting more for selling a particular pre-owned title.

The presentation is as a powerpoint below.

<img src="http://g.recordit.co/lDme5PjuLc.gif" width="50%" height="75%">

## Built With

* [Python](https://docs.python.org/3/) - The programming language used
* [Pandas](https://pandas.pydata.org/pandas-docs/stable/index.html) - library providing high-performance, easy-to-use data structures and data analysis tools for the Python programming language
* [MySQL](https://www.mysql.com/) -  MySQL is an open-source relational database management system for SQL
* [Tableau](https://www.tableau.com/) - Popular Data visualization tool
* [MatPlotLib](https://matplotlib.org/contents.html) - Matplotlib is a Python 2D plotting library which produces publication quality figures in a variety of hardcopy formats and interactive environments across platforms
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Python library for pulling data out of HTML and XML files

## Authors

* **Christopher Angeles** - [cangeles14](https://github.com/cangeles14)

## Acknowledgments

* [Ironhack](https://www.ironhack.com/en/data-analytics) -  Data Analytics Bootcamp @ Ironhack Paris

