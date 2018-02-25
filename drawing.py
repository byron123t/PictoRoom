from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk

WIDTH = 3
HEIGHT = 3
image = [[(255, 255, 255)] * WIDTH for x in range(HEIGHT)]
print(image)
def create_drawing():
	print("create drawing") # Opens new gui with blank drawing template

def draw_line():
	print("draw line") # Use mouse prev and current position to change array values

def change_pixels_in_radius(int brush_size):
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
