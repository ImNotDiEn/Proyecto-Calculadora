from math import log10, sin, cos, pi, radians


class Calculadora:
    """Motor de la calculadora. Independiente de la interfaz gráfica."""

    def __init__(self):
        self.reset()

    def reset(self):
        """Reinicia el estado a valores iniciales."""
        self.display = '0'
        self.op = None
        self.v = 0.0
        self.new = True
        return self.display

    def input(self, k):
        """Procesa una tecla: '0'-'9', '.', '+-*/', '=', 'C', 'sin', 'cos', 'log', 'π'."""
        try:
            if k in '0123456789.':
                self._digit(k)
            elif k in '+-*/':
                self.v = float(self.display or 0)
                self.op = k
                self.new = True
            elif k == '=':
                self._equals()
            elif k == 'C':
                self.reset()
            elif k == 'sin':
                self.display = str(round(sin(radians(float(self.display or 0))), 8)); self.new = True
            elif k == 'cos':
                self.display = str(round(cos(radians(float(self.display or 0))), 8)); self.new = True
            elif k == 'log':
                self.display = str(round(log10(float(self.display or 1)), 8)); self.new = True
            elif k == 'π':
                self.display = str(round(pi, 10)); self.new = True
        except Exception:
            self.display = "Error"
            self.new = True
        return self.display

    def _digit(self, k):
        self.display = k if self.new else self.display + k
        self.new = False

    def _equals(self):
        x = float(self.display or 0)
        o = self.op
        if o is None:
            r = x  # sin operación pendiente, conserva el número
        else:
            r = {'+': self.v + x, '-': self.v - x, '*': self.v * x, '/': self.v / x}[o]
        self.display = str(round(r, 10))
        self.op = None
        self.new = True