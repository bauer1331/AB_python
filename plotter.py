# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 08:52:28 2016

@author: andrewbrown
"""

def plot(file):
    import pandas as pd
    df = pd.read_csv(file)
    df['ctr_bucket_factor'] = df['ctr_bucket'].astype('category')
    p = ggplot(aes(x='adv_id', y='fractional_delivery', color = 'ctr_bucket'), data = df) + \
    geom_point() + \
    ylim(0, 5) + \
    xlim(0, 125) + \
    geom_hline(yintercept = [1], color = 'red') + \
    facet_wrap("targetting") + \
    theme_matplotlib(rc={"figure.figsize": "22, 16"}, matplotlib_defaults=False) + \
    scale_colour_gradient2(low='red', high='white')
    
    print p
plot("output_removeNA.csv")




#    theme_matplotlib(rc={"figure.figsize": "22, 16"}, matplotlib_defaults=False) + \
