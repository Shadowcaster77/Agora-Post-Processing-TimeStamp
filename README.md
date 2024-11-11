# Utility Scripts for Agora/Savannah

This repo contains scripts to process the time stamps recorded when Agora/Savannah is executed.

## Environment Management

We use `pipenv` as the virtual environment to manage the package dependency within this project.

1. `pip install pipenv` if you do not have `pipenv` yet.
2. `pipenv shell` to initiate the env.
3. `pipenv install` to install the required Python packages.

## General Post-processing

1. Use `mvp_test.sh` to run different mode of Agora/Savannah, and the standard output will be recorded as log files.
2. Python scripts under `analyzer/` process (parse) the `.log` output from Agora's `stdout`. The most common functions are reading CPU and elapsed times.
3. Plotting scripts under `plotter/` use the function/output of these parsers.

## Generate Plots

* Put raw data under `data/` or the standard output under `log/`.
* Run the scripts under `plotter/`. Some plotters have hard-coded log path that needs to be modified.
* Find the figures under `fig/`.

### Plotting results from WiNTECH 23

All WiNTECH results are under `data/wintech`.
Please move the needed raw data to `data/` to generate plots.

## Benchmark

We also benchmark (unit test) libraries and classes used in Agora.
So far, we primarily work on testing Armadillo, a C++ based matrix operation library.

* Testing programs are under `benchmark/`.
* To compile, run `make` under `benchmark/`.
* To run test program, run `*.a` under `benchmark/`.

## Scripts

We have some helper functions that automate running Agora.
These scripts are placed under `script/`, but should be run along with Agora programs.

## Reference

* If you have any question for this utility repo, please contact [@cstandy](https://github.com/cstandy).
* The GitHub repo for [Agora](https://github.com/Agora-wireless/Agora/).
* The GitHub repor for [Savannah](https://github.com/functions-lab/Savannah).
