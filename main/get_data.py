from bokeh.models import ColumnDataSource

import pandas as pd

def get_data(data, year, countries): 
  df = data
  # read dataset.xlsx sheet timeline get data from row 1 to 563 
  # df = pd.read_excel('dataset.xlsx', sheet_name='Timeline', header=0 )
  df = df.iloc[1:562,0:35]
  df.dropna(inplace=True)
  #convert column Total Kasus to datetime format
  df.iloc[:,0] = pd.to_datetime(df.iloc[:,0])
  df['Total'] = df.drop('Total Kasus', axis=1).sum(axis=1)  

  df['month'] = df.iloc[:,0].dt.strftime('%m')
  df['year'] = df.iloc[:,0].dt.strftime('%Y')
  # group by month and year then sum each column 
  df = df.groupby(['year','month']).sum()
  # merge index 
  df = df.iloc[df.index.get_level_values('year') == year]
  df = df.reset_index()
  # combine year and month to one column named date
  df['date'] = df['year'] + '-' + df['month']
  # set column date to index
  df.set_index('date', inplace=True) 
  
  df = df[countries]

  df = df.reset_index()


  return df

