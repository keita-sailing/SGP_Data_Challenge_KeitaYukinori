from bs4 import BeautifulSoup
from datetime import datetime
import numpy as np
    
def read_xml(file_name, read_option):
    with open(file_name) as doc:
        soup = BeautifulSoup(doc, "xml") #Read xml by BeautifulSoup
    
    if read_option == 'RaceStartTime':
        Starttimes = soup.Race.RaceStartTime['Start'].split('+')[0]
        s_format = '%Y-%m-%dT%H:%M:%S'
        return datetime.strptime(Starttimes, s_format)

    elif read_option == 'Mark':
        Marks = soup.Course.find_all('Mark')
        mark_dict = {mark['Name']: np.array([mark['TargetLat'], mark['TargetLng']]).astype('float64') for mark in Marks}
        return mark_dict
    
    elif read_option == 'Boundary' or read_option == 'Exclusion Zone':
        Boundaries = soup.find_all('CourseLimit')
        positions = [[limit['Lat'], limit['Lon']] for limits in Boundaries if limits['name'] == read_option for limit in limits.find_all('Limit')]
        positions.append(positions[0])
        return np.array(positions,  dtype='float64')