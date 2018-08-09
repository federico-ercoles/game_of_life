from tkinter import Frame, Button
from gol_controls import (
    step_forward, step_backward, sim_start, sim_stop, configure, set_size, randomize, load_state, save_state,
    quit_simulation)


class ControlPanel (Frame):
    def __init__(self, game_screen):
        Frame.__init__(self, game_screen.window)
        self.buttons = []

        self.step_btn = Button(self, height=1, width=20, text="Next step",
                               font=("Helvetica", 10), command=lambda: step_forward(game_screen))
        self.step_btn.grid(row=0, column=0, padx=5, pady=2)
        self.buttons.append(self.step_btn)

        self.back_btn = Button(self, height=1, width=20, text="Previous step",
                               font=("Helvetica", 10), command=lambda: step_backward(game_screen))
        self.back_btn.grid(row=0, column=1, padx=5, pady=2)
        self.buttons.append(self.back_btn)

        self.sim_start_btn = Button(self, height=1, width=20, text="Start simulation",
                                    font=("Helvetica", 10), command=lambda: sim_start(game_screen))
        self.sim_start_btn.grid(row=1, column=0, padx=5, pady=2)
        self.buttons.append(self.sim_start_btn)

        self.sim_stop_btn = Button(self, height=1, width=20, text="Stop simulation",
                                   font=("Helvetica", 10), command=lambda: sim_stop(game_screen))
        self.sim_stop_btn.grid(row=1, column=1, padx=5, pady=2)
        self.buttons.append(self.sim_stop_btn)

        self.set_btn = Button(self, height=1, width=20, text="Set configuration",
                              font=("Helvetica", 10), command=lambda: configure(game_screen))
        self.set_btn.grid(row=2, column=0, padx=5, pady=2)
        self.buttons.append(self.set_btn)

        self.resize_btn = Button(self, height=1, width=20, text="Set grid size",
                                 font=("Helvetica", 10), command=lambda: set_size(game_screen))
        self.resize_btn.grid(row=2, column=1, padx=5, pady=2)
        self.buttons.append(self.resize_btn)

        self.save_state_btn = Button(self, height=1, width=20, text="Save current state",
                                     font=("Helvetica", 10), command=lambda: save_state(game_screen))
        self.save_state_btn.grid(row=3, column=0, padx=5, pady=2)
        self.buttons.append(self.save_state_btn)

        self.load_state_btn = Button(self, height=1, width=20, text="Load a saved state",
                                     font=("Helvetica", 10), command=lambda: load_state(game_screen))
        self.load_state_btn.grid(row=3, column=1, padx=5, pady=2)
        self.buttons.append(self.load_state_btn)

        self.random_btn = Button(self, height=1, width=20, text="Randomize configuration",
                                 font=("Helvetica", 10), command=lambda: randomize(game_screen))
        self.random_btn.grid(row=4, column=0, padx=5, pady=2)
        self.buttons.append(self.random_btn)

        self.empty_btn = Button(self, height=1, width=20, text='Empty configuration',
                                font=('Helvetica', 10), command=game_screen.blank)
        self.empty_btn.grid(row=4, column=1, padx=5, pady=2)
        self.buttons.append(self.empty_btn)

        self.switch_btn = Button(self, height=1, width=20, text='Show output in Excel' * (game_screen.view.type() == 'tk')
                                 + 'Show output in window' * (game_screen.view.type() == 'xl'),
                                 font=('Helvetica', 10), command=game_screen.switch_view)
        self.switch_btn.grid(row=5, column=0, padx=5, pady=2)
        self.buttons.append(self.switch_btn)

        self.quit_btn = Button(self, height=1, width=20, text="Quit simulation",
                               font=("Helvetica", 10), command=lambda: quit_simulation(game_screen))
        self.quit_btn.grid(row=5, column=1, padx=5, pady=2)
        self.buttons.append(self.quit_btn)
