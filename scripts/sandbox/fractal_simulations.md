# fractal landscape evolution simulations

## install dependencies
```
g.extension extension=r.cpt2grass
```

## steady state erosion-deposition simulation
```
g.mapset -c mapset=fractal_ss_erdep
g.region res=1 n=150870 s=150720 w=597290 e=597440
r.surf.fractal output=elevation
r.neighbors -c --overwrite input=elevation output=smoothed_elevation size=11
g.region res=1 n=150845 s=150745 w=597315 e=597415
r.mapcalc expression="elevation = smoothed_elevation" --overwrite
g.remove -f type=raster name=smoothed_elevation
r.evolution -f elevation=elevation runs=event rain_duration=60 rain_interval=60 threads=6 grav_diffusion=0.05
```

## steady state flux simulation
```
g.mapset -c mapset=fractal_ss_flux
g.mapsets mapset=fractal_ss_erdep operation=add
g.region res=1 n=150845 s=150745 w=597315 e=597415
g.copy raster=elevation@fractal_ss_erdep,elevation
g.mapsets mapset=fractal_ss_erdep operation=remove
r.evolution -f elevation=elevation runs=event rain_duration=60 rain_interval=60 detachment_value=0.0001 transport_value=0.01 threads=6 grav_diffusion=0.05
```

## steady state usped simulation
```
g.mapset -c mapset=fractal_ss_usped
g.mapsets mapset=fractal_ss_erdep operation=add
g.region res=1 n=150845 s=150745 w=597315 e=597415
g.copy raster=elevation@fractal_ss_erdep,elevation
g.mapsets mapset=fractal_ss_erdep operation=remove
r.evolution -f elevation=elevation runs=event mode=usped rain_duration=720 rain_interval=720
```

# steady state rusle simulation
```
g.mapset -c mapset=fractal_ss_rusle
g.mapsets mapset=fractal_ss_erdep operation=add
g.region res=1 n=150845 s=150745 w=597315 e=597415
g.copy raster=elevation@fractal_ss_erdep,elevation
g.mapsets mapset=fractal_ss_erdep operation=remove
r.evolution -f elevation=elevation runs=event mode=rusle rain_duration=240 rain_interval=240 grav_diffusion=0.01
```

Higher gravitational diffusion causes a ridge to form along the centerline of the channel.
```
r.evolution -f elevation=elevation runs=event mode=rusle rain_duration=240 rain_interval=240 grav_diffusion=0.05
```
