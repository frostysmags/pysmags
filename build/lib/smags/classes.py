import threading, queue, time, signal, sys

class QThread:
    def __init__(self, *args:list[callable], **kwargs) -> None:
        self.__debugMode__ = False
        self.__displayDebug__ = False
        self.__running__ = True
        self.__threadCore__ = None
        self.threadQueue = queue.Queue()
        self.__threadArgs__ = args
        self.__threadKWArgs__ = kwargs
        self.threadName = args[0].__name__
        signal.signal(signal.SIGINT, self.__handle_sigint__)
        if 'loop' in kwargs and kwargs['loop'] == True:
            self.__threadCore__ = threading.Thread(target=self.__loopThreadFunction__)
        else:
            self.__threadCore__ = threading.Thread(target=self.__threadFunction__)
        if 'debug' in kwargs and kwargs['debug'] == [True]:
            self.__debugMode__ = True
        if 'debug' in kwargs and kwargs['debug'] == [True, True]:
            self.__debugMode__ = True
            self.__displayDebug__ = True
        
    def clearQueue(self) -> str:
        print(f"Cleared Queue of Thread Running '{self.threadName}'\n" if self.__debugMode__ and self.__displayDebug__ else "", end="")
        self.threadQueue.queue.clear()
        return f"Cleared Queue of Thread Running '{self.threadName}'" if self.__debugMode__ else None

    def start(self) -> str:
        print(f"Starting Thread Running '{self.threadName}\n'" if self.__debugMode__ and self.__displayDebug__ else "", end="")
        self.__threadCore__.start()
        return f"Starting Thread Running '{self.threadName}'" if self.__debugMode__ else None

    def stop(self) -> str:
        print(f"Stopping Thread Running '{self.threadName}'\n" if self.__debugMode__ and self.__displayDebug__ else "", end="")
        self.__running__ = False
        self.threadQueue.queue.clear()
        self.__threadCore__.join()
        return f"Stopping Thread Running '{self.threadName}'" if self.__debugMode__ else None
    
    def __handle_sigint__(self, signum, frame):
        self.__running__ = False
        self.threadQueue.queue.clear()
        sys.exit()

    def __threadFunction__(self) -> None:
        self.__threadArgs__[0]()
    
    def __loopThreadFunction__(self) -> None:
        while self.__running__:
            self.__threadArgs__[0]()

    def __del__(self) -> str:
        print(f"Thread Running '{self.threadName}' Terminated\n" if self.__debugMode__ and self.__displayDebug__ else "", end="")
        self.threadQueue.queue.clear()
        self.__threadCore__.join()
        return f"Thread Running '{self.threadName}' Terminated" if self.__debugMode__ else None


class TimeThread:
    def __init__(self, **kwargs) -> None:
        '''
        use one of the following kwargs if applicable\n
        debug=True # Allows debugging with selective debugging\n
        debug=[True, True] # Displays all debugs by default\n
        '''
        self.__mainThread__ = QThread(self.timeTrack, loop=True, **kwargs)
        self.__clock__ = {
            'seconds': 0,
            'minutes': 0,
            'hours' : 0
        }
        self.__start__()

    def __start__(self):
        self.__mainThread__.start()
    
    def timeTrack(self):
        time.sleep(1)
        # self.__clock__['seconds'] += 1
        # if self.__clock__['seconds'] % 60:
        #     self.__clock__['seconds'] = 0
        #     self.__clock__['minutes'] += 1
        # if self.__clock__['minutes'] % 60:
        #     self.__clock__['minutes'] = 0
        #     self.__clock__['hours'] += 1
        self.clock['seconds'] += 1
        self.clock['minutes'] += (self.clock['seconds'] == 60)
        self.clock['hours'] += (self.clock['minutes'] == 60)
        self.clock['minutes'] %= 60
        self.clock['seconds'] %= 60
    
    def active(self):
        return f'[{"{:02d}".format(self.__clock__["hours"])}:{"{:02d}".format(self.__clock__["minutes"])}:{"{:02d}".format(self.__clock__["seconds"])}]'

    def activeRAW(self):
        return self.__clock__

    def stop(self):
        self.__mainThread__.stop()