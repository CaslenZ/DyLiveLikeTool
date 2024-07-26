import tkinter as tk
import webbrowser
import time
import pynput
from tkinter import messagebox
import os
import datetime
from tkinter import simpledialog, Tk, Label, PhotoImage
from PIL import Image, ImageTk

class DyLiveLikeTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DyLiveLikeTool by Caslen Z")
        self.root.wm_attributes("-topmost", 1)  # 使窗口始终在最上方

        # 锁定窗口大小
        self.root.minsize(400, 500)
        self.root.maxsize(400, 500)

        # 设置窗口大小和背景颜色
        self.root.geometry("400x400")
        self.root.configure(bg='#f0f0f0')  # 背景颜色

        # 加载背景图片
        self.image = Image.open("Bgi.png")  # 将"your_background_image.jpg"替换为实际的图片路径
        self.photo = ImageTk.PhotoImage(self.image)

        # 创建一个 Label 用于显示背景图
        self.background_label = Label(self.root, image=self.photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)  # 使背景图填充整个窗口

        # 直播间链接及输入框在同一行
        self.link_frame = tk.Frame(self.root, bg='#f0f0f0')  # 框架背景颜色
        self.link_label = tk.Label(self.link_frame, text="直播间链接:", font=('Arial', 12), bg='#f0f0f0')  # 字体和背景颜色
        self.link_label.pack(side=tk.LEFT)
        self.link_entry = tk.Entry(self.link_frame, font=('Arial', 12), width=30)  # 字体和宽度
        self.link_entry.pack(side=tk.LEFT)
        self.link_frame.grid(row=0, column=0, padx=10, pady=10, sticky='ew')  # 使用 grid 布局

        # 点赞方式及下拉菜单在同一行
        self.like_method_frame = tk.Frame(self.root, bg='#f0f0f0')  # 框架背景颜色
        self.like_method_label = tk.Label(self.like_method_frame, text="点赞方式:", font=('Arial', 12), bg='#f0f0f0')  # 字体和背景颜色
        self.like_method_label.pack(side=tk.LEFT)
        self.like_method_var = tk.StringVar()
        self.like_method_var.set("鼠标左键")  # 设置初始值
        self.like_method_option = tk.OptionMenu(self.like_method_frame, self.like_method_var, "鼠标左键", "键盘 Z 键")  # 先创建 OptionMenu
        self.like_method_option["font"] = ('Arial', 12)  # 再设置字体
        self.like_method_option.pack(side=tk.LEFT)
        self.like_method_frame.grid(row=1, column=0, padx=10, pady=10, sticky='ew')  # 使用 grid 布局

        # 点赞数量及输入框在同一行
        self.like_count_frame = tk.Frame(self.root, bg='#f0f0f0')  # 框架背景颜色
        self.like_count_label = tk.Label(self.like_count_frame, text="点赞数量:", font=('Arial', 12), bg='#f0f0f0')  # 字体和背景颜色
        self.like_count_label.pack(side=tk.LEFT)
        self.like_count_entry = tk.Entry(self.like_count_frame, font=('Arial', 12), width=10)  # 字体和宽度
        self.like_count_entry.pack(side=tk.LEFT)
        self.like_count_frame.grid(row=2, column=0, padx=10, pady=10, sticky='ew')  # 使用 grid 布局

        # 点赞间隔及输入框在同一行
        self.like_interval_frame = tk.Frame(self.root, bg='#f0f0f0')  # 框架背景颜色
        self.like_interval_label = tk.Label(self.like_interval_frame, text="点赞间隔(秒):", font=('Arial', 12), bg='#f0f0f0')  # 字体和背景颜色
        self.like_interval_label.pack(side=tk.LEFT)
        self.like_interval_entry = tk.Entry(self.like_interval_frame, font=('Arial', 12), width=10)  # 字体和宽度
        self.like_interval_entry.pack(side=tk.LEFT)
        self.like_interval_frame.grid(row=3, column=0, padx=10, pady=10, sticky='ew')  # 使用 grid 布局

        # 保存配置、跳转、点赞、导出配置、载入配置按钮在同一行
        self.button_frame = tk.Frame(self.root, bg='#f0f0f0')  # 框架背景颜色
        self.save_config_button = tk.Button(self.button_frame, text="保存配置", font=('Arial', 12), bg='#4CAF50', fg='white', relief=tk.RAISED, bd=2, command=self.save_config)  # 按钮样式
        self.save_config_button.pack(side=tk.LEFT, padx=5)  # 内边距
        self.jump_button = tk.Button(self.button_frame, text="跳转", font=('Arial', 12), bg='#2196F3', fg='white', relief=tk.RAISED, bd=2, command=self.jump)  # 按钮样式
        self.jump_button.pack(side=tk.LEFT, padx=5)  # 内边距
        self.like_button = tk.Button(self.button_frame, text="点赞", font=('Arial', 12), bg='#FF5722', fg='white', relief=tk.RAISED, bd=2, command=self.start_like)  # 按钮样式
        self.like_button.pack(side=tk.LEFT, padx=5)  # 内边距
        self.export_config_button = tk.Button(self.button_frame, text="导出配置", font=('Arial', 12), bg='#9C27B0', fg='white', relief=tk.RAISED, bd=2, command=self.export_config)  # 按钮样式
        self.export_config_button.pack(side=tk.LEFT, padx=5)  # 内边距
        self.load_config_button = tk.Button(self.button_frame, text="载入配置", font=('Arial', 12), bg='#607D8B', fg='white', relief=tk.RAISED, bd=2, command=self.load_config)  # 按钮样式
        self.load_config_button.pack(side=tk.LEFT, padx=5)  # 内边距
        self.button_frame.grid(row=4, column=0, padx=10, pady=10, sticky='ew')  # 使用 grid 布局

        # 状态栏
        self.status_label = tk.Label(self.root, text="状态栏:", font=('Arial', 12), bg='#f0f0f0')  # 字体和背景颜色
        self.status_label.grid(row=5, column=0, padx=10, pady=10, sticky='w')  # 修改为 grid 布局

        self.status_text = tk.StringVar()
        self.status_display = tk.Label(self.root, textvariable=self.status_text, font=('Arial', 12), bg='#f0f0f0', wraplength=350)  # 字体、背景颜色和文本换行宽度
        self.status_display.grid(row=6, column=0, padx=10, pady=10, sticky='ew')  # 修改为 grid 布局

        # 创建支持链接
        self.support_link = tk.Label(self.root, text="帮助与反馈", font=('Arial', 12), fg='blue', cursor="hand2", bg='#f0f0f0')
        self.support_link.grid(row=7, column=0, padx=10, pady=10, sticky='w')
        self.support_link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/CaslenZ/DyLiveLikeTool/blob/main/README.md"))

        self.previous_mouse_position = None  # 用于记录上一次的鼠标位置

        self.saved_link = None  # 保存上次保存的直播间链接
        self.saved_method = None  # 保存上次保存的点赞方式
        self.saved_count = None  # 保存上次保存的点赞数量
        self.saved_interval = None  # 保存上次保存的点赞间隔

    def save_config(self):
        link = self.link_entry.get()
        if not (link.startswith("https://live.douyin.com") or link.startswith("live.douyin.com") or link.startswith("HTTPS://LIVE.DOUYIN.COM") or link.startswith("LIVE.DOUYIN.COM")):
            self.status_text.set("直播间链接格式不准确。")
            return
        try:
            count = int(self.like_count_entry.get())
            if count < 10 or count > 3000:
                self.status_text.set("点赞数量应在 10~3000 之间。")
                return
        except ValueError:
            self.status_text.set("点赞数量应该是整数。")
            return

        try:
            interval = float(self.like_interval_entry.get())
            if not 0.1 <= interval <= 0.4:
                self.status_text.set("点赞间隔应在 0.1~0.4 秒之间。")
                return
        except ValueError:
            self.status_text.set("点赞间隔应该是数字。")
            return

        self.saved_link = link  # 保存当前配置
        self.saved_method = self.like_method_var.get()
        self.saved_count = count
        self.saved_interval = interval

        self.status_text.set(f'''保存配置成功
        链接 - {link}
        点赞方式 - {self.like_method_var.get()}
        点赞数量 - {count}
        点赞间隔 - {interval}''')

    def jump(self):
        if not self.check_saved_config():  # 新增：在跳转前检查是否保存了配置
            messagebox.showwarning("提示", "请先保存配置！")
            return
        link = self.link_entry.get()
        try:
            webbrowser.open(link)
            self.status_text.set("网页已跳转")
        except:
            self.status_text.set("网页跳转无效")

    def start_like(self):
        link = self.link_entry.get()
        method = self.like_method_var.get()
        count = self.like_count_entry.get()
        interval = self.like_interval_entry.get()

        self.link_entry.config(state='disabled')
        self.like_count_entry.config(state='disabled')
        self.like()

    def like(self):
        if self.like_method_var.get() == "鼠标左键":
            self.status_text.set("选择了鼠标左键点赞方式")
            messagebox.showinfo("提示", "请将鼠标指针移动到直播间范围内，5 秒后开始点赞任务")
        elif self.like_method_var.get() == "键盘 Z 键":
            self.status_text.set("选择了键盘 Z 键点赞方式")
            messagebox.showinfo("提示", "请不要打开任何输入框，并且点击一下直播间的窗口，7 秒后开始点赞任务")
        time.sleep(5)
        if self.like_method_var.get() == "鼠标左键":
            mouse = pynput.mouse.Controller()
            count = 0
            while count < int(self.like_count_entry.get()):
                self.status_text.set(f"当前点赞计数: {count}")
                current_mouse_position = self.root.winfo_pointerxy()  # 获取当前鼠标位置
                if self.previous_mouse_position is not None:
                    # 计算鼠标移动的距离
                    distance = ((current_mouse_position[0] - self.previous_mouse_position[0])**2 + (current_mouse_position[1] - self.previous_mouse_position[1])**2)**0.5
                    if distance > 50:  # 可根据需要调整这个阈值来定义大幅度移动
                        self.status_text.set("鼠标大幅度移动，暂停点赞")
                        break
                self.previous_mouse_position = current_mouse_position  # 更新上一次的鼠标位置
                mouse.click(pynput.mouse.Button.left)
                count += 1
                self.status_text.set(f"已点赞 {count} 次")
                time.sleep(float(self.like_interval_entry.get()))  # 使用输入的点赞间隔
        elif self.like_method_var.get() == "键盘 Z 键":
            keyboard = pynput.keyboard.Controller()
            count = 0
            while count < int(self.like_count_entry.get()):
                self.status_text.set(f"当前点赞计数: {count}")
                current_mouse_position = self.root.winfo_pointerxy()  # 获取当前鼠标位置
                if self.previous_mouse_position is not None:
                    # 计算鼠标移动的距离
                    distance = ((current_mouse_position[0] - self.previous_mouse_position[0])**2 + (current_mouse_position[1] - self.previous_mouse_position[1])**2)**0.5
                    if distance > 50:  # 可根据需要调整这个阈值来定义大幅度移动
                        self.status_text.set("鼠标大幅度移动，暂停点赞")
                        break
                self.previous_mouse_position = current_mouse_position  # 更新上一次的鼠标位置
                keyboard.press('z')
                keyboard.release('z')
                count += 1
                self.status_text.set(f"已点赞 {count} 次")
                time.sleep(float(self.like_interval_entry.get()))  # 使用输入的点赞间隔
        self.link_entry.config(state='normal')
        self.like_count_entry.config(state='normal')

    def check_saved_config(self):
        link = self.link_entry.get()
        if not link:
            return False
        try:
            count = int(self.like_count_entry.get())
            if not self.like_method_var.get():
                return False
        except ValueError:
            return False

        try:
            interval = float(self.like_interval_entry.get())
        except ValueError:
            return False

        return True

    def export_config(self):
        if not self.check_saved_config():
            messagebox.showwarning("保存失败", "请完整填写所有内容。")
            return
        link = self.link_entry.get()
        method = self.like_method_var.get()
        count = self.like_count_entry.get()
        interval = self.like_interval_entry.get()  # 获取点赞间隔

        live_name = tk.simpledialog.askstring("直播间名字", "请输入直播间名字:")
        if not live_name:
            return

        current_time = datetime.datetime.now().strftime('%m-%d-%H-%M-%S')

        # 创建 Config 文件夹，如果不存在
        if not os.path.exists('Config'):
            os.makedirs('Config')

        file_name = f"Config/{live_name}-{current_time}.czad"
        with open(file_name, 'w') as f:
            f.write(f"Link\n{link}\nMethod\n{method}\nCount\n{count}\nInterval\n{interval}")  # 保存点赞间隔
        self.status_text.set("保存成功")

    def load_config(self):
        from tkinter import filedialog
        file_path = tk.filedialog.askopenfilename(filetypes=[("CZAD files", "*.czad")])
        if not file_path:
            return

        with open(file_path, 'r') as f:
            lines = f.readlines()
            if len(lines) < 7:  # 检查文件内容行数是否足够
                messagebox.showwarning("载入失败", "配置被损坏，请重新选择配置文件。")
                return
            link = lines[1].strip()
            method = lines[3].strip()
            count = lines[5].strip()
            interval = lines[7].strip()  # 读取点赞间隔

        self.link_entry.delete(0, tk.END)
        self.link_entry.insert(0, link)
        self.like_method_var.set(method)
        self.like_count_entry.delete(0, tk.END)
        self.like_count_entry.insert(0, count)
        self.like_interval_entry.delete(0, tk.END)
        self.like_interval_entry.insert(0, interval)  # 加载点赞间隔

        self.status_text.set("载入成功")

    def stop_like(self):
        messagebox.showinfo("点赞完成",
                            f"点赞完成，当前时间：{time.strftime('%Y-%m-%d %H:%M:%S')}，点赞数量：{self.status_text.get().split('已点赞 ')[1].split(' 次')[0]}")

if __name__ == "__main__":
    app = DyLiveLikeTool()
    app.root.mainloop()