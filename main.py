import tkinter as tk
from tkinter import font
import json
import os

class taskmaneagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("task_maneager")
        self.root.geometry("600x400")
        
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(BASE_DIR, "tasks.json")
        
        self.tasks = []
        self.themes = {
            "dark": {
                "BG_COLOR": "#4E4E4E",
                "FG_COLOR": "#E0E0E0",
                "ENTRY_BG": "#424242",
                "card_color": "#4B4B4B",
                "ACTIVE_COLOR": "#007ACC",
                "INACTIVE_COLOR": "#3F3F3F",
                "BTN_FG": "#FFFFFF"
            },
            "light": {
                "BG_COLOR": "#F8F9FA",
                "FG_COLOR": "#212529",
                "ENTRY_BG": "#FFFFFF",
                "card_color": "#E9ECEF",
                "ACTIVE_COLOR": "#0D6EFD",
                "INACTIVE_COLOR": "#CED4DA",
                "BTN_FG": "#FFFFFF"       
            },
            "ocean": {
                "BG_COLOR": "#0F172A",
                "FG_COLOR": "#F1F5F9",
                "ENTRY_BG": "#1E293B",
                "card_color": "#334155",
                "ACTIVE_COLOR": "#38BDF8",
                "INACTIVE_COLOR": "#64748B",
                "BTN_FG": "#0F172A"
            },
            "forest": {
                "BG_COLOR": "#064E3B",
                "FG_COLOR": "#ECFDF5",
                "ENTRY_BG": "#3C6138",
                "card_color": "#3F6637",
                "ACTIVE_COLOR": "#709954",
                "INACTIVE_COLOR": "#3E5541",
                "BTN_FG": "#FFFFFF"
            },
            "red": {
                "BG_COLOR": "#C73C3C",          
                "FG_COLOR": "#ffffff",          
                "ENTRY_BG": "#ff8989",          
                "card_color": "#b14f4f",        
                "ACTIVE_COLOR": "#be0000",      
                "INACTIVE_COLOR": "#ff6e6e",    
                "BTN_FG": "#000000"             
            },
            "purple": {
                "BG_COLOR": "#1e1b2e",          
                "FG_COLOR": "#f3e8ff",          
                "ENTRY_BG": "#2d2640",          
                "card_color": "#2a223f",        
                "ACTIVE_COLOR": "#7c3aed",      
                "INACTIVE_COLOR": "#3b2a59",    
                "BTN_FG": "#ffffff"             
            }
        }
        
        self.current_theme_name = "dark"
        self.current_theme = "dark"
        self.normal_font = font.Font(family="Helvetica", size=12)
        self.strike_font = font.Font(family="Helvetica", size=12, overstrike=True)
        self.root.config(bg=self.themes[self.current_theme]["BG_COLOR"])
        
        self.tasks_db = {
            "شنبه": [], "یکشنبه": [], "دوشنبه": [], "سه‌شنبه": [],
            "چهارشنبه": [], "پنج‌شنبه": [], "جمعه": []
        }
        self.current_day = "شنبه"

        
        self.load_tasks()

        self.setup_ui()


    def draw_progress_circle(self, completed, total):
        self.progress_canvas.delete("all")
        
        # رنگ‌های پس‌زمینه تم فعلی
        current_theme_colors = self.themes[self.current_theme]
        bg_color = current_theme_colors["BG_COLOR"]
        active_color = current_theme_colors["ACTIVE_COLOR"]
        inactive_color = current_theme_colors["INACTIVE_COLOR"]
        fg_color = current_theme_colors["FG_COLOR"]
        
        # تنظیم رنگ پس‌زمینه خود بوم
        self.progress_canvas.config(bg=bg_color)
        
        # مختصات دایره روی بوم
        x1, y1, x2, y2 = 5, 5, 55, 55
        
        # ۱. کشیدن دایره کاملِ کم‌رنگ به عنوان پس‌زمینه پیشرفت
        self.progress_canvas.create_oval(
            x1, y1, x2, y2, 
            outline=inactive_color, 
            width=6
        )
        
        # اگر کل تسک‌ها صفر بود، درصد صفر است
        if total == 0:
            percent = 0
            extent = 0
        else:
            percent = int((completed / total) * 100)
            extent = -360 * (completed / total) # منفی برای چرخش ساعت‌گرد
            
        # ۲. کشیدن کمان پیشرفت (Arc) بر اساس درصد انجام شده
        if total > 0:
            self.progress_canvas.create_arc(
                x1, y1, x2, y2, 
                start=90, # شروع از بالای دایره
                extent=extent, 
                outline=active_color, 
                width=6, 
                style=tk.ARC
            )
            
        # ۳. نوشتن درصد دقیق وسط دایره
        self.progress_canvas.create_text(
            30, 30, 
            text=f"{percent}%", 
            fill=fg_color, 
            font=("Arial", 9, "bold")
        )
    
    
    def switch_day(self,day):
        self.current_day
        self.current_day = day
        self.show_tasks()
        self.update_button_colors()
        
    def toggle_theme_menu(self):
        if hasattr(self, 'theme_menu_frame') and self.theme_menu_frame.winfo_exists():
            self.theme_menu_frame.destroy()
        else:
            theme = self.themes[self.current_theme]
            
            parent_frame = self.theme_btn.master 
            
            self.theme_menu_frame = tk.Frame(parent_frame, bg=theme["BG_COLOR"])
            
            self.theme_menu_frame.pack(side=tk.LEFT, padx=5)
            
            for theme_key in self.themes.keys():
                btn = tk.Button(
                    self.theme_menu_frame,
                    text=theme_key.capitalize(),
                    command=lambda t=theme_key: self.select_theme(t),
                    bg=self.themes[theme_key]["card_color"], 
                    fg=self.themes[theme_key]["FG_COLOR"],
                    relief="flat",
                    padx=6,
                    pady=2
                )
                btn.pack(side=tk.LEFT, padx=2)




    def select_theme(self, theme_name):
        # ۱. تنظیم تم انتخابی کاربر
        self.current_theme = theme_name
        
        # ۲. اعمال رنگ‌ها به کل برنامه
        self.apply_theme()
        
        # ۳. بستن منوی انتخاب تم پس از انتخاب
        if hasattr(self, 'theme_menu_frame') and self.theme_menu_frame.winfo_exists():
            self.theme_menu_frame.destroy()



    def apply_theme(self):
        theme = self.themes[self.current_theme]
        
        self.root.config(bg=theme["BG_COLOR"])
        
        self.days_frame.config(bg=theme["BG_COLOR"])
        self.main_frame.config(bg=theme["BG_COLOR"])
        self.tasks_frame.config(bg=theme["BG_COLOR"])
        self.entry.config(bg=theme["ENTRY_BG"], fg=theme["FG_COLOR"], insertbackground=theme["FG_COLOR"])
        
        self.theme_btn.config(command=self.toggle_theme_menu)
        self.update_button_colors()
        self.show_tasks()

        
    
    def init_default_tasks(self):
        """ساختار پیش‌فرض تسک‌ها برای روزهای هفته"""
        self.tasks_db = {
            "شنبه": [], "یکشنبه": [], "دوشنبه": [], "سه‌شنبه": [],
            "چهارشنبه": [], "پنج‌شنبه": [], "جمعه": []
        }
        
    def load_tasks(self):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.tasks_db = json.load(f)
            except json.JSONDecodeError:
                print("فایل خراب است یا اجرا نمیشود ")
                self.init_default_tasks()
        else:
            self.init_default_tasks()
    
    def save_tasks(self):
        print("در حال ذخیره سازی...")
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.tasks_db, f, indent=4, ensure_ascii=False)
        print("ذخیره شد!")
            
    
    def update_button_colors(self):
        for btn in self.days_frame.winfo_children():
            if isinstance(btn, tk.Button):
                try:
                    if btn.cget("text") == self.current_day:
                        btn.config(bg=self.themes[self.current_theme]["ACTIVE_COLOR"])
                    else:
                        btn.config(bg=self.themes[self.current_theme]["INACTIVE_COLOR"])
                except tk.TclError:
                    continue

    
    def setup_ui(self):
        # ۱. فریم دکمه‌های روزهای هفته (در سمت راست)
        self.days_frame = tk.Frame(self.root, bg=self.themes[self.current_theme]["BG_COLOR"])
        self.days_frame.pack(side="right", fill="y", padx=10, pady=20)

        for day in self.tasks_db.keys():
            btn = tk.Button(self.days_frame, text=day, 
                            command=lambda d=day: self.switch_day(d), 
                            bg="#444", fg="white", width=12)
            btn.pack(pady=2)
        
        self.theme_btn = tk.Button(self.days_frame, text="تغییر تم", 
                                   command=self.toggle_theme_menu,
                                   bg="#555", fg="white", width=12)
        self.theme_btn.pack(pady=10, side="bottom")

        self.update_button_colors()

        # ۲. فریم اصلی (در سمت چپ) برای محتوای تسک‌ها و ورودی
        self.main_frame = tk.Frame(self.root, bg=self.themes[self.current_theme]["BG_COLOR"])
        self.main_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        # ۳. بخش بالایی (شامل عنوان روز و دایره پیشرفت) - این جا ساخته می‌شود تا همیشه وجود داشته باشد
        self.top_task_frame = tk.Frame(self.main_frame, bg=self.themes[self.current_theme]["BG_COLOR"])
        self.top_task_frame.pack(fill="x", pady=(0, 10))

        self.day_title_label = tk.Label(
            self.top_task_frame, 
            text="", 
            font=("Arial", 14, "bold"),
            bg=self.themes[self.current_theme]["BG_COLOR"],
            fg=self.themes[self.current_theme]["FG_COLOR"]
        )
        self.day_title_label.pack(side="left")

        self.progress_canvas = tk.Canvas(
            self.top_task_frame, 
            width=60, 
            height=60, 
            highlightthickness=0,
            bg=self.themes[self.current_theme]["BG_COLOR"]
        )
        self.progress_canvas.pack(side="right")

        # ۴. فیلد ورودی تسک جدید
        self.entry = tk.Entry(self.main_frame, bg=self.themes[self.current_theme]["ENTRY_BG"], fg=self.themes[self.current_theme]["FG_COLOR"])
        self.entry.pack(fill="x", pady=(0, 20))
        self.entry.bind('<Return>', self.add_task)

        # ۵. فریم نگهدارنده لیست تسک‌ها
        self.tasks_frame = tk.Frame(self.main_frame, bg=self.themes[self.current_theme]["BG_COLOR"])
        self.tasks_frame.pack(fill="both", expand=True)

        # ۶. نمایش اولیه تسک‌ها و دایره پیشرفت
        self.show_tasks()

        
    
    def add_task(self,event=None):
        task_text = self.entry.get()
        if task_text:
        # تسک جدید به صورت دیکشنری با وضعیت اولیه False اضافه می‌شود
            new_task_item = {"text": task_text, "done": False}
            self.tasks_db[self.current_day].append(new_task_item) # اضافه کردن به لیست روز فعلی
            self.entry.delete(0, tk.END)
            self.save_tasks()
            self.show_tasks()
    
    def remove_task(self, task_item):
        # حذف از لیستِ آن روز
        self.tasks_db[self.current_day].remove(task_item)
        # فراخوانی مجدد برای رفرش کردن نمایش
        self.save_tasks()
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
        self.save_tasks()
    
    def show_tasks(self):
        # پاک کردن نمایش قبلی (فقط تسک‌ها)
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()
        
        theme = self.themes[self.current_theme]
        current_tasks = self.tasks_db.get(self.current_day, []) 
        
        # ۱. به‌روزرسانی متن عنوان روز در بالای لیست
        if hasattr(self, 'day_title_label'):
            self.day_title_label.config(text=f"برنامه‌های {self.current_day}")

        for task_item in current_tasks:
            card = tk.Frame(self.tasks_frame, bg=theme["card_color"], bd=0)
            card.pack(fill="x", pady=5, padx=5)
        
            var = tk.BooleanVar(value=task_item["done"]) 
            
            # تعیین رنگ متن بر اساس تم و وضعیت انجام شدن
            if task_item["done"]:
                current_color = "#888888"
            else:
                current_color = theme["FG_COLOR"] 
                
            current_font = self.strike_font if task_item["done"] else self.normal_font 
            
            task_check = tk.Checkbutton(
                card, 
                text=task_item["text"],
                variable=var,
                bg=theme["card_color"], 
                activebackground=theme["card_color"],
                selectcolor=theme["ENTRY_BG"],
                highlightthickness=0,
                relief="flat",
                fg=current_color,
                font=current_font
            )           
            
            task_check.config(command=lambda item=task_item, v=var, w=task_check: self.toggle_task(item, v, w))
            task_check.pack(side="left", padx=10)

            # دکمه حذف
            delete_btn = tk.Button(
                card, 
                text="×", 
                bg=theme["card_color"], 
                fg="red", 
                activebackground=theme["card_color"],
                bd=0, 
                command=lambda item=task_item: self.remove_task(item)
            )
            delete_btn.pack(side="right", padx=10)

        # ۲. محاسبه و رسم دایره پیشرفت بیرون از حلقه (تا همیشه و حتی برای لیست‌های خالی هم اجرا شود)
        total_tasks = len(current_tasks)
        completed_tasks = sum(1 for task in current_tasks if task["done"])
        self.draw_progress_circle(completed_tasks, total_tasks)


    
    
if __name__ == "__main__": 
    root = tk.Tk()
    app = taskmaneagerApp(root)
    root.mainloop()
