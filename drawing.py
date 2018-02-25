from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk

WIDTH = 3
HEIGHT = 3
image = [[(255, 255, 255)] * WIDTH for x in range(HEIGHT)]
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

def mouse_move(event):
	print("Mouse move")
	global prev_x
	global prev_y
	x = event.x
	y = event.y
	# draw_line(draw_window, prev_x, prev_y, x, y)
	prev_x = x
	prev_y = y

def create_drawing():
	global draw_window_open
	print("create drawing") # Opens new gui with blank drawing template
	if (not draw_window_open):
		draw_window = tk.Toplevel(top)
		send_drawing_button = tk.Button(draw_window, text="Send", command=lambda: send_image_info(draw_window))
		draw_window.bind("<Button-1>", mouse_click)
		draw_window.bind("<B1-Motion>", mouse_move)
		send_drawing_button.pack()
		draw_window.protocol("CLOSE_DRAW_WINDOW", lambda: close_drawing(draw_window))
		draw_window_open = True

def close_drawing(draw_window):
	global draw_window_open
	draw_window_open = False

def send_image_info(draw_window):
	close_drawing(draw_window)
	draw_window.destroy()
	print(image)

def draw_line(draw_window, prev_x, prev_y, x, y):
	print("draw line") # Use mouse prev and current position to change array values

def change_pixels_in_radius(brush_size, x, y):
	for i in range(brush_size):
		for j in range(brush_size):
			global image
			if (brush_size - i < brush_size - 1 and brush_size - j < brush_size - 1):
				if (0 <= x + i and x + i < WIDTH and 0 <= y + j and y + j < HEIGHT):
					image[x+i][y+j] = [0,0,0]
				if (0 <= x - i and x + i < WIDTH and 0 <= y - j and y - j < HEIGHT):
					image[x-i][y-j] = [0,0,0]
				
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

tk.mainloop()
