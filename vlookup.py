# -*- coding: utf-8 -*-
"""
Andrew Brown 12-29-2015
Look up values from one or more columns in data frame obj and insert them into
data frame dataframe.  The lookup is accomplished by selecting the first row of 
obj where all of the columns in the keymapping dictionary have the same value.
The keys in keymapping correspond to the indices in dataframe of any columns
that should be used as keys; the values correspond to the indices in object of
they key columns.  A dictionary with n elements will thus require identical
values in all n columns betweeen dataframe and obj for a succesful match.

Specify the indices of columns in obj to be copied to dataframe by passing a
list of indices to objvals.

Labelmapping is a dictionary where the keys are the column names of the columns
from obj to be inserted and the values are the names the columns will have once
inserted into dataframe.
"""

def vlookup (dataframe, obj, keymapping, objvals, labelmapping):
    import pandas as pd
    new_data = pd.DataFrame()
    for i in range(len(dataframe)):
        for j in range(len(keymapping)):
            if j == 0:
                matches = obj[dataframe.iloc[i, keymapping.keys()[j]] == \
                obj.iloc[:,keymapping.values()[j]]]
            else:
                matches = matches[dataframe.iloc[i, keymapping.keys()[j]] == \
                matches.iloc[:,keymapping.values()[j]]]
        matches = matches.reset_index(drop = True)
        if len(matches) < 1:
            cols = obj.columns      
            no_match = pd.DataFrame('NA', index = [0], columns = cols)  
            for i in range(len(keymapping)):
                no_match.iloc[0,i] = keymapping.values()[i]
            new_data = new_data.append(no_match.iloc[0, objvals])
        else:
            new_data = new_data.append(matches.iloc[0, objvals])
    new_data = new_data.reset_index()
    dataframe = pd.concat([dataframe, new_data], axis = 1)
    
    # just select the columns we want - not the index column that was included
    good_cols = []
    for i in range(len(dataframe.columns)):
        if dataframe.columns[i] == 'index':
            continue
        else:
            good_cols.append(i)
    dataframe = dataframe.iloc[:,good_cols]
    
    # rename the inserted columns based on labelmapping
    j = 0
    for i in objvals:
        dataframe.rename(columns={labelmapping.keys()[j]: \
        				labelmapping.values()[j]}, inplace = True)
        j = j + 1
    return dataframe
