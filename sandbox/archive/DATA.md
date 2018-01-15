# lidar

## reproject 2004

cd nc_spm_fort_bragg/lidar

txt2las -skip 1 -i be3710945900go20040820.txt -o be3710945900go20040820.las -parse xyz

txt2las -skip 1 -i be3710946900go20040820.txt -o be3710946900go20040820.las -parse xyz

las2las --a_srs=EPSG:6543 --t_srs=EPSG:3358 -i be3710945900go20040820.las -o ncspm_be3710945900go20040820.las

las2las --a_srs=EPSG:6543 --t_srs=EPSG:3358 -i be3710946900go20040820.las -o ncspm_be3710946900go20040820.las

## reproject 2012

cd nc_spm_fort_bragg/lidar

las2las --a_srs=EPSG:6543 --t_srs=EPSG:3358 -i I-08.las -o ncspm_I-08.las

las2las --a_srs=EPSG:6543 --t_srs=EPSG:3358 -i J-08.las -o ncspm_J-08.las

g.region n=151030 s=150580 w=597195 e=597645 save=region res=0.3

## reproject 2016

cd nc_spm_fort_bragg/lidar

las2las 7884_1.las --scale 0.001 0.001 0.001 -o 7884_1_scaled.las

las2las --a_srs=EPSG:2264 --t_srs=EPSG:3358 -i 7884_1_scaled.las -o ncspm_7884_1.las

## compute digital elevation model for 2004

v.in.lidar -r -t input=fort_bragg_data/ncspm_be3710945900go20040820.las output=be3710945900go20040820

v.in.lidar -r -t input=fort_bragg_data/ncspm_be3710945900go20040820.las output=be3710946900go20040820

v.patch input=be3710945900go20040820,be3710946900go20040820 output=points_204

g.remove -f type=vector name=be3710945900go20040820,be3710946900go20040820

v.kernel input=points_2004 output=kernel_2004 radius=4 kernel=uniform

r.mapcalc "voids_2004 = if(kernel_2002==0,1,null())"

r.random -d input=elevation_2012 cover=voids_2004 npoints=2% vector=fill_2004

v.patch input=points_2004,fill_2004 output=patch_2004

g.rename vector=patch_2004,points_2004 --overwrite

g.remove -f type=vector name=fill_2004

g.remove -f type=raster name=kernel_2004,voids_2004

v.surf.rst input=points_2004 elevation=elevation_2004 tension=30 smooth=1

## compute digital elevation model for 2012

v.in.lidar -r -t input=fort_bragg_data/I-08_spm.las output=i_08 class_filter=2

v.in.lidar -r -t input=fort_bragg_data/J-08_spm.las output=j_08 class_filter=2

v.patch input=i_08,j_08 output=points_2012

g.remove -f type=vector name=i_08,j_08

v.surf.rst input=points_2012 elevation=elevation_2012 tension=10 smooth=1

## compute digital elevation model for 2016

v.in.lidar -r -t input=fort_bragg_data/ncspm_7884_1.las output=points_2016

v.kernel input=points_2016 output=kernel_2016 radius=4 kernel=uniform

r.mapcalc "voids_2016 = if(kernel_2016==0,1,null())"

r.random -d input=elevation_2012 cover=voids_2016 npoints=4% vector=fill_2016

v.patch input=points_2016,fill_2016 output=patch_2016

g.rename vector=patch_2016,points_2016 --overwrite

g.remove -f type=vector name=fill_2016

g.remove -f type=raster name=kernel_2016,voids_2016

v.surf.rst input=points_2016 elevation=elevation_2016 tension=7 smooth=1

## compute differences in time series

r.mapcalc "difference_2004_2016 = elevation_2016 - elevation_2004"

r.mapcalc "difference_2004_2012 = elevation_2012 - elevation_2004"

r.mapcalc "difference_2012_2016 = elevation_2016 - elevation_2012"

r.colors map=difference_2004_2016 color=differences

r.colors map=difference_2004_2012 color=differences

r.colors map=difference_2012_2016 color=differences

## compute watershed

r.watershed elevation=elevation_2016 threshold=300000 basin=watersheds

r.mapcalc "watershed = if(watersheds == 4, 1, null())"

r.to.vect -s input=watershed output=watershed type=area

g.remove -f type=raster name=watersheds,watershed

## fix lidar shift

wxGUI.vdigit

v.select ainput=points_2012 binput=mask output=points_2012_a operator=intersects

v.select ainput=points_2012 binput=mask output=points_2012_b operator=disjoint

v.edit map=points_2012_a type=point tool=move move=0,0,0.7 bbox=597645,151030,597195,150580

v.patch input=points_2012_a,points_2012_b output=corrected_2012

v.surf.rst input=corrected_2012 elevation=elevation_2012 tension=10 smooth=1 --overwrite

r.mapcalc "difference_2004_2012 = elevation_2012 - elevation_2004" --overwrite

r.mapcalc "difference_2012_2016 = elevation_2016 - elevation_2012" --overwrite

g.remove -f type=vector name=points_2012_a,points_2012_b

## multiple return 2012

r.in.lidar input=fort_bragg_data/ncspm_I-08.las output=vegetation_2012 method=max resolution=2 class_filter=3,4,5 return_filter=first

r.colors map=vegetation_2012 color=viridis

# imagery

# import imagery web mapping services

g.region res=1

r.in.wms url=https://nccoastalatlas.org/geoserver/ows?service=wms output=naip_2009 layers=naip2009:img srs=4326 wms_version=1.3.0

r.in.wms url=https://nccoastalatlas.org/geoserver/ows?service=wms output=naip_2010 layers=naip2010:img srs=4326 wms_version=1.3.0

r.in.wms url=https://nccoastalatlas.org/geoserver/ows?service=wms output=naip_2012 layers=naip2012:img srs=4326 wms_version=1.3.0

# import imagery

g.region region=region res=1

r.import input=fort_bragg_data/n_3507963_ne_17_1_20060622.tif output=naip_2006 title=naip_2006 resample=nearest resolution=value resolution_value=1 extent=region

r.composite red=naip_2006.1 green=naip_2006.2 blue=naip_2006.3 output=naip_2006

r.import input=fort_bragg_data/m_3507963_ne_17_1_20090603.tif output=naip_2009 title=naip_2009 resample=nearest resolution=value resolution_value=1 extent=region

r.composite red=naip_2009.1 green=naip_2009.2 blue=naip_2009.3 output=naip_2009

r.import input=fort_bragg_data/m_3507963_ne_17_1_20100627.tif output=naip_2010 title=naip_2010 resample=nearest resolution=value resolution_value=1 extent=region

r.composite red=naip_2010.1 green=naip_2010.2 blue=naip_2010.3 output=naip_2010

r.import input=fort_bragg_data/m_3507963_ne_17_1_20120531.tif output=naip_2012 title=naip_2012 resample=nearest resolution=value resolution_value=1 extent=region

r.composite red=naip_2012.1 green=naip_2012.2 blue=naip_2012.3 output=naip_2012

r.import input=fort_bragg_data/m_3507963_ne_17_1_20140517.tif output=naip_2014 title=naip_2014 resample=nearest resolution=value resolution_value=1 extent=region

r.composite red=naip_2014.1 green=naip_2014.2 blue=naip_2014.3 output=naip_2014

## classify imagery

i.group group=imagery subgroup=naip_2014 input=naip_2014.1,naip_2014.2,naip_2014.3

i.cluster group=imagery subgroup=naip_2014 signaturefile=signature_naip_2014 classes=2

i.maxlik group=imagery subgroup=naip_2014 signaturefile=signature_naip_2014 output=classification_naip_2014

r.colors map=classification_naip_2014 color=viridis

## categorize imagery

r.recode input=classification_naip_2014 output=recode_naip_2014 rules=imagery_to_landcover.txt

r.mapcalc "landcover = if(isnull(vegetation_2012), recode_naip_2014, 43)"

r.colors map=landcover rules=color_landcover.txt

r.category map=landcover separator=pipe rules=landcover_categories.txt

## derive k factor, c factor, mannings, and runoff

v.import input=fort_bragg_data/wss_aoi_2017-05-21_15-12-11/wss_aoi_2017-05-21_15-12-11\spatial\soilmu_a_aoi.shp output=soils extent=region

v.to.rast input=soils@PERMANENT output=soil_types use=cat memory=3000

r.recode input=soil_types output=soils rules=soil_classification.txt

r.category map=soils separator=pipe rules=soil_categories.txt

r.colors map=soils color=sepia

r.recode input=soils output=k_factor rules=soil_to_kfactor.txt

r.colors map=k_factor color=sepia

r.recode input=landcover output=c_factor rules=landcover_to_cfactor.txt

r.colors map=c_factor color=sepia

r.recode input=landcover output=mannings rules=landcover_to_mannings.txt

r.colors map=mannings color=sepia

r.recode input=landcover output=runoff rules=landcover_to_runoff.txt

r.colors map=runoff color=water

g.remove -f type=raster name=soil_types,recode_naip_2014,classification_naip_2014
