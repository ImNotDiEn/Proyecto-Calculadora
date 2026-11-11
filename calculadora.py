from math import log10, sin, cos, pi, radians


def _fmt(n):
    """Muestra enteros sin .0. Ej: 8.0 → '8', 2.5 → '2.5'."""
    n = round(n, 10)
    return str(int(n)) if n == int(n) else str(n)


class Calculadora:

    def __init__(self):
        self.reset()

    def reset(self):
        self.display = '0'
        self.expr = ''
        self.op = None
        self.v = 0.0
        self.new = True
        return self.display

    def input(self, k):
        try:
            if k in '0123456789.':
                self._digit(k)
            elif k in '+-*/':
                self._operator(k)
            elif k == '=':
                self._equals()
            elif k == 'C':
                self.reset()
            elif k == 'sin':
                self._unary(lambda x: sin(radians(x)), 'sin')
            elif k == 'cos':
                self._unary(lambda x: cos(radians(x)), 'cos')
            elif k == 'log':
                self._unary(log10, 'log')
            elif k == 'π':
                self.display = _fmt(pi)
                self.new = True
        except Exception:
            self.display, self.expr, self.new, self.op = "Error", '', True, None
        return self.display

    def _digit(self, k):
        if self.expr.endswith('='):
            self.expr = ''
        if self.new:
            self.display = '0' if k == '.' else k
            self.new = False
        else:
            if k == '.' and '.' in self.display:
                return
            self.display = self.display + k if self.display != '0' else k

    def _operator(self, op):
        if self.op and not self.new:
            self._equals()
        self.v = float(self.display or 0)
        self.op = op
        self.new = True
        self.expr = f"{_fmt(self.v)} {op}"

    def _equals(self):
        if self.op is None:
            return
        x = float(self.display or 0)
        r = {'+': self.v + x, '-': self.v - x,
             '*': self.v * x, '/': self.v / x}[self.op]
        self.expr = f"{_fmt(self.v)} {self.op} {_fmt(x)} ="
        self.display = _fmt(r)
        self.op = None
        self.new = True

    def _unary(self, fn, label):
        x = float(self.display or 0)
        self.expr = f"{label}({self.display})"
        self.display = _fmt(fn(x))
        self.new = True