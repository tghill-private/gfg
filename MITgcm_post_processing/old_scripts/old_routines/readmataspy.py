import scipy.io

a = scipy.io.loadmat('variables.mat', None, False, squeeze_me=True, chars_as_strings=True)

nx = int(a['nx'])
ny = int(a['ny'])
nz = int(a['nz'])
dx = a['dx']
dy = a['dy']
dz = a['dz']
start_time = int(a['startTime'])
end_time = int(a['endTime'])
sec_per_iter = int(a['secPerIter'])
sec_per_file = int(a['secPerFile'])

