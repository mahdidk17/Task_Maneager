import tkinter as tk
from tkinter import font
import json
import os

class taskmaneagerApp:
    def __init__(self, root):
        self.root =root
        self.root.title("task_maneager")
        self.root.geometry("600x400")
        
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        FILE_PATH = os.path.join(BASE_DIR, "tasks.json")
        
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
                "BG_COLOR": "#C73C3C",          # کرم بسیار ملایم و روشن برای پس‌زمینه اصلی
                "FG_COLOR": "#ffffff",          # خاکستری-بنفش ملایم و خوانا برای متن‌ها
                "ENTRY_BG": "#ff8989",          # پس‌زمینه ملایم برای کادرهای ورودی
                "card_color": "#b14f4f",        # رنگ کارت‌های تسک (کرم/هلویی ملایم)
                "ACTIVE_COLOR": "#be0000",      # آبی پاستیلی روشن برای دکمه/روز فعال
                "INACTIVE_COLOR": "#ff6e6e",    # هلویی پاستیلی برای دکمه‌های غیرفعال
                "BTN_FG": "#000000"             # رنگ متن روی دکمه‌ها
            },
            "purple": {
                "BG_COLOR": "#1e1b2e",          # بنفش بسیار تیره و مدرن برای پس‌زمینه اصلی
                "FG_COLOR": "#f3e8ff",          # بنفش خیلی روشن و گچی برای متن‌ها
                "ENTRY_BG": "#2d2640",          # بنفش تیره ملایم برای کادرهای ورودی
                "card_color": "#2a223f",        # رنگ کارت‌های تسک (بنفش شیک و دارک)
                "ACTIVE_COLOR": "#7c3aed",      # بنفش سلطنتی و پررنگ برای دکمه/روز فعال
                "INACTIVE_COLOR": "#3b2a59",    # بنفش تیره برای دکمه‌های غیرفعال
                "BTN_FG": "#ffffff"             # رنگ متن سفید برای کنتراست عالی
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
        self.load_tasks()
        self.current_day = "شنبه"
        self.setup_ui()

    def switch_day(self,day):
        self.current_day
        self.current_day = day
        self.show_tasks()
        self.update_button_colors()
        
    def toggle_theme_menu(self):
        # بررسی می‌کنیم آیا فریم منوی تم قبلاً ساخته شده و باز است یا نه
        if hasattr(self, 'theme_menu_frame') and self.theme_menu_frame.winfo_exists():
            # اگر باز بود، آن را حذف (بسته) می‌کنیم
            self.theme_menu_frame.destroy()
        else:
            # گرفتن رنگ تم فعلی
            theme = self.themes[self.current_theme]
            
            # پیدا کردن فریمِ والدِ دکمه تم (همان جایی که دکمه اصلی قرار دارد)
            parent_frame = self.theme_btn.master 
            
            # ایجاد فریم منو درون همان والد
            self.theme_menu_frame = tk.Frame(parent_frame, bg=theme["BG_COLOR"])
            
            # قرار دادن فریم منو دقیقا در کنار دکمه اصلی (مثلاً سمت چپ یا راستِ دکمه اصلی)
            # نکته: بسته به اینکه دکمه اصلی چطور pack شده، این فریم کنارش می‌نشیند
            self.theme_menu_frame.pack(side=tk.LEFT, padx=5)
            
            # به ازای هر تم، یک دکمه می‌سازیم
                        # به ازای هر تم، یک دکمه می‌سازیم
            for theme_key in self.themes.keys():
                btn = tk.Button(
                    self.theme_menu_frame,
                    text=theme_key.capitalize(),
                    command=lambda t=theme_key: self.select_theme(t),
                    # اینجا داریم رنگ دکمه را دقیقاً از دیکشنری همان تم می‌گیریم:
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
        self.days_frame = tk.Frame(self.root, bg=self.themes[self.current_theme]["BG_COLOR"])
        self.days_frame.pack(side="right", fill="y", padx=10, pady=20)

        for day in self.tasks_db.keys():
            btn = tk.Button(self.days_frame, text=day, 
                            command=lambda d=day: self.switch_day(d), # باید self باشد
                            bg="#444", fg="white", width=12)
            btn.pack(pady=2)
        
        self.theme_btn = tk.Button(self.days_frame, text="تغییر تم 🌗", 
                                   command=self.toggle_theme_menu,
                                   bg="#555", fg="white", width=12)
        self.theme_btn.pack(pady=10, side="bottom") # پایین فریم روزها قرار می‌گیرد

        
        self.update_button_colors() # باید self باشد

        # ۲. بخش اصلی
        self.main_frame = tk.Frame(self.root, bg=self.themes[self.current_theme]["BG_COLOR"])
        self.main_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        # ۳. ورودی
        self.entry = tk.Entry(self.main_frame, bg=self.themes[self.current_theme]["ENTRY_BG"], fg=self.themes[self.current_theme]["FG_COLOR"])
        self.entry.pack(fill="x", pady=(0, 20))
        self.entry.bind('<Return>', self.add_task) # باید self باشد

        # ۴. نگهدارنده تسک‌ها
        self.tasks_frame = tk.Frame(self.main_frame, bg=self.themes[self.current_theme]["BG_COLOR"])
        self.tasks_frame.pack(fill="both", expand=True)

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
        
        for task_item in current_tasks:
            card = tk.Frame(self.tasks_frame, bg=theme["card_color"], bd=0)
            card.pack(fill="x", pady=5, padx=5)
        
            var = tk.BooleanVar(value=task_item["done"]) 
            
            # تعیین رنگ متن بر اساس تم و وضعیت انجام شدن
            if task_item["done"]:
                current_color = "#888888" # خاکستری ملایم برای تسک‌های انجام شده
            else:
                current_color = theme["FG_COLOR"] # رنگ متن اصلی از تم (سفید در دارک، مشکی در لایت)
                
            current_font = self.strike_font if task_item["done"] else self.normal_font 
            
            task_check = tk.Checkbutton(
                card, 
                text=task_item["text"],
                variable=var,
                bg=theme["card_color"], 
                activebackground=theme["card_color"],
                selectcolor=theme["ENTRY_BG"], # رنگ پس‌زمینه باکس کوچک تیک
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

    
    
if __name__ == "__main__": 
    root = tk.Tk()
    app = taskmaneagerApp(root)
    root.mainloop()
