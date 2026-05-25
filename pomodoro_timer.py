"""简易桌面番茄钟 - 25分钟工作，5分钟休息"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import winsound
import platform


class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("番茄钟")
        self.root.geometry("400x350")
        self.root.resizable(False, False)

        # 计时器状态
        self.is_running = False
        self.is_paused = False
        self.time_left = 25 * 60  # 25分钟
        self.is_break = False
        self.timer_thread = None

        self.setup_ui()

    def setup_ui(self):
        # 标题
        title_label = tk.Label(
            self.root,
            text="🍅 番茄钟",
            font=("Microsoft YaHei", 20, "bold")
        )
        title_label.pack(pady=20)

        # 状态标签
        self.status_label = tk.Label(
            self.root,
            text="工作时间",
            font=("Microsoft YaHei", 12)
        )
        self.status_label.pack(pady=5)

        # 时间显示
        self.time_label = tk.Label(
            self.root,
            text="25:00",
            font=("Consolas", 48, "bold"),
            fg="#e74c3c"
        )
        self.time_label.pack(pady=20)

        # 进度条
        self.progress = ttk.Progressbar(
            self.root,
            length=300,
            mode='determinate',
            maximum=25 * 60
        )
        self.progress.pack(pady=10)
        self.progress['value'] = 25 * 60

        # 按钮框架
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        # 开始按钮
        self.start_button = tk.Button(
            button_frame,
            text="开始",
            command=self.start_timer,
            font=("Microsoft YaHei", 12),
            width=8,
            bg="#27ae60",
            fg="white",
            relief="flat"
        )
        self.start_button.grid(row=0, column=0, padx=5)

        # 暂停按钮
        self.pause_button = tk.Button(
            button_frame,
            text="暂停",
            command=self.pause_timer,
            font=("Microsoft YaHei", 12),
            width=8,
            bg="#f39c12",
            fg="white",
            relief="flat",
            state="disabled"
        )
        self.pause_button.grid(row=0, column=1, padx=5)

        # 重置按钮
        self.reset_button = tk.Button(
            button_frame,
            text="重置",
            command=self.reset_timer,
            font=("Microsoft YaHei", 12),
            width=8,
            bg="#95a5a6",
            fg="white",
            relief="flat"
        )
        self.reset_button.grid(row=0, column=2, padx=5)

    def format_time(self, seconds):
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"

    def update_display(self):
        self.time_label.config(text=self.format_time(self.time_left))
        if not self.is_break:
            self.progress['value'] = 25 * 60 - self.time_left
        else:
            self.progress['value'] = 5 * 60 - self.time_left

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.is_paused = False
            self.start_button.config(state="disabled")
            self.pause_button.config(state="normal", text="暂停")
            self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
            self.timer_thread.start()

    def pause_timer(self):
        if self.is_running:
            if self.is_paused:
                self.is_paused = False
                self.pause_button.config(text="暂停")
            else:
                self.is_paused = True
                self.pause_button.config(text="继续")

    def reset_timer(self):
        self.is_running = False
        self.is_paused = False
        self.is_break = False
        self.time_left = 25 * 60
        self.start_button.config(state="normal")
        self.pause_button.config(state="disabled", text="暂停")
        self.status_label.config(text="工作时间")
        self.time_label.config(fg="#e74c3c")
        self.progress.config(maximum=25 * 60)
        self.update_display()

    def play_beep(self):
        """播放提示音"""
        try:
            for _ in range(3):
                winsound.Beep(800, 200)
                time.sleep(0.1)
        except:
            pass

    def run_timer(self):
        total_time = 25 * 60 if not self.is_break else 5 * 60

        while self.time_left > 0:
            if not self.is_running:
                return
            if self.is_paused:
                time.sleep(0.1)
                continue

            self.update_display()
            time.sleep(1)
            self.time_left -= 1

        # 计时结束
        self.is_running = False
        self.play_beep()

        if not self.is_break:
            # 工作时间结束，进入休息
            self.root.after(0, lambda: messagebox.showinfo(
                "番茄钟",
                "工作时间结束！休息一下吧~"
            ))
            self.is_break = True
            self.time_left = 5 * 60
            self.root.after(0, self.break_mode)
        else:
            # 休息时间结束
            self.root.after(0, lambda: messagebox.showinfo(
                "番茄钟",
                "休息结束！准备开始工作吧~"
            ))
            self.root.after(0, self.reset_timer)

    def break_mode(self):
        self.status_label.config(text="休息时间")
        self.time_label.config(fg="#27ae60")
        self.progress.config(maximum=5 * 60, value=5 * 60)
        self.start_button.config(state="normal")
        self.pause_button.config(state="disabled", text="暂停")


def main():
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
