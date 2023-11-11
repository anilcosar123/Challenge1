import pandas as pd

#extract the file here



#insert data from file into columns
mydataset = {
    'time': [15.04],
    'statBVP': [100],
    'statIBI': [50],
    'statHR': [60]    
    }


#showcase the info in a frame build UI
myvar = pd.DataFrame(mydataset)





print(myvar)