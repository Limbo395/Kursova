from tkinter import messagebox, simpledialog
from sql import *
import tkinter as tk
from tkinter import ttk
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

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

def Report(root):
    def report_file():
        styles = getSampleStyleSheet()
        centered_style = ParagraphStyle(
            "Centered",
            parent=styles["Normal"],
            fontSize=32,
            alignment=1)

        report_text = "Report"
        report_contitul = Paragraph(report_text, centered_style)
        return report_contitul

    def table_to_report(treeview):
        headers = []
        data = []
        for col in treeview["columns"]:
            headers.append(treeview.heading(col, option="text"))
        for child in treeview.get_children():
            values = [treeview.item(child, "values")]
            data.extend(values)
        table_data1 = [headers] + data
        table = Table(table_data1)
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('FONTSIZE', (0, 0), (-1, -1), 5),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)])
        table.setStyle(style)
        return table


    def text_to_file(text):
        styles = getSampleStyleSheet()
        paragraph = Paragraph(text, styles["Normal"])
        return paragraph



    

    filename = simpledialog.askstring("Імʼя фалйлу", "Введіь імʼя файлу для звіту:")
    if filename == None or filename == "":
        return
    filename = filename + ".pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    
    doc.build([report_file(), Spacer(1, 50), 
               table_to_report(make_tree(root, show_all("BRV"))), Spacer(1, 20),
               table_to_report(make_tree(root, show_all("RRV"))), Spacer(1, 20),
               table_to_report(make_tree(root, show_all("TRV"))), Spacer(1, 20),
               table_to_report(make_tree(root, show_all("DIV"))), Spacer(1, 20),
               table_to_report(make_tree(root, show_all("Storages"))), Spacer(1, 20),
               text_to_file("RAV amount: "),table_to_report(make_tree(root, for_report("RAV_amount"))),  Spacer(1, 10),
               text_to_file("RAV activity:"),table_to_report(make_tree(root, for_report("RAV_activity"))),  Spacer(1, 10),
               text_to_file("DIV amount"),table_to_report(make_tree(root, for_report("DIV_amount"))),  Spacer(1, 10),
               text_to_file("DIV activity:"),table_to_report(make_tree(root, for_report("DIV_activity"))),  Spacer(1, 10),
               table_to_report(make_tree(root, for_report("CriticalStorages"))), Spacer(1, 20),
               table_to_report(make_tree(root, for_report("OverdueStorages"))), Spacer(1, 20)])




def button_click_for_table(root, variant):
    def on_closing():
        root.deiconify()
        window.destroy()
        return

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
                        search_window.destroy()
                        return
            else:
                column_index = tree['columns'].index(search_category)
                for item in tree.get_children():
                    values = tree.item(item, 'values')
                    if search_query in str(values[column_index]).lower():
                        tree.selection_set(item)
                        tree.focus(item)
                        search_window.destroy()
                        return

            messagebox.showinfo("Search", "No matching results found.")

        search_window = tk.Toplevel()
        search_window.title("Search")
        search_window.resizable(False, False)

        label_category = tk.Label(search_window, text="Search Category:", font=("DIN Condensed Bold (Body)", 14))
        label_category.pack(side=tk.LEFT, padx=5, pady=5)

        categories = ["All"] + list(tree['columns'])
        combo_search = ttk.Combobox(search_window, values=categories, state="readonly")
        combo_search.current(0)
        combo_search.pack(side=tk.LEFT, padx=5, pady=5)

        label_search = tk.Label(search_window, text="Search Query:", font=("DIN Condensed Bold (Body)", 14))
        label_search.pack(side=tk.LEFT, padx=5, pady=5)

        entry_search = tk.Entry(search_window, width=70)
        entry_search.pack(side=tk.LEFT, padx=5, pady=5)

        button_search = tk.Button(search_window, text="Search", command=search)
        button_search.pack(side=tk.LEFT, padx=5, pady=50)
  
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
        def display_additional_tables():
            if variant == "BRV" or variant == "TRV" or variant == "RRV" or variant == "DIV":
                tables_to_display = ["Vocabulare_StorageId", "Vocabulare_Radionuclide", "Vocabulare_StorageMethods"]
            elif variant == "Storages":
                tables_to_display = ["Vocabulare_StorageCondition", "Vocabulare_TypesOfStorage"]
            else:
                return

            additional_window = tk.Toplevel(edit_window)
            additional_window.title("Additional Tables")
            additional_window.resizable(False, False)

            for table_name in tables_to_display:
                table_tree = make_tree(additional_window, show_all(table_name))
                table_tree.pack()

            additional_window.protocol("WM_DELETE_WINDOW", lambda: additional_window.destroy())

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
        edit_window.resizable(False, False)

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


        display_tables_button = tk.Button(edit_window, text="Display Additional Tables", command=display_additional_tables)
        display_tables_button.grid(row=len(columns) + 1, column=0, columnspan=2, pady=10)

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
            insert_row(variant, new_values)
            tree.insert("", "end", values=new_values)
            window.deiconify()
            add_window.destroy()

        def display_additional_tables():
            if variant == "BRV" or variant == "TRV" or variant == "RRV" or variant == "DIV":
                tables_to_display = ["Vocabulare_StorageId", "Vocabulare_Radionuclide", "Vocabulare_StorageMethods"]
            elif variant == "Storages":
                tables_to_display = ["Vocabulare_StorageCondition", "Vocabulare_TypesOfStorage"]
            else:
                return
            additional_window = tk.Toplevel(add_window)
            additional_window.title("Additional Tables")
            additional_window.resizable(False, False)

            for table_name in tables_to_display:
                table_tree = make_tree(additional_window, show_all(table_name))
                table_tree.pack()

            additional_window.protocol("WM_DELETE_WINDOW", lambda: additional_window.destroy())

        window.withdraw()
        add_window = tk.Toplevel(window)
        add_window.title("Add New Row")
        add_window.protocol("WM_DELETE_WINDOW", lambda: on_closing_third_window())
        add_window.resizable(False, False)

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

        display_tables_button = tk.Button(add_window, text="Display Additional Tables", command=display_additional_tables)
        display_tables_button.grid(row=len(columns) + 1, column=0, columnspan=2, pady=10)

    root.withdraw()
    window = tk.Toplevel(root)
    window.title("Таблиця з бази даних")
    window.protocol("WM_DELETE_WINDOW", lambda: on_closing())
    window.resizable(False, False)

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

button_Report = tk.Button(root, text="Зберегти звіт", command=lambda: Report(root))
button_Report.pack(pady=10)




root.resizable(False, False)
root.mainloop()

