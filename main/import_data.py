from bokeh.models import ColumnDataSource

import pandas as pd

def import_data():  
  df = pd.read_excel('dataset.xlsx', sheet_name='Timeline', header=0, skiprows=0, nrows=562) 
  
  return df

