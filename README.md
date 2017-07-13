# Heterogeneous Wireless Sensor Network Simulation

A program based on [An Improved Centralized Algorithm for Distance-Preserving Dominating Sets in Heterogeneous Wireless Sensor Networks](http://ieeexplore.ieee.org/document/7859930/).

## Preparation

### Virtualenv
We use [Python](https://www.python.org) version 3 to develop this program.  So, you might want to use ``virtualenv`` to manage its dependencies.
If you already have Python, type the following command to install virtualenv:
```shell
$ pip install virtualenv
```

After installation, to activate the environment, to create new environment type:
```shell
$ virtualenv -p PATH_TO_PYTHON3 env
```
This command will create a folder name ``env`` in your current directory which contains a copy of Python.
Note that you need to replace `PATH_TO_PYTHON3` by your python3 executable path, e.g. ``$ virtualenv -p python3 env``.

Every time you need to run the program or install new packages, you just activate the environment by:
```shell
$ . env/bin/activate
```

### Required packages
To install required packages, after the first time you activate the environment type:
```shell
pip install -r requirement.txt
```

## Usage

### Setting
Experiment settings are specified in `setting.py`:

| variable        | type      | description                                                                                          |
|-----------------|-----------|------------------------------------------------------------------------------------------------------|
| `r_mins`        | `list`    | list of $r_{min}$                                                                                    |
| `rhos`          | `list`    | list of $\rho$                                                                                       |
| `cases`         | `integer` | number of testcases                                                                                  |
| `nums`          | `range`   | range of number of nodes                                                                             |
| `input_folder`  | `string`  | name of folder containing files in which each line describe details of node in graph as `x y radius` |
| `output_folder` | `string`  | name of folder to keep simulation result                                                             |

### Generating graphs
```shell
$ python graph.py
```

### Simulation
```shell
$ python simulate.py
```

### Plotting the result
```shell
$ python plot.py <r_min> <rho>
```
