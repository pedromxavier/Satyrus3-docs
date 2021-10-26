from satyrus import SatAPI, Posiform

from cstream import devnull

with devnull:
    import xpress as xp

import numpy as np

class xpress(SatAPI):
    """"""

    def solve(self, energy: Posiform, **params):
        """
        Parameters
        ----------
        energy: Posiform
        """
        x, Q, c = energy.qubo()

        # pylint: disable=no-member
        V = np.array([xp.var(vartype=xp.binary, name=v) for v in x])

        with devnull:
            P = xp.problem(*V, V @ Q @ V)
            P.solve()

        s = {v: int(P.getSolution(V[x[v]])) for v in x}
        e = P.getObjVal()

        return (s, e + c)

