import tkinter as tk
from tkinter import ttk, messagebox, StringVar
import sqlite3
from datetime import datetime
from tkcalendar import DateEntry

def get_race_names():
    conn = sqlite3.connect('galactic_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT race_name FROM galactic_race where is_deleted=0')
    race_names = [row[0] for row in cursor.fetchall()]

    conn.close()
    return race_names

class GalacticApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Galactic App")
        self.create_widgets()

    def create_widgets(self):
        # Заголовок
        title_label = ttk.Label(self.root, text="Galactic App", font=("Helvetica", 16))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Выпадающий список для выбора справочника
        dictionary_label = ttk.Label(self.root, text="Выберите справочник:")
        dictionary_label.grid(row=1, column=0, columnspan=2, pady=10)

        self.dictionary_var = tk.StringVar()
        dictionary_combobox = ttk.Combobox(self.root, textvariable=self.dictionary_var, values=["galactic_race", "technology"])
        dictionary_combobox.grid(row=2, column=0, columnspan=2, pady=10)

        # Кнопка для просмотра данных
        view_button = ttk.Button(self.root, text="Просмотреть данные", command=self.view_data)
        view_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Отображение данных
        self.data_tree = ttk.Treeview(self.root, columns=(1, 2, 3, 4, 5, 6, 7), show="headings", height=10)
        self.data_tree.grid(row=4, column=0, columnspan=2, padx=10)

        # Прокрутка для Treeview
        data_scroll = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.data_tree.yview)
        data_scroll.grid(row=4, column=2, sticky=(tk.N, tk.S))
        self.data_tree.configure(yscrollcommand=data_scroll.set)

        # Кнопка для редактирования данных
        edit_button = ttk.Button(self.root, text="Редактировать данные", command=self.edit_data)
        edit_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Кнопка для добавления данных
        add_button = ttk.Button(self.root, text="Добавить данные", command=self.add_data)
        add_button.grid(row=6, column=0, columnspan=2, pady=10)

        # Кнопка для удаления данных
        delete_button = ttk.Button(self.root, text="Удалить данные", command=self.delete_data)
        delete_button.grid(row=7, column=0, columnspan=2, pady=10)
        
        name_label = ttk.Label(self.root, text="Жуковская Дарья Вячеславовна")
        name_label.grid(row=8, column=0, columnspan=2, pady=10)
        
        kurs_label = ttk.Label(self.root, text="4 курс, 4 группа, 2023 год")
        kurs_label.grid(row=9, column=0, columnspan=2, pady=10)
 
    def view_data(self):
        selected_dictionary = self.dictionary_var.get()

        if not selected_dictionary:
            return

        conn = sqlite3.connect('galactic_database.db')
        cursor = conn.cursor()

        # Выборка данных без удаленных записей
        cursor.execute(f'SELECT * FROM "{selected_dictionary}" WHERE is_deleted=0')
        if selected_dictionary == "galactic_race":
            columns = [(1, "Имя"), (2, "Дата встречи"), (3, "Домашняя планета"), (4, "Индекс развития"), (5, ""), (6, "")]
            for col, col_name in columns:
              self.data_tree.heading(col, text=col_name, command=lambda c=col: self.sort_column(c, "galactic_race"))
            cursor.execute(f'SELECT race_name, first_encounter_date, home_planet, development_index FROM "{selected_dictionary}" WHERE is_deleted=0')
            

        if selected_dictionary == "technology":
            columns = [(1, "Название технологии"), (2, "Дата изобретения"), (3, "Уровень сложности"), (4, "Применение"), (5, "Название расы" ), (6, "Энергопотребление")]
            for col, col_name in columns:
              self.data_tree.heading(col, text=col_name, command=lambda c=col: self.sort_column(c, "technology"))
            cursor.execute(f'SELECT technology_name, invention_date, complexity_level, application, race_name, power_consumption FROM "{selected_dictionary}" WHERE is_deleted=0')
            
        data = cursor.fetchall()

        conn.close()

        # Очистка данных в Treeview перед отображением новых данных
        for i in self.data_tree.get_children():
            self.data_tree.delete(i)

        # Вставка данных в Treeview
        for row in data:
            self.data_tree.insert("", "end", values=row)
            
    def sort_column(self, col, selected_dictionary):
        data = [(self.data_tree.set(item, col), item) for item in self.data_tree.get_children('')]

        # Выбор функции сравнения в зависимости от типа данных в колонке
        if (col in (1, 2, 3) and selected_dictionary == "galactic_race") or col in (1, 2, 4, 5) and selected_dictionary == "technology":  # Колонки с датой и строкой
            data.sort(key=lambda x: (self.get_type(x[0]), x[0]))
        elif col in (5,6) and selected_dictionary == "galactic_race":
            nothing = 0
        else:
            data.sort(key=lambda x: float(x[0]) if x[0] != 'NULL' else float('inf'))  # Предполагаем, что остальные колонки содержат числа

        for index, (val, item) in enumerate(data):
            self.data_tree.move(item, '', index)

    def get_type(self, value):
        if value == 'NULL':
          return 3  # NULL
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return 0  # Дата
        except ValueError:
            try:
                float(value)
                return 1  # Число
            except ValueError:
                return 2  # Строка
            
    def add_data(self):
        selected_dictionary = self.dictionary_var.get()

        # Создаем окно добавления данных
        add_window = tk.Toplevel(self.root)
        add_window.title("Добавить данные")
        if selected_dictionary == "galactic_race":
        # Создаем виджеты для ввода данных
          name_label = ttk.Label(add_window, text="Имя:")
          name_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
          name_entry = ttk.Entry(add_window)
          name_entry.grid(row=0, column=1, padx=10, pady=5)
          
          date_label = ttk.Label(add_window, text="Дата встречи:")
          date_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
          date_entry = DateEntry(add_window, date_pattern="yyyy-mm-dd")
          date_entry.grid(row=1, column=1, padx=10, pady=5)
          null_var = StringVar()
          null_checkbox = ttk.Checkbutton(add_window, text="NULL", variable=null_var, onvalue="1", offvalue="0")
          null_checkbox.grid(row=1, column=2, padx=10, pady=5, sticky=tk.W)

          planet_label = ttk.Label(add_window, text="Домашняя планета:")
          planet_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
          planet_entry = ttk.Entry(add_window)
          planet_entry.grid(row=2, column=1, padx=10, pady=5)

          index_label = ttk.Label(add_window, text="Индекс развития:")
          index_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
          index_entry = ttk.Entry(add_window)
          index_entry.grid(row=3, column=1, padx=10, pady=5)
          
        if selected_dictionary == "technology":
        # Создаем виджеты для ввода данных
          name_label = ttk.Label(add_window, text="Название технологии:")
          name_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
          name_entry = ttk.Entry(add_window)
          name_entry.grid(row=0, column=1, padx=10, pady=5)

          date_label = ttk.Label(add_window, text="Дата изобретения:")
          date_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
          date_entry = DateEntry(add_window, date_pattern="yyyy-mm-dd")
          date_entry.grid(row=1, column=1, padx=10, pady=5)
          null_var = StringVar()
          null_checkbox = ttk.Checkbutton(add_window, text="NULL", variable=null_var, onvalue="1", offvalue="0")
          null_checkbox.grid(row=1, column=2, padx=10, pady=5, sticky=tk.W)

          level_label = ttk.Label(add_window, text="Уровень сложности:")
          level_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
          level_entry = ttk.Entry(add_window)
          level_entry.grid(row=2, column=1, padx=10, pady=5)

          application_label = ttk.Label(add_window, text="Применение:")
          application_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
          application_entry = ttk.Entry(add_window)
          application_entry.grid(row=3, column=1, padx=10, pady=5)
          
          race_label = ttk.Label(add_window, text="Название расы:")
          race_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
          race_names = get_race_names()
          race_combobox = ttk.Combobox(add_window)
          race_combobox['values'] = race_names
          race_combobox.grid(row=4, column=1, padx=10, pady=5)
          
          power_label = ttk.Label(add_window, text="Энергопотребление:")
          power_label.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
          power_entry = ttk.Entry(add_window)
          power_entry.grid(row=5, column=1, padx=10, pady=5)
          

        # Функция для добавления новой записи
        def add_new_entry():
           if selected_dictionary == "galactic_race":
            # Извлечение данных из виджетов и добавление новой записи в базу данных
            new_name = name_entry.get()
            new_date = None if null_var.get() else date_entry.get()
            new_planet = planet_entry.get()
            new_index = index_entry.get()
            
            # Проверка наличия данных
            if not new_name or not new_planet:
                messagebox.showwarning("Ошибка", "Заполните все поля")
                return
            if new_index.lower() == 'null' or new_index.lower() == '' or new_index.lower() == ' ' or new_index.lower() == 'none' or new_index == null_var:
              new_index = null_var
            else:
              try:
                new_index = float(new_index)
              except ValueError:
                messagebox.showwarning("Ошибка", "Неверный формат индекса развития(должно быть число)")
                return
              if float(new_index) > 10 or float(new_index) < 1:
                messagebox.showwarning("Ошибка", "Неверный формат индекса развития(Должно принадлежать интервалу от 1 до 10)")
                return
            
            # Добавление данных в базу данных
            conn = sqlite3.connect('galactic_database.db')
            cursor = conn.cursor()
            
            if new_date  == None:
              formatted_date = "NULL"
            else:
             try:
                formatted_date = datetime.strptime(new_date, "%Y-%m-%d").date()
             except ValueError:
                messagebox.showwarning("Ошибка", "Неверный формат даты")
                conn.close()

            # Добавление новой записи в базу данных
            cursor.execute(f'''
                SELECT * FROM "{selected_dictionary}" 
                WHERE race_name=? AND is_deleted=1
                ''', (new_name,))
            existing_deleted_entry = cursor.fetchone()

            if existing_deleted_entry:
              cursor.execute(f'''
                UPDATE "{selected_dictionary}" 
                SET first_encounter_date=?, home_planet=?, development_index=?, is_deleted=0
                WHERE race_id=?
                ''', (formatted_date, new_planet, new_index, existing_deleted_entry[0]))
            else:
              cursor.execute(f'''
               INSERT INTO "{selected_dictionary}" (race_name, first_encounter_date, home_planet, development_index, is_deleted)
               VALUES (?, ?, ?, ?, 0)
               ''', (new_name, formatted_date, new_planet, new_index))

            conn.commit()
            conn.close()

            # Обновление данных в Treeview
            self.view_data()

            add_window.destroy()
            

           if selected_dictionary == "technology":
            # Извлечение данных из виджетов и добавление новой записи в базу данных
            new_name = name_entry.get()
            new_date = None if null_var.get() else date_entry.get()
            new_level = level_entry.get()
            new_application = application_entry.get()
            new_race = race_combobox.get()
            new_power = power_entry.get()            

            # Проверка наличия данных
            if not new_name or not new_level or not new_application or not new_race:
                messagebox.showwarning("Ошибка", "Заполните все поля")
                return
            
            if new_power.lower() == 'null' or new_power.lower() == '' or new_power.lower() == ' ' or new_power.lower() == 'none':
              new_power = "NULL"
            else:
              try:
                new_power = float(new_power)
              except ValueError:
                messagebox.showwarning("Ошибка", "Неверный формат энергопотребления(должно быть число)")
                return
         
            try:
                new_level = int(new_level)
            except ValueError:
                messagebox.showwarning("Ошибка", "Неверный формат уровня развития(должно быть число)")
                return  
            
            if int(new_level) > 10 or int(new_level) < 1:
                messagebox.showwarning("Ошибка", "Неверный формат уровня сложности(Должно принадлежать интервалу от 1 до 10)")
                return
            # Добавление данных в базу данных
            conn = sqlite3.connect('galactic_database.db')
            cursor = conn.cursor()

            # Форматируем дату в соответствии с форматом в базе данных
            if new_date  == None:
              formatted_date = "NULL"
            else:
             try:
                formatted_date = datetime.strptime(new_date, "%Y-%m-%d").date()
             except ValueError:
                messagebox.showwarning("Ошибка", "Неверный формат даты")
                conn.close()

            # Добавление новой записи в базу данных

            cursor.execute(f'''
                SELECT * FROM "{selected_dictionary}" 
                WHERE technology_name=? AND is_deleted=1
                ''', (new_name,))
            existing_deleted_entry = cursor.fetchone()

            if existing_deleted_entry:
              cursor.execute(f'''
                UPDATE "{selected_dictionary}" 
                SET invention_date=?, complexity_level=?, application=?, race_name = ?, power_consumption = ?, is_deleted=0
                WHERE technology_id=?
                ''', (formatted_date, new_level, new_application, new_race, new_power, existing_deleted_entry[0]))
            else:
              cursor.execute(f'''
                INSERT INTO "{selected_dictionary}" (technology_name, invention_date, complexity_level, application, race_name, power_consumption, is_deleted)
                VALUES (?, ?, ?, ?, ?, ?, 0)
                ''', (new_name, formatted_date, new_level, new_application, new_race, new_power))
              
            conn.commit()
            conn.close()

            # Обновление данных в Treeview
            self.view_data()

            add_window.destroy()
        add_button = ttk.Button(add_window, text="Добавить", command=add_new_entry)
        add_button.grid(row=7, column=0, columnspan=2, pady=10)
    
    def delete_data(self):
        selected_dictionary = self.dictionary_var.get()
        selected_item = self.data_tree.selection()

        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите запись для удаления")
            return

        confirm = messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить выбранную запись?")
        
        if confirm:

            conn = sqlite3.connect('galactic_database.db')
            cursor = conn.cursor()
            if selected_dictionary == "technology":
               cursor.execute(f'UPDATE "{selected_dictionary}" SET is_deleted=1 WHERE technology_name=?', (self.data_tree.item(selected_item, 'values')[0],))
            if selected_dictionary == "galactic_race":
               cursor.execute(f'UPDATE "{selected_dictionary}" SET is_deleted=1 WHERE race_name=?', (self.data_tree.item(selected_item, 'values')[0],))

            conn.commit()
            conn.close()

            # Обновление данных в Treeview
            self.view_data()

    def edit_data(self):
        selected_dictionary = self.dictionary_var.get()
        selected_item = self.data_tree.selection()

        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите запись для редактирования")
            return

        # Создаем окно редактирования
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Редактировать данные")

        # Получаем данные выбранной записи
        selected_data = self.data_tree.item(selected_item, 'values')

        if selected_dictionary == "galactic_race":
        # Создаем виджеты для ввода данных
          name_label = ttk.Label(edit_window, text="Имя:")
          name_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
          name_entry = ttk.Entry(edit_window)
          name_entry.grid(row=0, column=1, padx=10, pady=5)
          name_entry.insert(0, selected_data[0])

          date_label = ttk.Label(edit_window, text="Дата встречи (ДД.ММ.ГГГГ):")
          date_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
          date_entry = DateEntry(edit_window, date_pattern="yyyy-mm-dd")
          date_entry.grid(row=1, column=1, padx=10, pady=5)
          # date_entry.insert(0, selected_data[1])
          null_var = StringVar()
          null_checkbox = ttk.Checkbutton(edit_window, text="NULL", variable=null_var, onvalue="1", offvalue="0")
          null_checkbox.grid(row=1, column=2, padx=10, pady=5, sticky=tk.W)

          planet_label = ttk.Label(edit_window, text="Домашняя планета:")
          planet_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
          planet_entry = ttk.Entry(edit_window)
          planet_entry.grid(row=2, column=1, padx=10, pady=5)
          planet_entry.insert(0, selected_data[2])

          index_label = ttk.Label(edit_window, text="Индекс развития:")
          index_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
          index_entry = ttk.Entry(edit_window)
          index_entry.grid(row=3, column=1, padx=10, pady=5)
          index_entry.insert(0, selected_data[3])
          ##########################################################################################################
        if selected_dictionary == "technology":
          name_label = ttk.Label(edit_window, text="Название технологии::")
          name_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
          name_entry = ttk.Entry(edit_window)
          name_entry.grid(row=0, column=1, padx=10, pady=5)
          name_entry.insert(0, selected_data[0])

          date_label = ttk.Label(edit_window, text="Дата изобретения (ДД.ММ.ГГГГ):")
          date_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
          date_entry = DateEntry(edit_window, date_pattern="yyyy-mm-dd")
          date_entry.grid(row=1, column=1, padx=10, pady=5)
          null_var = StringVar()
          null_checkbox = ttk.Checkbutton(edit_window, text="NULL", variable=null_var, onvalue="1", offvalue="0")
          null_checkbox.grid(row=1, column=2, padx=10, pady=5, sticky=tk.W)      

          level_label = ttk.Label(edit_window, text="Уровень сложности:")
          level_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
          level_entry = ttk.Entry(edit_window)
          level_entry.grid(row=2, column=1, padx=10, pady=5)
          level_entry.insert(0, selected_data[2])

          application_label = ttk.Label(edit_window, text="Применение:")
          application_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
          application_entry = ttk.Entry(edit_window)
          application_entry.grid(row=3, column=1, padx=10, pady=5)
          application_entry.insert(0, selected_data[3])
          
          race_label = ttk.Label(edit_window, text="Название расы:")
          race_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
          race_names = get_race_names()
          race_combobox = ttk.Combobox(edit_window)
          race_combobox['values'] = race_names
          race_combobox.grid(row=4, column=1, padx=10, pady=5)
          race_combobox.insert(0, selected_data[4])

          power_label = ttk.Label(edit_window, text="Энергопотребление:")
          power_label.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
          power_entry = ttk.Entry(edit_window)
          power_entry.grid(row=5, column=1, padx=10, pady=5)
          power_entry.insert(0, selected_data[5])
          

        # Функция для сохранения изменений
        def save_changes():
           if selected_dictionary == "technology":
            # Извлечение данных из виджетов редактирования и обновление записи в базе данных
            new_name = name_entry.get()
            new_date = None if null_var.get() else date_entry.get()
            new_level = level_entry.get()
            new_application = application_entry.get()
            new_race = race_combobox.get()
            new_power = power_entry.get()

            # Проверка наличия данных
            if not new_name or not new_level or not new_application or not new_race:
                messagebox.showwarning("Ошибка", "Заполните поля")
                return
            if new_power.lower() == 'null' or new_power.lower() == '' or new_power.lower() == ' ' or new_power.lower() == 'none':
              new_power = "NULL"
            else:
              try:
                new_power = float(new_power)
              except ValueError:
                messagebox.showwarning("Ошибка", "Неверный формат энергопотребления(должно быть число)")
                return
              if float(new_power) < 0:
                 messagebox.showwarning("Ошибка", "Неверный формат энергопотребления(число не должно быть отрицательным)")
         
            try:
                new_level = int(new_level)
            except ValueError:
                messagebox.showwarning("Ошибка", "Неверный формат уровня сложности(должно быть число)")
                return  

            if int(new_level) > 10 or int(new_level) < 1:
              messagebox.showwarning("Ошибка", "Неверный формат уровня сложности(Должно принадлежать интервалу от 1 до 10)")
              return
            # Добавление данных в базу данных
            conn = sqlite3.connect('galactic_database.db')
            cursor = conn.cursor()
            # Обновление данных в базе данных
            conn = sqlite3.connect('galactic_database.db')
            cursor = conn.cursor()

            # Форматируем дату в соответствии с форматом в базе данных
            if new_date  == None:
              formatted_date = "NULL"
            else:
             try:
                formatted_date = datetime.strptime(new_date, "%Y-%m-%d").date()
             except ValueError:
                messagebox.showwarning("Ошибка", "Неверный формат даты")
                conn.close()

            # Обновление данных в базе данных
            cursor.execute(f'''
                UPDATE "{selected_dictionary}" 
                SET technology_name=?, invention_date=?, complexity_level=?, application=?, race_name = ?, power_consumption = ?
                WHERE technology_name=?
            ''', (new_name, formatted_date, new_level, new_application, new_race,new_power, selected_data[0]))

            conn.commit()
            conn.close()

            # Обновление данных в Treeview
            self.view_data()

            edit_window.destroy()
     #######################################################################################
           if selected_dictionary == "galactic_race":
            # Извлечение данных из виджетов редактирования и обновление записи в базе данных
            new_name = name_entry.get()
            new_date = None if null_var.get() else date_entry.get()
            new_planet = planet_entry.get()
            new_index = index_entry.get()

            # Проверка наличия данных
            if not new_name or not new_planet:
                messagebox.showwarning("Ошибка", "Заполните поля")
                return
            
            if new_index.lower() == 'null' or new_index.lower() == '' or new_index.lower() == ' ' or new_index.lower() == 'none' or new_index == null_var:
              new_index = "NULL"
            else:
              try:
                new_index = float(new_index)
              except ValueError:
                messagebox.showwarning("Ошибка", "Неверный формат индекса развития(должно быть число)")
                return
              if float(new_index) > 10 or float(new_index) < 1:
                messagebox.showwarning("Ошибка", "Неверный формат индекса развития(Должно принадлежать интервалу от 1 до 10)")
                return  
            
            
            # Обновление данных в базе данных
            conn = sqlite3.connect('galactic_database.db')
            cursor = conn.cursor()

            # Форматируем дату в соответствии с форматом в базе данных
            if new_date  == None:
              formatted_date = "NULL"
            else:
             try:
                formatted_date = datetime.strptime(new_date, "%Y-%m-%d").date()
             except ValueError:
                messagebox.showwarning("Ошибка", "Неверный формат даты")
                conn.close()

            # Обновление данных в базе данных
            cursor.execute(f'''
                UPDATE "{selected_dictionary}" 
                SET race_name=?, first_encounter_date=?, home_planet=?, development_index=?
                WHERE race_name=?
            ''', (new_name, formatted_date, new_planet, new_index, selected_data[0]))

            conn.commit()
            conn.close()

            # Обновление данных в Treeview
            self.view_data()

            edit_window.destroy()

        save_button = ttk.Button(edit_window, text="Сохранить", command=save_changes)
        save_button.grid(row=6, column=0, columnspan=2, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = GalacticApp(root)
    root.mainloop()
