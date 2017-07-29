#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import StringIO
import Tkinter as tk
import tkFileDialog
import tkMessageBox
import traceback
import zipfile

from tools.recovery import xlsx_remove_protections


class App:
    def __init__(self, master):
        frame = tk.Frame(master)
        frame.pack()
        tk.Label(frame, text='Remove excel (.xlsx) workbook protection, '
                             'worksheet protections and read-only protec'
                             'tion. \n'
                             '[1] Note that open password cannot be remo'
                             'ved. \n'
                             '[2] .xls and other formats are not support'
                             'ed.',
                 compound=tk.LEFT, bitmap='questhead', wraplength=400, padx=10,
                 justify=tk.LEFT).pack(side=tk.TOP, padx=5)
        buttom_frame = tk.Frame(frame)
        buttom_frame.pack(side=tk.TOP, pady=10)
        self.button_open = tk.Button(buttom_frame, text='Open', fg='black',
                                     command=self.open)
        self.button_open.pack(side=tk.LEFT)
        self.button_save = tk.Button(buttom_frame, text='Save as', fg='black',
                                     state=tk.DISABLED, command=self.save)
        self.button_save.pack(side=tk.LEFT)
        self.output = ''
        self.file_type_opt = {
            'defaultextension': '*.xlsx',
            'filetypes': (('Excel file', '*.xlsx'), ('All types', '*.*')),
        }

    def open(self):
        self.button_save.config(state=tk.DISABLED)
        fp = tkFileDialog.askopenfile(mode='rb', **self.file_type_opt)
        if fp is None:
            return
        with fp:
            try:
                s = StringIO.StringIO()
                with zipfile.ZipFile(fp, 'r') as zipin, \
                        zipfile.ZipFile(s, 'w') as zipout:
                    xlsx_remove_protections(zipin, zipout)
                self.output = s.getvalue()
                assert(len(self.output) > 0)
            except Exception as e:
                logging.exception(e)
                tkMessageBox.showinfo(title='Error',
                                      message='Format not supported.')
                return
        self.button_save.config(state=tk.NORMAL)

    def save(self):
        fp = tkFileDialog.asksavefile(mode='wb', **self.file_type_opt)
        if fp is None:
            return
        with fp:
            fp.write(self.output)

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Excel Password Recovery')
    app = App(root)
    root.mainloop()