def term_enter_key_callback(self):
    compiler_thread = linux.task.Thread(target=self.run_cmd,
                                        args=(self.curr_text[3:],
                                              self.mainTextArea.size()))
    compiler_thread.daemon = True
    compiler_thread.start()
    self.curr_text = '>> '
    self.mainTextArea.insert(ui.tk.END, self.curr_text)
    self.mainTextArea.yview_scroll(1, ui.tk.UNITS)
    self.root.update()
    return

##end
