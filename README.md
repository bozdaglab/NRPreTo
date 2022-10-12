
# NRPreTo (a 2 level NR protein clasification tool)

NRPreTo is a 2 level NR protein classification tool.
Need to work on the introduction

## Requirements

Following python libraries must be installed in the system in order to run NRPreTo:
1. Boruta 0.3
```bash
pip install Boruta
```
2. Hyperopt 0.2.7
```bash
pip install hyperopt
```
    
## How to run NRPreto

To run NRPreTo with default settings (feature selection = True and hyper parameters tuning = True) at both level, run the following command

```bash
  python3 main.py 
```
To run NRPreTo with no feature selection at both level, run the following command

```bash
  python3 main.py --feature_selection = 0
```

To run NRPreTo with no hyperparameter tuning at both level, run the following command

```bash
  python3 main.py --hyperparameter_tune = 0
```
To run NRPreTo with different combination of settings at both level, run the following command

```bash
  python3 main.py --feature_selection = 0 --hyperparameter_tune = 1
```
## Data Folder

We have provided subsets of following dataset for user to test NRPreTo.
1. Benchmark Dataset 1 (train (100 samples) and independent (100 samples))
2. Benchmark Dataset 2 (train (84 samples) and independent (86 samples))
3. Human Protein Reference Database (HPRD) (81 samples)
4. Refseq Dataset (83 samples)


## Script Description

#### main.py
This is a main script. You need to run this script to run NRPreTo. 

#### hyperparameter_tune.py
This scripts uses Hyperopt package in order to select best hyperparameters for RF model. User can edit 'Space' (line 13) dictionary in order to change hyperparameter range pool. User can also change scoring method (line 26) in order to change metrics to evaluate models with different hyperparameters.

#### feature_rank.py
This scripts uses Borutapy package in order to select important features for RF model. User can edit RF models hyperparameters (line 12) to be used for feature ranking.

#### utilities.py
This script is comprised on small functions used to build the method.

#### model_eval.py
This script is used to evaluate model at 2 different levels.




## Feedback

If you have any feedback, please reach out to us at serdar.bozdag@unt.edu

