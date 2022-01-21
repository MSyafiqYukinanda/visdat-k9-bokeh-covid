from bokeh.layouts import row, column, widgetbox        
from bokeh.models import Select, Div , MultiSelect, HoverTool
from bokeh.plotting import curdoc, figure

from get_data import get_data 
from import_data import import_data 

GRAPH_WIDTH = 600
GRAPH_HEIGHT = 400 
PAGE_TITLE = "Indonesia Covid-19 Statistics Comparison"
POPULAR_SERIES = { '2021' : '2021', '2020' : '2020'}
div_widget = Div(text="", width=400, height=100)
controls = None

#------------------------------------------------------------------------------
dataset = import_data()
YEAR = POPULAR_SERIES['2021'] 
PROVINCES = ['Aceh', 'Bali']
PROVINCES_LIST = ['Total'] + [x for x in dataset.columns[1:35]]
#------------------------------------------------------------------------------
# array of colors containing 36 colors
colors = [
  "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf", 
  "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf", 
  "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
]

def make_plot(**kwargs): 
  source = get_data(dataset, YEAR, PROVINCES)
  x = [x[0] for x in source[['date']].to_numpy()]
  y = [[[x[0]/100000 for x in source[[item]].to_numpy()], item] for item in PROVINCES]
  p = figure(title="Jumlah Kasus Covid-19 Per 100.000 Jiwa",x_range=x, plot_height=GRAPH_HEIGHT, plot_width=GRAPH_WIDTH, **kwargs)
  tooltips = [
    (x, '@'+x) for x in PROVINCES 
  ]
  p.add_tools(HoverTool(tooltips=tooltips))
  
  i=0
  for item in y:
    p.line(x, item[0], legend_label=item[1], line_width=2, color=colors[i]) 
    i = i+1

  return p

def onChangeTahun(attr, old, new):
  global YEAR 
  YEAR = POPULAR_SERIES[selectTahun.value]

  source = get_data(dataset, YEAR, PROVINCES)
  x = [x[0] for x in source[['date']].to_numpy()]
  y = [[[x[0]/100000 for x in source[[item]].to_numpy()], item] for item in PROVINCES]

  p = figure(title="Jumlah Kasus Covid-19 Per 100.000 Jiwa",x_range=x, plot_height=GRAPH_HEIGHT, plot_width=GRAPH_WIDTH)
  tooltips = [
    (x, '@'+x) for x in PROVINCES 
  ]
  p.add_tools(HoverTool(tooltips=tooltips))
  
  i=0
  for item in y:
    p.line(x, item[0], legend_label=item[1], line_width=2, color=colors[i]) 
    i = i+1

  layout = column(row(controls, p), div_widget)
  curdoc().clear() 
  curdoc().add_root(layout) 

def onChangeProvince(attr, old, new): 
  global PROVINCES
  PROVINCES = multiSelectProvince.value

  source = get_data(dataset, YEAR, PROVINCES)
  x = [x[0] for x in source[['date']].to_numpy()]
  y = [[[x[0]/100000 for x in source[[item]].to_numpy()], item] for item in PROVINCES]

  p = figure(title="Jumlah Kasus Covid-19 Per 100.000 Jiwa",x_range=x, plot_height=GRAPH_HEIGHT, plot_width=GRAPH_WIDTH)
  tooltips = [
    (x, '@'+x) for x in PROVINCES 
  ]
  p.add_tools(HoverTool(tooltips=tooltips))
  
  i=0
  for item in y:
    p.line(x, item[0], legend_label=item[1], line_width=2, color=colors[i])
    i = i+1

  layout = column(row(controls, p), div_widget)
  curdoc().clear() 
  curdoc().add_root(layout)  

# #------------------------------------------------------------------------------ 

selectTahun = Select(title='Tahun', options=sorted(POPULAR_SERIES.keys()), value='2021')
selectTahun.on_change('value', onChangeTahun) 

multiSelectProvince = MultiSelect(value=PROVINCES, options=PROVINCES_LIST, height= 300)
multiSelectProvince.on_change("value", onChangeProvince )

controls = widgetbox([selectTahun, multiSelectProvince], width=200) 

layout = column(row(controls, make_plot()), div_widget)

curdoc().add_root(layout)
curdoc().title = PAGE_TITLE     

# bokeh serve --show main/