import csv
from collections import defaultdict
import glob, os, re
import numpy as np

bbest=dict()
for city in pop: #city is our tested epidemic center, for loop on all regions
    w=defaultdict(int) #create default dictionary for incoming trips in every region

    with open("OD_Matrix_daily_flows.csv",'r') as f:
        read=csv.reader(f,delimiter=',')
        next(read) #jump header
        for j,i in enumerate(read): #read lines
            n2=i[0] #origin of OD flow
            if n2==city: #if origin corresponds to designed epidemic hub
                d2=i[1] #destination of OD flow
                data=i[2] #read date of OD flow from dataset as number of days from start of the year
                #onset format must be the same
                if data<onset[d2]-7 and data>onset[d2]-21: 
                    #take mobility from 3 weeks before to one 1 week before of destination onset
                    w[d2]+=float(i[k]) #sum the inflow in area d2 from origin == city
        x,y=[],[]          
        for p in pop:
            if p!=city: #check the Pearson correlation for each origin wrt destinations incidence peaks
                x.append(log10((w[p]/pop[p]))) #fraction of inflow wrt to local population
                y.append(log10(peak[p]/pop[p])) #incidence peak
                
        R=np.corrcoef(x,y)[0][1]
        bbest[city]=R*len(x)/max(n_destinations) 
        #Pearson correlation * # of destionations / max # of destinations per any origin in the country
