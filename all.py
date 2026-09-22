import tkinter as tk
from tkinter import font

class taskmaneagerApp:
    def __init__(self, root):
        self.root =root
        self.root.title("task_maneager")
        self.root.geometry("600x400")
        
        self.tasks = []
        self.ACTIVE_COLOR = "#0078D7"  
        self.INACTIVE_COLOR = "#444"
        self.BG_COLOR = "#2E2E2E"
        self.FG_COLOR = "#FFFFFF"
        self.ENTRY_BG = "#3E3E3E"
        self.card_color = "#3E3E3E"
        self.normal_font = font.Font(family="Helvetica", size=12)
        self.strike_font = font.Font(family="Helvetica", size=12, overstrike=True)
        self.root.config(bg=self.BG_COLOR)
        self.tasks_db = {
    "شنبه": [], "یکشنبه": [], "دوشنبه": [], "سه‌شنبه": [],
    "چهارشنبه": [], "پنج‌شنبه": [], "جمعه": []
}       
        self.current_day = "شنبه"

        self.setup_ui()
    def switch_day(self,day):
        self.current_day
        self.current_day = day
        self.show_tasks()
        self.update_button_colors()
    
    def update_button_colors(self):
        for btn in self.days_frame.winfo_children():
            if btn.cget("text") == self.current_day:
                btn.config(bg=self.ACTIVE_COLOR)
            else:
                btn.config(bg=self.INACTIVE_COLOR)
    
    def setup_ui(self):
        # ۱. ساخت نوار روزها (دقت کن همه با self. تعریف می‌شوند)
        self.days_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        self.days_frame.pack(side="right", fill="y", padx=10, pady=20)

        for day in self.tasks_db.keys():
            btn = tk.Button(self.days_frame, text=day, 
                            command=lambda d=day: self.switch_day(d), # باید self باشد
                            bg="#444", fg="white", width=12)
            btn.pack(pady=2)
        
        self.update_button_colors() # باید self باشد

        # ۲. بخش اصلی
        self.main_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        self.main_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        # ۳. ورودی
        self.entry = tk.Entry(self.main_frame, bg=self.ENTRY_BG, fg=self.FG_COLOR)
        self.entry.pack(fill="x", pady=(0, 20))
        self.entry.bind('<Return>', self.add_task) # باید self باشد

        # ۴. نگهدارنده تسک‌ها
        self.tasks_frame = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        self.tasks_frame.pack(fill="both", expand=True)

        self.show_tasks()
        
    
    def add_task(self,event=None):
        task_text = self.entry.get()
        if task_text:
        # تسک جدید به صورت دیکشنری با وضعیت اولیه False اضافه می‌شود
            new_task_item = {"text": task_text, "done": False}
            self.tasks_db[self.current_day].append(new_task_item) # اضافه کردن به لیست روز فعلی
            self.entry.delete(0, tk.END)
            self.show_tasks()
    
    def remove_task(self, task_item):
        # حذف از لیستِ آن روز
        self.tasks_db[self.current_day].remove(task_item)
        # فراخوانی مجدد برای رفرش کردن نمایش
        self.show_tasks()

    
    def toggle_task(self, task_item, var, widget):
    # آپدیت وضعیت در ساختار داده اصلی
        task_item["done"] = var.get() 

        if task_item["done"]: # تیک خورد
            widget.config(fg="gray", font=self.strike_font) 
            print(f"تسک '{task_item['text']}' انجام شد.")
        else: # تیک برداشته شد
            widget.config(fg="white", font=self.normal_font) 
            print(f"تسک '{task_item['text']}' دوباره فعال شد.")
    def show_tasks(self):
    # پاک کردن نمایش قبلی (فقط تسک‌ها)
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()
    
    # نمایش لیست جدید بر اساس وضعیت ذخیره شده
    # ما باید به هر دیکشنری تسک دسترسی داشته باشیم
        for task_item in self.tasks_db[self.current_day]: 
            card = tk.Frame(self.tasks_frame, bg=self.card_color, bd=0)
            card.pack(fill="x", pady=5, padx=5)
        
        # مقدار اولیه BooleanVar باید از وضعیت تسک در دیکشنری خوانده شود
            var = tk.BooleanVar(value=task_item["done"]) 
            current_color ="gray" if task_item["done"] else "white"
            current_font =self.strike_font if task_item["done"] else self.normal_font 
            task_check = tk.Checkbutton(
                card, 
                text=task_item["text"], # متن تسک از دیکشنری خوانده می‌شود
                variable=var,
                bg=self.card_color, 
                activebackground=self.card_color,
                selectcolor=self.card_color,
                highlightthickness=0,
                relief="flat",
                fg=current_color,
                font=current_font
                # فونت اولیه را اینجا تنظیم می‌کنیم بر اساس وضعیت
            
            )           
        # Command باید به دیکشنریِ واقعی تسک ارجاع دهد
            task_check.config(command=lambda item=task_item, v=var, w=task_check: self.toggle_task(item, v, w))
            task_check.pack(side="left", padx=10)

        # دکمه حذف
        # Command باید به دیکشنریِ واقعی تسک ارجاع دهد
            delete_btn = tk.Button(card, text="×", bg=self.card_color, fg="red", bd=0, 
                command=lambda item=task_item: self.remove_task(item))
            delete_btn.pack(side="right")
    
    
if __name__ == "__main__": 
    root = tk.Tk()
    app = taskmaneagerApp(root)
    root.mainloop()
