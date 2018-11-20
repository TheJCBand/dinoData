import pandas as pd
import numpy as np
import csv
from sklearn.feature_extraction.text import CountVectorizer
import sklearn.model_selection

# Data format:
# X = [Specimen_Part, length, width, height, circumference]

def splitData(csvFile):
    XNum = []
    XString = []
    yString = []
    XCols = ['Specimen_Part', 'Length', 'Width', 'Height', 'Circumference']
    # XStringCols = ['Specimen_Part']
    # yCol = ['Accepted_Name']
    with open(csvFile) as file:
        # XData = np.genfromtxt(file, delimiter=',')
        # XData = pd.read_csv(file, usecols=XCols)
        # XStringData = pd.read_csv(file, usecols=XStringCols)
        # yData = pd.read_csv(file, usecols=yCol)
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row[5] == '':
                length = 0
            else:
                length = row[5]
            if row[6] == '':
                width = 0
            else:
                width = row[6]
            if row[7] == '':
                height = 0
            else:
                height = row[7]
            if row[8] == '':
                circumference = 0
            else:
                circumference = row[8]
            if row[10] == '':
                longitude = 0 
            else:
                longitude = row[10]
            if row[11] == '':
                latitude = 0
            else:
                latitude = row[11]
            yString.append(row[9])
            nextRow = [length, width, height, circumference, longitude, latitude]
            XNum.append(nextRow)
            XString.append(row[1])
    
    XNum = np.asarray(XNum, dtype = np.float)
    
    vectorizer = CountVectorizer()
    boneBag = vectorizer.fit_transform(XString)
    boneBagArray = boneBag.toarray()
    boneBagArray = np.asarray(boneBagArray, dtype = np.float)
    boneNames = vectorizer.get_feature_names()
    
    labelVec = CountVectorizer()
    speciesBag = labelVec.fit_transform(yString)
    y = speciesBag.toarray()
    y = np.asarray(y, dtype = np.float)
    speciesNames = labelVec.get_feature_names()
    
    X = np.concatenate((boneBagArray, XNum), axis=1)
    
    X_train, X_testCV, y_train, y_testCV = sklearn.model_selection.train_test_split(X, y, test_size=0.4, random_state=0)
    X_crossVal, X_test, y_crossVal, y_test = sklearn.model_selection.train_test_split(X_testCV, y_testCV, test_size=0.5, random_state=0)    
    
    return X_train, X_crossVal, X_test, y_train, y_crossVal, y_test
