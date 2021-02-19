from tkinter import *
import tkinter.font
import haptics 
import time
import sys

ROW_NUM = 12
intense_var = []
root = None
hap_text = None
isexit = False
state_text = None

def make_label_box(frm, name, num) :
    global intense_var, root
    if name == "None" :
        var = DoubleVar(root)
        var.set(0.)
        intense_var.append(var)
        return 0
    temp_frm = Frame(frm)
    temp_frm.pack(side = TOP)

    b = tkinter.Button(temp_frm, overrelief="solid", text = '▷', 
        width=1, height = 1,command= lambda: hap_play(name), repeatdelay=1000, repeatinterval=100)
    b.pack(side = RIGHT)

    label = Label(temp_frm, text = name, anchor = W, width = 15)
    label.pack(side = LEFT)

    var = DoubleVar(root)
    var.set(num)
    intense_var.append(var)

    w = Spinbox(temp_frm, from_ = 0., to = 10., 
                increment = 0.1, width = 5, textvariable = var)
    w.pack(side = RIGHT)



def hap_play(name) :
    haptics.GUI_active(name)

def apply_value() :
    haptics.logger.info("applied") 
    f = open("./PUBG/TactFiles/intense.txt", 'w') 
    for i in range(len(intense_var)) :  
        # print(intense_var[i].get())
        haptics.intense[i] = intense_var[i].get()
        if not 0<=haptics.intense[i]<=10 :
            haptics.intense[i] = 1
        data = str(haptics.intense[i]) + "\n"
        f.write(data)
    f.close()


def state_change(stat) :
    global state_text 
    state_text.delete(1.0, END)
    state_text.insert("current", stat)

def hap_change(hap) :
    global hap_text 
    hap_text.delete(1.0, END)
    hap_text.insert("current", hap)

def setGUI() :
    global intense_var, root, state_text, hap_text, isexit
    intense_var = []

    root = Tk()
    root.title("PUBG player")
    root.geometry("600x350")
    root.resizable(True, True)

    title_font=tkinter.font.Font(family="Lucida Grande", size=13, weight="bold")
    bottom_frame = Frame(root)
    bottom_frame.pack(side = BOTTOM, pady = 10)
    top_frame = Frame(root)
    top_frame.pack(side = TOP, pady = 10)
    frame1 = Frame(root)
    frame1.pack(side = LEFT, padx =7)
    frame2 = Frame(root)
    frame2.pack(side = LEFT, padx =7)
    frame3 = Frame(root)
    frame3.pack(side = LEFT, padx =7)

    title_label = Label(top_frame, text = "Intensity of Haptics, 0 to 10", anchor = CENTER, width = 30, font = title_font)
    title_label.pack(side = TOP)

    B = Button(bottom_frame, width=10 ,height= 1, text = "Apply", command = apply_value)
    B.pack(side = RIGHT, padx =10)

    state_text=Text(bottom_frame, width = 10, height = 1)
    state_text.pack(side = RIGHT, padx =10)
    state_label = Label(bottom_frame, text = "Game State ", anchor = W, width = 10)
    state_label.pack(side = RIGHT)
    
    hap_text=Text(bottom_frame, width = 20, height = 1)
    hap_text.pack(side = RIGHT, padx =10)
    hap_label = Label(bottom_frame, text = "Haptic Type ", anchor = W, width = 10)
    hap_label.pack(side = RIGHT)

    for i in range(ROW_NUM-2) :
        make_label_box(frame1, haptics.tacts[i], haptics.intense[i])
    for i in range(ROW_NUM-2,ROW_NUM*2) :
        make_label_box(frame2, haptics.tacts[i], haptics.intense[i])
    for i in range(ROW_NUM*2, ROW_NUM*3) :
        make_label_box(frame3, haptics.tacts[i], haptics.intense[i])

    root.mainloop()
    isexit = True

# setGUI()