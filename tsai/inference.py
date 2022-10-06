# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/052a_inference.ipynb.

# %% auto 0
__all__ = []

# %% ../nbs/052a_inference.ipynb 2
from fastai.learner import load_learner
from fastai.learner import Learner
from fastcore.basics import patch

# %% ../nbs/052a_inference.ipynb 3
@patch
def get_X_preds(self: Learner, X, y=None, bs=64, with_input=False, with_decoded=True, with_loss=False):
    if with_loss and y is None:
        print("cannot find loss as y=None")
        with_loss = False
    dl = self.dls.valid.new_dl(X, y=y, bs=bs)
    output = list(self.get_preds(dl=dl, with_input=with_input, with_decoded=with_decoded, with_loss=with_loss, reorder=False))
    if with_decoded and len(self.dls.tls) >= 2 and hasattr(self.dls.tls[-1], "tfms") and hasattr(self.dls.tls[-1].tfms, "decodes"):
        output[2 + with_input] = self.dls.tls[-1].tfms.decode(output[2 + with_input])
    return tuple(output)
