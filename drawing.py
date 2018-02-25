#!/usr/bin/env python3
import base64
import io
import os
from socket import AF_INET, socket, SOCK_STREAM
import sys
from threading import Thread
import traceback

import tkinter as tk
from tkinter import *
import png
from PIL import ImageTk, Image

WIDTH = 500
HEIGHT = 300
image = [[255, 255, 255] * WIDTH for x in range(HEIGHT)]
prev_x = 0
prev_y = 0
img = 0 # garbage value
top = 0 # garbage value
brush_size = 5
is_drawing_in_queue = False

def mouse_click(event, top, erase):
	if event.widget != canvas:
		return
	global is_drawing_in_queue
	is_drawing_in_queue = True
	global prev_x
	global prev_y
	x = event.x
	y = event.y
	change_pixels_in_radius(x, y, erase)
	prev_x = x
	prev_y = y
	render(top)

def mouse_move(event, top, erase):
	if event.widget != canvas:
		return
	global prev_x
	global prev_y
	x = event.x
	y = event.y
	draw_line(top, x, y, erase)
	prev_x = x
	prev_y = y
	render(top)

def exit_click(event, top):
	send_image_info(top)
	close_drawing(top)

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

def create_drawing():
	global top_open
	global img
	global top
	global img_on_canvas
	global canvas
	canvas = Canvas(top, width=WIDTH, height=HEIGHT, bg='black')
	img_on_canvas = canvas.create_image(0, 0, image=img, anchor=NW)
	canvas.pack()
	canvas.update()
	top.bind("<Button-1>", lambda event, arg=top: mouse_click(event, arg, False))
	top.bind("<B1-Motion>", lambda event, arg=top: mouse_move(event, arg, False))
	top.bind("<Button-2>", lambda event, arg=top: exit_click(event, arg))
	top.bind("<Button-3>", lambda event, arg=top: mouse_click(event, arg, True))
	top.bind("<B3-Motion>", lambda event, arg=top: mouse_move(event, arg, True))
	top.bind("<Button-4>", scroll_brush_size)
	top.bind("<Button-5>", scroll_brush_size)
	top.bind("<MouseWheel>", scroll_brush_size)

def send_message():
	global image
	global is_drawing_in_queue
	if (is_drawing_in_queue):
		if (s):
			foo = open('temp.png', 'rb').read()
			s.send(base64.b64encode(foo) + b'\xde\xad\xbe\xef')
		image = [[255, 255, 255] * WIDTH for x in range(HEIGHT)]
		draw_png()
		is_drawing_in_queue = False
		render(top)

def get_magnitude(delt_x, delt_y):
	return (delt_x ** 2 + delt_y ** 2) ** .5

def draw_line(top, x, y, draw):
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
			if (0 <= y + i and y + i < HEIGHT and 0 <= x + j and x + j < WIDTH):
				for k in range(3):
					image[y+i][(x+j) * 3 + k] = int(draw) * 255

def render(top):
	draw_png()
	canvas.itemconfig(img_on_canvas, image=img)

def draw_png():
	global img
	f = open('temp.png', 'wb')
	w = png.Writer(WIDTH, HEIGHT)
	w.write(f, image)
	f.close()
	img = ImageTk.PhotoImage(Image.open('temp.png'))

BUF_SIZE = 1048576

foo = []

num_images = 0

def handle_incoming(s, frame, canvas):
	global foo, num_images
	full_data = b''
	while (True):
		try:
			data = s.recv(BUF_SIZE)
			if (not data):
				print('disconnected')
				os._exit(1)
			full_data += data
			if (data[-4:] != b'\xde\xad\xbe\xef'):
				continue
			foo.append(ImageTk.PhotoImage(Image.open(io.BytesIO(base64.b64decode(full_data[:-4])))))
			full_data = b''
			l = tk.Label(frame, image=foo[-1])
			l.pack()
			num_images += 1
			l.update_idletasks()
			canvas.config(scrollregion=(0, 0, WIDTH, frame.winfo_reqheight()))
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

	canvas = tk.Canvas(superframe, height=HEIGHT + 1, width=WIDTH)
	canvas.pack(side=tk.LEFT)

	scrollbar = tk.Scrollbar(superframe, command=canvas.yview)
	scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

	canvas.configure(yscrollcommand=scrollbar.set)

	canvas.bind('<Configure>', lambda event: on_configure(event, canvas))

	frame = tk.Frame(canvas)
	canvas.create_window((0,0), window=frame, anchor='nw')

	superframe.pack()

	if (s):
		Thread(target=lambda: handle_incoming(s, frame, canvas), daemon=True).start()

	img = None
	draw_png()
	create_drawing()
	send_button = tk.Button(top, text="Send", command=send_message)
	send_button.pack()

	top.mainloop()

img_on_canvas = None

s = None

if __name__ == "__main__":
	main()
