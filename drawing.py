#!/usr/bin/env python3
import base64
import io
import os
from socket import AF_INET, socket, SOCK_STREAM
import sys
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
brush_size = 5
is_drawing_in_queue = False

def mouse_click(event, draw_window, erase):
	global prev_x
	global prev_y
	x = event.x
	y = event.y
	change_pixels_in_radius(x, y, erase)
	prev_x = x
	prev_y = y
	render(draw_window)

def mouse_move(event, draw_window, erase):
	global prev_x
	global prev_y
	x = event.x
	y = event.y
	draw_line(draw_window, x, y, erase)
	prev_x = x
	prev_y = y
	render(draw_window)

def exit_click(event, draw_window):
	send_image_info(draw_window)
	close_drawing(draw_window)

def scroll_brush_size(event):
	global brush_size
	if event.num == 5 or event.delta == -120:
		brush_size -= 1
	if event.num == 4 or event.delta == 120:
		brush_size += 1

	if brush_size < 1:
		brush_size = 1
	elif brush_size > 15:
		brush_size = 15
	int(brush_size)

def create_drawing():
	global draw_window_open
	global img
	global top
	global img_on_canvas
	global canvas
	global is_drawing_in_queue
	is_drawing_in_queue = True
	if (not draw_window_open):
		draw_window_open = True
		draw_window = tk.Toplevel(top)
		canvas = Canvas(draw_window, width=WIDTH, height=HEIGHT, bg='black')
		img_on_canvas = canvas.create_image(0, 0, image=img, anchor=NW)
		canvas.pack()
		canvas.update()
		# send_drawing_button = tk.Button(draw_window, text="Send", command=lambda: send_image_info(draw_window))
		draw_window.bind("<Button-1>", lambda event, arg=draw_window: mouse_click(event, arg, False))
		draw_window.bind("<B1-Motion>", lambda event, arg=draw_window: mouse_move(event, arg, False))
		draw_window.bind("<Button-2>", lambda event, arg=draw_window: exit_click(event, arg))
		draw_window.bind("<Button-3>", lambda event, arg=draw_window: mouse_click(event, arg, True))
		draw_window.bind("<B3-Motion>", lambda event, arg=draw_window: mouse_move(event, arg, True))
		draw_window.bind("<Button-4>", scroll_brush_size)
		draw_window.bind("<Button-5>", scroll_brush_size)
		draw_window.bind("<MouseWheel>", scroll_brush_size)
		# send_drawing_button.pack()
		draw_window.protocol("WM_DELETE_WINDOW", lambda: close_drawing(draw_window))

def close_drawing(draw_window):
	global draw_window_open
	draw_window_open = False
	draw_window.destroy()

def send_image_info(draw_window):
	close_drawing(draw_window)
	draw_png()

def send_message():
	global image
	global is_drawing_in_queue
	if (is_drawing_in_queue):
		if (s):
			foo = open('temp.png', 'rb').read()
			s.send(base64.b64encode(foo))
		image = [[255, 255, 255] * WIDTH for x in range(HEIGHT)]
		draw_png()
		is_drawing_in_queue = False

def get_magnitude(delt_x, delt_y):
	return (delt_x**2 + delt_y**2)**.5

def draw_line(draw_window, x, y, draw):
	global prev_x
	global prev_y

	diff_x = x - prev_x
	diff_y = y - prev_y
	magnitude = get_magnitude(diff_x, diff_y)
	if magnitude == 0:
		return
	x_incr = diff_x / magnitude
	y_incr = diff_y / magnitude

	while get_magnitude(x - prev_x, y - prev_y) > 1:
		prev_x += x_incr
		prev_y += y_incr
		change_pixels_in_radius(int(prev_x), int(prev_y), draw)

def change_pixels_in_radius(x, y, draw):
	global brush_size
	for i in range(-1 * brush_size + 1, brush_size):
		for j in range(-1 * brush_size + 1, brush_size):
			global image
			if (0 <= y + i and y + i < WIDTH and 0 <= x + j and x + j < HEIGHT):
				for k in range(3):
					image[y+i][(x+j) * 3 + k] = int(draw) * 255

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

BUF_SIZE = 16384

foo = []

num_images = 0

def handle_incoming(s, frame, canvas):
	global foo, num_images
	while (True):
		try:
			data = s.recv(BUF_SIZE)
			if (not data):
				print('disconnected')
				os._exit(1)
			foo.append(ImageTk.PhotoImage(Image.open(io.BytesIO(base64.b64decode(data)))))
			l = tk.Label(frame, image=foo[-1])
			l.pack()
			num_images += 1
			canvas.config(scrollregion=(0, 0, 300, 300 + frame.winfo_reqheight()))
			canvas.yview_moveto(1)
		except Exception as e:
			sys.stderr.write(traceback.format_exc())
			os._exit(1)

def on_configure(event, canvas):
	canvas.configure(scrollregion=canvas.bbox('all'))

def main(s_s=None):
	global s
	global top
	global img
	s = s_s
	top = tk.Tk()
	top.title("PictoRoom")

	superframe = tk.Frame(top)

	canvas = tk.Canvas(superframe, height=301, width=300)
	canvas.pack(side=tk.LEFT)

	scrollbar = tk.Scrollbar(superframe, command=canvas.yview)
	scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

	canvas.configure(yscrollcommand=scrollbar.set)

	canvas.bind('<Configure>', lambda event: on_configure(event, canvas))

	frame = tk.Frame(canvas)
	canvas.create_window((0,0), window=frame, anchor='nw')

	superframe.pack()

	new_drawing_button = tk.Button(top, text="New Drawing", command=create_drawing)
	new_drawing_button.pack()
	send_button = tk.Button(top, text="Send", command=send_message)
	send_button.pack()

	if (s):
		Thread(target=lambda: handle_incoming(s, frame, canvas), daemon=True).start()

	img = None
	draw_png()

	top.mainloop()

img_on_canvas = None

s = None

if __name__ == "__main__":
	main()
