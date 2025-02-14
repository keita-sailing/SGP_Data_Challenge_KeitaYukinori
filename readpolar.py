import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

def calc_VMG(row, tws, downwind=False):
    vmg = row[tws] * np.cos(np.deg2rad(row.name))
    if downwind: return -vmg
    return vmg

def read_polar(filename):
    df = pd.read_csv(filename, index_col=0)
    tws = df.columns.values
    for tws in df.columns.values:
        df[f'{tws}_upwind_VMG'] = df.apply(lambda x: calc_VMG(x, tws), axis=1)
        df[f'{tws}_dnwind_VMG'] = df.apply(lambda x: calc_VMG(x, tws, downwind=True), axis=1)
    return df

def vmg_twa(polar_df):
    for leg in ['upwind', 'dnwind']:
        data = np.empty((0,2), dtype='float64')
        for tws in [x for x in polar_df.columns.values if len(x.split('_'))==1]:
            ranking = np.argsort(polar_df[f'{tws}_{leg}_VMG'].to_list())[::-1]
            max_vmg_twa = polar_df.index.values[ranking[0]]
            data = np.append(data, np.round([[float(tws), float(max_vmg_twa)]], 1), axis=0)
        if leg == 'upwind':
            f_upwind = interp1d(data[:,0], data[:,1], kind="linear")
        else:
            f_downwind = interp1d(data[:,0], data[:,1], kind="linear")
    return f_upwind, f_downwind