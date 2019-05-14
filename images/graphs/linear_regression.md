# Linear regression

## Set region
g.region vector=subwatershed

## Baseline 2012-2016
r.regression.line mapx=elevation_2012@PERMANENT mapy=elevation_2016@PERMANENT
```
y = a + b*x
   a (Offset): -0.254813
   b (Gain): 1.002773
   R (sumXY - sumX*sumY/N): 0.999329
   N (Number of elements): 19226
   F (F-test significance): 14318481.907321
   meanX (Mean of map1): 106.183153
   sdX (Standard deviation of map1): 4.054545
   meanY (Mean of map2): 106.222834
   sdY (Standard deviation of map2): 4.068519
```

## ERDEP
r.regression.line mapx=elevation_2012@PERMANENT mapy=elevation_2016_01_01_02_00_00@ss_erdep
```
y = a + b*x
   a (Offset): 0.107050
   b (Gain): 0.998926
   R (sumXY - sumX*sumY/N): 0.999333
   N (Number of elements): 19226
   F (F-test significance): 14387605.899509
   meanX (Mean of map1): 106.183153
   sdX (Standard deviation of map1): 4.054545
   meanY (Mean of map2): 106.176207
   sdY (Standard deviation of map2): 4.052897
```

## RUSLE
r.regression.line mapx=elevation_2012@PERMANENT mapy=elevation_2016_01_01_02_00_00@rusle
```
y = a + b*x
   a (Offset): -0.127633
   b (Gain): 1.001103
   R (sumXY - sumX*sumY/N): 0.999848
   N (Number of elements): 19226
   F (F-test significance): 63183164.797364
   meanX (Mean of map1): 106.183153
   sdX (Standard deviation of map1): 4.054545
   meanY (Mean of map2): 106.172603
   sdY (Standard deviation of map2): 4.059634
```

## USPED
r.regression.line mapx=elevation_2012@PERMANENT mapy=elevation_2016_01_01_02_00_00@usped
```
y = a + b*x
   a (Offset): -0.042093
   b (Gain): 1.000245
   R (sumXY - sumX*sumY/N): 0.999514
   N (Number of elements): 19226
   F (F-test significance): 19760637.703019
   meanX (Mean of map1): 106.183153
   sdX (Standard deviation of map1): 4.054545
   meanY (Mean of map2): 106.167064
   sdY (Standard deviation of map2): 4.057511
```

## R comparison
baseline - erdep
```
−0.000004
```

baseline - rusle
```
−0.000519
```

baseline - usped
```
−0.000185
```

# Bivariate Scatterplots

## Baseline
r.scatterplot input=elevation_2012,elevation_2016 color_raster=elevation_2012 output=scatterplot_2012_2016 vector_mask=subwatershed

g.region vector=scatterplot_2012_2016 res=0.1 -p

v.mkgrid -h map=scatterplot_grid_2012_2016

v.vect.stats points=scatterplot_2012_2016 areas=scatterplot_grid_2012_2016 count_column=count

v.colors map=scatterplot_grid_2012_2016 use=attr column=count color=viridis

d.vect map=scatterplot_grid_2012_2016 where="count > 0" icon=basic/point

v.mkgrid --overwrite map=grid box=1,1

d.vect map=grid fill_color=none color=grey width=1


```
Regression Statistics for Scatterplot(s)
Regression equation for raster map <elevation_2012> vs. <elevation_2016>:

   elevation_2016 = -0.254813 + 1.002773(elevation_2012)

N = 19226
R = 0.999329
R-squared = 0.998658
F = 14318481.907321
```

## 2012 - SIMWE
r.scatterplot input=elevation_2012,elevation_2016_01_01_02_00_00@ss_erdep color_raster=elevation_2012 output=scatterplot_2012_erdep vector_mask=subwatershed

v.mkgrid -h map=scatterplot_grid_2012_erdep

v.vect.stats points=scatterplot_2012_erdep areas=scatterplot_grid_2012_erdep count_column=count

v.colors map=scatterplot_grid_2012_erdep use=attr column=count color=viridis

d.vect map=scatterplot_grid_2012_erdep where="count > 0" icon=basic/point


## 2012 - RUSLE
r.scatterplot input=elevation_2012,elevation_2016_01_01_02_00_00@rusle color_raster=elevation_2012 output=scatterplot_2012_rusle vector_mask=subwatershed

v.mkgrid -h map=scatterplot_grid_2012_rusle

v.vect.stats points=scatterplot_2012_rusle areas=scatterplot_grid_2012_rusle count_column=count

v.colors map=scatterplot_grid_2012_rusle use=attr column=count color=viridis

d.vect map=scatterplot_grid_2012_rusle where="count > 0" icon=basic/point

```
Regression Statistics for Scatterplot(s)
Regression equation for raster map <elevation_2012> vs. <elevation_2016_01_01_02_00_00>:

   elevation_2016_01_01_02_00_00 = -0.127633 + 1.001103(elevation_2012)

N = 19226
R = 0.999848
R-squared = 0.999696
F = 63183164.797364
```

## 2012 - USPED
r.scatterplot input=elevation_2012,elevation_2016_01_01_02_00_00@usped color_raster=elevation_2012 output=scatterplot_2012_usped vector_mask=subwatershed

v.mkgrid -h map=scatterplot_grid_2012_usped

v.vect.stats points=scatterplot_2012_usped areas=scatterplot_grid_2012_usped count_column=count

v.colors map=scatterplot_grid_2012_usped use=attr column=count color=viridis

d.vect map=scatterplot_grid_2012_usped where="count > 0" icon=basic/point
