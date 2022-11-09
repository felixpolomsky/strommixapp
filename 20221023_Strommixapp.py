import urllib.request
from html_table_parser.parser import HTMLTableParser
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
 
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
 
import time

def url_get_contents(url):

    req = urllib.request.Request(url=url)
    f = urllib.request.urlopen(req)

    return f.read()

def time_in_range(start, end, x):

    if start < x <= end:
        return True

now = datetime.now()-timedelta(hours=1, minutes=30)
date=now.strftime("%d.%m.%Y %H:%M")
datum1, time=str(date).split(' ')
url=f'https://transparency.entsoe.eu/generation/r2/actualGenerationPerProductionType/show?name=&defaultValue=false&viewType=TABLE&areaType=CTY&atch=false&datepicker-day-offset-select-dv-date-from_input=D&dateTime.dateTime={datum1}+00:00|CET|DAYTIMERANGE&dateTime.endDateTime={datum1}+00:00|CET|DAYTIMERANGE&area.values=CTY|10Y1001A1001A83F!CTY|10Y1001A1001A83F&productionType.values=B01&productionType.values=B02&productionType.values=B03&productionType.values=B04&productionType.values=B05&productionType.values=B06&productionType.values=B07&productionType.values=B08&productionType.values=B09&productionType.values=B10&productionType.values=B11&productionType.values=B12&productionType.values=B13&productionType.values=B14&productionType.values=B20&productionType.values=B15&productionType.values=B16&productionType.values=B17&productionType.values=B18&productionType.values=B19&showConsumption.values=SHOW_CONSUMPTION&dateTime.timezone=CET_CEST&dateTime.timezone_input=CET+(UTC+1)+/+CEST+(UTC+2)'
xhtml = url_get_contents(url).decode('utf-8')
p = HTMLTableParser()
p.feed(xhtml)
data=p.tables[0]
columns=('time', 'Biomass', 'Actual Consumption (Biomass)', 'Fossil Brown coal/Lignite', 'Actual Consumption (Fossil Brown coal/Lignite)', 'Fossil Coal-derived gas', 'Actual Consumption (Fossil Coal-derived gas)', 'Fossil Gas', 'Actual Consumption (Fossil Gas)', 'Fossil Hard coal', 'Actual Consumption (Fossil Hard coal)', 'Fossil Oil', 'Actual Consumption (Fossil Oil)', 'Fossil Oil shale', 'Actual Consumption (Fossil Oil shale)', 'Fossil Peat', 'Actual Consumption (Fossil Peat)', 'Geothermal', 'Actual Consumption (Geothermal)', 'Hydro Pumped Storage', 'Actual Consumption (Hydro Pumped Storage)','Hydro Run-of-river and poundage', 'Actual Consumption (Hydro Run-of-river and poundage)', 'Hydro Water Reservoir', 'Actual Consumption (Hydro Water Reservoir)', 'Marine', 'Actual Consumption (Marine)', 'Nuclear', 'Actual Consumption (Nuclear)','Other', 'Actual Consumption (Other)', 'Other renewable', 'Actual Consumption (Other renewable)', 'Solar', 'Actual Consumption (Solar)', 'Waste', 'Actual Consumption (Waste)','Wind Offshore', 'Actual Consumption (Wind Offshore)', 'Wind Onshore', 'Actual Consumption (Wind Onshore)')
df=pd.DataFrame(data[5:], columns=columns)
for item in df['time']:
    start, end = item.split(' - ')
    if time_in_range(start, end, time):
        index=df.index[df['time']==item].tolist()    
df2=df.drop(['time', 'Actual Consumption (Biomass)', 'Actual Consumption (Fossil Brown coal/Lignite)', 'Actual Consumption (Fossil Coal-derived gas)', 'Actual Consumption (Fossil Gas)', 'Actual Consumption (Fossil Hard coal)', 'Actual Consumption (Fossil Oil)', 'Actual Consumption (Fossil Oil shale)', 'Actual Consumption (Fossil Peat)', 'Actual Consumption (Geothermal)', 'Actual Consumption (Hydro Pumped Storage)', 'Actual Consumption (Hydro Run-of-river and poundage)', 'Actual Consumption (Hydro Water Reservoir)', 'Actual Consumption (Marine)', 'Actual Consumption (Nuclear)', 'Actual Consumption (Other)', 'Actual Consumption (Other renewable)', 'Actual Consumption (Solar)', 'Actual Consumption (Waste)', 'Actual Consumption (Wind Offshore)', 'Actual Consumption (Wind Onshore)'], axis=1)

df3 = df2.replace({'-', 'n/e', 'N/A'},0)
for item in df3.columns.values.tolist():
    df3[item]=df3[item].astype(int)
#ax = df3.iloc[index].plot.bar(stacked=True)
#ax.legend(bbox_to_anchor=(1.1, 1.05))
df4=df3.iloc[index]
alle=[]
renewable=['Biomass', 'Geothermal', 'Hydro Pumped Storage', 'Hydro Run-of-river and poundage', 'Hydro Water Reservoir', 'Marine', 'Other renewable', 'Solar', 'Wind Offshore', 'Wind Onshore']
renewable2=[]
nonrenewable=['Fossil Brown coal/Lignite', 'Fossil Coal-derived gas', 'Fossil Gas', 'Fossil Hard coal', 'Fossil Oil', 'Fossil Oil shale', 'Fossil Peat', 'Nuclear', 'Other', 'Waste']
nonrenewable2=[]
y=[]
for item in df4.columns.values.tolist():
    alle.append(item)
    if df4[item].values < 1000:
        y.append(item)
df4['Others'] = df4[y].sum(axis=1)
df4=df4.drop(y, axis=1)
x = []
for sublist in df4.values:
    for item in sublist:
        x.append(item)
labels=df4.columns.values.tolist()
dfrenvsfos=df4
dfrencsfoslabels=dfrenvsfos.columns.values.tolist()
for item in renewable:
    if item in dfrencsfoslabels:
        renewable2.append(item)
for item in nonrenewable:
    if item in dfrencsfoslabels:
        nonrenewable2.append(item)
dfrenvsfos['renewable']=dfrenvsfos[renewable2].sum(axis=1)
dfrenvsfos['nonrenewable']=dfrenvsfos[nonrenewable2].sum(axis=1)
dfrenvsfos=dfrenvsfos.drop(dfrencsfoslabels, axis=1)
dfrencsfoslabels=dfrenvsfos.columns.values.tolist()
dfrenvsfosx = []
for sublist in dfrenvsfos.values:
    for item in sublist:
        dfrenvsfosx.append(item)
plt.figure(0)
plt.pie(x, labels=labels, autopct='%1.1f%%')
plt.savefig('strommix.png')
plt.figure(1)
plt.pie(dfrenvsfosx, labels=dfrencsfoslabels, autopct='%1.1f%%')
plt.savefig('strommixrenvsfosx.png')

class FirstScreen(Screen):
    pass
 
class SecondScreen(Screen):
    pass

class ThirdScreen(Screen):
    pass

class FourthScreen(Screen):
    pass

class FifthScreen(Screen):
    pass
 
class ColourScreen(Screen):
    colour = ListProperty([1., 0., 0., 1.])
 
class MyScreenManager(ScreenManager):
    def new_colour_screen(self):
        name = str(time.time())
        self.current = name
 
root_widget = Builder.load_string('''
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
MyScreenManager:
    transition: FadeTransition()
    FirstScreen:
    SecondScreen:
    ThirdScreen:
    FourthScreen:
<FirstScreen>:
    name: 'mainapp'
    BoxLayout:
        orientation: 'vertical'
        Button:
            text: 'Strommix Deutschland!'
            font_size: 30
            on_release: app.root.current = 'strommix'
        Button:
            text: 'Strommix erneuerbar vs Fossil!'
            font_size: 30
            on_release: app.root.current = 'renewvsfossil'
        Button:
            text: 'Gasersparnis'
            font_size: 30
            on_release: app.root.current = 'gasersparnis'
        Button:
            text: 'Doku'
            font_size: 30
            on_release: app.root.current='doku'
<SecondScreen>:
    name: 'strommix'
    BoxLayout:
        orientation: 'horizontal'
        Image:
            source: 'strommix.png'
            allow_stretch: False
            keep_ratio: False
        Button:
            text:'return'
            font_size: 30
            on_release: app.root.current = 'mainapp'
<ThirdScreen>:
    name: 'renewvsfossil'
    BoxLayout:
        Image:
            source: 'strommixrenvsfosx.png'
            allow_stretch: False
            keep_ratio: False        
        Button:
            text:'to be implemented'
            font_size: 30
            on_release: app.root.current = 'mainapp'          
<FourthScreen>:
    name: 'gasersparnis'
    BoxLayout:
        TextInput:
            multiline:True
            halign:"right"
            font_size:55
        Button:
            text:'return'
            font_size: 30
            on_release: app.root.current = 'mainapp'
    
''')

 
class ScreenManagerApp(App):
    def build(self):
        return root_widget
 
ScreenManagerApp().run()