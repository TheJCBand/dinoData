import requests
import os

dinosaurs = ['Triceratops',
    'Tyrannosaurus',
    'Allosaurus',
    'Velociraptor',
    'Ankylosaurus',
    'Stegosaurus',
    'Apatosaurus',
    'Spinosaurus',
    'Iguanodon']

baseUrl = 'https://paleobiodb.org/data1.2/'
midUrl = '.csv?datainfo&rowcount&base_name='
dataOptions = ['occs/list',
    'specs/list',
    'specs/measurements',
    'occs/strata',
    'colls/list',
    'occs/diversity',
    'taxa/list',
    'taxa/opnions',
    'taxa/refs',
    'taxa/byref']
dataOptionTitles = ['Occurrences',
    'Specimens',
    'Measurements',
    'Geological_strata',
    'Collections',
    'Diversity_over_time',
    'Taxa',
    'Opinions',
    'Bibliographic_references',
    'Taxa_by_ref']


if not os.path.exists('dinoData'):
    os.makedirs('dinoData')

for species in dinosaurs:
    i = 0
    for option in dataOptions:
        url = '%s%s%s%s'%(baseUrl,option,midUrl,species)
        r = requests.get(url, allow_redirects=True)
        open('dinoData/%s_%s.csv'%(species,dataOptionTitles[i]), 'wb').write(r.content)
        i += 1
        
