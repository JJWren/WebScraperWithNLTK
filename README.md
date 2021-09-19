# WebScraperWithNLTK

This was meant to practice building a web scraper and using the NLTK library (Natural Language Translation Kit).

Currently, it scrapes through the given website and all of the landing page's links. It downloads all of the images into a local folder next to the script file
and compiles all the collected data into a table on a text file.

The NLTK I used performed... poorly, due to my bad design lol.
However, there is room for improvement such as using sentence fragments instead of words to gather context to decipher parts of speech.


## Future plans:
I plan on making a new program based around this concept for checking websites for malware (checking links, images, downloadables, etc).
If the mentioned sections contain potentially harmful instances, the site will be flagged and all scraping will halt.
A log will be appended to from the program containing all flagged websites.

This could easily be refactored for a variety of scraping purposes.
