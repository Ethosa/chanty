class Selector:
    S = "@s"
    P = "@p"
    A = "@a"
    E = "@e"

    @staticmethod
    def e(**kwargs) -> str:
        if not kwargs:
            return "@e"
        parts = [f"{k}={v}" for k, v in kwargs.items()]
        return f"@e[{','.join(parts)}]"
