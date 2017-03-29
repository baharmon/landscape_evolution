# detachment vs. transport
* toggle based on coefficient
* see line 561
* remove mode toggle
* revise gui sections

# event vs. series
* toggle based on input
* see line 554

# r.watershed
* add depression parameter to r.watershed
* derive from landcover class

# rusle3d
* use length_slope output from r.watershed for LS?

# usped
* should evolve formula be for erdep or flux? using erdep...

# questions
* can m and n be derived?
- from soil, slope, shear stress, or detach / trans coefficient?
* default params for m and n?
- rusle3d m = 0.2-0.6, n = 1-1.3
- upsed m = 1-1.6, n = 1-1.3

# input params

#%option
#% key: mode
#% type: string
#% required: yes
#% multiple: no
#% answer: simwe_mode
#% options: simwe_mode,usped_mode,rusle_mode
#% description: Erosion deposition, transport limited, or detachment limited mode
#% descriptions: simwe_mode;erosion-deposition mode;usped_mode;transport limited mode;rusle_mode;detachment limited mode
#% guisection: Basic
#%end
