import tkinter as tk
import random
import string

# --- تعریف مجموعه‌های کاراکتر و داده‌های ثابت ---
# این بخش بدون تغییر باقی مانده است
LOWERCASE_CHARS = string.ascii_lowercase
UPPERCASE_CHARS = string.ascii_uppercase
DIGITS = string.digits
SYMBOLS = "!@#$%^&*"
ANIMAL_NAMES = [
    "gorbe", "sag", "shir", "babr", "palang", "gav", "oos", "fil",
    "zarafe", "boz", "meymoon", "khers", "roobah", "gorg"
]

# --- تعریف توابع ---

def toggle_personal_fields():
    """فیلدهای نام و سن را بر اساس انتخاب کاربر فعال یا غیرفعال می‌کند."""
    if personalize_var.get() == True:
        name_entry.config(state="normal")
        age_entry.config(state="normal")
    else:
        name_entry.config(state="disabled")
        age_entry.config(state="disabled")
        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)

def generate_password():
    """تابع اصلی برای تولید پسورد بر اساس تنظیمات کاربر."""
    strength = strength_var.get()
    password_chars = []
    all_chars = ""

    # 1. تعیین طول و نوع کاراکترها بر اساس سطح قدرت
    # مقادیر "ضعیف"، "متوسط" و ... با معادل انگلیسی جایگزین شده‌اند
    if strength == "Weak":
        length = 8
        all_chars = LOWERCASE_CHARS + DIGITS
        password_chars.append(random.choice(LOWERCASE_CHARS))
        password_chars.append(random.choice(DIGITS))
    elif strength == "Medium":
        length = 12
        all_chars = LOWERCASE_CHARS + UPPERCASE_CHARS + DIGITS
        password_chars.append(random.choice(LOWERCASE_CHARS))
        password_chars.append(random.choice(UPPERCASE_CHARS))
        password_chars.append(random.choice(DIGITS))
    elif strength == "Strong":
        length = 16
        all_chars = LOWERCASE_CHARS + UPPERCASE_CHARS + DIGITS + SYMBOLS
        password_chars.append(random.choice(LOWERCASE_CHARS))
        password_chars.append(random.choice(UPPERCASE_CHARS))
        password_chars.append(random.choice(DIGITS))
        password_chars.append(random.choice(SYMBOLS))
    else: # Very Strong
        length = 20
        all_chars = LOWERCASE_CHARS + UPPERCASE_CHARS + DIGITS + SYMBOLS
        password_chars.append(random.choice(LOWERCASE_CHARS))
        password_chars.append(random.choice(UPPERCASE_CHARS))
        password_chars.append(random.choice(DIGITS))
        password_chars.append(random.choice(SYMBOLS))
        animal = random.choice(ANIMAL_NAMES)
        password_chars.extend(list(animal.capitalize()))

    # 2. بررسی بخش شخصی‌سازی
    if personalize_var.get() == True:
        name = name_entry.get().strip()
        age = age_entry.get().strip()
        if name:
            password_chars.extend(list(name[:3])) # اضافه کردن 3 حرف اول نام
        if age and age.isdigit():
            password_chars.append(age)
    
    # 3. پر کردن بقیه پسورد با کاراکترهای تصادفی
    remaining_length = length - len(password_chars)
    if remaining_length > 0:
        for _ in range(remaining_length):
            password_chars.append(random.choice(all_chars))

    # 4. در هم ریختن و ساختن پسورد نهایی
    random.shuffle(password_chars)
    final_password = "".join(password_chars[:length]) # اطمینان از طول صحیح پسورد
    
    # 5. نمایش نتیجه
    password_var.set(final_password)
    status_label.config(text=f"Password with '{strength}' level generated!")

def copy_to_clipboard():
    """پسورد نمایش داده شده را در کلیپ‌بورد سیستم کپی می‌کند."""
    password = password_var.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        status_label.config(text="Password copied successfully!")
    else:
        status_label.config(text="First, generate a password!")

# --- ساخت پنجره و اجزای گرافیکی (GUI) ---

# ساخت پنجره اصلی
root = tk.Tk()
root.title("Simple Password Generator")
root.geometry("380x400")
root.config(padx=10, pady=10) # ایجاد کمی فاصله از لبه‌های پنجره

# متغیرهای کنترلی برای Tkinter
strength_var = tk.StringVar(value="Medium") # مقدار پیش‌فرض انگلیسی شد
personalize_var = tk.BooleanVar()
password_var = tk.StringVar()

# --- چیدن اجزا در پنجره (متن‌ها به انگلیسی تغییر کرده‌اند) ---

# 1. بخش انتخاب سطح قدرت
tk.Label(root, text="Password Strength:", font=("Tahoma", 11)).pack(pady=(0, 5))
tk.Radiobutton(root, text="Weak", variable=strength_var, value="Weak").pack(anchor="w")
tk.Radiobutton(root, text="Medium", variable=strength_var, value="Medium").pack(anchor="w")
tk.Radiobutton(root, text="Strong", variable=strength_var, value="Strong").pack(anchor="w")
tk.Radiobutton(root, text="Very Strong", variable=strength_var, value="Very Strong").pack(anchor="w")

# 2. بخش شخصی‌سازی
tk.Checkbutton(root, text="Personalize with name and age", variable=personalize_var, command=toggle_personal_fields).pack(pady=(10, 0))
tk.Label(root, text="Name:").pack()
name_entry = tk.Entry(root, state="disabled")
name_entry.pack(fill="x")
tk.Label(root, text="Age:").pack()
age_entry = tk.Entry(root, state="disabled")
age_entry.pack(fill="x")

# 3. دکمه تولید پسورد
generate_button = tk.Button(root, text="Generate Password", font=("Tahoma", 12, "bold"), command=generate_password)
generate_button.pack(pady=15, ipady=5) # ipady برای ارتفاع بیشتر دکمه

# 4. بخش نمایش نتیجه
tk.Label(root, text="Generated Password:", font=("Tahoma", 11)).pack()
result_entry = tk.Entry(root, textvariable=password_var, state="readonly", justify="center", font=("Courier", 12))
result_entry.pack(fill="x", ipady=5)
copy_button = tk.Button(root, text="Copy", command=copy_to_clipboard)
copy_button.pack(pady=5)

# 5. لیبل وضعیت
status_label = tk.Label(root, text="Ready to generate a password...", fg="blue")
status_label.pack()

# --- شروع حلقه اصلی برنامه ---
# این خط برنامه را در حال اجرا نگه می‌دارد تا کاربر بتواند با آن تعامل کند.
root.mainloop()