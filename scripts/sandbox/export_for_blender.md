# export maps for subregion
g.mapset mapset=subregion -c
g.region region=subregion res=1

## existing maps
r.mapcalc expression="elevation = elevation_2012"
r.mapcalc expression="landcover = landcover"
r.mapcalc expression="bare_ground = if(landcover==31,1,0)"
r.colors map=bare_ground color=grey
r.mapcalc expression="mixed_forest = if(landcover==43,1,0)"
r.colors map=mixed_forest color=grey
r.mapcalc expression="grass = if(landcover==71,1,0)"
r.colors map=grass color=grey
r.mapcalc expression="landforms = landforms_2012"
r.mapcalc expression="valleys = if(landforms==9 ||| landforms==10,1,0)"
r.colors map=valleys color=grey
r.mapcalc expression="ridges = if(landforms==3 ||| landforms==4,1,0)"
r.colors map=ridges color=grey
r.mapcalc expression="slopes = if(landforms==6,1,0)"
r.colors map=slopes color=grey
r.mapcalc expression="pits = if(landforms==2 ||| landforms==8)"
r.colors map=pits color=grey
r.mapcalc expression="forest = if(valleys==1,0,mixed_forest)"
r.colors map=forest color=grey
r.out.gdal input=elevation output=elevation.tif format=GTiff
r.out.gdal input=grass output=grass.tif format=GTiff
r.out.gdal input=mixed_forest output=mixed_forest.tif format=GTiff
r.out.gdal input=bare_ground output=bare_ground.tif format=GTiff
r.out.gdal input=slopes output=slopes.tif format=GTiff
r.out.gdal input=ridges output=ridges.tif format=GTiff
r.out.gdal input=valleys valleys.tif format=GTiff
r.out.gdal input=forest output=forest.tif format=GTiff

## evolved maps
g.mapsets mapset=ss_flux operation=add
r.mapcalc expression="evolved_elevation = elevation_2016_01_01_02_00_00@ss_flux"
r.mapcalc expression="landforms = landforms@ss_flux"
r.mapcalc expression="valleys = if(landforms==9 ||| landforms==10,1,0)" --overwrite
r.colors map=valleys color=grey
r.mapcalc expression="ridges = if(landforms==3 ||| landforms==4,1,0)" --overwrite
r.colors map=ridges color=grey
r.mapcalc expression="slopes = if(landforms==6,1,0)" --overwrite
r.colors map=slopes color=grey
r.mapcalc expression="pits = if(landforms==2 ||| landforms==8)" --overwrite
r.colors map=pits color=grey
r.out.gdal input=evolved_elevation output=evolved_elevation.tif format=GTiff
r.out.gdal input=slopes output=evolved_slopes.tif format=GTiff
r.out.gdal input=ridges output=evolved_ridges.tif format=GTiff
r.out.gdal input=valleys evolved_valleys.tif format=GTiff
r.out.gdal input=pits output=evolved_pits.tif format=GTiff

# export maps for region
g.mapset mapset=region -c
g.region region=region res=1

## existing maps
r.mapcalc expression="elevation = elevation_2012"
r.mapcalc expression="bare_ground = if(landcover==31,1,0)"
r.colors map=bare_ground color=grey
r.mapcalc expression="mixed_forest = if(landcover==43,1,0)"
r.colors map=mixed_forest color=grey
r.mapcalc expression="grass = if(landcover==71,1,0)"
r.colors map=grass color=grey
r.mapcalc expression="landforms = landforms_2012" --overwrite
r.mapcalc expression="valleys = if(landforms==9 ||| landforms==10,1,0)" --overwrite
r.colors map=valleys color=grey
r.mapcalc expression="ridges = if(landforms==3 ||| landforms==4,1,0)" --overwrite
r.colors map=ridges color=grey
r.mapcalc expression="slopes = if(landforms==6,1,0)" --overwrite
r.colors map=slopes color=grey
r.mapcalc expression="pits = if(landforms==2 ||| landforms==8)" --overwrite
r.colors map=pits color=grey
r.mapcalc expression="forest = if(valleys==1,0,mixed_forest)"
r.colors map=forest color=grey
r.out.gdal input=elevation output=elevation.tif format=GTiff
r.out.gdal input=grass output=grass.tif format=GTiff
r.out.gdal input=mixed_forest output=mixed_forest.tif format=GTiff
r.out.gdal input=bare_ground output=bare_ground.tif format=GTiff
r.out.gdal input=slopes output=slopes.tif format=GTiff
r.out.gdal input=ridges output=ridges.tif format=GTiff
r.out.gdal input=valleys valleys.tif format=GTiff
r.out.gdal input=forest output=forest.tif format=GTiff

## evolved maps
g.mapsets mapset=ss_flux operation=add
r.mapcalc expression="evolved_elevation = elevation_2016_01_01_02_00_00@ss_flux"
r.mapcalc expression="landforms = landforms@ss_flux" --overwrite
r.mapcalc expression="valleys = if(landforms==9 ||| landforms==10,1,0)" --overwrite
r.colors map=valleys color=grey
r.mapcalc expression="ridges = if(landforms==3 ||| landforms==4,1,0)" --overwrite
r.colors map=ridges color=grey
r.mapcalc expression="slopes = if(landforms==6,1,0)" --overwrite
r.colors map=slopes color=grey
r.mapcalc expression="pits = if(landforms==2 ||| landforms==8)" --overwrite
r.colors map=pits color=grey
r.out.gdal input=evolved_elevation output=evolved_elevation.tif format=GTiff
r.out.gdal input=slopes output=evolved_slopes.tif format=GTiff
r.out.gdal input=ridges output=evolved_ridges.tif format=GTiff
r.out.gdal input=valleys evolved_valleys.tif format=GTiff
r.out.gdal input=pits output=evolved_pits.tif format=GTiff










r.out.gdal input=mixed_forest output=mixed_forest.tif format=GTiff
r.out.gdal input=bare_ground output=bare_ground.tif format=GTiff
r.out.gdal input=slopes output=slopes.tif format=GTiff
r.out.gdal input=ridges output=ridges.tif format=GTiff
r.out.gdal input=valleys valleys.tif format=GTiff
r.out.gdal input=forest output=forest.tif format=GTiff
