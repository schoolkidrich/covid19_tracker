from flask import Flask, render_template
import pandas as pd
import random


app = Flask(__name__)


def loadData():

    # read data from cdc link
    df = pd.read_csv('https://data.cdc.gov/api/views/9mfq-cb36/rows.csv')

    # drop unwanted/ rename columns
    df = df[['submission_date','state','new_case','new_death']]
    df.rename(columns = {'submission_date':'date',
                        'state':'state',
                        'new_case':'cases',
                        'new_death':'deaths'},
             inplace=True)

    # rename NYC to NY
    df['state'].replace({
        'NYC':'NY'
        }, inplace=True)
        
    # modify date string
    df['date'] = pd.to_datetime(df['date']).astype(str)
    return(df)


def dfToJson(df):
    data = []
    for index,items in df.iterrows():
        mapping = dict()
        for i,item in enumerate(items):
            mapping[df.columns[i]] = item
        data.append(mapping)
    return data


@app.route('/')
def welcome():
  return render_template("index.html")


@app.route('/api/state=<variable>', methods = ['GET'])
def getState(variable):
  covid19 = loadData()
  state = variable.upper()
  states = set(covid19['state'])

  if state in states:
    string = f'"{state}"'
    covid19 = covid19.query(f'state == {string}')
    covid19 = covid19.drop(columns = 'state')

  elif state == 'ALL':
    pass
    
  else:
    codes = dict()
    codes['valid_states'] = list(states)
    return (f'{codes}'.replace("'",'"'))

  covid19 = covid19.groupby('date').sum().reset_index()
  data = dfToJson(covid19)
  out_str = f'{data}'
  return out_str.replace("'",'"')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=random.randint(2000,9000))