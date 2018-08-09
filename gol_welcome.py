from tkinter import Frame, Label, Button, Tk, TOP, LEFT, BOTTOM, X
from gol_gui import GameScreen


class WelcomeScreen:
    def __init__(self, window):
        self.window = window

        top_frame = Frame(self.window, height=100)
        top_frame.pack(fill=X, expand=1)

        bottom_frame = Frame(self.window, height=50)
        bottom_frame.pack(side=BOTTOM, fill=X, expand=1)

        title = Label(top_frame, text="Welcome to the Game of Life!",
                      font=("Helvetica", 16), fg="blue", bd=5, relief="groove")
        title.pack(side=TOP, fill=X, expand=1)

        xl_btn = Button(top_frame, height=1, width=20, text="Open game in Excel", font=("Helvetica", 10),
                        command=lambda: self.load('xl'))
        xl_btn.pack(side=LEFT, expand=1, pady=15)

        tk_btn = Button(top_frame, height=1, width=20, text="Open game in window", font=("Helvetica", 10),
                        command=lambda: self.load('tk'))
        tk_btn.pack(side=LEFT, expand=1, pady=15)

        quit_btn = Button(bottom_frame, height=1, width=20, text='Close application', font=('Helvetica', 10),
                          command=self.window.destroy)
        quit_btn.pack(expand=1, pady=15)

    def load(self, view_type):
        self.window.destroy()
        window = Tk()
        conway_app = GameScreen(window, view_type)
        conway_app.window.lift()
        conway_app.window.attributes('-topmost', True)
        conway_app.window.mainloop()


if __name__ == '__main__':
    root = Tk()
    app = WelcomeScreen(root)
    app.window.mainloop()
