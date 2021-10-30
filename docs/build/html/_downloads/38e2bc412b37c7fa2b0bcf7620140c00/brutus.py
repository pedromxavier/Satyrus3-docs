# Standard Library
import itertools as it

# Satyrus
from satyrus import SatAPI, Posiform

class brutus(SatAPI):
    """\
    Satyrus API Brute-Force Solver
    """
    
    def solve(self, energy: Posiform, **params):
        """\
        Parameters
        ----------
        energy: Posiform

        Returns
        -------
        dict[str, int]
            Problem Solution, mapping between variables and states
        float
            Solution's associated energy scalar value
        """
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
    def states(n: int) -> tuple:
        """\
        Generates all possible $2^{n}$ binary states

        Parameters
        ----------
        n: int

        Yields
        ------
        tuple[float]
        """
        return it.product(*((1, 0) for _ in range(n)))
