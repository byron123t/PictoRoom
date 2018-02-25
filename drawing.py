from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk

WIDTH = 3
HEIGHT = 3
image = [[(255, 255, 255)] * WIDTH for x in range(HEIGHT)]
draw_window_open = False

def create_drawing():
	global draw_window_open
	print("create drawing") # Opens new gui with blank drawing template
	if (not draw_window_open):
		draw_window = tk.Toplevel(top)
		send_drawing_button = tk.Button(draw_window, text="Send", command=lambda: send_image_info(draw_window))
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

def draw_line(draw_window):
	print("draw line") # Use mouse prev and current position to change array values

def change_pixels_in_radius(brush_size):
	print("find pixels in radius")

top = tk.Tk()
top.title("PictoRoom")

messages_frame = tk.Frame(top)
scrollbar = tk.Scrollbar(messages_frame)
msg_list = tk.Listbox(messages_frame, height=15, width=50,
						yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH);
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
