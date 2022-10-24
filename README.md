
# NRPreTo (a two level NR protein clasification tool)

NRPreTo is a two level Nuclear Receptor (NR) protein subfamily classification tool in which the first level  predicts whether a protein sequence is a NR or not and second level predicts the sub-class of the said NR proteins.Only true positive proteins predicted as NRs at level-1 are taken ahead for the second level prediction.Feature selection was done at both levels independently to select important descriptors from an initial 13,494 descriptors calculated using iFeature package.We also performed hyper-parameters tuning at each level to obtained best performing model. NRPreTo has successfully predicted 59 novel NR from human proteome when tested on HRPD and Refseq datasets.

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
  #for example if user wants to perform hyper-parameters tune but not feature selection, execute following line of code
  python3 main.py --feature_selection = 0 --hyperparameter_tune = 1
```
## Data Folder

We have provided subsets of following dataset for user to test NRPreTo.
1. Benchmark Dataset 1 (train (100 samples) and independent (100 samples))
2. Benchmark Dataset 2 (train (84 samples) and independent (86 samples))
3. Human Protein Reference Database (HPRD) (81 samples)
4. Refseq Dataset (83 samples)

Both benchmark datasets were prepared from the Nuclear Receptor Database (NucleaRDB Release 5.0) 
containing 3016 NR sequences which are phylogenetically classified into seven subfamilies with
each subfamily containing NR sequences from different animal species.

#Feature generation using iFeature package

Feature generation was done using the standalone version of iFeature package as per the instructions described in the github repository at https://github.com/Superzchen/iFeature. iFeature is an open source Python-based toolkit for generating a multitude of descriptors for protein and peptide sequences. 
For this study we calculated 13,494 descriptors which belong to seven descriptor groups shown in table 6. We downloaded iFeature package provided in their github repository and followed the instructions to calculate the above mentioned seven descriptor group individually which were concatenated later leading to 13,494 descriptors.              

## Script Description

#### main.py
This is a main script. User need to run this script to run NRPreTo. 

#### hyperparameter_tune.py
This scripts uses Hyperopt package in order to select best hyperparameters for RF model. User can edit 'Space' (line 13) dictionary in order to change hyperparameter range pool. User can also change scoring method (line 26) in order to change metrics to evaluate models with different hyperparameters.

#### feature_rank.py
This scripts uses Borutapy package in order to select important features for RF model. User can edit RF models hyperparameters (line 12) to be used for feature ranking.

#### utilities.py
This script is comprised of helper functions that are used to build the method.

#### model_eval.py
This script is used to evaluate model at 2 different levels. This scripts provides both confusion matrix and model performance in terms of F1, Accuracy, Presicion, Recall, ROC-AUC score and Mathews Correlation Coefficient.




## Run Locally

Clone the project

```bash
  git clone https://github.com/bozdaglab/NRPreTo
```

Install libraries

```bash
  pip install Boruta
  pip install hyperopt
```

Run NRPreTo

```bash
  python3 main.py 
```

