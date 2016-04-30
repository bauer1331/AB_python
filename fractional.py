# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 12:34:11 2015

@author: andrewbrown
"""

def fractional_deliv(media_type, curr_adv, sf):
    import pandas as pd
    # Find total cpm-days and contracted imps for specified media type.   
    curr_adv_mt = curr_adv[curr_adv['media_type'] == media_type]    
    curr_adv_mt_cpm_days = sum(curr_adv_mt['cpm-days'])
    if curr_adv_mt_cpm_days < 1:
        return None
    sf_adv_mt = (sf[(sf['Opportunity Name'] == curr_adv_mt.iloc[0,0]) 
                & (sf['Product Name'] == media_type)])
    if len(sf_adv_mt) < 1:
        return None
    sf_adv_mt.reset_index(drop = True)   # do we need this line?
    curr_adv_mt = curr_adv_mt.reset_index(drop = True)
    product_imps = sf_adv_mt.iloc[0,1]
    
    # Get expected fractional delivery for each of the current campaigns.
    # Assumes there are no duplicate campaigns in input file.
    # Put fractional delivery, campaign name, media type in a separate DF.
    fractional_delivery = pd.DataFrame(columns = ['campaign_name', 'media_type',
                                       'fractional_delivery'])    
    for j in xrange(0, len(curr_adv_mt)):
        temp_fractional_deliv = pd.DataFrame(0, index = [0], columns = 
        ['campaign_name', 'media_type', 'fractional_delivery'])
        expected_fractional_deliv = (curr_adv_mt.iloc[j,14]
                                    / curr_adv_mt_cpm_days)

            
        temp_fractional_deliv.iloc[0,0] = curr_adv_mt.iloc[j,1]
        temp_fractional_deliv.iloc[0,1] = curr_adv_mt.iloc[j,6]
        expected_imps = expected_fractional_deliv * product_imps
        actual_fractional_deliv = curr_adv_mt.iloc[j,2] / expected_imps
        temp_fractional_deliv.iloc[0,2] = actual_fractional_deliv
        fractional_delivery = fractional_delivery.append(temp_fractional_deliv,
                                                         ignore_index = True)
    return fractional_delivery
