"""
    Utils for memory scripting
"""

from atmega.ram import RAM
from time import sleep, time
from sys import platform
from time import gmtime, strftime
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox
import os

if platform == "win32":
    import winsound # TODO unix equivalent

def spawn_box(title, text, icon=QMessageBox.Warning):
    """
        Spawn a message box
        :param title: title of the message box
        :param text: text of the message box
        :param icon: icon of the message box
    """
    box = QMessageBox()
    box.setWindowTitle(title)
    box.setText(text)
    box.setIcon(icon)
    box.exec()


class TextSignal(QtCore.QObject):
    """ Output signal """
    output = QtCore.pyqtSignal(str)


class TextWorker(QtCore.QThread):
    """ Worker that emit text output """
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.signal = TextSignal()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.kwargs['output'] = self.signal.output

    @QtCore.pyqtSlot()
    def run(self):
        self.fn(*self.args, **self.kwargs)

class FallbackOutput:
    """ Fallback output for the script reader """
    @staticmethod
    def emit(*args, **kwargs):
        print(*args, **kwargs)


class ScriptExe:
    """ Script reader """
    def __init__(self, device=None):
        """
            Initialisation of the script executer with callback functions.
            :param device: device that will perform the commands
            :param log_function: callback function that will be called on errors
        """
        if device is None:
            device = RAM()
        self.ram = device
        self.stop = False
        self.running = False
        self.pause = False
        self.glist = [0]*(device.ram_size - 40)

    def on_error_stop(self):
        """ Stop the execution of the script """
        play_sound()
        self.ram.close()

    def exec_file(self, file, output=None):
        """ Execute a script """
        if output is None:
            output = FallbackOutput
        lines = open_file(file)
        start_time = time()
        first_iteration = True
        looping = False
        inside_loop = False
        last_comp = False
        counter = 1
        while not self.stop and (first_iteration or looping):
            while self.pause: # Paused
                sleep(0.2)
            current_time = round(time() - start_time, 2)
            output.emit(f"Passe n⁰{counter}")
            output.emit(f"Temps cumulé {current_time}s")
            for line in lines:
                subline = line.split()
                command = subline[0]
                arg = subline[1:]
                nb_arg = len(arg)

                if command == "CONNECT":
                    pass # Class already connected

                elif command == "INIT_RAM":
                    if not first_iteration and not inside_loop:
                        continue
                    if nb_arg not in [1, 2]:
                        output.emit("Invalid number of arguments")
                        self.on_error_stop()
                        return
                    output.emit(line)
                    value = int(arg[0], base=16)
                    complement = False
                    increment = False
                    if nb_arg == 2:
                        complement = "COMP" in arg[1]
                        increment = "INCR" in arg[1]
                    try:
                        self.ram.reset(value, increment, complement)
                        output.emit("OK")
                    except:
                        output.emit("Reset error")
                        self.on_error_stop()
                        return

                elif command == "LIRE_RAM":
                    if not first_iteration and not inside_loop:
                        continue
                    output.emit(line)
                    if nb_arg not in [1, 2]:
                        output.emit("Invalid number of arguments")
                        self.on_error_stop()
                        return
                    reserve_stack = int(arg[0])
                    block_size = 64
                    if nb_arg == 2:
                        block_size = int(arg[1])
                    try:
                        self.ram.dump_to_file("Dump_RAM.txt", reserve_stack, block_size)
                    except:
                        output.emit("Error on ram dump")
                        self.on_error_stop()
                        return

                elif command == "COPY":
                    if not first_iteration and not inside_loop:
                        continue
                    output.emit(line)
                    if nb_arg not in [2, 3]:
                        output.emit("Invalid number of arguments")
                        self.on_error_stop()
                        return
                    increment = False
                    diff_only = False
                    if nb_arg == 3:
                        increment = "INCR" in arg[2]
                        diff_only = "COMP" in arg[2]
                    if not diff_only or last_comp:
                        copy(arg[0], arg[1], increment)

                elif command == "BAUDRATE":
                    if not first_iteration and not inside_loop:
                        continue
                    output.emit(line)
                    if nb_arg != 1:
                        output.emit("Invalid number of arguments")
                        self.on_error_stop()
                        return
                    baudrate = int(arg[0])
                    try:
                        self.ram.change_baudrate(baudrate)
                        output.emit("Baudrate OK")
                    except:
                        output.emit("Error on baudrate change")

                elif command == "WAIT_SYNC":
                    pass # Everything is synched by the API

                elif command == "COMP":
                    if not first_iteration and not inside_loop:
                        continue
                    output.emit(line)
                    if nb_arg not in [2, 3]:
                        output.emit("Invalid number of arguments")
                        self.on_error_stop()
                        return

                    beep_on_error = False
                    stop_on_error = False
                    if nb_arg == 3:
                        beep_on_error = "BEEP" in arg[2]
                        stop_on_error = "STOP" in arg[2]

                    nb_error = compare(arg[0], arg[1], self.glist)
                    last_comp = nb_error > 0
                    if nb_error:
                        output.emit(f"Found {nb_error} differences")
                        if beep_on_error:
                            frequency = 2500  # Set Frequency To 2500 Hertz
                            duration = 1000   # Set Duration To 1000 ms= 1 seconde
                            play_sound(frequency, duration)
                        elif stop_on_error:
                            output.emit("Error. Stopping the script")
                            self.on_error_stop()
                            return
                    else:
                        output.emit("Fichiers identiques")

                elif command == "DEBLOOP":
                    if nb_arg != 0:
                        output.emit("Invalid number of arguments")
                        self.on_error_stop()
                        return
                    output.emit(line)
                    inside_loop = True

                elif command == "LOOP":
                    if nb_arg not in [1, 3]:
                        output.emit("Invalid number of arguments")
                        self.on_error_stop()
                        return
                    output.emit(line)
                    sleep(float(arg[0]))
                    if nb_arg == 3:
                        if arg[1] != "PENDANT":
                            output.emit("Invalid argument")
                            self.on_error_stop()
                            return
                        max_time = int(arg[2])
                        looping = time() - start_time < max_time

                elif command == "MEM_INIT_OK":
                    pass # error raised in INIT_RAM

                elif command == "SEND_RES":
                    pass # Socked not implemented TODO?

                else:
                    output.emit(f"Unknown command: {command}")
                    self.on_error_stop()
                    return

            first_iteration = False
            counter += 1


def compare(old, new, glist):
    """
        Compares two dump files and modify glist

        :param old: old file
        :param new: new file
        :param glist: comparison list
    """
    try:
        fo = open(old, "r+")
        fn = open(new, "r+")
    except OSError:
       raise Exception("Could not open/read file")

    lo = fo.readlines()
    ln = fn.readlines()
    fo.close()
    fn.close()

    if len(lo) != len(ln):
        raise Exception("Two dumps differ in size")

    n_diff = 0
    for n, (vo, vn) in enumerate(zip(lo, ln)):
        # each line is in the format addr:value
        # we extract the value
        no = int(vo.split(':')[1], base=16)
        nn = int(vn.split(':')[1], base=16)
        # xor to get the difference
        for i in range(8):
            bo = (no >> i) & 1
            bn = (nn >> i) & 1
            if bn > bo:
                n_diff += 1
                if 0 < glist[n*8 + i] < 3:
                    glist[n*8 + i] = 3
                else:
                    glist[n*8 + i] = 1
            elif bo > bn:
                n_diff += 1
                if 0 < glist[n*8 + i] < 3:
                    glist[n*8 + i] = 3
                else:
                    glist[n*8 + i] = 2
    return n_diff


def copy(source, dest, increment):
    """
        Copy a file.
        :param source: source file
        :param dest: destination file
        :param increment: Append the date to the filename
    """
    dest_name = dest
    if increment:
        date_incr = strftime("%d_%b_%Y_a_%HH%M", gmtime()).upper()
        extless_dest = dest.replace(".txt", "")
        dest_name = extless_dest + '_' + date_incr + '.txt'
    try:
        s = open(source, "r+")
        d = open(dest_name, "w+")
    except OSError:
        raise Exception("Could not open/read file")
    for line in s.readlines():
        d.write(line)
    s.close()
    d.close()

def open_file(file):
    """ Open a file while removing comments and empty lines """
    try:
        f = open(file, "r+", encoding="ISO-8859-1")
    except OSError:
        raise Exception("Cannot open file")
    lines = f.readlines()
    f.close()
    cleaned_lines = []
    for l in lines:
        l = l.split("//")[0]
        if l and not l.isspace():
            cleaned_lines.append(l)
    return cleaned_lines

def play_sound(frequency=2500, duration=1000):
    """ Plays a sound """
    if platform == "win32":
        winsound.Beep(frequency, duration)
    elif "linux" in platform:
        # FIXME use something else
        os.system("beep -f " + str(frequency) + " -l " +  str(duration))
    else:
        raise Exception("Unknown operating system. Cannot play beep")
