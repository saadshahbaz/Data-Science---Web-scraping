# Web-scraping

## The goal of this project is to get all the relationships of a multiple celebrities and return the output as a json file. 

## Goal
Writing a script that collects the relationships for a set of celebrities provided in a JSON configuration file. The code is to be written in such a way that when run twice on a specific celebrity, it will use data exclusively from the cache the second time.

## To run this file, you will need the following things:
1. collect_relationships.py
2. An empty directory
3. A json file consiting the name of the directory and all the names of the celebrities who's output we want (an example can be found in the repository)


## In the terminal, run the following command

`$ python collect_relationships.py -c <config-file.json> -o <output_file>`

## Required libraries:
#### 1. BeautifulSoup
   to install beautifulsoup please run the following command in your command line: `$ pip install beautifulsoup4` 
    
#### 2. Pandas
   to install pandas please following command in your command line: `$ pip install pandas` 
    
#### 3. requests
   to install requests please following command in your command line: `$ pip install requests` 
    

#### The website use for scraping is: https://www.whosdatedwho.com/
        
