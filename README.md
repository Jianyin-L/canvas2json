# Canvas to Json
Scrape HTML canvas and save it to json.  


## Features
Scrape HTML canvas in urls listed in a txt file and save them as json.  
If needed, the canvas element can also be saved as png file.  
Note the code is based on Firefox.  


## Steps
1. Clone this repository
2. Install dependencies
`pip install -r requirements.txt`
3. Specify the absolute path to the Webdriver in _canvas2json.py_ in line 18. 
4. Run the following command line  
`python3 canvas2json.py [txt file] [output folder] [whether to save png, 1 is yes]`  
sample command line  
`python3 canvas2json.py urls.txt result 1`  
This will scrape all the urls in the _urls.txt_ file and saved as json file in _result_ folder. png output will also be saved in _result_ folder.   


## To do
* Restore json to canvas
