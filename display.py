import time
from tkinter import *
from PIL import Image
from PIL import ImageTk
import picture_amalgamation

class gui:
    def __init__(self):
        self.window = Tk()
        self.window.title("Picture Amalgamation")
        self.img = Image.open("images/hd.jpg")
        self.window.configure(bg='black')

        self.w, self.h = self.img.size
        self.img = self.img.resize((self.w//4, self.h//4))

        self.window.geometry(str(self.w) + "x" + str(self.h))
        self.render = ImageTk.PhotoImage(self.img)
        self.render_arr = []
        self.arr_files = []

        self.labels = []
        self.last_label = None
        self.current_image = None
        self.last_pop = None

    def callback(self, event):
        last = self.last_label
        label = event.widget
        label.config(bg='red')
        if last and last != label:
            last.config(bg='black')

        self.current_image = label.cget("text")
        self.last_label = label
        self.popup(label)


    def popup(self, widget):
        if self.last_pop:
            self.last_pop.destroy()
        pop = Toplevel()
        self.last_pop = pop
        pop.title("Selected Image")
        row = widget.grid_info()['row']  # Row of the button
        column = widget.grid_info()['column']
        file = self.arr_files[row][column]

        image = Image.open(file).resize((600, 400))
        tk_image = ImageTk.PhotoImage(image)
        w, h = image.size
        pop.geometry(str(w) + "x" + str(h))

        label = Label(pop, image=tk_image)
        label.grid(row=0, column=0)
        pop.protocol("WM_DELETE_WINDOW", pop.quit())
        pop.bind('<Escape>', lambda e: pop.quit())
        pop.mainloop()


    def draw(self, base_path, dir_path, box_size=100):
        img, arr, self.arr_files = picture_amalgamation.amalgamate(base_path, dir_path, box_size)
        self.w, self.h = img.size
        self.w += 30
        self.h += 10
        self.window.geometry(str(self.w) + "x" + str(self.h))
        self.render_arr = [[0 for i in range(len(arr[0]))] for j in range(len(arr))]
        for r in range(len(arr)):
            for c in range(len(arr[0])):
                try:
                    self.render_arr[r][c] = ImageTk.PhotoImage(arr[r][c])
                except:
                    self.render_arr[r][c] = ImageTk.PhotoImage(arr[0][0])


        for row in range(len(arr)):
            for col in range(len(arr[0])):
                label = Label(self.window, image=self.render_arr[row][col], bg='black', text="hi", borderwidth=0)
                label.grid(row=row, column=col, pady=0, padx=0)
                label.bind("<Button-1>", self.callback)

    def run(self):
        self.window.mainloop()
