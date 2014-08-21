import sys
import os.path
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

pd.options.display.mpl_style = 'default'

font = {'family' : 'Serif',
        'size'   : 6}


matplotlib.rc('font', **font)

files = list()
times = list()
sigma = list()
PLOT_DATA = list()
ZERO_DATA = list()
ZERO_DATA_PAUL = list()
FAILED_DATA = list()

base_filename = '../../19_8_sweep_09/'

for root, dirs, files in os.walk(base_filename):
  for name in dirs:
  	sigma.append(name)
  	##print name
     
kappa = 9.98e-8


for i in range(len(sigma)):
	last = ''
	end = False
	#print sigma[i]
	k = 0
	while(end==False):
		end2 = False		
		filename_k = base_filename + str(sigma[i]) + "/data_" + str(k)
		if os.path.isfile(base_filename+str(sigma[i]) + "/data_time.dat") == False:
			FAILED_DATA.append([float(sigma[i][0:6])*1e-6, 1.7e-6])
			end = True
		elif os.path.isfile(filename_k+"_0.dat") == True:
			last = filename_k
			k+=1
			continue
		else:
			j = 0
			end = True
			radius = []
			impulse = np.zeros((3))
			while(end2 == False):
				if os.path.isfile(last+"_" + str(j) + ".dat") == True:
					data = []
					file = open(last+"_" + str(j) + ".dat")
					line = file.readline()
					line = file.readline()
					while line:
						data.append(line)
						line = file.readline()
					file.close()
					r   = np.zeros((len(data),3))
					r_eff = np.zeros((3))
					l   = np.zeros((len(data),3))
					eps = np.zeros((len(data),3))
					rxeps = np.zeros((len(data),3))
					for b in range(len(data)):
						r[b] = data[b].split()

					for b in range(3):
						l[0][b] = r[0][b]-r[-1][b]
					for q in range(1,len(r)):
						for b in range(3):
							l[q][b] = r[q][b]-r[q-1][b]

					for b in range(len(r)):
						for q in range(3):
							eps[b][q] = l[b][q]
					for b in range(len(r)):
						rxeps[b] = np.cross(r[b], eps[b])	
						for q in range(3):
							impulse[q] += rxeps[b][q]
				
					impulse *= kappa / 2 
					total_impulse = np.sqrt(pow(impulse[0],2) + pow(impulse[1],2) + pow(impulse[2],2))
					radius.append(0)
					radius[-1] = np.sqrt(total_impulse / (np.pi * kappa))
					#print radius
					j+=1
				

				else:
					##print i
					if len(radius)==1:
						ZERO_DATA.append([float(sigma[i][0:6])*1e-6, radius[0]])
					else:
						print sigma[i], radius[0], radius[1]
						PLOT_DATA.append([float(sigma[i][0:6])*1e-6, radius[0], radius[1]])
					end = True
					end2 = True
	#print i

PAUL_DATA = []
data = []
file = open(base_filename+'Run3.dat')
line = file.readline()
while line:
	data.append(line)
	line = file.readline()
file.close()
for j in range(len(data)):
	if float((data[j].split())[1]) < 0.0000001:
		ZERO_DATA_PAUL.append(np.zeros(3))
		ZERO_DATA_PAUL[-1] = data[j].split()
		for i in range(3):
			ZERO_DATA_PAUL[-1][i] = float(ZERO_DATA_PAUL[-1][i])*1e-6 
	else:
		PAUL_DATA.append(np.zeros((3)))
		PAUL_DATA[-1] = data[j].split()
		for i in range(3):
			PAUL_DATA[-1][i] = float(PAUL_DATA[-1][i])*1e-6 

fig = plt.figure(figsize=plt.figaspect(1.2), facecolor='w', edgecolor='w')
ax = fig.add_subplot(111, axisbg ='w')
#ax2 = fig.add_subplot(212, axisbg='w',sharex=ax)

#plt.subplots_adjust(left=None, bottom=0.1, right=None, top=None, wspace=None, hspace=0.1)

left  = 0.125  # the left side of the subplots of the figure
right = 0.9    # the right side of the subplots of the figure
bottom = 0.1   # the bottom of the subplots of the figure
top = 0.9      # the top of the subplots of the figure
wspace = 0.2   # the amount of width reserved for blank space between subplots
hspace = 0.2   # the amount of height reserved for white space between subplots


np.savetxt(base_filename+'../post/PAUL_DATA.dat', PAUL_DATA, fmt='%6.6e', delimiter=' ', newline='\n')
np.savetxt(base_filename+'../post/PLOT_DATA.dat', PLOT_DATA, fmt='%6.6e', delimiter=' ', newline='\n')
np.savetxt(base_filename+'../post/ZERO_DATA.dat', ZERO_DATA, fmt='%6.6e', delimiter=' ', newline='\n')
np.savetxt(base_filename+'../post/ZERO_DATA_PAUL.dat', ZERO_DATA_PAUL, fmt='%6.6e', delimiter=' ', newline='\n')
np.savetxt(base_filename+'../post/FAILED_DATA.dat', FAILED_DATA, fmt='%6.6e', delimiter=' ', newline='\n')

BIG_DATA = []
LITTLE_DATA = []
for i in range(len(PLOT_DATA)):
	BIG_DATA.append(max(PLOT_DATA[i][1],PLOT_DATA[i][2]))
	LITTLE_DATA.append(min(PLOT_DATA[i][1],PLOT_DATA[i][2]))

PLOT_DATA = np.transpose(PLOT_DATA)

ALL_DATA = np.asarray([PLOT_DATA[0],LITTLE_DATA, BIG_DATA])
ALL_DATA = np.transpose(ALL_DATA)
ALL_DATA = np.sort(ALL_DATA, axis=0)

PAUL_DATA = np.transpose(PAUL_DATA)
ZERO_DATA = np.transpose(ZERO_DATA)
ZERO_DATA_PAUL = np.transpose(ZERO_DATA_PAUL)
FAILED_DATA = np.transpose(FAILED_DATA)
BIG_DATA = np.transpose(BIG_DATA)
LITTLE_DATA = np.transpose(LITTLE_DATA)

ALL_DATA = np.transpose(ALL_DATA)

p1 = ax.plot(PAUL_DATA[0], PAUL_DATA[1], linewidth=0,  c='g', marker='o', markersize=3, alpha=0.6)
p2 = ax.plot(PAUL_DATA[0], PAUL_DATA[2], linewidth=0,  c='g', marker='o', markersize=3, alpha=0.6)


r1 = ax.plot(PLOT_DATA[0], PLOT_DATA[1], linewidth=0, c='b', marker='^', markersize=3, alpha=0.6)
r2 = ax.plot(PLOT_DATA[0], PLOT_DATA[2], linewidth=0, c='b', marker='^', markersize=3, alpha=0.6)

r0 = ax.plot(ZERO_DATA[0], ZERO_DATA[1], linewidth=0, c='r', markersize=3, marker='^', alpha=0.6)
p0 = ax.plot(ZERO_DATA_PAUL[0], ZERO_DATA_PAUL[2], linewidth=0, markersize=3, c='r', marker='o', alpha=0.6)

failed = ax.plot(FAILED_DATA[0], FAILED_DATA[1], linewidth=0, c='c', markersize=3, marker='o', alpha=0.6)

ax.vlines(PLOT_DATA[0], PLOT_DATA[1], PLOT_DATA[2], linewidth=1, alpha=0.3, color='b')
ax.vlines(PAUL_DATA[0], PAUL_DATA[1], PAUL_DATA[2], linewidth=1, alpha=0.3, color='g')
#ax.legend([p1, p0, r2, r0, failed], ["Paul's data", "Paul's single ring", "Matt & Rory's data", "Matt & Rory's single ring", "Failed runs"], 
#		loc=4, prop={'size':6})


ax.set_xticks([0,0.09e-6,0.25e-6,0.5e-6])
ax.set_xticklabels([0,0.09,0.25,0.5])
ax.set_yticks([0,0.9e-6,1e-6,1.5e-6])
ax.set_yticklabels([0,0.9,1,1.5])
ax.set_ylabel('Effective radius (um)')


ax.set_xlim(0,5.5e-7)
ax.set_ylim(0.000,1.75e-6)

# rdif1 = ax2.plot(ALL_DATA[0],ALL_DATA[1]-0.9e-6, linewidth=0, c='b', marker='^', markersize=3, alpha=0.6)
# rdif2 = ax2.plot(ALL_DATA[0],ALL_DATA[2]-1e-6, linewidth=0, c='b', marker='^', markersize=3, alpha=0.6)
# pdif1 = ax2.plot(PAUL_DATA[0],PAUL_DATA[1]-0.9e-6, linewidth=0, c='g', marker='o', markersize=3, alpha=0.6)
# pdif2 = ax2.plot(PAUL_DATA[0],PAUL_DATA[2]-1e-6, linewidth=0, c='g', marker='o', markersize=3, alpha=0.6)
# pdif_av = ax2.plot(PAUL_DATA[0],((PAUL_DATA[1]-0.9e-6+PAUL_DATA[2]-1e-6)/2), '-', linewidth=1, c='g', alpha=1)
# rdif_av = ax2.plot(ALL_DATA[0],((ALL_DATA[1]-0.9e-6+ALL_DATA[2]-1e-6)/2), '-', linewidth=1, c='b', alpha=1)

# ax2.vlines(ALL_DATA[0], ALL_DATA[1]-0.9e-6, ALL_DATA[2]-1e-6, linewidth=1, alpha=0.3, color='b')
# ax2.vlines(PAUL_DATA[0], PAUL_DATA[1]-0.9e-6, PAUL_DATA[2]-1e-6, linewidth=1, alpha=0.3, color='g')

# ax2.axhline(0, linestyle='-', linewidth=1, zorder=0, color='k') # horizontal lines

# ax2.set_xlim(0,5e-7)
# ax2.set_xticks([0,0.025e-6, 0.09e-6,0.25e-6,0.5e-6])
# ax2.set_xticklabels([0,0.025,0.09,0.25,0.50])
# ax2.set_yticks([0,-0.5e-6,0.5e-6])
# ax2.set_yticklabels([0,-0.5, 0.5])
ax.set_xlabel('Impact parameter (um)')
# ax2.set_ylim(-1e-6,1e-6)


fig.savefig(base_filename+'../post/impact_vs_r_eff.png', dpi=200, facecolor='w', edgecolor='w',
        orientation='portrait', pad_inchemarkersize=0.1)
