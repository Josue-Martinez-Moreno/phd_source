import matplotlib
matplotlib.use('agg')
import sys
from netCDF4 import Dataset
import os
os.environ["PROJ_LIB"] = "/g/data/v45/jm5970/env/track_env/share/proj"
import cmocean as cm
from trackeddy.tracking import *
from trackeddy.datastruct import *
from trackeddy.geometryfunc import *
from trackeddy.physics import *
from trackeddy.plotfunc import *
from numpy import *

outputfilenumber =int(sys.argv[1])
init=127
end=154

layer=1

outfile='/g/data/v45/jm5970/trackeddy_output/simple_ocean_w_ridges/2layer/npy/'

# Output data path
outputpath='/home/552/nc3020/SOchanBcBtEddySat/layer2/layer2_tau2e-1_manyshortridges/archive/output{0:03}/'.format(outputfilenumber)

# Import SSH values to python environment.
ncfile=Dataset(outputpath+'prog.nc')
time=ncfile.variables['Time'][:]

eta = squeeze(ncfile.variables['e'][:,layer,:,:])
#print(np.shape(eta))

# Import geographic coor#dinates (Lon,Lat)
lon=ncfile.variables['xh'][:] 
lat=ncfile.variables['yh'][:]

# Import SSH 10 yrs mean values to python environment.
ncfile=Dataset('/g/data/v45/jm5970/trackeddy_output/simple_ocean_w_ridges/2layer/pre-processing/mean_ssh_{0:03}_{1:03}.nc'.format(init,end))
ssh_mean=squeeze(ncfile.variables['e'][layer,:,:])

# Import geographic coordinates (Lon,Lat)
#lon=ncfile.variables['Longitude'][:]
#lat=ncfile.variables['Latitude'][:]

areamap=array([[0,len(lon)],[0,len(lat)]])

filters = {'time':{'type':'historical','t':None,'t0':None,'value':ssh_mean},
           'spatial':{'type':None,'window':None,'mode':None}}

preferences={'ellipse':0.85,'eccentricity':0.95,'gaussian':0.85}
areaparm={'constant':np.inf}

levels = {'max':(eta-ssh_mean).max(),'min':0.005,'step':0.005}
eddytd=analyseddyzt(eta,lon,lat,0,shape(eta)[0],1,levels,areamap=areamap,mask='',maskopt='forcefit'\
                    ,preferences=preferences,filters=filters,areaparms=areaparm,destdir='',physics='',diagnostics=False,pprint=True)
print("Saving Positive",outputfilenumber)
save(outfile+'2layer_{0:05}_{1}_pos.npy'.format(outputfilenumber,layer),eddytd)

levels = {'max':-(eta-ssh_mean).min(),'min':0.005,'step':0.005}
eddytdn=analyseddyzt(-eta,lon,lat,0,shape(eta)[0],1,levels,areamap=areamap,mask='',maskopt='forcefit'\
                     ,preferences=preferences,filters=filters,areaparms=areaparm,destdir='',physics='',diagnostics=False,pprint=False)
print("Saving Negative",outputfilenumber)
save(outfile+'2layer_{0:05}_{1}_neg.npy'.format(outputfilenumber,layer),eddytdn)
