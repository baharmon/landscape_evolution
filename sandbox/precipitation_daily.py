import csv
from collections import defaultdict


# full path filename for precipitation data
precipitation = "//Users//Brendan//landscape_evolution//sandbox//precipitation//Harmon_Lake_Daily//Lake_Daily_2001.txt"

precip = defaultdict(list)
parsed_precip = defaultdict(list)

with open(precipitation) as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        for (i,v) in enumerate(row):
            precip[i].append(v)
#print(precip[1])


#parsed_precip = {k: v for k, v in precip.iteritems() if v[1] >= 0.1}
parsed_precip = dict(filter(lambda (a,(b)): float(b) >= 0.01, precip.items()))

print parsed_precip[1]


#points_small = dict(filter(lambda (a,(b,c)): b<5 and c < 5, points.items()))

#precip = dict((k, v) for k, v in d.items() if v >= 10)
#print precip



#{k:v for (k,v) in columns.items() if v >= 0.01}
#print columns


# write new csv file with filtered values


## full path filename for precipitation data
#precipitation = "//Users//Brendan//landscape_evolution//sandbox//precipitation//Harmon_Lake_Daily//Lake_Daily_2001.txt"
#
## open txt file with precipitation data
#with open(precipitation) as csvfile:
#
#    # check for header
#    has_header = csv.Sniffer().has_header(csvfile.read(1024))
#
#    # rewind
#    csvfile.seek(0)
#
#    # skip header
#    if has_header:
#        next(csvfile)
#
#    # parse time and precipitation
#    precip = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
#    for row in precip:
#        if float(row[1])>=0.01:
#            print row[1]


    # # initial run
    # initial = next(precip)
    # evol.start = initial[0]
    # #evol.rain_intensity = float(initial[1]) # mm/hr
    # evol.rain_intensity = 'rain_intensity'
    # gscript.run_command('r.mapcalc',
    #     expression="{rain_intensity} = {initial}".format(rain_intensity=evol.rain_intensity,
    #         initial=float(initial[1])),
    #     overwrite=True)
