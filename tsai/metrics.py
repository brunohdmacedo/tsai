# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/051_metrics.ipynb.

# %% auto 0
__all__ = ['recall_at_specificity', 'lift', 'lift_at_specificity', 'top_k_lift', 'mean_per_class_accuracy',
           'MatthewsCorrCoefBinary', 'get_task_metrics', 'accuracy_multi', 'metrics_multi_common', 'precision_multi',
           'recall_multi', 'specificity_multi', 'balanced_accuracy_multi', 'Fbeta_multi', 'F1_multi', 'mae', 'mape']

# %% ../nbs/051_metrics.ipynb 2
import sklearn.metrics as skm
from fastai.metrics import * 
from .imports import *

# %% ../nbs/051_metrics.ipynb 3
mk_class('ActivationType', **{o:o.lower() for o in ['No', 'Sigmoid', 'Softmax', 'BinarySoftmax']},
         doc="All possible activation classes for `AccumMetric")

# %% ../nbs/051_metrics.ipynb 4
def MatthewsCorrCoefBinary(sample_weight=None):
    "Matthews correlation coefficient for single-label classification problems"
    return AccumMetric(skm.matthews_corrcoef, dim_argmax=-1, activation=ActivationType.BinarySoftmax, thresh=.5, sample_weight=sample_weight)

# %% ../nbs/051_metrics.ipynb 5
def get_task_metrics(dls, binary_metrics=None, multi_class_metrics=None, regression_metrics=None, verbose=True): 
    if dls.c == 2: 
        pv('binary-classification task', verbose)
        return binary_metrics
    elif dls.c > 2: 
        pv('multi-class task', verbose)
        return multi_class_metrics
    else:
        pv('regression task', verbose)
        return regression_metrics

# %% ../nbs/051_metrics.ipynb 7
def accuracy_multi(inp, targ, thresh=0.5, sigmoid=True, by_sample=False):
    "Computes accuracy when `inp` and `targ` are the same size."
    if sigmoid: inp = inp.sigmoid()
    correct = (inp>thresh)==targ.bool()
    if by_sample:
        return (correct.float().mean(-1) == 1).float().mean()
    else:
        inp,targ = flatten_check(inp,targ)
        return correct.float().mean()
    
def metrics_multi_common(inp, targ, thresh=0.5, sigmoid=True, by_sample=False):
    "Computes TP, TN, FP, FN when `inp` and `targ` are the same size."
    if not by_sample: inp,targ = flatten_check(inp,targ)
    if sigmoid: inp = inp.sigmoid()
    pred = inp>thresh
    
    correct = pred==targ.bool()
    TP = torch.logical_and(correct, (targ==1).bool()).sum()
    TN = torch.logical_and(correct, (targ==0).bool()).sum()
    
    incorrect = pred!=targ.bool()
    FN = torch.logical_and(incorrect, (targ==1).bool()).sum()
    FP = torch.logical_and(incorrect, (targ==0).bool()).sum()
    
    N =  targ.size()[0]
    return N, TP, TN, FP, FN

def precision_multi(inp, targ, thresh=0.5, sigmoid=True):
    "Computes precision when `inp` and `targ` are the same size."
    
    inp,targ = flatten_check(inp,targ)
    if sigmoid: inp = inp.sigmoid()
    pred = inp>thresh
    
    correct = pred==targ.bool()
    TP = torch.logical_and(correct,  (targ==1).bool()).sum()
    FP = torch.logical_and(~correct, (targ==0).bool()).sum()

    precision = TP/(TP+FP)
    return precision

def recall_multi(inp, targ, thresh=0.5, sigmoid=True):
    "Computes recall when `inp` and `targ` are the same size."
    
    inp,targ = flatten_check(inp,targ)
    if sigmoid: inp = inp.sigmoid()
    pred = inp>thresh
    
    correct = pred==targ.bool()
    TP = torch.logical_and(correct,  (targ==1).bool()).sum()
    FN = torch.logical_and(~correct, (targ==1).bool()).sum()

    recall = TP/(TP+FN)
    return recall

def specificity_multi(inp, targ, thresh=0.5, sigmoid=True):
    "Computes specificity (true negative rate) when `inp` and `targ` are the same size."
    
    inp,targ = flatten_check(inp,targ)
    if sigmoid: inp = inp.sigmoid()
    pred = inp>thresh
    
    correct = pred==targ.bool()
    TN = torch.logical_and(correct,  (targ==0).bool()).sum()
    FP = torch.logical_and(~correct, (targ==0).bool()).sum()

    specificity = TN/(TN+FP)
    return specificity

def balanced_accuracy_multi(inp, targ, thresh=0.5, sigmoid=True):
    "Computes balanced accuracy when `inp` and `targ` are the same size."
    
    inp,targ = flatten_check(inp,targ)
    if sigmoid: inp = inp.sigmoid()
    pred = inp>thresh
    
    correct = pred==targ.bool()
    TP = torch.logical_and(correct,  (targ==1).bool()).sum()
    TN = torch.logical_and(correct,  (targ==0).bool()).sum()
    FN = torch.logical_and(~correct, (targ==1).bool()).sum()
    FP = torch.logical_and(~correct, (targ==0).bool()).sum()

    TPR = TP/(TP+FN)
    TNR = TN/(TN+FP)
    balanced_accuracy = (TPR+TNR)/2
    return balanced_accuracy

def Fbeta_multi(inp, targ, beta=1.0, thresh=0.5, sigmoid=True):
    "Computes Fbeta when `inp` and `targ` are the same size."
    
    inp,targ = flatten_check(inp,targ)
    if sigmoid: inp = inp.sigmoid()
    pred = inp>thresh
    
    correct = pred==targ.bool()
    TP = torch.logical_and(correct,  (targ==1).bool()).sum()
    TN = torch.logical_and(correct,  (targ==0).bool()).sum()
    FN = torch.logical_and(~correct, (targ==1).bool()).sum()
    FP = torch.logical_and(~correct, (targ==0).bool()).sum()

    precision = TP/(TP+FP)
    recall = TP/(TP+FN)
    beta2 = beta*beta
    
    if precision+recall > 0:
        Fbeta = (1+beta2)*precision*recall/(beta2*precision+recall)
    else:
        Fbeta = 0
    return Fbeta

def F1_multi(*args, **kwargs):
    return Fbeta_multi(*args, **kwargs)  # beta defaults to 1.0

# %% ../nbs/051_metrics.ipynb 8
def mae(inp,targ):
    "Mean absolute error between `inp` and `targ`."
    inp,targ = flatten_check(inp,targ)
    return torch.abs(inp - targ).mean()

# %% ../nbs/051_metrics.ipynb 9
def mape(inp,targ):
    "Mean absolute percentage error between `inp` and `targ`."
    inp,targ = flatten_check(inp, targ)
    return (torch.abs(inp - targ) / torch.clamp_min(targ, 1e-8)).mean()

# %% ../nbs/051_metrics.ipynb 10
def _recall_at_specificity(inp, targ, specificity=.95, axis=-1):
    inp0 = inp[(targ == 0).data]
    inp1 = inp[(targ == 1).data]
    thr = torch.sort(inp0).values[-int(len(inp0) * (1 - specificity))]
    return (inp1 > thr).float().mean()

recall_at_specificity = AccumMetric(_recall_at_specificity, specificity=.95, activation=ActivationType.BinarySoftmax, 
                                    flatten=False, name='recall_at_specificity')

# %% ../nbs/051_metrics.ipynb 11
def _lift(inp, targ, axis=-1):
    "Calculates lift as precision / average rate"
    return targ[(torch.argmax(inp, -1) == 1).data].mean() / targ.mean()

lift = AccumMetric(_lift, activation=ActivationType.BinarySoftmax, flatten=False, name='lift')

def _lift_at_specificity(inp, targ, specificity=0.95, axis=-1):
    "Calculates lift as precision / average rate at a given specificity"
    inp0 = inp[(targ == 0).data]
    thr = torch.sort(inp0).values[-int(len(inp0) * (1 - specificity))]
    return (targ[(inp >= thr).data] == 1).float().mean() / (targ == 1).float().mean()

lift_at_specificity = AccumMetric(_lift_at_specificity, specificity=.95, activation=ActivationType.BinarySoftmax, 
                                  flatten=False, name='lift_at_specificity')

def _top_k_lift(inp, targ, k=0.01):
    """Top k over random k lift calculated as the ratio between precision at 
    top k % positive probabilities and average ratio"""
    top_k_thr = torch.sort(inp).values[-int(k * len(inp))]
    return targ[(inp >= top_k_thr).data].float().mean() / (targ == 1).float().mean()

top_k_lift = AccumMetric(_top_k_lift, k=.01, activation=ActivationType.BinarySoftmax, flatten=False, name='top_k_lift')

# %% ../nbs/051_metrics.ipynb 12
def _mean_per_class_accuracy(y_true, y_pred, *, labels=None, sample_weight=None, normalize=None):
    cm = skm.confusion_matrix(y_true, y_pred, labels=labels, sample_weight=sample_weight, normalize=normalize)
    return (cm.diagonal() / cm.sum(1)).mean()

mean_per_class_accuracy = skm_to_fastai(_mean_per_class_accuracy)
