import tkinter as tk
import tkinter.ttk as ttk


root = tk.Tk()
root.title('GlobalStrength')
frame_main = tk.Frame()
frame_main.grid(row=0, column=0)
# main sheets
sheet = ttk.Notebook(frame_main)
sheet_material = ttk.Frame(sheet)
sheet.add(sheet_material,text='Materials')
sheet_laminate = ttk.Frame(sheet)
sheet.add(sheet_laminate,text='Laminates')
sheet_elements = ttk.Frame(sheet)
sheet.add(sheet_elements,text='Global strength')
sheet.grid(row=0, column=0)
# sheet materials
frame_material_button = tk.Frame(sheet_material)
frame_material_button.pack(side="top", fill='both')
canvas_material = tk.Canvas(sheet_material, borderwidth=0)
frame_material = tk.Frame(canvas_material)
scroll_material_vertical = tk.Scrollbar(sheet_material, orient="vertical", command=canvas_material.yview)
canvas_material.configure(yscrollcommand=scroll_material_vertical.set)
scroll_material_vertical.pack(side="right", fill="y")
canvas_material.pack(side="top", fill="both", expand=True)
canvas_material.create_window((1, 1), window=frame_material, anchor="nw")
frame_material.bind("<Configure>", lambda event: canvas_material.configure(scrollregion=canvas_material.bbox("all")))


root.mainloop()