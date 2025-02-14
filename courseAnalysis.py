import pandas as pd
import numpy as np

import pyproj
grs80 = pyproj.Geod(ellps='GRS80')


mark_list = [['SL1','SL2'],['M1'],['LG1','LG2'],['WG1','WG2'],['LG1','LG2'],['WG1','WG2'],['LG1'],['FL1','FL2']]

def markCenterPos(row, mark):
    if len(mark) == 1:
        return [row[f'{mark[0]}_LATITUDE_deg'], row[f'{mark[0]}_LONGITUDE_deg']]
    elif len(mark) == 2:
        return [np.mean([row[f'{mark[0]}_LATITUDE_deg'], row[f'{mark[1]}_LATITUDE_deg']]), np.mean([row[f'{mark[0]}_LONGITUDE_deg'], row[f'{mark[1]}_LONGITUDE_deg']])]


def calcLegDistance(leg, row):
    mark0_pos = markCenterPos(row, mark_list[leg-1])
    mark1_pos = markCenterPos(row, mark_list[leg])
    azimuth1, _, distance = grs80.inv(mark0_pos[1], mark0_pos[0], mark1_pos[1], mark1_pos[0])
    return distance


def distance2finish(row, COUNTRY_CODE):
    leg = int(row[f'{COUNTRY_CODE}_LEG_NUMBER'])

    if leg >= 8: return 0
    elif np.isnan(row[f'{COUNTRY_CODE}_LATITUDE']): return np.nan
    if leg == 0:
        mark0_pos = markCenterPos(row, [mark_list[0][0]])
        mark1_pos = markCenterPos(row, [mark_list[0][1]])
    else:
        mark0_pos = markCenterPos(row, mark_list[leg-1])
        mark1_pos = markCenterPos(row, mark_list[leg])

    current_pos = [row[f'{COUNTRY_CODE}_LATITUDE'], row[f'{COUNTRY_CODE}_LONGITUDE']]
    azimuth1, _, distance1 = grs80.inv(mark1_pos[1], mark1_pos[0], mark0_pos[1], mark0_pos[0])
    azimuth2, _, distance2 = grs80.inv(mark1_pos[1], mark1_pos[0], current_pos[1], current_pos[0])

    u = [n*distance1 for n in [np.cos(np.deg2rad(azimuth1)), np.sin(np.deg2rad(azimuth1))]]
    v = [n*distance2 for n in [np.cos(np.deg2rad(azimuth2)), np.sin(np.deg2rad(azimuth2))]]

    if leg==0:
        distance2nextmark = abs(np.cross(u, v)/np.linalg.norm(u))
    else:
        distance2nextmark = abs(np.dot(u, v)/np.linalg.norm(u))
    if leg == 7: return round(distance2nextmark, 2)

    distance2finish = distance2nextmark
    for i in range(leg+1, 8):
        distance2finish += row[f'LEG{i}_DISTANCE']
    return round(distance2finish, 2)


def distance2leader(df, COUNTRY_LIST):
    df = df.ffill().bfill()
    for COUNTRY_CODE in COUNTRY_LIST:
        df[f'{COUNTRY_CODE}_Distance2Finish'] = df.apply(lambda x: distance2finish(row=x, COUNTRY_CODE=COUNTRY_CODE), axis=1)

    distance2leaderList = []
    for index, row in df.iterrows():
        distance2finish_list = [row[f'{COUNTRY_CODE}_Distance2Finish'] for COUNTRY_CODE in COUNTRY_LIST]
        ranking = np.argsort(distance2finish_list)
        new_row = []
        for i, country in enumerate(COUNTRY_LIST):
            if i == ranking[0]:
                distance2leader = 0
            else:
                topboat_pos = row[f'{COUNTRY_LIST[ranking[0]]}_Distance2Finish']
                boat_pos = row[f'{country}_Distance2Finish']
                distance2leader = boat_pos - topboat_pos
            new_row.append(round(distance2leader))
        distance2leaderList.append(new_row)

    append_df = pd.DataFrame(distance2leaderList, columns=[f'{COUNTRY_CODE}_Distance2Leader' for COUNTRY_CODE in COUNTRY_LIST])
    return pd.concat([df, append_df], axis=1)


def vmc(df, COUNTRY_LIST):
    mark_list = [['SL1','SL2'],['M1'],['LG1','LG2'],['WG1','WG2'],['LG1','LG2'],['WG1','WG2'],['LG1'],['FL1','FL2']]
    for COUNTRY_CODE in COUNTRY_LIST:
        vmc = []
        azimuth = []
        sog = df[f'{COUNTRY_CODE}_GPS_SOG']
        cog = df[f'{COUNTRY_CODE}_GPS_COG']
        leg = df[f'{COUNTRY_CODE}_LEG_NUMBER']

        for index, row in df.iterrows():
            mark0_pos = markCenterPos(row, mark_list[leg[index]-1])
            mark1_pos = markCenterPos(row, mark_list[leg[index]])
            azi, _, _ = grs80.inv(mark0_pos[1], mark0_pos[0], mark1_pos[1], mark1_pos[0])
            vmc.append(int(sog[index] * np.cos(np.deg2rad(cog[index]-azi))))
            azimuth.append(round(azi, 2))

        append_df = pd.DataFrame([vmc, azimuth], index=[f'{COUNTRY_CODE}_VMC', f'{COUNTRY_CODE}_Mark_Angle']).T
        df = pd.concat([df, append_df], axis=1)
    return df


def saileddistance(df, COUNTRY_LIST):
    for COUNTRY_CODE in COUNTRY_LIST:
        distance = []
        lat = df[f'{COUNTRY_CODE}_LATITUDE']
        lon = df[f'{COUNTRY_CODE}_LONGITUDE']

        for index, row in df.iterrows():
            if index==0: continue
            pos0 = [lat[index-1], lon[index-1]]
            pos1 = [lat[index], lon[index]]
            azi, _, dis = grs80.inv(pos0[1], pos0[0], pos1[1], pos1[0])
            distance.append(round(dis, 2))

        append_df = pd.DataFrame(distance, columns=[f'{COUNTRY_CODE}_Sailed_Distance'])
        df = pd.concat([df, append_df], axis=1)
    return df
