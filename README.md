# Agora-Post-Processing-TimeStamp

This repo contains files to process the time stamps by running Agora.

## Basic

Use `pipenv` as the virtual env to run this project.

1. `pip install pipenv` if you do not have `pipenv` yet
2. `pipenv shell` to initiate the env
3. `pipenv install` to install the required Python packages

## Plotting results from WiNTECH 23

* Put raw data under `data/`
    * All WiNTECH results are under `data/wintech`, please move the needed to under `data/`
* Run the scripts under `plot/`
* Find the figures under `fig/`

If you have any question for this part, please contact @cstandy .

## General Agora Post-processing

* Python scripts are under `python/`, including
    * Post-processing (parsing) the `.txt` output from Agora's `stdout`
    * Further plotting scripts using the outputs of these parsers
* Put the standard output under `log/`
