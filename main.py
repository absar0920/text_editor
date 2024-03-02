import os
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import askyesnocancel

def text_editor():
   filepath = None
   unsaved_changes = False

   def set_unsaved_changes(event=None):
       nonlocal unsaved_changes
       unsaved_changes = True
       update_title()

   def update_title():
       title = 'Text Editor'
       if filepath:
           title += f' - {os.path.basename(filepath)}'
       if unsaved_changes:
           title += ' - Unsaved Changes'
       window.title(title)

   def open_file(event=None):
       nonlocal filepath, unsaved_changes
       if unsaved_changes and askyesnocancel('Unsaved Changes', 'You have unsaved changes. Do you want to save them?'):
           save_file()
       filepath = askopenfilename(
           filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')]
       )
       if not filepath:
           return
       txt_edit.delete(1.0, tk.END)
       with open(filepath, 'r') as input_file:
           text = input_file.read()
           txt_edit.insert(tk.END, text)
       unsaved_changes = False
       update_title()

   def save_file(event=None):
       nonlocal filepath, unsaved_changes
       if filepath is None:
           filepath = asksaveasfilename(
               defaultextension='txt',
               filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')],
           )
       if not filepath:
           return
       with open(filepath, 'w') as output_file:
           text = txt_edit.get(1.0, tk.END)
           output_file.write(text)
       unsaved_changes = False
       update_title()

   def save_file_as():
       nonlocal filepath
       filepath = asksaveasfilename(
           defaultextension='txt',
           filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')],
       )
       if not filepath:
           return
       with open(filepath, 'w') as output_file:
           text = txt_edit.get(1.0, tk.END)
           output_file.write(text)
       unsaved_changes = False
       update_title()

   def exit_editor(event=None):
       if unsaved_changes and askyesnocancel('Unsaved Changes', 'You have unsaved changes. Do you want to save them?'):
           save_file()
       window.destroy()

   window = tk.Tk()
   window.title('Text Editor')
   window.rowconfigure(0, minsize=800, weight=1)
   window.columnconfigure(1, minsize=800, weight=1)

   txt_edit = tk.Text(window, bg='light yellow', fg='black', insertbackground='black')
   txt_edit.bind('<<Modified>>', set_unsaved_changes)
   fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=2, bg='light blue')
   btn_open = tk.Button(fr_buttons, text='Open', command=open_file, bg='white', fg='black')
   btn_save = tk.Button(fr_buttons, text='Save', command=save_file, bg='white', fg='black')
   btn_save_as = tk.Button(fr_buttons, text='Save As...', command=save_file_as, bg='white', fg='black')

   btn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
   btn_save.grid(row=1, column=0, sticky='ew', padx=5)
   btn_save_as.grid(row=2, column=0, sticky='ew', padx=5)

   fr_buttons.grid(row=0, column=0, sticky='ns')
   txt_edit.grid(row=0, column=1, sticky='nsew')

   window.bind('<Control-s>', save_file)
   window.bind('<Control-o>', open_file)
   window.bind('<Control-q>', exit_editor)

   window.protocol('WM_DELETE_WINDOW', exit_editor)

   window.mainloop()

if __name__ == '__main__':
  text_editor()
