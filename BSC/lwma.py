"""
\begin{equation*}
    \left\{x_{t}\right\} =
    \frac{\sum_{i=1}^m (m-i+1) \times x_{t-i}  + \sum_{j=1}^n (n-j+1) \times x_{t+j} }{\sum_{i, j = 1}^{m, n} (m-i+1) \times L_i + \sum_{j=1}^n (n-j+1) \times L_j} \;
\end{equation*}

Boolean coefficients to remove weights:
\begin{equation*}
         L_i, L_j =
    \begin{cases}
      1, & \text{if}\ x_{t-i}, x_{t+j} > 0 \\
      0, & \text{otherwise}
    \end{cases}
\end{equation*}
"""

# Code according to the LATEX math equation above
# script has been used for time series imputation of long-term macroeconomic data

import pandas as pd; from typing import Iterable;


class LWMA:
    def __init__(self, m=2, n=2):
        """
        Args:
            n: number of observations to consider forward in time
            m: number of observations to consider back in time
        """
        self.m = m
        self.n = n

    def fit_transform(self, series: Iterable) -> pd.Series:
        """
        Method to impute missing values in a time series deploying the windowing technique
        Args:
            series: Any iterable data structure (list, pd.Series, np.array, etc.).
        Returns:
            pd.Series: Imputed time series
        """


        # ensure that argument is an instance of pd.Series
        # copy to avoid modifying the input time series
        if not isinstance(series, pd.Series):
            copy = pd.Series(series).copy()
        else:
            copy = series.copy()
        
        # handle NaNs at the beginning and end of series
            
        # handle NaNs at the beginning and end of series
        first_non_zero_index = copy.ne(0).idxmax()
        copy.iloc[0:first_non_zero_index] = copy.loc[first_non_zero_index]

        last_non_zero_index = copy.ne(0)[::-1].idxmax()
        copy.iloc[last_non_zero_index:] = copy.loc[last_non_zero_index]

        # back and forward fill
        copy.iloc[:first_non_zero_index] = copy.iloc[first_non_zero_index]
        copy.iloc[last_non_zero_index:] = copy.iloc[last_non_zero_index]


        # generating the indices of the time series
        all_indices = pd.Series(range(len(copy)))

        # ensure that no NaNs are present
        copy.fillna(0, inplace=True)

        # boolean mask whether value is missing or not
        zero = float(0)
        zero_mask = copy.eq(zero)

        # getting the indices of the missing values using the mask
        zero_indices = all_indices.index[zero_mask]

        # generating the weights
        # highest weights for observations close to the target observation (linearly decreasing)
        w_m = pd.Series(range(1, self.m + 1)[::-1])
        w_n = pd.Series(range(1, self.n + 1)[::-1])

        # indices for how many observations before and after are taken into consideration
        m_back = pd.Series(range(1, self.m + 1))
        n_forw = pd.Series(range(1, self.n + 1))


        # select observations in the current window
        for t in zero_indices:
            try:
                back_m = copy.iloc[t - m_back]
                forw_n = copy.iloc[t + n_forw]
            except IndexError:
                m_back = pd.Series(range(1, self.m))
                n_forw = pd.Series(range(1, self.n))
                continue

            # m values back in time times their weights
            bwd = [(back_m.iloc[i] * w_m.iloc[i]) for i in range(self.m)]

            # n values forward in time times their weights
            fwd = [(forw_n.iloc[j] * w_n.iloc[j]) for j in range(self.n)]

            # boolean, whether values backward or forward are 0 or not

            # if 0 -> they are missing in the data (NaN values)
            L_i = [1 if i > 0 else 0 for i in bwd]
            L_j = [1 if j > 0 else 0 for j in fwd]

            # denominator: comprised of the sum of weights, minus the weights
            # that are not considered if values of fwd or bwd are 0
            denom = sum(w_m.iloc[i] * L_i[i] for i in range(self.m))
            denom += sum(w_n.iloc[j] * L_j[j] for j in range(self.n))

            missing_val = sum(bwd[i] * L_i[i] for i in range(self.m))
            missing_val += sum(fwd[j] * L_j[j] for j in range(self.n))

            missing_val /= denom

            copy.iloc[t] = missing_val

        return copy