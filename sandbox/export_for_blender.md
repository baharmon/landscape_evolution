g.region region=subregion res=1

r.mapcalc expression="elevation = elevation_2016"

r.mapcalc expression="landcover = landcover"
r.mapcalc expression="bare_ground = if(landcover==31,1,0)"
r.colors map=bare_ground color=grey
r.mapcalc expression="mixed_forest = if(landcover==43,1,0)"
r.colors map=mixed_forest color=grey
r.mapcalc expression="grass = if(landcover==71,1,0)"
r.colors map=grass color=grey

r.mapcalc expression="landforms = landforms_2016"
r.mapcalc expression="ridges = if(landforms==8 ||| landforms==9 ||| landforms==10,1,0)"
r.colors map=valleys color=grey
r.mapcalc expression="ridges = if(landforms==2 ||| landforms==3 ||| landforms==4,1,0)" --overwrite
r.colors map=ridges color=grey
r.mapcalc expression="slopes = if(landforms==6,1,0)" --overwrite
r.colors map=slopes color=grey

r.mapcalc expression="forest = if(valleys==1,0,mixed_forest)"
r.colors map=forest color=grey

# Export
r.out.gdal input=grass output=grass.tif format=GTiff
r.out.gdal input=mixed_forest output=mixed_forest.tif format=GTiff
r.out.gdal input=bare_ground output=bare_ground.tif format=GTiff
r.out.gdal input=slopes output=slopes.tif format=GTiff
r.out.gdal input=ridges output=ridges.tif format=GTiff
r.out.gdal input=valleys valleys.tif format=GTiff
r.out.gdal input=forest output=forest.tif format=GTiff
