from tkinter import *  # 导入 Tkinter 库

root = Tk()  # 创建窗口对象的背景色
root.title("纵横股市之龙腾四海")
root.geometry("1280x800")

# 创建两个列表
li = ['C', 'python', 'php', 'html', 'SQL', 'java']
movie = ['CSS', 'jQuery', 'Bootstrap']
listb = Listbox(root)  # 创建两个列表组件
listb.grid(column=1, row=1)
listb2 = Listbox(root)
listb2.grid(column=1, row=2)
lbl = Label(root, text="Hello")
lbl.grid(column=2, row=3)

def clicked():
    lbl.configure(text="Button was clicked!")

btn = Button(root, text="Click Me", command=clicked)
btn.grid(column=1, row=3)

for item in li:  # 第一个小部件插入数据
    listb.insert(0, item)

for item in movie:  # 第二个小部件插入数据
    listb2.insert(0, item)

#listb.pack()  # 将小部件放置到主窗口中
#listb2.pack()
#btn.pack()

root.mainloop()  # 进入消息循环