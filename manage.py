import tkinter as tk
import sqlite3
from tkinter import messagebox

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Администрирование базы данных")
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Создание элементов интерфейса
        self.label1 = tk.Label(self, text="Товар:")
        self.label1.grid(row=0, column=0)
        self.entry1 = tk.Entry(self)
        self.entry1.grid(row=0, column=1)
        self.label2 = tk.Label(self, text="Номер телефона:")
        self.label2.grid(row=1, column=0)
        self.entry2 = tk.Entry(self)
        self.entry2.grid(row=1, column=1)
        self.submit_button = tk.Button(self, text="Добавить заказ", command=self.add_order)
        self.submit_button.grid(row=2, column=0, columnspan=2)
        self.label3 = tk.Label(self, text="Список заказов:")
        self.label3.grid(row=3, column=0, columnspan=2)
        self.order_listbox = tk.Listbox(self, width=50)
        self.order_listbox.grid(row=4, column=0, columnspan=2)
        self.delete_button = tk.Button(self, text="Удалить заказ", command=self.delete_order)
        self.delete_button.grid(row=5, column=0, columnspan=2)
        self.deliver_button = tk.Button(self, text="Отметить как доставленный", command=self.deliver_order)
        self.deliver_button.grid(row=6, column=0, columnspan=2)
        self.refresh_button = tk.Button(self, text="Обновить список заказов", command=self.refresh_order_list)
        self.refresh_button.grid(row=7, column=0, columnspan=2)

    def add_order(self):
        # Добавление нового заказа в базу данных
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO orders (user_id, status, item) VALUES (?, ?, ?)", (0, "Новый заказ", self.entry1.get()))
        order_id = cursor.lastrowid
        conn.commit()
        conn.close()
        # Обновление списка заказов
        self.refresh_order_list()
        # Отправка уведомления о новом заказе
        messagebox.showinfo("Новый заказ", f"Поступил новый заказ №{order_id}\n\nТовар: {self.entry1.get()}\nНомер телефона: {self.entry2.get()}")
        # Очистка полей ввода
        self.entry1.delete(0, 'end')
        self.entry2.delete(0, 'end')

    def delete_order(self):
        # Получение выбранного заказа из списка
        selected_order = self.order_listbox.get(self.order_listbox.curselection())
        order_id = selected_order.split(" ")[0]

        # Удаление заказа из базы данных
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
        conn.commit()
        conn.close()
        # Обновление списка заказов
        self.refresh_order_list()
        # Отправка уведомления об удалении заказа
        messagebox.showinfo("Заказ удален", f"Заказ №{order_id} удален")

    def deliver_order(self):
        # Получение выбранного заказа из списка
        selected_order = self.order_listbox.get(self.order_listbox.curselection())
        order_id = selected_order.split(" ")[0]
        # Изменение статуса заказа на "Доставлен"
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE orders SET status = ? WHERE id = ?", ("Доставлен", order_id))
        conn.commit()
        conn.close()
        # Обновление списка заказов
        self.refresh_order_list()
        # Отправка уведомления об изменении статуса заказа
        messagebox.showinfo("Статус заказа изменен", f"Статус заказа №{order_id} изменен на 'Доставлен'")

    def refresh_order_list(self):
        # Очистка списка заказов
        self.order_listbox.delete(0, 'end')
        # Получение списка заказов из базы данных
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()
        conn.close()
        # Заполнение списка заказов
        for order in orders:
            self.order_listbox.insert('end', f"Заказ №{order[0]}: {order[2]} ({order[1]})")

root = tk.Tk()
app = Application(master=root)
app.mainloop()

       
