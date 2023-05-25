
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter.messagebox import showinfo
import cv2
from keras.models import load_model
import numpy as np
import pandas as pd
from numpy.ma.core import sort

# data = pd.read_csv('D:/Money.csv')
# c = data['Ngay phat hanh'].values

root = Tk()
style = Style()
style.configure('TButton', font=('arial', 15, 'bold'))
root.title('mondo animale')
global path

model = load_model('data23.h5')
classes = ['scoiattolo', 'gatto', 'farfalla', 'mucca', 'elefante', 'cavallo', 'gallina', 'ragno', 'pecora', 'cane']
class_name = sort(classes)

# root.iconbitmap('')
root.geometry('900x500')
label = Label( root, text='Image animals',font=('arial', 15, 'bold'))
label.grid(row=0, column=0, columnspan=2, padx=50, pady=(50,0))

box = Canvas(root, width=303, height=303, background='white')
box.grid(row=1, column=0, padx=55, pady=20)
box.create_rectangle(1,1, 306, 306, width=4)

def insert():
    global img, path
    path= filedialog.askopenfilename(title="Select an Image", filetype=(('image    files','.jpeg'),('image    files','.png'),('all files','.')))
    img= Image.open(path)
    img = img.resize((300,300))
    img=ImageTk.PhotoImage(img)
    # label= Label(win, image= img)
    # label.image= img
    # label.pack()
    box.create_image(3, 3,anchor=NW, image=img)

def predict():
    global path, image
    print(path)
    image = cv2.imread(path)
    image = cv2.resize(image, (224,224))
    image = image.astype('float32')/255.0
    image = np.expand_dims(image, axis=0)

    pred = model.predict(image)
    res = class_name[np.argmax(pred)]
    # d = [np.argmax(pred)]
    print(pred)

    animals = []
    # for n in range(1, 100):
    animals.append((f'{res}', f'{res}'))

    # add data to the treeview
    for contact in animals:
        tree.insert('', END, values=contact)


btn1 = Button(root, text='Insert', style='TButton', command=lambda:insert())
btn1.grid(row=2, column=0, padx=60, sticky='w')

btn2= Button(root, text='Predict', style='TButton', command=lambda:predict())
btn2.grid(row=2, column=0, padx=60, sticky='e')

columns = ('RESULT')

tree = Treeview(root,height=2, columns=columns, show='headings')

# define headings
tree.heading('RESULT', text='RESULT')

# tree.heading('email', text='Email')

# generate sample data


def item_selected(event):
    for selected_item in tree.selection():
        item = tree.item(selected_item)
        record = item['values']
        # show a message
        showinfo(title='Information', message=','.join(record))


tree.bind('<<TreeviewSelect>>', item_selected)

tree.grid(row=1, column=1,pady=(20, 0), sticky='nsew')

# add a scrollbar
scrollbar = Scrollbar(root, orient=VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=1, column=2, sticky='ns')
    
root.mainloop()

