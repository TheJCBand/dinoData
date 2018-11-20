#!/usr/bin/env python

import requests
import os
import csv
import pandas as pd
from collections import OrderedDict

def getData(dinosaurs,threshold):

    specimenNo = []
    specimenPart = []
    identifiedName = []
    acceptedName = []
    acceptedRank = []
    length = []
    width = []
    height = []
    circumference = []
    genus = []
    longitude = []
    latitude = []

    csvHeader = ['Specimen_Number',
        'Specimen_Part',
        'Identified_Name',
        'Accepted_Name',
        'Accepted_Rank',
        'Length',
        'Width',
        'Height',
        'Circumference',
        'Genus',
        'Longitude',
        'Latitude']
    
    noRec = 'THIS REQUEST RETURNED NO RECORDS'
    serverError = ['<html><head><title>500 Server Error</title></head>']
    
    baseUrl = 'https://paleobiodb.org/data1.2/specs/list.csv?base_name='
    specIdUrl = 'https://paleobiodb.org/data1.2/specs/measurements.csv?spec_id='

    if not os.path.exists('dinoData'):
        os.makedirs('dinoData')

    for species in dinosaurs:
        noData = False
        url = '%s%s%s'%(baseUrl,species,'&show=genus,coords')
        r = requests.get(url, allow_redirects=True)
        with open('data/%s.csv'%(species), 'wb') as csvfile:
            csvfile.write(r.content)
        
        with open('data/%s.csv'%(species), 'r') as csvfile:
            csvFileReader = csv.reader(csvfile)
        
            noData = next(csvFileReader) == serverError
            # next(csvFileReader)
            for checkRow in csvFileReader:
                if noData == False:
                    noData = checkRow[0] == noRec
        with open('data/%s.csv'%(species), 'r') as csvfile:
            csvFileReader = csv.reader(csvfile)
            next(csvFileReader)
            specimenCounter = []
            if noData == False:
                for row in csvFileReader:
                    specimenCounter.append(row[0])
            nSpecimens = len(specimenCounter)
            if nSpecimens >= threshold:
                with open('data/%s.csv'%(species), 'r') as csvfile:
                    csvFileReader2 = csv.reader(csvfile)
                    next(csvFileReader2)
                    for row2 in csvFileReader2:
                        specimenNo.append(row2[0])
                        specimenPart.append(row2[9])
                        identifiedName.append(row2[15])
                        acceptedName.append(row2[19])
                        acceptedRank.append(row2[20])
                        genus.append(row2[25])
                        longitude.append(row2[26])
                        latitude.append(row2[27])
    
    for specimen in specimenNo:
        specUrl = '%s%s'%(specIdUrl,specimen)
        specReq = requests.get(specUrl, allow_redirects=True)
        open('data/Specimen%s.csv'%(specimen), 'wb').write(specReq.content)
        measurements = pd.read_csv('data/Specimen%s.csv'%(specimen), usecols=['measurement','average'])
        measLabels = measurements['measurement'].tolist()
        measVals = measurements['average'].tolist()
        if 'length' in measLabels:
            lengthIndex = measLabels.index('length')
            length.append(measVals[lengthIndex])
        else:
            length.append('')
        if 'width' in measLabels:
            widthIndex = measLabels.index('width')
            width.append(measVals[widthIndex])
        else:
            width.append('')   
        if 'height' in measLabels:
            heightIndex = measLabels.index('height')
            height.append(measVals[heightIndex])
        else:
            height.append('')
        if 'circumference' in measLabels:
            circumferenceIndex = measLabels.index('circumference')
            circumference.append(measVals[circumferenceIndex])
        else:
            circumference.append('')
    
    # print(specimenNo)
    
    df = pd.DataFrame(OrderedDict({
        csvHeader[0]: specimenNo,
        csvHeader[1]: specimenPart,
        csvHeader[2]: identifiedName,
        csvHeader[3]: acceptedName,
        csvHeader[4]: acceptedRank,
        csvHeader[5]: length,
        csvHeader[6]: height,
        csvHeader[7]: width,
        csvHeader[8]: circumference,
        csvHeader[9]: genus,
        csvHeader[10]: longitude,
        csvHeader[11]: latitude}))
    df.to_csv("data/allData.csv", sep=',',index=False)
    
    df = df[pd.isna(df['Genus']) == False]   
    df = df[pd.isna(df['Longitude']) == False]   
    df = df[pd.isna(df['Latitude']) == False]   
    
    return df
        
                
                
