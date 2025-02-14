import numpy as np

import pyproj
grs80 = pyproj.Geod(ellps='GRS80')



def metric_vector(lng1, lat1, lng2, lat2, unit=False):
    azimuth1, _, distance = grs80.inv(lng1, lat1, lng2, lat2) 
    vec = np.array([np.cos(np.deg2rad(azimuth1)), np.sin(np.deg2rad(azimuth1))])
    if unit: return vec
    return vec * distance

def manuever(current_tack, total_manuever=0):
    if current_tack == 'stbd': return 'port', total_manuever+1
    elif current_tack == 'port': return 'stbd', total_manuever+1


def UpwindDownwindVectors(upwindTWA, downwindTWA, twd, tws):
    ##calculate upwind and downwind vecters
    vecs = {}
    azimuth = {}
    for course in ['up_port', 'up_stbd', 'down_port', 'down_stbd']:
        twa = upwindTWA(tws) if course.split('_')[0] == 'up' else downwindTWA(tws)
        azimuth[course] = twd + twa if course.split('_')[1] == 'port' else twd - twa
        vecs[course] = np.round(np.array([np.cos(np.deg2rad(azimuth[course])), np.sin(np.deg2rad(azimuth[course]))]), 3)
    return azimuth, vecs

def drawLayline(targetmark_position, ThisLeg, azimuth, boundaries):
    laylines = {}
    for mark, mark_position in targetmark_position.items():
        for tack in ['port', 'stbd']:
            for j in range(len(boundaries)-1):
                crossdata = determin_cross(mark_position, azimuth[f'{ThisLeg}_{tack}'] - 180, boundaries[j:j+2])
                if crossdata['cross']:
                    laylines[f'{mark}_{tack}'] = np.array([mark_position, crossdata['crosspoint']])
                    break
    return laylines

def determin_cross(position, azimuth, target_line):
    vec_ab = metric_vector(target_line[0,1], target_line[0,0], target_line[1,1], target_line[1,0])
    vec_oa = metric_vector(position[1], position[0], target_line[0,1], target_line[0,0])
    v = np.array([np.cos(np.deg2rad(azimuth)), np.sin(np.deg2rad(azimuth))])
    s = np.cross(vec_ab, vec_oa) / np.cross(vec_ab, v)

    vec_ao = metric_vector(target_line[0,1], target_line[0,0], position[1], position[0])
    u = vec_ab / np.linalg.norm(vec_ab)
    t = np.cross(vec_ao, s*v) / np.cross(vec_ao, u)
    
    if s >= 1 and t/np.linalg.norm(vec_ab) >= 0 and t/np.linalg.norm(vec_ab)<=1:
        lon, lat, _ = grs80.fwd(position[1], position[0], azimuth, s)
        crosspoint = np.array([lat, lon])
        return {'cross':True, 'crosspoint':crosspoint, 's':s}
    else: return {'cross':False, 'crosspoint':None, 's':None}

def determin_markDirection(targetmark_position, current_position, vecs):
    LEG = {}
    on_layline = {}

    for mark, mark_position in targetmark_position.items():
        vecs[mark] = np.round(metric_vector(current_position[1], current_position[0], mark_position[1], mark_position[0], unit=True), 3)

        if np.cross(vecs['up_stbd'], vecs[mark]) > 0 and np.cross(vecs['up_port'], vecs[mark]) < 0:
            LEG[mark] = 'up'
            on_layline[mark] = False

        elif np.cross(vecs['up_port'], vecs[mark]) >= 0 and np.cross(vecs['down_port'], vecs[mark]) <= 0:
            on_layline[mark] = True
            LEG[mark] = 'port'

        elif np.cross(vecs['down_port'], vecs[mark]) > 0 and np.cross(vecs['down_stbd'], vecs[mark]) < 0:
            LEG[mark] = 'down'
            on_layline[mark] = False

        elif np.cross(vecs['down_stbd'], vecs[mark]) >= 0 and np.cross(vecs['up_stbd'], vecs[mark]) <= 0:
            on_layline[mark] = True
            LEG[mark] = 'stbd'

    return LEG, on_layline