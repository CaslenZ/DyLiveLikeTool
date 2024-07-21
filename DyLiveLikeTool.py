import tkinter as tk
import webbrowser
import time
import pynput
from tkinter import messagebox
import os
import datetime
from tkinter import simpledialog

class DyLiveLikeTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DyLiveLikeTool by CASLENZ")
        self.root.wm_attributes("-topmost", 1)  # 使窗口始终在最上方
        self.root.geometry("400x400")

        # 直播间链接及输入框在同一行
        self.link_frame = tk.Frame(self.root)
        self.link_label = tk.Label(self.link_frame, text="直播间链接:")
        self.link_label.pack(side=tk.LEFT)
        self.link_entry = tk.Entry(self.link_frame)
        self.link_entry.pack(side=tk.LEFT)
        self.link_frame.pack()

        # 点赞方式及下拉菜单在同一行
        self.like_method_frame = tk.Frame(self.root)
        self.like_method_label = tk.Label(self.like_method_frame, text="点赞方式:")
        self.like_method_label.pack(side=tk.LEFT)
        self.like_method_var = tk.StringVar()
        self.like_method_option = tk.OptionMenu(self.like_method_frame, self.like_method_var, "鼠标左键", "键盘 Z 键")
        self.like_method_option.pack(side=tk.LEFT)
        self.like_method_frame.pack()

        # 点赞数量及输入框在同一行
        self.like_count_frame = tk.Frame(self.root)
        self.like_count_label = tk.Label(self.like_count_frame, text="点赞数量:")
        self.like_count_label.pack(side=tk.LEFT)
        self.like_count_entry = tk.Entry(self.like_count_frame)
        self.like_count_entry.pack(side=tk.LEFT)
        self.like_count_frame.pack()

        # 一直点赞选项
        self.continuous_like_var = tk.BooleanVar()
        self.continuous_like_checkbox = tk.Checkbutton(self.root, text="一直点赞", variable=self.continuous_like_var, command=self.toggle_like_count_entry_state)
        self.continuous_like_checkbox.pack()

        # 保存配置、跳转、点赞、导出配置、载入配置按钮在同一行
        self.button_frame = tk.Frame(self.root)
        self.save_config_button = tk.Button(self.button_frame, text="保存配置", command=self.save_config)
        self.save_config_button.pack(side=tk.LEFT)
        self.jump_button = tk.Button(self.button_frame, text="跳转", command=self.jump)
        self.jump_button.pack(side=tk.LEFT)
        self.like_button = tk.Button(self.button_frame, text="点赞", command=self.start_like)
        self.like_button.pack(side=tk.LEFT)
        self.export_config_button = tk.Button(self.button_frame, text="导出配置", command=self.export_config)
        self.export_config_button.pack(side=tk.LEFT)
        self.load_config_button = tk.Button(self.button_frame, text="载入配置", command=self.load_config)
        self.load_config_button.pack(side=tk.LEFT)
        self.button_frame.pack()

        # 停止点赞按钮（初始隐藏）
        self.stop_like_button = tk.Button(self.root, text="停止点赞", command=self.stop_like)
        self.stop_like_button.pack_forget()

        # 状态栏
        self.status_label = tk.Label(self.root, text="状态栏:")
        self.status_label.pack()
        self.status_text = tk.StringVar()
        self.status_display = tk.Label(self.root, textvariable=self.status_text)
        self.status_display.pack()

        self.previous_mouse_position = None  # 用于记录上一次的鼠标位置

    def toggle_like_count_entry_state(self):
        if self.continuous_like_var.get():
            self.like_count_entry.config(state='disabled')
        else:
            self.like_count_entry.config(state='normal')

    def save_config(self):
        link = self.link_entry.get()
        if not (link.startswith("https://live.douyin.com/") or link.startswith("live.douyin.com")):
            self.status_text.set("401 错误")
            return
        try:
            count = int(self.like_count_entry.get())
            if count < 10 or count > 3000:
                self.status_text.set("402 错误")
                return
        except ValueError:
            self.status_text.set("403 错误")
            return
        self.status_text.set(f'''保存配置成功
        链接 - {link}
        点赞方式 - {self.like_method_var.get()}
        点赞数量 - {count}
        一直点赞 - {self.continuous_like_var.get()}''')

    def jump(self):
        link = self.link_entry.get()
        try:
            webbrowser.open(link)
            self.status_text.set("网页加载成功")
        except:
            self.status_text.set("网页加载失败")

    def start_like(self):
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
                time.sleep(0.1)  # 增加 0.5 秒的点赞间隔
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
                time.sleep(0.1)  # 增加 0.5 秒的点赞间隔
        self.link_entry.config(state='normal')
        self.like_count_entry.config(state='normal')

    def export_config(self):
        link = self.link_entry.get()
        method = self.like_method_var.get()
        count = self.like_count_entry.get()
        still_like = self.continuous_like_var.get()

        live_name = tk.simpledialog.askstring("直播间名字", "请输入直播间名字:")
        if not live_name:
            return

        current_time = datetime.datetime.now().strftime('%m-%d-%H-%M-%S')

        # 创建 Config 文件夹，如果不存在
        if not os.path.exists('Config'):
            os.makedirs('Config')

        file_name = f"Config/{live_name}-{current_time}.czad"
        with open(file_name, 'w') as f:
            f.write(f"Link\n{link}\nMethod\n{method}\nCount\n{count}\nStillLike\n{still_like}")
        self.status_text.set("保存成功")

    def load_config(self):
        from tkinter import filedialog
        file_path = tk.filedialog.askopenfilename(filetypes=[("CZAD files", "*.czad")])
        if not file_path:
            return

        with open(file_path, 'r') as f:
            lines = f.readlines()
            link = lines[1].strip()
            method = lines[3].strip()
            count = lines[5].strip()
            still_like = lines[7].strip()

        self.link_entry.delete(0, tk.END)
        self.link_entry.insert(0, link)
        self.like_method_var.set(method)
        self.like_count_entry.delete(0, tk.END)
        self.like_count_entry.insert(0, count)
        self.continuous_like_var.set(still_like == 'True')

        self.status_text.set("载入成功")

    def stop_like(self):
        messagebox.showinfo("点赞完成", f"点赞完成，当前时间：{time.strftime('%Y-%m-%d %H:%M:%S')}，点赞数量：{self.status_text.get().split('已点赞 ')[1].split(' 次')[0]}")

if __name__ == "__main__":
    app = DyLiveLikeTool()
    app.root.mainloop()