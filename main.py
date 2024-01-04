from tkinter import messagebox
from sql import *
import tkinter as tk
from tkinter import ttk

#Створити дерево за параметрами
def make_tree(window, rows):
    tree = ttk.Treeview(window, show="headings")
    tree.config(height=15)
    tree["columns"] = tuple(rows[0].keys())
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER)
    for row in rows:
        tree.insert("", "end", values=tuple(row.values()))
    return tree



#Функції для кнопока
def button_click_for_table(root, variant):
    def on_closing():
        root.deiconify()
        window.destroy()
    def search_in_tree(tree):
        def search():
            search_query = entry_search.get().lower()
            search_category = combo_search.get()
            if search_category == "All":
                for item in tree.get_children():
                    values = tree.item(item, 'values')
                    if search_query in str(values).lower():
                        tree.selection_set(item)
                        tree.focus(item)
                        return
            else:
                column_index = tree['columns'].index(search_category)
                for item in tree.get_children():
                    values = tree.item(item, 'values')
                    if search_query in str(values[column_index]).lower():
                        tree.selection_set(item)
                        tree.focus(item)
                        return

            messagebox.showinfo("Search", "No matching results found.")

        search_window = tk.Toplevel()
        search_window.title("Search")

        label_search = tk.Label(search_window, text="Search Query:", font=("DIN Condensed Bold (Body)", 14))
        label_search.pack(side=tk.RIGHT, padx=5, pady=5)

        entry_search = tk.Entry(search_window, width=70)
        entry_search.pack(side=tk.RIGHT, padx=5, pady=5)


        label_category = tk.Label(search_window, text="Search Category:", font=("DIN Condensed Bold (Body)", 14))
        label_category.pack(side=tk.LEFT, padx=5, pady=5)


        categories = ["All"] + list(tree['columns'])
        combo_search = ttk.Combobox(search_window, values=categories, state="readonly")
        combo_search.current(0)  # Встановлюємо вибір за замовчуванням на "All"
        combo_search.pack(side=tk.LEFT, padx=5, pady=5)


        button_search = tk.Button(search_window, text="Search", command=search)
        button_search.pack(padx=5, pady=5)

        search_window.grab_set()
        search_window.focus_set()
        search_window.wait_window()
        
    def edit_row(window):
        def on_closing_third_window():
            window.deiconify()
            edit_window.destroy()
            return
        def save_changes():
            new_values = [entry.get() for entry in entries]
            update_row(variant, new_values)
            tree.item(selected_item, values=new_values)
            window.deiconify()
            edit_window.destroy()
        window.withdraw()
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Edit", "Please select a row to edit.")
            window.deiconify()
            return

        columns = tree['columns']
        values = tree.item(selected_item)['values']

        edit_window = tk.Toplevel(window)
        edit_window.title("Edit Row")
        edit_window.protocol("WM_DELETE_WINDOW", lambda: on_closing_third_window())

        entries = []
        for index, (column, value) in enumerate(zip(columns, values)):
            tk.Label(edit_window, text=f"{column}:", font=("DIN Condensed Bold (Body)", 14)).grid(row=index, column=0, padx=5, pady=5)
            entry = tk.Entry(edit_window, width=70)
            entry.insert(0, value)
            entry.grid(row=index, column=1, padx=5, pady=5)
            if index == 0:
                entry.config(state="disabled")
            entries.append(entry)
        save_button = tk.Button(edit_window, text="Save", command=save_changes)
        save_button.grid(row=len(columns), column=0, columnspan=2, pady=10)

    def delete_row():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Delete", "Please select a row to delete.")
            window.deiconify()
            return

        confirm = messagebox.askyesno("Delete", "Are you sure you want to delete the selected row?")
        if confirm:
            row_id = tree.item(selected_item)['values'][0]
            delete_row_table(variant, row_id)
            tree.delete(selected_item)

    def add_new_row():
        def on_closing_third_window():
            window.deiconify()
            add_window.destroy()
            return
        def add_new():
            new_values = [entry.get() for entry in entries]
            insert_row(variant, new_values)  # pass values except for the ID
            tree.insert("", "end", values=new_values)
            window.deiconify()
            add_window.destroy()

        window.withdraw()
        add_window = tk.Toplevel(window)
        add_window.title("Add New Row")
        add_window.protocol("WM_DELETE_WINDOW", lambda: on_closing_third_window())

        entries = []
        columns = tree['columns']
        for index, column in enumerate(columns):
            tk.Label(add_window, text=f"{column}:", font=("DIN Condensed Bold (Body)", 14)).grid(row=index, column=0, padx=5, pady=5)
            entry = tk.Entry(add_window, width=70)
            if index == 0:
                existing_values = set(tree.item(item_id)['values'][0] for item_id in tree.get_children())
                new_value = 1
                while new_value in existing_values:
                    new_value += 1
                entry.insert(0, new_value)
                entry.config(state="disabled")
            entries.append(entry)
            entry.grid(row=index, column=1, padx=5, pady=5)

        add_button = tk.Button(add_window, text="Add", command=add_new)
        add_button.grid(row=len(columns), column=0, columnspan=2, pady=10)

    root.withdraw()
    window = tk.Toplevel(root)
    window.title("Таблиця з бази даних")
    window.protocol("WM_DELETE_WINDOW", lambda: on_closing())

    match variant:
        case "BRV":
            tree = make_tree(window, show_all("BRV"))
            tree.pack()
        case "RRV":
            tree = make_tree(window, show_all("RRV"))
            tree.pack()
        case "TRV":
            tree = make_tree(window, show_all("TRV"))
            tree.pack()
        case "DIV":
            tree = make_tree(window, show_all("DIV"))
            tree.pack()
        case "Storages":
            tree = make_tree(window, show_all("Storages"))
            tree.pack()

    button_search = tk.Button(window, font=("DIN Condensed Bold (Body)", 26), text="Search", command=lambda: search_in_tree(tree))
    button_search.pack(side=tk.LEFT, padx=50, pady=20)

    button_change = tk.Button(window, font=("DIN Condensed Bold (Body)", 26), text="Edit", command=lambda: edit_row(window))
    button_change.pack(side=tk.LEFT, padx=50, pady=20)

    button_delete = tk.Button(window, font=("DIN Condensed Bold (Body)", 26), text="Delete", command=delete_row)
    button_delete.pack(side=tk.RIGHT, padx=50, pady=20)

    button_add = tk.Button(window, font=("DIN Condensed Bold (Body)", 26), text="Add new", command=add_new_row)
    button_add.pack(side=tk.RIGHT, pady=20)





#Головне вікно з кнопками
root = tk.Tk()
root.title("Таблиця з бази даних")

button_BRV = tk.Button(root, text="Показати BRV", command=lambda: button_click_for_table(root, "BRV"))
button_BRV.pack(pady=10)

button_RRV = tk.Button(root, text="Показати RRV", command=lambda: button_click_for_table(root, "RRV"))
button_RRV.pack(pady=10)

button_TRV = tk.Button(root, text="Показати TRV", command=lambda: button_click_for_table(root, "TRV"))
button_TRV.pack(pady=10)

button_DIV = tk.Button(root, text="Показати DIV", command=lambda: button_click_for_table(root, "DIV"))
button_DIV.pack(pady=10)

button_Storages = tk.Button(root, text="Показати Storages", command=lambda: button_click_for_table(root, "Storages"))
button_Storages.pack(pady=10)




root.resizable(False, False)
root.mainloop()

