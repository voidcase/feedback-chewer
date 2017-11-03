import pandas as pd #using pandas.io (recommended in sklearn)


def parse_date(column):
    column = pd.to_datetime(column)
    column = [t.value // 10 ** 9 for t in column]
    return column

df = pd.read_csv('dataset.csv').drop(['Proposal'], axis = 1)

for header in ['Beamline', 'Department', 'User Affiliation']:
    dummies_beamline = pd.get_dummies(df[header])
    df = pd.concat([df.drop([header], axis=1) ,dummies_beamline], axis = 1)

df['Experiment start'] = parse_date(df['Experiment start'])
df['Experiment end'] = parse_date(df['Experiment end'])
df['Report submitted'] = parse_date(df['Report submitted'])


print(df.head())










