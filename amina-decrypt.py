import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
import base64
import hashlib
from PIL import Image, ImageTk
import requests
from io import BytesIO

# تحميل الأيقونة من الإنترنت
def download_icon(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return ImageTk.PhotoImage(img)

# إنشاء مفتاح التشفير باستخدام كلمة المرور
def generate_key(password):
    password = password.encode()
    key = hashlib.sha256(password).digest()  # تحويل كلمة المرور إلى 32 بايت
    return base64.urlsafe_b64encode(key)

# تشفير الرسالة
def encrypt_message():
    password = entry_password.get()
    if not password:
        messagebox.showerror("Error", "Please enter a password")
        return

    key = generate_key(password)
    cipher_suite = Fernet(key)

    message = entry_message.get().encode()
    encrypted_message = cipher_suite.encrypt(message).decode()

    entry_encrypted.delete(0, tk.END)
    entry_encrypted.insert(0, encrypted_message)

# فك تشفير الرسالة
def decrypt_message():
    password = entry_password.get()
    if not password:
        messagebox.showerror("Error", "Please enter a password")
        return

    key = generate_key(password)
    cipher_suite = Fernet(key)

    encrypted_message = entry_encrypted.get().encode()
    try:
        decrypted_message = cipher_suite.decrypt(encrypted_message).decode()
        entry_decrypted.delete(0, tk.END)
        entry_decrypted.insert(0, decrypted_message)
    except:
        messagebox.showerror("Error", "Invalid encryption key or message")

# إعداد الواجهة
root = tk.Tk()
root.title("SecureWave مُفتاح الأمان")
root.geometry("850x700")
root.resizable(False, False)
root.configure(bg="#26355D")

# تحميل وتعيين أيقونة
icon_url = "https://cdn-icons-png.flaticon.com/512/61/61457.png"  # استبدل هذا بالرابط الصحيح للأيقونة
icon_image = download_icon(icon_url)
root.iconphoto(False, icon_image)

# تقسيم الواجهة إلى عمودين
left_frame = tk.Frame(root, width=350, height=700, bg="#26355D")
left_frame.pack(side="left", fill="both")

right_frame = tk.Frame(root, width=600, height=700, bg="#141E46")
right_frame.pack(side="right", fill="both")

# إضافة الصورة في الجزء الأيسر
image_path = "capture_240915_002908.png"  # ضع مسار الصورة الصحيح هنا
image = Image.open(image_path)
image = image.resize((350, 700), Image.Resampling.LANCZOS)
photo = ImageTk.PhotoImage(image)

label_image = tk.Label(left_frame, image=photo, bg="#26355D")
label_image.place(x=0, y=0, relwidth=1, relheight=1)  # اجعل الصورة تملأ الجزء الأيسر

# إضافة الصورة في الجزء الأيمن
right_image_path = "photo_2024-09-14_05-21-15.png"  # ضع مسار الصورة الصحيح هنا
right_image = Image.open(right_image_path)
right_image = right_image.resize((600, 700), Image.Resampling.LANCZOS)  # حجم الجزء الأيمن بالكامل
right_photo = ImageTk.PhotoImage(right_image)

label_right_image = tk.Label(right_frame, image=right_photo, bg="#141E46")
label_right_image.place(x=0, y=0, relwidth=1, relheight=1)  # تملأ الصورة الجزء الأيمن

# إنشاء بوكس لتجميع الحقول المتعلقة بالتشفير مع شفافية وحواف منحنية
encryption_box = tk.Frame(right_frame, background="#1A2130", bd=2, relief="ridge", padx=10, pady=10)
encryption_box.place(relx=0.5, rely=0.5, anchor="center", width=400, height=530)  # تعديل الموقع إلى المركز

# إضافة الحقول والأزرار في البوكس المتعلق بالتشفير
label_welcome = tk.Label(encryption_box, text=".شفّر اليوم وأمّن الغد - أجعل محادثتك خاصة",
                         font=("Engravers MT", 15,), fg="#FFB0B0", bg="#1A2130", highlightthickness=0)
label_welcome.pack(pady=5)

# حقل الرسالة
label_message = tk.Label(encryption_box, text="Enter Text:", font=("Microsoft Sans Serif", 10), fg="white", bg="#1A2130")
label_message.pack(pady=3)
entry_message = tk.Entry(encryption_box, width=28, font=("Arial", 10))
entry_message.pack(pady=3, ipadx=5, ipady=3)
# حقل كلمة المرور
label_password = tk.Label(encryption_box, text="Enter Password:", font=("Microsoft Sans Serif", 10), fg="white", bg="#1A2130")
label_password.pack(pady=3)
entry_password = tk.Entry(encryption_box, show="*", width=28, font=("Arial", 10))
entry_password.pack(pady=3, ipadx=5, ipady=3)
# حقل النص المشفر
label_encrypted = tk.Label(encryption_box, text="Encrypted Message:", font=("Microsoft Sans Serif", 10), fg="white", bg="#1A2130")
label_encrypted.pack(pady=3)
entry_encrypted = tk.Entry(encryption_box, width=28, font=("Arial", 10))
entry_encrypted.pack(pady=3, ipadx=5, ipady=3)
# زر التشفير
btn_encrypt = tk.Button(encryption_box, text="Encryption", font=("Microsoft Sans Serif", 10, "bold"), command=encrypt_message, bg="#384B70", fg="white")
btn_encrypt.pack(pady=7, ipadx=5, ipady=5)

# العنوان الخاص بالمستلم
label_receiver = tk.Label(encryption_box, text="Receiver Side", font=("Engravers MT", 12, "bold"), fg="#FFB1B1", bg="#1A2130")
label_receiver.pack(pady=5)

# حقل النص بعد فك التشفير
label_decrypted = tk.Label(encryption_box, text="Decrypted Message:", font=("Microsoft Sans Serif", 10), fg="white", bg="#1A2130")
label_decrypted.pack(pady=3)
entry_decrypted = tk.Entry(encryption_box, width=28, font=("Arial", 10))
entry_decrypted.pack(pady=3, ipadx=5, ipady=3)

# زر فك التشفير
btn_decrypt = tk.Button(encryption_box, text="Decryption", font=("Microsoft Sans Serif", 10, "bold"), command=decrypt_message, bg="#384B70", fg="white")
btn_decrypt.pack(pady=7, ipadx=5, ipady=5)

# زر الخروج
btn_exit = tk.Button(encryption_box, text="Exit", font=("Microsoft Sans Serif", 10, "bold"), command=root.quit, bg="#c499f3", fg="#1A2130")
btn_exit.pack(pady=10, ipadx=15, ipady=2)

# تنفيذ التطبيق
root.mainloop()
