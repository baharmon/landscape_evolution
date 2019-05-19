# Linear regression

## Set region
g.region vector=subwatershed res=1
r.mask vector=subwatershed

## Baseline 2012-2016
r.regression.line mapx=elevation_2012_1m mapy=elevation_2016_1m@PERMANENT
```
y = a + b*x
   a (Offset): -0.201885
   b (Gain): 1.002306
   R (sumXY - sumX*sumY/N): 0.999490
   N (Number of elements): 19226
   F (F-test significance): 18823495.196710
   meanX (Mean of map1): 106.170402
   sdX (Standard deviation of map1): 4.055803
   meanY (Mean of map2): 106.213344
   sdY (Standard deviation of map2): 4.067231
```

## SIMWE
r.regression.line mapx=elevation_2012_1m mapy=elevation_simwe
```       
y = a + b*x
   a (Offset): -0.048322
   b (Gain): 1.000372
   R (sumXY - sumX*sumY/N): 0.998312
   N (Number of elements): 19226
   F (F-test significance): 5680403.746928
   meanX (Mean of map1): 106.170402
   sdX (Standard deviation of map1): 4.055803
   meanY (Mean of map2): 106.161534
   sdY (Standard deviation of map2): 4.064170
```

## RUSLE
r.regression.line mapx=elevation_2012_1m mapy=elevation_rusle
```
y = a + b*x
   a (Offset): -0.042211
   b (Gain): 1.000379
   R (sumXY - sumX*sumY/N): 0.999973
   N (Number of elements): 19226
   F (F-test significance): 361604088.919433
   meanX (Mean of map1): 106.170402
   sdX (Standard deviation of map1): 4.055803
   meanY (Mean of map2): 106.168460
   sdY (Standard deviation of map2): 4.057449
```

## USPED
r.regression.line mapx=elevation_2012_1m mapy=elevation_usped
```
y = a + b*x
   a (Offset): -0.062897
   b (Gain): 1.000514
   R (sumXY - sumX*sumY/N): 0.999743
   N (Number of elements): 19226
   F (F-test significance): 37335027.936762
   meanX (Mean of map1): 106.170402
   sdX (Standard deviation of map1): 4.055803
   meanY (Mean of map2): 106.162072
   sdY (Standard deviation of map2): 4.058932
```

## R comparison
baseline - simwe
```
0.001178
```

baseline - rusle
```
−0.000483
```

baseline - usped
```
−0.000253
```

# Bivariate Scatterplots of Difference

## SIMWE
```
N = 19226
R = -0.115982
R-squared = 0.013452
F = 262.125877

```

## RUSLE
```
N = 19226
R = -0.002643
R-squared = 0.000007
F = 0.134318
```

## USPED
```
N = 19226
R = -0.049370
R-squared = 0.002437
F = 46.970180
```

# Bivariate Scatterplots of Elevation

## Baseline
```
N = 19226
R = 0.999490
R-squared = 0.998980
F = 18823495.196710
```

## SIMWE
```
N = 19226
R = 0.998312
R-squared = 0.996627
F = 5680403.746928
```

## RUSLE
```
N = 19226
R = 0.999973
R-squared = 0.999946
F = 361604088.919433
```

## USPED
```
N = 19226
R = 0.999743
R-squared = 0.999486
F = 37335027.936762
```

# Bivariate Scatterplot Commands

## Baseline
r.scatterplot input=elevation_2012,elevation_2016 color_raster=elevation_2012 output=scatterplot_2012_2016 vector_mask=subwatershed

g.region vector=scatterplot_2012_2016 res=0.1 -p

v.mkgrid -h map=scatterplot_grid_2012_2016

v.vect.stats points=scatterplot_2012_2016 areas=scatterplot_grid_2012_2016 count_column=count

v.colors map=scatterplot_grid_2012_2016 use=attr column=count color=viridis

d.vect map=scatterplot_grid_2012_2016 where="count > 0" icon=basic/point

v.mkgrid --overwrite map=grid box=1,1

d.vect map=grid fill_color=none color=grey width=1


## 2012 - SIMWE
r.scatterplot input=elevation_2012,elevation_2016_01_01_02_00_00@simwe color_raster=elevation_2012 output=scatterplot_2012_simwe vector_mask=subwatershed

v.mkgrid -h map=scatterplot_grid_2012_simwe

v.vect.stats points=scatterplot_2012_simwe areas=scatterplot_grid_2012_simwe count_column=count

v.colors map=scatterplot_grid_2012_simwe use=attr column=count color=viridis

d.vect map=scatterplot_grid_2012_simwe where="count > 0" icon=basic/point


## 2012 - RUSLE
r.scatterplot input=elevation_2012,elevation_2016_01_01_02_00_00@rusle color_raster=elevation_2012 output=scatterplot_2012_rusle vector_mask=subwatershed

v.mkgrid -h map=scatterplot_grid_2012_rusle

v.vect.stats points=scatterplot_2012_rusle areas=scatterplot_grid_2012_rusle count_column=count

v.colors map=scatterplot_grid_2012_rusle use=attr column=count color=viridis

d.vect map=scatterplot_grid_2012_rusle where="count > 0" icon=basic/point


## 2012 - USPED
r.scatterplot input=elevation_2012,elevation_2016_01_01_02_00_00@usped color_raster=elevation_2012 output=scatterplot_2012_usped vector_mask=subwatershed

v.mkgrid -h map=scatterplot_grid_2012_usped

v.vect.stats points=scatterplot_2012_usped areas=scatterplot_grid_2012_usped count_column=count

v.colors map=scatterplot_grid_2012_usped use=attr column=count color=viridis

d.vect map=scatterplot_grid_2012_usped where="count > 0" icon=basic/point
