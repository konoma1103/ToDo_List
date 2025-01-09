import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from janome.tokenizer import Tokenizer
import gensim

model = gensim.models.KeyedVectors.load('cc_ja_300.model')
tokenizer = Tokenizer(wakati=True)

def get_categorize(task :str,category :list):
  max_vector = 0
  max_index = 0
  for i in tokenizer.tokenize(task):
    for j in range(len(category)):
      vector_score = model.similarity(i,category[j])
      if vector_score > max_vector:
        max_vector = vector_score
        max_index = j
  return max_index

def add_task(listbox, entry, year_entry, month_var, day_var):
    task = entry.get()
    year = year_entry.get()
    month = month_var.get()
    day = day_var.get()

    if task != "":
        index = get_categorize(task, category_list)
        task_deadline = f"{task} (期限 :{year}年{month}{day})"
        listbox[index].insert(tk.END, task_deadline)

        # ウィジェットを元に戻す
        entry.delete(0, tk.END)
        year_entry.delete(0, tk.END)
        month_var.set("--月")
        day_var.set("--日")
    else:
        messagebox.showwarning("入力エラー", "タスクを入力してください")

def delete_task(listbox):
    select = listbox.curselection()

    if len(select) >= 1:
        for index in select:
            listbox.delete(index)
    else:
        messagebox.showwarning("選択エラー", "削除するタスクを選択してください")

# カテゴリーを追加する関数
def add_category():
    category = category_entry.get()
    if category != "":
        category_list.append(category)
        category_entry.delete(0, tk.END)  # 入力ボックスをクリア
        make_tab(category)
    else:
        messagebox.showwarning("入力エラー", "カテゴリー名を入力してください")

def make_tab(tab_name):
    tab = tk.Frame(notebook)
    notebook.add(tab, text=tab_name)
    notebook.pack()

    listbox = tk.Listbox(tab, height=10, width=50, selectmode=tk.SINGLE)
    listbox.pack(pady=10)
    listbox_list.append(listbox)

    delete_button = tk.Button(tab, text="タスク削除", width=20, command=lambda: delete_task(listbox))
    delete_button.pack(pady=5)


root = tk.Tk()
root.title("ToDoリスト")
root.geometry("600x600")

category_list = ["就活","大学","バイト"]
listbox_list = []

notebook = ttk.Notebook(root)

#ホーム画面
home = tk.Frame(notebook)
notebook.add(home, text="ホーム")
notebook.pack()

category_title = tk.Label(home, text='カテゴリの追加', font=('MSゴシック', "10", "bold"), anchor=tk.SW, pady=10, width=30)
category_title.pack()
category_entry = tk.Entry(home, width=40)
category_entry.pack(pady=5)
category_button = tk.Button(home, text="カテゴリー追加", width=20, command=add_category)
category_button.pack(pady=5)

task_title = tk.Label(home, text='タスクの追加', font=('MSゴシック', "10", "bold"), anchor=tk.SW, pady=10, width=30)
task_title.pack()
entry_task = tk.Entry(home, width=40)
entry_task.pack(pady=5)

deadline = tk.Frame(home)
deadline_year = tk.Entry(deadline, width=10)
year_label = tk.Label(deadline,text="年")

var = tk.StringVar(deadline)
month = [
"--月","1月", "2月", "3月", "4月", "5月","6月", 
"7月", "8月", "9月", "10月","11月","12月"
]
var.set(month[0])
deadline_month = tk.OptionMenu(deadline, var, *month)

var2 = tk.StringVar(deadline)
day = [f"{i}日" for i in range(1,32)]
day.insert(0,"--日")
var2.set(day[0])
deadline_day = tk.OptionMenu(deadline, var2, *day)

deadline_year.pack(side=tk.LEFT)
year_label.pack(side=tk.LEFT)
deadline_month.pack(side=tk.LEFT)
deadline_day.pack(side=tk.LEFT)
deadline.pack()

add_button = tk.Button(home, text="タスク追加", width=20, command=lambda: add_task(listbox_list, entry_task, deadline_year, var, var2))
add_button.pack(pady=5)



for i in category_list:
    make_tab(i)

root.mainloop()