from sys import exc_info

from traceback import print_exc
from traceback import format_exc

from PySide6.QtCore import Slot
from PySide6.QtCore import Signal
from PySide6.QtCore import QObject
from PySide6.QtCore import QRunnable

class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    progress
        int indicating % progress

    '''
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    console = Signal(str)
    progress = Signal(int)

class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self,
                 fn,
                 *args, **kwargs):
        # super(Worker, self).__init__()  # Python 2
        # super python 3 style
        super().__init__()

        # Store constructor arguments (re-used for processing)
        console = True if kwargs['console'] is True else False
        progress = True if kwargs['progress'] is True else False
    
        del kwargs['console']
        del kwargs['progress']
    
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        if progress:
            self.kwargs['progress_callback'] = self.signals.progress
        if console:
            self.kwargs['progress_callback_console'] = self.signals.console

    @Slot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            print_exc()
            exctype, value = exc_info()[:2]
            self.signals.error.emit((exctype, value, format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done
