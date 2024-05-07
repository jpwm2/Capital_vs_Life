import tkinter as tk

# ウィンドウを作成
root = tk.Tk()
root.title("動的表示変更の例")

# StringVarを作成
label_var = tk.StringVar()
label_var.set("最初のテキスト")

# Labelを作成し、StringVarをテキストとして使用
label = tk.Label(root, textvariable=label_var)
label.pack()

# ボタンを作成し、クリックするとラベルのテキストを変更
def change_text():
    current_text = label_var.get()
    if current_text == "最初のテキスト":
        label_var.set("テキストが変更されました！")
    else:
        label_var.set("最初のテキスト")

button = tk.Button(root, text="テキスト変更", command=change_text)
button.pack()

# ウィンドウをメインループに入れる
root.mainloop()
