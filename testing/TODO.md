# TODO

## SIMULATIONS
* steady state erdep 120 min with diffusion and no mannings or runoff
  * try with diffusion of 0.1 then 0.5
* steady state RUSLE and USPED for Fort Bragg
  * steady state USPED
  * dynamic RULSE?
* simulations on fractal elevations for RUSLE, USPED, and SIMWE
  * hi and long fractal length
  * for figures in math sections
* simulation_2013_2016.py at 1m res with sink filling
  * depression filling final result with r.fill.dir or r.hydrodem
  * update r.evolution with sink filling parameter and function

## TASKS
* upload updated ncspm_evolution mapset
* 3D visualizations with m.nviz.image
* animate with g.gui.animation
* first release of code
    * doi
* model name: gully

## QUESTIONS
* what happens with regime change?
* will low values smooth the terrain?
* compare with and without mannings & c factor
* test at 3m res before 1m res

## NOTES
* diffusion 2.5 causes deposition in channel but also on slopes

## DEBUGGING
* Change min and max change values in r.evolution
  * Test first with parameters erdepmin, erdepmax, and fluxmax
