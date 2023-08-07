# Utility Scripts for Agora

This repo contains files to process the time stamps by running Agora.

## Basic

Use `pipenv` as the virtual env to run this project.

1. `pip install pipenv` if you do not have `pipenv` yet.
2. `pipenv shell` to initiate the env.
3. `pipenv install` to install the required Python packages.

## General Agora Post-processing

* Python scripts are under `python/`, including
    * Post-processing (parsing) the `.txt` output from Agora's `stdout`.
    * Further plotting scripts using the outputs of these parsers.
* Put the standard output under `log/`.

## Generate Plots

* Put raw data under `data/`.
* Run the scripts under `plot/`.
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

## Reference

* If you have any question for this utility repo, please contact [@cstandy](https://github.com/cstandy).
* The GitHub repo for [Agora](https://github.com/Agora-wireless/Agora/).
