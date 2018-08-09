import csv
import numpy as np
from json import load, dump
from os import listdir, path
from tkinter import Toplevel, Label, Button, filedialog, messagebox, Entry, Frame


# performs a step of the simulation / applies Conway's rules once
def step_forward(game_screen):
    game_screen.state_history.next_state()
    game_screen.view.draw_state(game_screen)


# draws the latest state saved in state_history
def step_backward(game_screen):
    game_screen.state_history.previous_state()
    game_screen.view.draw_state(game_screen)


# opens a popup window to enter the preferred grid size
def set_size(game_screen):
    popup = Toplevel()
    popup.title("Enter size")
    popup.attributes('-topmost', True)
    frame = Frame(popup)
    frame.grid(row=0, column=0)
    msg = Label(frame, text="New grid size (number between 5 and 25):", font=("Helvetica", 10))
    msg.grid(row=0, column=0)

    def validate(value, action_type):
        if action_type == '1':
            if not value.isdigit():
                return False
        return True

    entry = Entry(frame, validate='key')
    entry['validatecommand'] = (entry.register(validate), '%P', '%d')
    entry.grid(row=0, column=1)

    def submit():
        size = int(entry.get())
        if size in range(5, 26):
            game_screen.resize((size, size))
            popup.destroy()
        else:
            entry.delete(0, 10)
            messagebox.showerror('Error', 'Number not in range.')

    submit_btn = Button(frame, height=1, width=5, text='Submit', font=('Helvetica', 10), command=submit)
    submit_btn.grid(row=0, column=2)


# turns on manual configuration mode: draws an empty grid & starts accepting mouse input
def configure(game_screen):
    game_screen.view.set_state(game_screen)


# draws a random configuration
def randomize(game_screen):
    game_screen.state_history.random_state()
    game_screen.view.draw_state(game_screen)


# starts an automatic simulation
def sim_start(game_screen):

    # performs a simulation step & calls itself after 1 second
    def simulate(screen):
        if screen.in_auto_mode():
            step_forward(screen)
            screen.window.after(1000, lambda: simulate(screen))

    game_screen.set_auto_mode()
    simulate(game_screen)


# stops an active automatic simulation
def sim_stop(game_screen):
    game_screen.set_manual_mode()


# opens a save-file window, extension defaults to csv
def save_state(game_screen):
    state_number = len([name for name in listdir('./Saved_states')]) + 1
    default_name = 'State_' + str(state_number)
    file_name = filedialog.asksaveasfilename(initialdir='./Saved_states', initialfile=default_name,
                                             filetypes=(('csv files', '*.csv'), ('json files', '*.json')),
                                             title='Save file as...', defaultextension='.csv')
    try:
        with open(file_name, "w+", newline='') as f:
            if path.splitext(file_name)[-1] == ".csv":
                writer = csv.writer(f)
                writer.writerows(game_screen.state_history.current_state())
            elif path.splitext(file_name)[-1] == ".json":
                dump(game_screen.state_history.current_state().tolist(), f)
    except FileNotFoundError:
        messagebox.showerror('Error', 'File not saved.')


# opens a load-file window
def load_state(game_screen):
    file_name = filedialog.askopenfilename(initialdir='./Saved_states', title='Select file to load',
                                           filetypes=(('csv files', '*.csv'), ('json files', '*.json')))
    try:
        with open(file_name, "r", newline='') as f:
            if path.splitext(file_name)[-1] == ".csv":
                reader = csv.reader(f)
                state_array = np.array(list(reader)).astype("int")
            elif path.splitext(file_name)[-1] == ".json":
                state_array = np.array(load(f))
            else:
                state_array = np.zeros((10, 10), dtype=np.int16)
            game_screen.state_history.clear_history()
            game_screen.state_history.add_state(state_array)
            game_screen.view.draw_state(game_screen)
    except FileNotFoundError:
        messagebox.showerror('Error', 'No file selected.')


# saves and closes excel file if on excel and closes application
def quit_simulation(game_screen):
    game_screen.view.quit()
    game_screen.window.destroy()
