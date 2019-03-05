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
from trackeddy.init import *
from trackeddy.physics import *
from trackeddy.plotfunc import *
from numpy import *

outputfilenumber =int(sys.argv[1])
end=154

outfile='/g/data/v45/jm5970/trackeddy_output/simple_ocean_w_ridges/2layer/npy/'

# Output data path
outputpath='/home/552/nc3020/SOchanBcBtEddySat/layer2/layer2_tau2e-1_manyshortridges/archive/output{0:03}/'.format(outputfilenumber)

# Import SSH values to python environment.
ncfile=Dataset(outputpath+'prog.nc')
time=ncfile.variables['Time'][:]

eta = squeeze(ncfile.variables['e'][:,0,:,:])
#print(np.shape(eta))

# Import geographic coor#dinates (Lon,Lat)
lon=ncfile.variables['xh'][:] 
lat=ncfile.variables['yh'][:]

# Import SSH 10 yrs mean values to python environment.
ncfile=Dataset('/g/data/v45/jm5970/trackeddy_output/simple_ocean_w_ridges/2layer/pre-processing/mean_ssh_{0:03}_{0:03}.nc'.format(outputfilenumber,end))
ssh_mean=squeeze(ncfile.variables['e'][0,:,:])

# Import geographic coordinates (Lon,Lat)
#lon=ncfile.variables['Longitude'][:]
#lat=ncfile.variables['Latitude'][:]

areamap=array([[0,len(lon)],[0,len(lat)]])

filters = {'time':{'type':'historical','t':None,'t0':None,'value':ssh_mean},
           'spatial':{'type':'moving','window':120,'mode':'uniform'}}

preferences={'ellipse':0.70,'eccentricity':0.95,'gaussian':0.7}

levels = {'max':eta.max(),'min':0.01,'step':0.01}
eddytd=analyseddyzt(eta,lon,lat,0,shape(eta)[0],1,levels,areamap=areamap,mask='',maskopt='forcefit'\
                    ,preferences=preferences,filters=filters,destdir='',physics='',diagnostics=False,pprint=True)
print("Saving Positive",file_count)
save(outfile+'2layer_%05d_pos.npy' % file_count,eddytd)

levels = {'max':-eta.min(),'min':0.01,'step':0.01}
eddytdn=analyseddyzt(-eta,lon,lat,0,shape(eta)[0],1,levels,areamap=areamap,mask='',maskopt='forcefit'\
                     ,filters=filters,destdir='',physics='',diagnostics=False,pprint=False)
print("Saving Negative")
save(outfile+'2layer_%05d_neg.npy' % file_count,eddytdn)