Brainpicker is a web crawler specifically written for the wonderful site ["Brainpickings"](brainpickings.com) written by Maria Popova. It's purpose is to research Popovas 5000+ articles as a network to analyze her thought process and the many connections she draws between people and subjects.

Brainpicker is not intended for general use and therefore we do not see the use in packaging the application or deploying it. If anyone is interested in using or forking the application they are of course welcome to do so.

## Installation

Brainpicker is written in Python 3.6.0 so you are advised to set up a virtual environment and installing the requirements using:  
```pip install -r requirements.txt``` 

To actually run the application there are a few more requirements:
For the NER tagger you will need to have the [Stanford NER Server](https://nlp.stanford.edu/software/CRF-NER.shtml) application, a trained NER model (the 3 class model is sufficient) and Java version 1.8. Also the variables in the stanfordnerserver.sh file need to point to the location of these resources.

For the Classification of the tags you will also need the Averaged Perceptron Tagger from the nltk package. These can be obtained by running the ```download()``` command from the nltk package and selecting it from the 'models' tab in the download gui.