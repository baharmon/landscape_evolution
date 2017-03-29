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

# switch

sheer = (double)(cmul2 * gama[k][l] * sinsl);       /* shear stress */
/* if critical shear stress >= shear then all zero */
if ((sheer <= tau[k][l]) || (ct[k][l] == 0.)) {
si[k][l] = 0.;
sigma[k][l] = 0.;
}
else {
si[k][l] = (double)(dc[k][l] * (sheer - tau[k][l]));
sigma[k][l] = (double)(dc[k][l] / ct[k][l]) * (sheer - tau[k][l]) / (pow(sheer, 1.5));  /* rill erosion=1.5, sheet = 1.1 */
