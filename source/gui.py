from tkinter import *
from tkinter.filedialog import askdirectory, asksaveasfilename
from tkinter.messagebox import showerror
from main import StackDiffraction
import os

class Mainframe(Frame):
    def __init__(self,parent=None):
        Frame.__init__(self,parent)
        self.parent = parent

        frame_left = LeftFrame(self)
        frame_left.pack(side=LEFT,expand = YES, fill = BOTH)

        frame_right = RightFrame(self)
        frame_right.pack(side = LEFT,expand = YES, fill = BOTH)

        frame_left.message_box = frame_right.text_messages

class LeftFrame(LabelFrame):
    def __init__(self,parent=None):
        LabelFrame.__init__(self,parent,text="Options")
        self.parent = parent
        Tk.report_callback_exception = self.show_error
        self.message_box = Text(self)
        self.files = ""
        self.data = []

        var_button_open = StringVar()
        self.var_button_open = var_button_open
        button_open = Button(self,text = "Open Folder..",
                        command = lambda : self.onOpenFolder(self.message_box))
        button_open.pack(side = TOP)

        label_placeholder = Label(self,text="")
        label_placeholder.pack(side=TOP)

        var_bkg = BooleanVar()
        self.var_bkg = var_bkg
        chkbutton_bkg = Checkbutton(self,text="Background Subtract",
                                    variable = var_bkg,
                                    command = lambda: self.OnBkgSubt(self.message_box))
        chkbutton_bkg.pack(side = TOP)

        var_norm = BooleanVar()
        self.var_norm = var_norm
        chkbutton_norm = Checkbutton(self,text="Normalize\t     ",
                                    variable = var_norm,
                                    command = lambda: self.OnNormalize(self.message_box))
        chkbutton_norm.pack(side = TOP)

        var_smooth = BooleanVar()
        self.var_smooth = var_smooth
        chkbutton_smooth = Checkbutton(self,text = "Smooth\t\t     ",
                                        variable = var_smooth,
                                        command = lambda: self.OnSmooth(self.message_box))
        chkbutton_smooth.pack(side=TOP)

        var_separation = BooleanVar()
        var_separation_value = DoubleVar()
        self.var_separation = var_separation
        self.var_separation_value = var_separation_value
        var_separation_value.set(5.0)
        chkbutton_separation = Checkbutton(self,text = "Separate Plots\t     ",
                                            variable = var_separation,
                                            command = lambda : self.OnSeparation(self.message_box))
        chkbutton_separation.pack(side=TOP)

        label_separation = Label(self,text = "")
        self.label_separation = label_separation
        label_separation.pack(side = TOP)

        label_placeholder.pack(side = TOP)

        var_button_Export = StringVar()
        self.var_button_Export = var_button_Export
        button_Export = Button(self,text = "Export CSV",
                                command = lambda : self.OnExportCSV(self.message_box))
        self.button_Export = button_Export
        button_Export.pack(side = TOP)

    def onOpenFolder(self,message_box):
        self.var_button_open.set(askdirectory(title="Choose folder with CSV files",
                                initialdir= os.getcwd()))
        if self.var_button_open.get() == "":
            return
        self.MessageBoxUpdate(message_box,
        f"\n\nChanged working folder to {self.var_button_open.get()}")
        self.files = StackDiffraction.GetFiles(self,self.var_button_open.get())
        self.MessageBoxUpdate(message_box,
        f"\n\nFound {len(self.files)} csv files.")

    def OnBkgSubt(self,message_box):
        if self.var_bkg.get():
            self.MessageBoxUpdate(message_box,
            "\n\nBackground Subtract ON")
        else:
            self.MessageBoxUpdate(message_box,
            "\n\nBackground Subtract OFF")

    def OnNormalize(self,message_box):
        if self.var_norm.get():
            self.MessageBoxUpdate(message_box,
            "\n\nNormalize ON")
        else:
            self.MessageBoxUpdate(message_box,
            "\n\nNormalize OFF")

    def OnSmooth(self,message_box):
        if self.var_smooth.get():
            self.MessageBoxUpdate(message_box,
            "\n\nSmooth ON (Savintsky-Golay)")
        else:
            self.MessageBoxUpdate(message_box,
            "\n\nSmooth OFF")

    def OnSeparation(self,message_box):
        if self.var_separation.get():
            self.label_separation.pack_forget()
            self.label_separation = Entry(self,
                                        textvariable = self.var_separation_value)
            self.label_separation.pack(before=self.button_Export)
            self.MessageBoxUpdate(message_box,
            "\n\nSeparation ON")
        else:
            self.label_separation.pack_forget()
            self.label_separation = Label(self,text = "")
            self.label_separation.pack(before = self.button_Export)
            self.MessageBoxUpdate(message_box,
            "\n\nSeparation OFF")


    def OnExportCSV(self,message_box):
        self.var_button_Export.set(asksaveasfilename(
                                    defaultextension= ".csv",
                                    title="Save CSV File...",
                                    initialdir=os.getcwd()))
        if self.var_button_Export.get() == "":
            return
        if len(self.files) > 0:
            self.MessageBoxUpdate(self.message_box,
            "\n\nPlease wait...this may take a few seconds.")
            self.parent.config(cursor="watch") #I don't this does anything
            self.update_idletasks() #necesarry to force please wait message to print
            self.data.append(["2theta",*self.files])
            self.data.append(StackDiffraction.GetThetaValues(self,
                            self.var_button_open.get()))
            self.data.extend(StackDiffraction.GetHistograms(self,self.var_button_open.get(),
                                                            self.files,self.var_separation_value.get(),
                                                            bkg_subt=self.var_bkg.get(),
                                                            norm = self.var_norm.get(),
                                                            smooth = self.var_smooth.get(),
                                                            separate=self.var_separation.get()))
            self.MessageBoxUpdate(message_box,
            f"\n\nSaving CSV to directory {self.var_button_Export.get()}")
            StackDiffraction.SaveCSV(self,self.var_button_Export.get())
            self.MessageBoxUpdate(self.message_box,
            "\n\nSuccess! CSV file saved!")
            self.parent.config(cursor="")#I don't think this does anything
        else:
            self.MessageBoxUpdate(message_box,
                                    "\n\nNo export CSV files found.")

    def MessageBoxUpdate(self,message_box,message):
        message_box.config(state = 'normal')
        message_box.insert(INSERT,message)
        message_box.config(state = "disabled")
        message_box.see(END)

    def show_error(self,exc,val,tb):
        """The line below will catch all KeyErrors.
            It is is intended that KeyErrors will 
            only occur when trying to read 2theta
            values from a csv file."""
        if exc == KeyError:
            showerror("Error",message= "A KeyError was raised. This means that the CSV could not be read. Please check the welcome message to make sure CSV files are exported properly from GSAS-II.")

class RightFrame(LabelFrame):
    def __init__(self,parent=None):
        LabelFrame.__init__(self,parent,text = "Output")
        self.parent = parent

        welcome_message = """Welcome to PyStackXRD - v1.0.\n\nUse "Open Folder" to select a folder EXCLUSIVELY containing  exported CSV files from GSAS-II, and NO OTHER FILES.\n\nThe files must be exported from GSAS-II using the following  method:\nExport-->Powder Data-->histogram CSV file.\n\nCheck the boxes as desired.\n\nThe "Smooth" option uses a 10-point window and 2nd order Savintsky-Golay algorithm. These parameters cannot yet be edited.\n\nIf "Separate Plots" is enabled, enter a value to vertically separate the plots. The default is set to 1.0, so change it\naccordingly.\n\nPress "Export CSV" and select a path to save CSV file."""

        text_messages = Text(self,bg="black",fg="white")
        self.text_messages = text_messages
        text_messages.pack(side=TOP,expand = YES, fill = BOTH)
        text_messages.insert(INSERT,welcome_message)
        text_messages.config(state="disabled")


if __name__ == "__main__":
    root = Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    print(f"Detected screen resolution: {width} x {height}")
    root.geometry(f"{int(width*0.5)}x{int(height*0.5)}")
    root.title("PyStackXRD - v1.0")
    frame1 = Mainframe(parent=root)
    frame1.pack(fill = BOTH, expand = YES)
    root.resizable(False,False)
    root.mainloop()