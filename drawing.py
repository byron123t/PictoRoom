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

def mouse_click(event):
	print("Mouse clicked at", event.x, event.y)
	global prev_x
	global prev_y
	x = event.x
	y = event.y
	change_pixels_in_radius(5, x, y)
	prev_x = x
	prev_y = y

def mouse_move(event, draw_window):
	print("Mouse move")
	global prev_x
	global prev_y
	x = event.x
	y = event.y
	draw_line(draw_window, prev_x, prev_y, x, y)
	prev_x = x
	prev_y = y

def create_drawing():
	global draw_window_open
	print("create drawing") # Opens new gui with blank drawing template
	if (not draw_window_open):
		draw_window_open = True
		draw_window = tk.Toplevel(top)
		canvas = Canvas(draw_window, width=WIDTH, height=HEIGHT, bg='black')
		canvas.create_image(0, 0, image=img, anchor=NW)
		canvas.pack()
#		draw_window.update()
		canvas.update()
		send_drawing_button = tk.Button(draw_window, text="Send", command=lambda: send_image_info(draw_window))
		draw_window.bind("<Button-1>", mouse_click)
		draw_window.bind("<B1-Motion>", lambda event, arg=draw_window: mouse_move(event, arg))
		send_drawing_button.pack()
		draw_window.protocol("WM_DELETE_WINDOW", lambda: close_drawing(draw_window))

def close_drawing(draw_window):
	global draw_window_open
	draw_window_open = False
	draw_window.destroy()

def send_image_info(draw_window):
	close_drawing(draw_window)
	print(image)

def draw_line(draw_window, x, y):
	for i in range(0, x + 1):
		slope = (y - prev_y) / (x - prev_x)
		prev_y += slope
		if(x - prev_x < 0):
			prev_x -= 1
		else:
			prev_x += 1

def change_pixels_in_radius(brush_size, x, y):
	for i in range(brush_size):
		for j in range(brush_size):
			global image
			if (brush_size - i < brush_size - 1 and brush_size - j < brush_size - 1):
				if (0 <= x + i and x + i < WIDTH and 0 <= y + j and y + j < HEIGHT):
					image[x+i][y+j] = [0,0,0]
				if (0 <= x - i and x + i < WIDTH and 0 <= y - j and y - j < HEIGHT):
					image[x-i][y-j] = [0,0,0]
				

def render(draw_window, image):
	f = open('temp.png', 'wb')
	w = png.Writer(WIDTH, HEIGHT)
	w.write(f, image)
	f.close()
	print("render image")
	
	
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

# entry_field = tk.Entry(top, textvariable=my_msg)
# entry_field.bind("<Return>", send)
#entry_field.pack()
new_drawing_button = tk.Button(top, text="New Drawing", command=create_drawing)
new_drawing_button.pack()
send_button = tk.Button(top, text="Send") # , command=send)
send_button.pack()

f = open('temp.png', 'wb')
w = png.Writer(WIDTH, HEIGHT)
w.write(f, image)
f.close()

img = ImageTk.PhotoImage(Image.open('temp.png'))
#img = ImageTk.PhotoImage(Image.open('test.png'))
#canvas = Canvas(top, width=WIDTH, height=HEIGHT, bg='black')
#canvas.create_image(0, 0, image=img, anchor=NW)
#canvas.pack()

tk.mainloop()
