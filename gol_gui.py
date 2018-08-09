import numpy as np
from tkinter import Frame, Label, Tk, X, TOP, BOTTOM, DISABLED, NORMAL
from gol_views import ExcelView, TkView
from gol_controlpanel import ControlPanel
from gol_controls import quit_simulation
from gol_state_history import GameStateHistory


class GameScreen:
    def __init__(self, window, view_type, state_array=np.zeros((10, 10), dtype=np.int16)):
        self.window = window

        self.state_history = GameStateHistory(state_array)
        self.mode = ''

        self.top_frame = Frame(self.window)
        self.top_frame.pack(side=TOP, fill=X, expand=1)

        self.set_title(self.top_frame)

        if view_type == 'xl':
            self.view = ExcelView()
        elif view_type == 'tk':
            self.center_frame = Frame(self.window)
            self.center_frame.pack(fill=X, expand=1)
            self.view = TkView(self.center_frame)

        self.view.draw_state(self)

        self.bottom_frame = Frame(self.window, width=450, height=250)
        self.bottom_frame.pack(side=BOTTOM, fill=X, expand=1)
        self.button_frame = ControlPanel(self)
        self.button_frame.place(in_=self.bottom_frame, anchor="c", relx=.5, rely=.5)

        self.set_manual_mode()

    def set_manual_mode(self):
        self.mode = 'manual'
        for button in self.button_frame.buttons:
            button.config(state=NORMAL)

    def set_auto_mode(self):
        self.mode = 'auto'
        for button in filter(lambda b: b != self.button_frame.sim_stop_btn, self.button_frame.buttons):
            button.config(state=DISABLED)

    def set_edit_mode(self):
        self.mode = 'edit'
        for button in filter(lambda b: b != self.button_frame.set_btn, self.button_frame.buttons):
            button.config(state=DISABLED)

    def in_edit_mode(self):
        return self.mode == 'edit'

    def in_auto_mode(self):
        return self.mode == 'auto'

    def in_manual_mode(self):
        return self.mode == 'manual'

    def switch_between_edit_and_manual_mode(self):
        if self.mode == 'edit':
            self.set_manual_mode()
        elif self.mode == 'manual':
            self.set_edit_mode()

    def set_title(self, frame):
        self.window.title('Game of Life')
        title = Label(frame, text="Welcome to the Game of Life!",
                      font=("Helvetica", 16), fg="blue", bd=5, relief="groove")
        title.pack(fill=X, expand=1)

    # switches output between tk interface and excel file and vice-versa while keeping current state and history
    def switch_view(self):

        quit_simulation(self)
        window = Tk()
        new_app = GameScreen(window, 'tk' * (self.view.type() == 'xl') + 'xl' * (self.view.type() == 'tk'),
                             state_array=self.state_history.current_state())
        new_app.window.lift()
        new_app.window.attributes('-topmost', True)
        new_app.state_history = self.state_history
        new_app.window.mainloop()

    # draws an empty grid
    def blank(self):
        self.resize(self.state_history.current_shape())

    def resize(self, size):
        self.state_history.empty_state(size)
        self.view.draw_state(self)


if __name__ == "__main__":
    root = Tk()
    app = GameScreen(root, 'tk')
    app.window.mainloop()
