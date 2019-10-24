from tkinter import *
import torch


class View:

    def __init__(self, model, target_image_width=28, target_image_height=28, brush_size=20, title="Digit recognizer"):
        self._model = model

        self._target_image_width = target_image_width
        self._target_image_height = target_image_height

        self._brush_size = brush_size
        self._brush_color = "black"

        self._canvas_width = target_image_width * brush_size
        self._canvas_height = target_image_height * brush_size

        self._root = Tk()
        self._root.title(title)

        self._output_var = StringVar()
        self._out = Label(self._root, textvariable=self._output_var)

        self._correct_answer_var = StringVar()
        self._correct_answer_entry = Entry(textvariable=self._correct_answer_var)

        self._learn_btn = Button(text="Учить", width=10, command=self._learn)

        self._clear_btn = Button(text="Очистить", width=10, command=self._clear_canvas)
        self._recognize_btn = Button(text="Распознать", width=10, command=self._recognize_image)

        self._canvas = Canvas(self._root, width=self._canvas_width, height=self._canvas_height, bg="white")

        self._canvas.bind("<B1-Motion>", self._draw)

        self._canvas.grid(row=2, column=0, columnspan=7, padx=5, pady=5, sticky=E+W+S+N)
        self._canvas.columnconfigure(6, weight=1)
        self._canvas.rowconfigure(2, weight=1)

        self._clear_btn.grid(row=0, column=2)
        self._recognize_btn.grid(row=1, column=2)

        self._out.grid(row=0, column=4)

        self._correct_answer_entry.grid(row=1, column=4)

        self._learn_btn.grid(row=1, column=5)

        self._image = torch.zeros((28, 28))

        self._root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _on_closing(self):
        self._model.save()
        self._root.destroy()

    def start(self):
        self._root.mainloop()

    def _draw(self, event):
        x1 = event.x - self._brush_size // 2
        x2 = event.x + self._brush_size // 2
        y1 = event.y - self._brush_size // 2
        y2 = event.y + self._brush_size // 2

        self._canvas.create_rectangle(
            x1, y1, x2, y2, outline=self._brush_color,
            fill=self._brush_color, width=0
        )
        if event.x // self._brush_size < 28 and event.y // self._brush_size < 28:
            self._image[
                event.y // self._brush_size, event.x // self._brush_size
            ] = 255

    def _clear_canvas(self):
        self._canvas.create_rectangle(
            0, 0, self._canvas_width+2, self._canvas_height+2,
            outline="white", fill="white", width=0
        )
        self._image = torch.zeros((28, 28))
        self._correct_answer_var.set('')
        self._output_var.set('')

    def _recognize_image(self):
        result = self._model.predict(self._image)
        self._output_var.set(str(result))

    def _learn(self):
        text = self._correct_answer_var.get()
        if text.isdigit() and int(text) >= 0 and int(text) <= 9:
            self._model.learn(int(text))
