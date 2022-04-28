"""
    Utils for memory scripting
"""
from os import path
from math import log2, floor, ceil

from time import sleep, time
from time import gmtime, strftime

from PyQt5 import QtCore, QtMultimedia
from PyQt5.QtWidgets import QMessageBox

from atmega.ram import RAM

import atmega_gui
from atmega_gui.variable import device


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


class IntSignal(QtCore.QObject):
    """ Output signal """
    output = QtCore.pyqtSignal(int)


class TextWorker(QtCore.QThread):
    """ Worker that emit text output """
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.signal = TextSignal()
        self.sound = TextSignal()
        self.indicator = TextSignal()
        self.new_diff = TextSignal()
        self.progress = IntSignal()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.kwargs['output'] = self.signal.output
        self.kwargs['sound'] = self.sound.output
        self.kwargs['indicator'] = self.indicator.output
        self.kwargs['new_diff'] = self.new_diff.output
        self.kwargs['progress'] = self.progress.output

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
    def __init__(self, device):
        """
            Initialisation of the script executer with callback functions.
            :param ram_size: device that will perform the commands
            :param log_function: callback function that will be called on errors
        """
        device = device
        self.stop = False
        self.running = False
        self.pause = False
        self.incremental_list = None
        self.differential_list = None

    def on_error_stop(self, sound):
        """ Stop the execution of the script """
        sound.emit("error")

    def exec_file(self, file,
                  output=FallbackOutput, sound=FallbackOutput,
                  indicator=FallbackOutput, progress=FallbackOutput, new_diff=FallbackOutput):
        """ Execute a script """
        self.incremental_list = [0]*(device.ram_size)*8
        self.differential_list = [0]*(device.ram_size)*8
        lines = open_file(file)
        start_time = time()
        first_iteration = True
        looping = False
        inside_loop = False
        last_comp = False
        counter = 1
        # Everything is supposed to be good at the beginning
        indicator.emit("green")
        while not self.stop and (first_iteration or looping):
            if self.pause:
                # Orange color for pause state
                indicator.emit("orange")
                while self.pause: # Paused
                    sleep(0.2)
            if last_comp:
                indicator.emit("red")
            else:
                indicator.emit("green")
            current_time = round(time() - start_time, 2)
            output.emit(f"Passe n⁰{counter}")
            output.emit(f"Temps cumulé {current_time}s")
            for n, line in enumerate(lines):
                subline = line.split()
                command = subline[0]
                arg = subline[1:]
                nb_arg = len(arg)

                # Update progress
                progress.emit(int(100*n/len(lines)))

                if command == "CONNECT":
                    pass # Class already connected

                elif command == "INIT_RAM":
                    if not first_iteration and not inside_loop:
                        continue
                    if nb_arg not in [1, 2]:
                        output.emit("Invalid number of arguments")
                        self.on_error_stop(sound)
                        return
                    output.emit(line)
                    value = int(arg[0], base=16)
                    complement = False
                    increment = False
                    if nb_arg == 2:
                        complement = "COMP" in arg[1]
                        increment = "INCR" in arg[1]
                    try:
                        device.reset(value, increment, complement)
                        output.emit("OK")
                    except:
                        output.emit("Reset error")
                        self.on_error_stop(sound)
                        return

                elif command == "LIRE_RAM":
                    if not first_iteration and not inside_loop:
                        continue
                    output.emit(line)
                    if nb_arg not in [1, 2]:
                        output.emit("Invalid number of arguments")
                        self.on_error_stop(sound)
                        return
                    reserve_stack = int(arg[0])
                    block_size = 64
                    if nb_arg == 2:
                        block_size = int(arg[1])
                    try:
                        device.dump_to_file("Dump_RAM.txt", reserve_stack, block_size)
                    except:
                        output.emit("Error on ram dump")
                        self.on_error_stop(sound)
                        return

                elif command == "COPY":
                    if not first_iteration and not inside_loop:
                        continue
                    output.emit(line)
                    if nb_arg not in [2, 3]:
                        output.emit("Invalid number of arguments")
                        self.on_error_stop(sound)
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
                        self.on_error_stop(sound)
                        return
                    baudrate = int(arg[0])
                    try:
                        device.change_baudrate(baudrate)
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
                        self.on_error_stop(sound)
                        return

                    beep_on_error = False
                    stop_on_error = False
                    if nb_arg == 3:
                        beep_on_error = "BEEP" in arg[2]
                        stop_on_error = "STOP" in arg[2]

                    # Differential diff
                    self.differential_list = [0]*(self.ram.ram_size)*8
                    nb_error = compare(arg[0], arg[1], self.differential_list)
                    last_comp = nb_error > 0

                    # Incremental diff
                    compare(arg[0], arg[1], self.incremental_list)

                    # Write the diffs if there are diffs
                    if last_comp:
                        current_name = write_diff(self.differential_list, self.incremental_list)
                        new_diff.emit(current_name)

                    if nb_error:
                        output.emit(f"Found {nb_error} differences")
                        indicator.emit("red") # Update the state
                        if beep_on_error:
                            sound.emit("ding_dong")
                        elif stop_on_error:
                            output.emit("Error. Stopping the script")
                            self.on_error_stop(sound)
                            return
                    else:
                        output.emit("Fichiers identiques")

                elif command == "DEBLOOP":
                    if nb_arg != 0:
                        output.emit("Invalid number of arguments")
                        self.on_error_stop(sound)
                        return
                    output.emit(line)
                    inside_loop = True

                elif command == "LOOP":
                    if nb_arg not in [1, 3]:
                        output.emit("Invalid number of arguments")
                        self.on_error_stop(sound)
                        return
                    output.emit(line)
                    sleep(float(arg[0]))
                    if nb_arg == 3:
                        if arg[1] != "PENDANT":
                            output.emit("Invalid argument")
                            self.on_error_stop(sound)
                            return
                        max_time = int(arg[2])
                        looping = time() - start_time < max_time

                elif command == "MEM_INIT_OK":
                    pass # error raised in INIT_RAM

                elif command == "SEND_RES":
                    pass # Socked not implemented TODO?

                else:
                    output.emit(f"Unknown command: {command}")
                    self.on_error_stop(sound)
                    return

            first_iteration = False
            counter += 1
        # End of the program. We reset the indicator
        indicator.emit("grey")


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
                    glist[n*8 + i] = 0
                else:
                    glist[n*8 + i] = 1
            elif bo > bn:
                n_diff += 1
                if 0 < glist[n*8 + i] < 3:
                    glist[n*8 + i] = 0
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
        date_incr = strftime("%d_%b_%Y_a_%HH%MM%SS", gmtime()).upper()
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

def write_diff(diff_l, incr_l):
    """
        Write diff into a file.
        :param diff_l: the diffenrial list
        :param incr_l: the incremental list
        :return: the name of the created file
    """
    # Fichier output
    date_incr = strftime("%d_%b_%Y_a_%HH%MM%SS", gmtime()).upper()
    dest_name = date_incr + "_diff.txt"
    try:
        f = open(dest_name, "w+")
    except OSError:
        raise Exception("Could not open file")
    # Ecriture
    for d, i in zip(diff_l, incr_l):
        f.write(f"{d} {i}\n")
    f.close()
    # Return the final file
    return dest_name

def read_diff(filename):
    """
        Reads a diff
        :param filename: the file that contains the diff
        :return: a tupple for two lists (diffenrial and incremental)
    """
    try:
        f = open(filename, "r+")
    except OSError:
        raise Exception("Could not open file")

    lines = f.readlines()
    f.close()

    diff_l = []
    incr_l = []
    for line in lines:
        [d, i] = line.split()
        diff_l.append(int(d))
        incr_l.append(int(i))

    # Conversion into a list of list (dump should be a power of 2)
    len_power = log2(len(diff_l))
    line_len = 2**floor(len_power/2)
    col_len =  2**ceil(len_power/2)
    diff_l2d = [diff_l[i*col_len:(i+1)*col_len] for i in range(line_len)]
    incr_l2d = [incr_l[i*col_len:(i+1)*col_len] for i in range(line_len)]

    return diff_l2d, incr_l2d

def play_sound(sound):
    """
        Plays a sound inside a Qt context.
        :param file: the file to play sound in ding_dong, error or incorrect
    """
    if sound not in ["ding_dong", "error", "incorrect"]:
        raise Exception("Incorrect file")
    file = path.join(path.dirname(atmega_gui.__file__), "resources", "audio", sound + ".wav")
    QtMultimedia.QSound.play(file)
