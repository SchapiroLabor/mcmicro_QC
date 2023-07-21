import pandas as pd
from pathlib import Path

INPATH=Path('./examples/')

output = pd.DataFrame()

for infile in INPATH.rglob('*/quantification/*unmicst*.csv'):
    df = pd.read_csv(infile)
    sample = infile.parts[-3]
    name = infile.name.split('--')[0]
    stats = pd.DataFrame(df.mean().drop(['CellID', 'X_centroid', 'Y_centroid', 'Orientation', 'MajorAxisLength', 'MinorAxisLength', 'Eccentricity', 'Solidity', 'Extent'])).T
    stats.columns = ['Mean_' + c for c in stats.columns]
    stats['Mean_Signal'] = stats.iloc[:, :-2].mean(axis=1)
    stats['CellCount'] = df.shape[0]
    stats.index = [f'{sample}-{name}'] if sample != name else [sample]
    output = pd.concat([output, stats])

output.to_csv('stats.csv')