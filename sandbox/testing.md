# EXTENSION
g.extension r.evolution url=github.com/baharmon/landscape_evolution

# REGION
g.region raster=elevation res=0.3

# ERDEP
r.evolution elevation=elevation runs=event mode=simwe_mode rain_duration=30 start="2013-01-01 00:00:00" rain_interval=1

# FLUX
r.evolution elevation=elevation runs=event mode=simwe_mode rain_duration=30 transport_value=1 start="2013-01-01 00:00:00" rain_interval=1

transport_value=100

# TRANSPORT LIMITED
r.evolution elevation=elevation runs=event mode=simwe_mode rain_duration=30 detachment_value=1 start="2013-01-01 00:00:00" rain_interval=1

grav_diffusion=0.5

# USPED
r.evolution elevation=elevation runs=event mode=usped_mode rain_duration=30 start="2013-01-01 00:00:00" rain_interval=1

n=1.2
m=1.5

# RUSLE 3D
r.evolution elevation=elevation runs=event mode=rusle_mode rain_duration=30 start="2013-01-01 00:00:00" rain_interval=1

n=1.2
m=0.5

# COMPLEX ERDEP
g.copy raster=mannings_2013@PERMANENT,mannings_2013
g.copy raster=runoff_2013@PERMANENT,runoff_2013
r.evolution elevation=elevation runs=event mode=simwe_mode rain_duration=30 runoff=runoff_2013@complex_erdep mannings=mannings_2013 start="2015-10-06 00:00:00" rain_interval=1

# COMPLEX USPED
g.copy raster=k_factor@PERMANENT,k_factor
g.copy raster=c_factor_2013@PERMANENT,c_factor_2013
r.evolution elevation=elevation runs=event mode=usped_mode rain_duration=30 k_factor=k_factor c_factor=c_factor_2013 start="2015-10-06 00:00:00" rain_interval=1
