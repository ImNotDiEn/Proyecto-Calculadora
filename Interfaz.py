import tkinter as tk
from calculadora import Calculadora

BG, DISP, NUM, OP, FN, EQ, TXT = "#1e1e2e", "#2a2a3e", "#3a3a52", "#ff9500", "#4a4a6a", "#2ecc71", "#ffffff"

SHORTCUTS = {'s': 'sin', 'o': 'cos', 'l': 'log', 'p': 'π'}


def lighter(h, a=35):
    return '#' + ''.join(f'{min(255, int(h[i:i+2], 16) + a):02x}' for i in (1, 3, 5))


class Interfaz:
    def __init__(self, root):
        self.root = root
        self.calc = Calculadora()
        self._build()
        self._bind_keys()

    def _build(self):
        self.root.title("Calculadora Pre-Cálculo")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        self.display = tk.Entry(self.root, width=15, font=('Segoe UI', 26, 'bold'),
                                justify='right', bg=DISP, fg=TXT, bd=0,
                                state='readonly', readonlybackground=DISP)
        self.display.grid(row=0, column=0, columnspan=4, padx=12,
                          pady=(18, 22), ipady=14, sticky='ew')
        self._update('0')

        for i in range(4):
            self.root.columnconfigure(i, weight=1)
        for i in range(1, 7):
            self.root.rowconfigure(i, weight=1)

        layout = [
            ('sin', 1, 0, FN), ('cos', 1, 1, FN), ('log', 1, 2, FN), ('π', 1, 3, FN),
            ('7', 2, 0, NUM), ('8', 2, 1, NUM), ('9', 2, 2, NUM), ('÷', 2, 3, OP),
            ('4', 3, 0, NUM), ('5', 3, 1, NUM), ('6', 3, 2, NUM), ('×', 3, 3, OP),
            ('1', 4, 0, NUM), ('2', 4, 1, NUM), ('3', 4, 2, NUM), ('−', 4, 3, OP),
            ('C', 5, 0, FN), ('0', 5, 1, NUM), ('.', 5, 2, NUM), ('+', 5, 3, OP),
            ('=', 6, 0, EQ, 4),
        ]
        for item in layout:
            self._button(*item)

    def _button(self, text, row, col, color, span=1):
        b = tk.Button(self.root, text=text, font=('Segoe UI', 15, 'bold'),
                      bg=color, fg=TXT, bd=0, activebackground=lighter(color, 15),
                      activeforeground=TXT, relief='flat', cursor='hand2',
                      takefocus=0,
                      command=lambda x=text: self.press(x))
        b.grid(row=row, column=col, columnspan=span, padx=5, pady=5,
               sticky='nsew', ipady=10)
        b.bind('<Enter>', lambda ev: b.config(bg=lighter(color)))
        b.bind('<Leave>', lambda ev: b.config(bg=color))

    def press(self, key):
        """Traduce símbolos bonitos y delega al motor."""
        key = {'÷': '/', '×': '*', '−': '-'}.get(key, key)
        self._update(self.calc.input(key))

    def _update(self, text):
        self.display.config(state='normal')
        self.display.delete(0, tk.END)
        self.display.insert(0, text)
        self.display.config(state='readonly')

    def _bind_keys(self):
        self.root.bind('<Key>', self._on_key)

    def _on_key(self, event):
        c, k = event.char, event.keysym

        if c in '0123456789.+-*/=':
            self.press(c)
        elif c.lower() in SHORTCUTS:
            self.press(SHORTCUTS[c.lower()])
        elif c.lower() == 'c':
            self.press('C')
        elif k in ('Return', 'KP_Enter'):
            self.press('=')
        elif k in ('Escape', 'Delete'):
            self.press('C')
        elif k == 'KP_Add':      self.press('+')
        elif k == 'KP_Subtract': self.press('-')
        elif k == 'KP_Multiply': self.press('*')
        elif k == 'KP_Divide':   self.press('/')


if __name__ == '__main__':
    root = tk.Tk()
    Interfaz(root)
    root.mainloop()