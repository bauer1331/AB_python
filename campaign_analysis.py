# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 13:34:28 2015

@author: andrewbrown
"""
def campaign_analysis(appnexus, DBM, uber, salesforce):
    # Read in files and select + order desired columns    
    import pdb    
    import pandas as pd
    from vlookup import vlookup
    from fractional import fractional_deliv
    an = pd.read_csv(appnexus)
    dbm = pd.read_csv(DBM)
    ub = pd.read_csv(uber)
    sf = pd.read_csv(salesforce)
    an_columns_to_select = ["advertiser", "campaign", "imps", "clicks",
                            "imps_viewed", "view_measured_imps", "media_type",
                            "AV", "RTR", "ROS", "AUD", "cpm", "days", 
                            "Exchange"]
    dbm_columns_to_select = ["Advertiser", "Line Item", "Impressions",
                             "clicks", "Active View: Viewable Impressions",
                             "Active View: Measurable Impressions", 
                             "media_type","AV", "RTR", "ROS", "AUD", "cpm", 
                             "days", "Exchange"]
    an = an[an_columns_to_select]
    dbm = dbm[dbm_columns_to_select]
    
    # Standardize column names and consolidate to single data frame
    dbm.columns = ["advertiser", "campaign", "imps", "clicks", "imps_viewed",
                   "view_measured_imps", "media_type", "AV", "RTR", "ROS", 
                   "AUD", "cpm", "days", "Exchange"]
    combined = an.append(dbm)
    combined = combined.reset_index(drop=True)
    
    # Get the CPM-days for every campaign
    cpm_days = []
    for i in xrange(0, len(combined)):
        curr_cpm_days = combined.iloc[i, 11] * combined.iloc[i, 12]
        cpm_days.append(curr_cpm_days)        
    cpm_days = pd.Series(cpm_days)
    combined['cpm-days'] = pd.Series(cpm_days, index = combined.index)
    combined = combined.rename(columns = {0 : 'cpm-days'})
    
    # Get unique advertisers
    advertisers_set = set(combined.iloc[:,0])
    advertisers = list(advertisers_set)
        
    # Filter to data one advertiser at a time
    # Calculate and extract fractional delivery - the percentage of expected imps
    # each campaign actually delivered
    fd_std = pd.DataFrame(columns=['campaign_name', 'media_type', 
                                   'fractional_delivery'])
    fd_mob = pd.DataFrame(columns=['campaign_name', 'media_type', 
                                   'fractional_delivery'])
    fd_tab = pd.DataFrame(columns=['campaign_name', 'media_type', 
                                   'fractional_delivery'])
    fd_svd = pd.DataFrame(columns=['campaign_name', 'media_type', 
                                   'fractional_delivery'])                               
    for i in xrange(0, len(advertisers)):
        curr_adv = combined[combined['advertiser']==advertisers[i]]           
        fd_std = fd_std.append(fractional_deliv("STD", curr_adv, sf), 
                               ignore_index = True)
        fd_mob = fd_mob.append(fractional_deliv("MOB", curr_adv, sf), 
                               ignore_index = True)
        fd_tab = fd_tab.append(fractional_deliv("TAB", curr_adv, sf), 
                               ignore_index = True)
        fd_svd = fd_svd.append(fractional_deliv("SVD", curr_adv, sf), 
                               ignore_index = True)
        
    fd = fd_std.append(fd_mob, ignore_index = True)
    fd = fd.append(fd_tab, ignore_index = True)
    fd = fd.append(fd_svd, ignore_index = True)
    
    
    # now use a vlookuplike funciton to insert this into correct locations of combined
    # is that even necessary? it might already be in order
    keymapping = {1:0, 6:1}
    data_to_insert = [2]
    labelmapping = {"fractional_delivery":"fractional_delivery"}
    combined_plus_fd = vlookup(combined, fd, keymapping, data_to_insert,
                               labelmapping)
    combined_plus_fd.to_csv("output.csv")
    
campaign_analysis("prd_an_in.csv", "prd_dbm_in.csv",
                  "prd_sf_in.csv", "prd_sf_in.csv")