from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk
from tkinter import *
import png
from PIL import ImageTk, Image

WIDTH = 300
HEIGHT = 300
image = [[255, 255, 255] * WIDTH for x in range(HEIGHT)]
draw_window_open = False
prev_x = 0
prev_y = 0
img = 0 # garbage value
top = 0 # garbage value

def mouse_click(event, draw_window):
	print("Mouse clicked at", event.x, event.y)
	global prev_x
	global prev_y
	x = event.x
	y = event.y
	change_pixels_in_radius(5, x, y)
	prev_x = x
	prev_y = y
	render(draw_window)

def mouse_move(event, draw_window):
	print("Mouse move")
	global prev_x
	global prev_y
	x = event.x
	y = event.y
	draw_line(draw_window, x, y)
	prev_x = x
	prev_y = y
	render(draw_window)

def create_drawing():
	global draw_window_open
	global img
	global top
	global img_on_canvas
	global canvas
	print("create drawing") # Opens new gui with blank drawing template
	if (not draw_window_open):
		draw_window_open = True
		draw_window = tk.Toplevel(top)
		canvas = Canvas(draw_window, width=WIDTH, height=HEIGHT, bg='black')
		img_on_canvas = canvas.create_image(0, 0, image=img, anchor=NW)
		canvas.pack()
#		draw_window.update()
		canvas.update()
		send_drawing_button = tk.Button(draw_window, text="Send", command=lambda: send_image_info(draw_window))
		draw_window.bind("<Button-1>", lambda event, arg=draw_window: mouse_click(event, arg))
		draw_window.bind("<B1-Motion>", lambda event, arg=draw_window: mouse_move(event, arg))
		send_drawing_button.pack()
		draw_window.protocol("WM_DELETE_WINDOW", lambda: close_drawing(draw_window))

def close_drawing(draw_window):
	global draw_window_open
	draw_window_open = False
	draw_window.destroy()

def send_image_info(draw_window):
	close_drawing(draw_window)
	draw_png()
	print(image)

def send_message():
	global image
	image = [[255, 255, 255] * WIDTH for x in range(HEIGHT)]
	draw_png()

def get_magnitude(delt_x, delt_y):
	return (delt_x**2 + delt_y**2)**.5

def draw_line(draw_window, x, y):
	global prev_x
	global prev_y

	diff_x = x - prev_x
	diff_y = y - prev_y
	magnitude = get_magnitude(diff_x, diff_y)
	x_incr = diff_x / magnitude
	y_incr = diff_y / magnitude

	while get_magnitude(x - prev_x, y - prev_y) > 1:
		prev_x += x_incr
		prev_y += y_incr
		change_pixels_in_radius(5, int(prev_x), int(prev_y))

def change_pixels_in_radius(brush_size, x, y):
	for i in range(-1 * brush_size + 1, brush_size):
		for j in range(-1 * brush_size + 1, brush_size):
			global image
			if (0 <= y + i and y + i < WIDTH and 0 <= x + j and x + j < HEIGHT):
				for k in range(3):
					image[y+i][(x+j) * 3 + k] = 0

def render(draw_window):
	draw_png()
	canvas.itemconfig(img_on_canvas, image=img)

def draw_png():
	global img
	f = open('temp.png', 'wb')
	w = png.Writer(WIDTH, HEIGHT)
	w.write(f, image)
	f.close()
	img = ImageTk.PhotoImage(Image.open('temp.png'))

def main():
	print("in main methods")
	global top
	global img
	top = tk.Tk()
	top.title("PictoRoom")

	messages_frame = tk.Frame(top)
	scrollbar = tk.Scrollbar(messages_frame)
	msg_list = tk.Listbox(messages_frame, height=15, width=50,
						yscrollcommand=scrollbar.set)
	scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
	msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
	msg_list.pack()

	messages_frame.pack()

	new_drawing_button = tk.Button(top, text="New Drawing", command=create_drawing)
	new_drawing_button.pack()
	send_button = tk.Button(top, text="Send", command=send_message)
	send_button.pack()
	img = ImageTk.PhotoImage(Image.open('temp.png'))
	tk.mainloop()
	draw_png()
img_on_canvas = None
if __name__ == "__main__":
    main()
