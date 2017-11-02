import pandas as pd #using pandas.io (recommended in sklearn)


def parse_date(column):
    column = pd.to_datetime(column)
    column = [t.value // 10 ** 9 for t in column]
    return column

df = pd.read_csv('dataset.csv').drop(['Proposal'], axis = 1)

dummies_beamline = pd.get_dummies(df['Beamline'])
df = pd.concat([df.drop(['Beamline'], axis=1) ,dummies_beamline], axis = 1)

dummies_department = pd.get_dummies(df['Department']) #adds many columns...
df = pd.concat([df.drop(['Department'], axis=1) ,dummies_department], axis = 1)

dummies_user_aff = pd.get_dummies(df['User Affiliation']) #adds many columns...
df = pd.concat([df.drop(['User Affiliation'], axis=1) ,dummies_department], axis = 1)

df['Experiment start'] = parse_date(df['Experiment start'])
df['Experiment end'] = parse_date(df['Experiment end'])
df['Report submitted'] = parse_date(df['Report submitted'])


print(df.head())










