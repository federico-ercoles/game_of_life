import numpy as np
import xlwings as xw
from tkinter import messagebox, Canvas


class ExcelView:
    def __init__(self):
        self._view_type = 'xl'
        self.book = xw.Book('conway_graphics.xlsm')
        xw.apps.active.activate(steal_focus=True)

    def type(self):
        return self._view_type

    def draw_state(self, game_screen):
        wb = xw.Book(self.book.fullname)
        ws = wb.sheets.active
        shape = np.shape(game_screen.state_history.current_state())
        initial_cell = (3, 2)
        xw.apps.active.screen_updating = False
        for border in range(7, 13):
            ws.range(initial_cell, tuple(map(sum, zip(initial_cell, (19, 19))))).api.Borders(
                border).LineStyle = -4142
        ws.range(initial_cell, tuple(map(sum, zip(initial_cell, (19, 19))))).value = np.zeros((20, 20), dtype=np.int16)
        for border in range(7, 13):
            ws.range(initial_cell,
                     tuple(map(sum, zip(initial_cell, shape, (-1, -1))))).api.Borders(border).LineStyle = 1
            ws.range(initial_cell,
                     tuple(map(sum, zip(initial_cell, shape, (-1, -1))))).api.Borders(border).Weight = 3
        ws.range(initial_cell, tuple(map(sum, zip(initial_cell, shape, (-1, -1))))).value = \
            game_screen.state_history.current_state()
        xw.apps.active.screen_updating = True

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def set_state(self, game_screen):
        messagebox.showerror('Error', 'Can\'t configure board in Excel mode.')

    def quit(self):
        self.book.save()
        self.book.close()
        xw.apps.active.quit()


class TkView:
    def __init__(self, tk_frame):
        self._view_type = 'tk'
        self.canvas = Canvas(tk_frame, width=400, height=400)
        self.canvas.pack(padx=10, pady=10, expand=1)

    def type(self):
        return self._view_type

    def draw_state(self, game_screen):

        def draw_square(canvas, position, shape, color):
            height = float(canvas.cget("height"))
            width = float(canvas.cget("width"))
            sqr_height = (height - 2) / shape[1]
            sqr_width = (width - 2) / shape[0]
            canvas.create_rectangle((position[1] - 1) * sqr_width + 2,
                                    (position[0] - 1) * sqr_height + 2,
                                    position[1] * sqr_width + 2,
                                    position[0] * sqr_height + 2,
                                    fill=color)

        current_shape = np.shape(game_screen.state_history.current_state())
        for i in range(current_shape[0]):
            for j in range(current_shape[1]):
                if game_screen.state_history.current_state()[i, j]:
                    draw_square(self.canvas, (i + 1, j + 1), current_shape, "black")
                else:
                    draw_square(self.canvas, (i + 1, j + 1), current_shape, "white")

    def set_state(self, game_screen):

        def set_cell(screen, event):
            # when manually creating a configuration, activates or deactivates a cell based on mouse click

            height = float(screen.view.canvas.cget("height"))
            width = float(screen.view.canvas.cget("width"))
            sqr_height = (height - 2) / screen.state_history.current_shape()[1]
            sqr_width = (width - 2) / screen.state_history.current_shape()[0]
            if screen.in_edit_mode():
                x, y = int((event.y + 1) // sqr_height), int((event.x + 1) // sqr_width)
                screen.state_history.current_state()[x][y] = (screen.state_history.current_state()[x][y] + 1) % 2
                self.draw_state(screen)

        game_screen.switch_between_edit_and_manual_mode()

        if game_screen.in_edit_mode():
            game_screen.blank()

            def set_cell_handler(event, event_screen=game_screen):
                return set_cell(event_screen, event)

            self.canvas.bind("<Button-1>", set_cell_handler)
            game_screen.button_frame.set_btn.config(text="Setting board", font=("Helvetica", 10))
        else:
            self.canvas.unbind("<Button-1>")
            game_screen.button_frame.set_btn.config(text="Set configuration", font=("Helvetica", 10))

    def quit(self):
        pass
