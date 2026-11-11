import tkinter as tk
from calculadora import Calculadora

BG, DISP, NUM, OP, FN, EQ, TXT, SUB = "#1e1e2e", "#2a2a3e", "#3a3a52", "#ff9500", "#4a4a6a", "#2ecc71", "#ffffff", "#8888aa"
SHORTCUTS = {'s': 'sin', 'o': 'cos', 'l': 'log', 'p': 'π'}


def lighter(h, a=35):
    return '#' + ''.join(f'{min(255, int(h[i:i+2], 16) + a):02x}' for i in (1, 3, 5))


class Interfaz:
    def __init__(self, root):
        self.root = root
        self.calc = Calculadora()
        self._build()
        self.root.bind('<Key>', self._on_key)

    def _build(self):
        self.root.title("Calculadora Pre-Cálculo")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.expr_lbl = tk.Label(self.root, text='', font=('Segoe UI', 12),
                                 bg=DISP, fg=SUB, anchor='e', padx=10)
        self.expr_lbl.grid(row=0, column=0, columnspan=4, padx=12,
                           pady=(18, 0), sticky='ew')

        # Display principal
        self.display = tk.Entry(self.root, width=15, font=('Segoe UI', 26, 'bold'),
                                justify='right', bg=DISP, fg=TXT, bd=0,
                                state='readonly', readonlybackground=DISP)
        self.display.grid(row=1, column=0, columnspan=4, padx=12,
                          pady=(0, 22), ipady=12, sticky='ew')
        self._update('0', '')

        for i in range(4):
            self.root.columnconfigure(i, weight=1)
        for i in range(2, 8):
            self.root.rowconfigure(i, weight=1)

        layout = [
            ('sin', 2, 0, FN), ('cos', 2, 1, FN), ('log', 2, 2, FN), ('π', 2, 3, FN),
            ('7',   3, 0, NUM), ('8', 3, 1, NUM), ('9', 3, 2, NUM), ('÷', 3, 3, OP),
            ('4',   4, 0, NUM), ('5', 4, 1, NUM), ('6', 4, 2, NUM), ('×', 4, 3, OP),
            ('1',   5, 0, NUM), ('2', 5, 1, NUM), ('3', 5, 2, NUM), ('−', 5, 3, OP),
            ('C',   6, 0, FN),  ('0', 6, 1, NUM), ('.', 6, 2, NUM), ('+', 6, 3, OP),
            ('=',   7, 0, EQ, 4),
        ]
        for item in layout:
            self._button(*item)

    def _button(self, text, row, col, color, span=1):
        b = tk.Button(self.root, text=text, font=('Segoe UI', 15, 'bold'),
                      bg=color, fg=TXT, bd=0, activebackground=lighter(color, 15),
                      activeforeground=TXT, relief='flat', cursor='hand2',
                      takefocus=0, command=lambda x=text: self.press(x))
        b.grid(row=row, column=col, columnspan=span, padx=5, pady=5,
               sticky='nsew', ipady=10)
        b.bind('<Enter>', lambda ev: b.config(bg=lighter(color)))
        b.bind('<Leave>', lambda ev: b.config(bg=color))

    def press(self, key):
        key = {'÷': '/', '×': '*', '−': '-'}.get(key, key)
        result = self.calc.input(key)
        self._update(result, self.calc.expr)

    def _update(self, text, expr=''):
        self.expr_lbl.config(text=expr)
        self.display.config(state='normal')
        self.display.delete(0, tk.END)
        self.display.insert(0, text)
        self.display.config(state='readonly')

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