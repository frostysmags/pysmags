import threading, queue, time, signal, sys

class QThread:
    def __init__(self, *args:list[callable], **kwargs) -> None:
        '''
        args:\n
        1 REQUIRED: callable variable (function) that the thread will operate\n
        kwargs:\n
        loop:bool # Use to run callable variable 0 (function | args[0]) through a while loop until QThread stop or termination 
        debug:bool # Use only for debugging purposes - prints status outputs for each function called in QThread
        '''
        self.__debugMode__ = False;self.__running__ = True;self.__threadCore__ = None;self.__threadArgs__ = args;self.__threadKWArgs__ = kwargs;self.__closing_thread__=False
        self.threadQueue = queue.Queue();self.threadName = args[0].__name__.strip("_")
        if 'loop' in kwargs and kwargs['loop'] == True:
            self.__threadCore__ = threading.Thread(target=self.__loopThreadFunction__)
        else:
            self.__threadCore__ = threading.Thread(target=self.__threadFunction__)
        if 'debug' in kwargs and kwargs['debug'] == True: self.__debugMode__ = True
        signal.signal(signal.SIGINT, self.__handle_sigint__)
        
    def clearQueue(self) -> None:
        '''Clears the QThread Queue'''
        self.threadQueue.queue.clear()
        print(f"Cleared Queue of Thread Running '{self.threadName}'\n" if self.__debugMode__ else "", end="")

    def start(self) -> None:
        '''Starts the QThread which will run the arg[0] callable variable'''
        print(f"Starting Thread Running '{self.threadName}'\n" if self.__debugMode__ else "", end="")
        self.__threadCore__.start()

    def stop(self) -> None:
        '''Stops the Qthread and clears the QThread Queue'''
        print(f"Stopping Thread Running '{self.threadName}'\n" if self.__debugMode__ else "", end="")
        self.__running__ = False
        self.threadQueue.queue.clear()
        self.__threadCore__.join()
    
    def __handle_sigint__(self, signum, frame) -> None:
        '''Handles CTRL+C exit signal'''
        if not self.__closing_thread__:
            self.__closing_thread__ = True
            print(f"Force Shutting Down Thread Running '{self.threadName}'\n" if self.__debugMode__ else "", end="")
            self.__running__ = False
            self.clearQueue()
            exit(0)

    def __threadFunction__(self) -> None:
        '''Runs all callable variables (functions) once'''
        for func in self.__threadArgs__:
            func()
    
    def __loopThreadFunction__(self) -> None:
        '''Runs args[0] through a while loop until QThread stop or termination'''
        while self.__running__:
            self.__threadArgs__[0]()

    def __del__(self) -> None:
        self.threadQueue.queue.clear()
        self.__threadCore__.join()
        print(f"Thread Running '{self.threadName}' Terminated\n" if self.__debugMode__ else "", end="")


class TimeThread:
    def __init__(self, start_on_create:bool=True, **kwargs) -> None:
        '''
        A Thread that runs in the background keeping track of how long the thread's been active\n
        start_on_create # Default: True | Starts the thread upon instantiation
        kwargs:\n
        debug=True # Use only for debugging purposes - prints status outputs for each function called in QThread
        '''
        self.__mainThread__ = QThread(self.__timeTrack__, loop=True, **kwargs)
        self.__clock__ = {
            'seconds': 0,
            'minutes': 0,
            'hours' : 0
        }
        if start_on_create: self.__start__()

    def __start__(self) -> None:
        '''Initializes the TimeThread to start tracking time'''
        self.__mainThread__.start()
    
    def __timeTrack__(self) -> None:
        '''Sleeps for 1 second and tracks the data to the TimeThread's clock variable'''
        time.sleep(1)
        self.__clock__['seconds'] += 1
        self.__clock__['minutes'] += (self.__clock__['seconds'] == 60)
        self.__clock__['hours'] += (self.__clock__['minutes'] == 60)
        self.__clock__['minutes'] %= 60
        self.__clock__['seconds'] %= 60

    def active(self) -> str:
        '''
        Returns a time value in the format [hh:mm:ss]\n
        example return: [03:15:26]
        '''
        return f'[{"{:02d}".format(self.__clock__["hours"])}:{"{:02d}".format(self.__clock__["minutes"])}:{"{:02d}".format(self.__clock__["seconds"])}]'

    def activeRAW(self) -> dict:
        '''
        Returns the clock dictionary with the following information:\n
        clock {
            'seconds': int,
            'minutes': int,
            'hours': int
        }
        '''
        return self.__clock__

    def stop(self) -> None:
        '''Stops the TimeThread'''
        self.__mainThread__.stop()