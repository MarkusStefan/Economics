# Code according to the LATEX math equation above
# with variables as in the thesis
import numpy as np
import pandas as pd

def lwma(series, m=2, n=2):

  # check if series argument is an instance of pd.Series
  # copy to avoid modifying the input time series
  if type(series) != type(pd.Series):
    copy = pd.Series(series).copy()

  else:
    copy = series.copy()

  # generating the indices of the time series
  all = pd.Series(range(len(copy)))

  # replacing NaN values by 0
  copy.fillna(0, inplace=True)

  # boolean mask whether value is missing or not
  zero = float(0)
  zero_mask = copy.eq(zero)

  # getting the indices of the missing values using the mask
  zero_idx = all.index[zero_mask]

  # generating the weights
  # highest weights for obs close to the target obs (linearly decreasing)
  w_m = pd.Series(range(1, m+1)[::-1])
  w_n = pd.Series(range(1, n+1)[::-1])

  # indices for how many obs before and after are taken into consideration
  mback = pd.Series(range(1, m+1))
  nforw = pd.Series(range(1, n+1))

  # select obs in the current window
  for t in zero_idx:
    back_m = copy.iloc[t - mback]
    forw_n = copy.iloc[t + nforw]

    # m values back in time times their weights
    bwd = []
    for i in range(m):
      bwd.append(back_m.iloc[i] * w_m.iloc[i])

    # n values forward in time times their weights
    fwd = []
    for j in range(n):
      fwd.append(forw_n.iloc[j] * w_n.iloc[j])

    # boolean, whether values backward or forward are 0 or not
    # if 0 -> they are missing in the data (NaN values)
    L_i = [1 if i > 0 else 0 for i in bwd]
    L_j = [1 if j > 0 else 0 for j in fwd]

    # denominator: comprised of the sum of weights, minus the weights
    # that are not considered if values of fwd or bwd are 0
    denom = 0
    for i in range(m):
      denom += w_m.iloc[i] * L_i[i]
    for j in range(n):
      denom += w_n.iloc[j] * L_j[j]

    missing_val = 0
    for i in range(m):
      missing_val += bwd[i] * L_i[i]
    for j in range(n):
      missing_val += fwd[j] * L_j[j]

    missing_val /= denom

    copy.iloc[t] = missing_val

  return copy
