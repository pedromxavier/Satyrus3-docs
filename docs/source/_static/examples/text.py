from satyrus import Posiform, SatAPI

class text(SatAPI):

    def solve(self, energy: Posiform, **params):
        return str(energy)
