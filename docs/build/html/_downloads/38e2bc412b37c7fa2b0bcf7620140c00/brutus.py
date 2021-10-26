from satyrus import SatAPI, Posiform

import itertools as it
import numpy as np

class brutus(SatAPI):
    """"""
    
    def solve(self, energy: Posiform, **params):
        """"""
        x = energy.variables

        E = None
        S = None

        n = len(x)

        for s in self.states(n):
            e = float(energy({x[i]: s[i] for i in range(n)}))
            if E is None or e < E:
                E = e
                S = s
        
        return ({x[i]: int(S[i]) for i in range(n)}, E)

    @staticmethod
    def states(n: int) -> np.ndarray:
        """\
        Generates all possible $2^{n}$ binary states

        Parameters
        ----------
        n: int

        Yields
        ------
        np.ndarray[float]
        """
        for s in it.product(*((1, 0) for _ in range(n))):
            yield np.array(s, dtype=float)
