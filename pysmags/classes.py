import threading, queue, time, signal, os

class QThread:
    def __init__(self, *args:callable, **kwargs) -> None:
        '''
        args:\n
        * A Callable Function passed as a variable: this function will be called by the thread\n
        * List Arg Functions: (alternate use) example [func0, func0arg0, func0arg1, ..., func0argN], [func1, func1arg0], ..., [funcN, funcNarg0]\n
        \t└── with this you can operate multiple functions with their respective arguments provided within a list\n
        \t└── Do not utilize this functionality if your first arg is not of the list arg function type as it will be ignored\n
        kwargs:\n
        * loop:[bool] # Use to run callable variable 0 (function == args[0]) through a while loop until QThread stop or termination\n
        * debug:[bool] # Use only for debugging purposes - prints status outputs for each function called in QThread\n
        * name:[string] # to name the QThread - default name will be created and set to passed arg[0] function variable name\n
        \t\t\tor arg[0][0] if using list arg functions\n
        '''
        self.__debugMode__ = False;self.__running__ = True;self.__threadCore__ = None;self.__threadArgs__ = args;self.__threadKWArgs__ = kwargs;self.__closing_thread__=False
        self.threadQueue = queue.Queue(); self.__threadActiveType__ = None
        if len(args) > 1:
            self.__threadActiveType__ = 'multi'
            for arg in args:
                if type(arg) != list:
                    print('ERROR')
                    raise Exception("Types provided in QThread are not all of type: list")
            self.threadName = args[0][0].__name__.strip("_")
        elif len(args) == 1:
            self.__threadActiveType__ = 'mono'
            if type(args[0]) == list:
                self.__threadActiveType__ = 'monolist'
                self.threadName = args[0][0].__name__.strip("_")
            else:
                self.threadName = args[0].__name__.strip("_")
        else:
            print("WARNING!!! A THREAD HAS NO RUNNING PROCESS - DEBUG AND OTHER FUNCTIONALITY MAY CRASH THE PROGRAM")
        if 'loop' in kwargs and kwargs['loop'] == True:
            self.__threadCore__ = threading.Thread(target=self.__loopThreadFunction__)
        else:
            self.__threadCore__ = threading.Thread(target=self.__threadFunction__)
        if 'debug' in kwargs and kwargs['debug'] == True: self.__debugMode__ = True
        if 'name' in kwargs: self.threadName = kwargs['name']
        print(f"Thread '{self.threadName}' active type is '{self.__threadActiveType__}'\n" if self.__debugMode__ else "", end="")
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
        try:
            self.__threadCore__.join()
        except Exception as e:
            print(f"Thread Running '{self.threadName}' Unable to Join\n" if self.__debugMode__ else "", end="")

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
        if self.__threadActiveType__ == 'mono':
                self.__threadArgs__[0]()
        elif self.__threadActiveType__ == 'monolist':
            self.__threadArgs__[0][0](*self.__threadArgs__[0][1:])
        elif self.__threadActiveType__ == 'multi':
            for func in self.__threadArgs__:
                func[0](*func[1:])
    
    def __loopThreadFunction__(self) -> None:
        '''Runs args[0] through a while loop until QThread stop or termination'''
        while self.__running__:
            self.__threadArgs__[0]()

    def __del__(self) -> None:
        self.stop()
        print(f"Thread Running '{self.threadName}' Terminated\n" if self.__debugMode__ else "", end="")


class TimeThread:
    def __init__(self, start_on_create:bool=True, **kwargs) -> None:
        '''
        A Thread that runs in the background keeping track of how long the thread's been active\n
        * start_on_create # Default: True | Starts the thread upon instantiation\n
        kwargs:\n
        * debug=True # Use only for debugging purposes - prints status outputs for each function called in QThread\n
        '''
        self.__mainThread__ = QThread(self.__timeTrack__, loop=True, **kwargs)
        self.__clock__ = {
            'seconds': 0,
            'minutes': 0,
            'hours' : 0
        }
        if start_on_create: self.__mainThread__.start()

    def start(self) -> None:
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

class KBThread:
    def __init__(self, stopcode:str="stop", **kwargs) -> None:
        '''
        kwargs: #custom commands you can pass through to the keyboard thread
        example: exfunc=lambda:somefunc()
        '''
        self.__closing_thread__ = False
        self.__mainThread__ = QThread(self.__keyTrack__,loop=True, **kwargs)
        self.stopcode = stopcode
        self.commands = {}
        self.defaultCommands = {
            'help': lambda: self.__helpcommand__(),
            '?': lambda: self.__helpcommand__(),
            'clear': lambda: os.system("cls"),
            'cls': lambda: os.system("cls"),
            # self.stopcode: lambda: self.__mainThread__.stop()
            self.stopcode: lambda: self.stop()
        }
        for kw in kwargs:
            if not kw == 'debug' and not kw == 'loop':
                self.commands[kw] = kwargs[kw]
        self.runCommand = ""
        # signal.signal(signal.SIGINT, self.__handle_sigint__) ### THIS CODE TO FIX CTRL+C EXIT SIGNAL

    def start(self) -> None:
        self.__mainThread__.start()

    def isRunning(self) -> bool:
        if self.__mainThread__.__running__:
            return True
        else:
            return False

    def stop(self) -> None:
        self.__mainThread__.stop()

    def __keyTrack__(self) -> None:
        if self.__mainThread__.__running__:
            self.runCommand = input() # ERROR OCCURS WHILE ATTEMPTING CTRL+C EXIT DUE TO INPUT PREMATURE EXIT
        for command in self.commands:
            if self.runCommand == command:
                self.commands[command]()
                self.runCommand = ""
        for command in self.defaultCommands:
            if self.runCommand == command:
                self.defaultCommands[command]()

    def __helpcommand__(self) -> None:
        print("Available Commands:")
        for cmd in self.defaultCommands:
            print(f"\t-\t{cmd}")
        for cmd in self.commands:
            print(f"\t-\t{cmd}")
        print("_-"*20)
    ### THIS CODE TO FIX CTRL+C EXIT SIGNAL
    # def __handle_sigint__(self, signum, frame) -> None:
    #     '''Handles CTRL+C exit signal'''
    #     if not self.__closing_thread__:
    #         self.__closing_thread__ = True
    #         print(f"Force Shutting Down Thread Running '{self.threadName}'\n" if self.__mainThread__.__debugMode__ else "", end="")
    #         exit(0)