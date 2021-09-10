from satyrus import SatAPI, Posiform

class qubo(SatAPI):

    def solve(self, posiform: Posiform, **params: dict) -> tuple[dict, float]:
        x, Q, c = posiform.qubo()

        print(f"x = {x}")
        print(f"Q = {Q}")
        print(f"c = {c}")

        return ""