# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 13:02:59 2020

@author: Sriram
"""

import subprocess
import os
import pandas as pd
import numpy as np
from datetime import datetime

# Check Working directory and set the path
if os.path.split(os.getcwd())[-1]=='notebooks':
    os.chdir("../")

# Function to pull latest data from John Hopkins GITHUB page
def get_john_hopkins():
    'We use git pull to save the data in the folder COVID-19. Data saved as csv files under various names'
    git_pull = subprocess.Popen( "git pull" , 
                     cwd = os.path.dirname( 'data/raw/COVID-19/' ), 
                     shell = True, 
                     stdout = subprocess.PIPE, 
                     stderr = subprocess.PIPE )
    (out, error) = git_pull.communicate()
    
    print("Error : " + str(error)) 
    print("out : " + str(out))

if __name__ == '__main__':
    get_john_hopkins()