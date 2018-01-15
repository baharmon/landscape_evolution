Fractal surface
```
r.surf.fractal --overwrite output=fractal_surface dimension=2.9
```

Low pass filter
```
r.mapcalc "smoothed_surface = (fractal_surface@gully[-1,-1] + fractal_surface@gully[-1,0] + fractal_surface@gully[1,1] + fractal_surface@gully[0,-1] + fractal_surface@gully[0,0] + fractal_surface@gully[0,1] + fractal_surface@gully[1,-1] + fractal_surface@gully[1,0] + fractal_surface@gully[1,1]) / 9" --overwrite
```
