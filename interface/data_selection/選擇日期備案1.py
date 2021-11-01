#時間
import calendar, datetime
from tkinter import *
class Calendar (Canvas):
    # Create the widget
    def __init__ (self, root, *cnf, **kw):
        """
Construct a calendar widget with all the canvas functionality.
Key words are listed in the config function's help.
        """
        try:
            self.levels = kw ["levels"]
            del kw ["levels"]
        except:
            try:
                self.levels = kw ["Levels"]
                del kw ["Levels"]
            except: self.levels = 3
        try:
            self.close = kw ["close_action"]
            del kw ["close_action"]
        except:
            try:
                self.close = kw ["Close_action"]
                del kw ["Close_action"]
            except:
                try:
                    self.close = kw ["close_Action"]
                    del kw ["close_Action"]
                except:
                    try:
                        self.close = kw ["Close_Action"]
                        del kw ["Close_Action"]
                    except: self.close = 2
        self.sup, self.cur, self.root, self.cal, self.year, self.month, self.level, self.added, self.end = super (Calendar, self), [0, 0, 1, datetime.date.today().year, datetime.date.today().month], root, calendar.TextCalendar (), datetime.date.today().year, datetime.date.today().month, 2 if self.levels > 1 else 3, 0, False
        self.sup.__init__ (root, *cnf, **kw)
        self.rect = self.create_rectangle (0, 0, 0, 0)
        self.bind ("<Configure>", lambda event: self.__setup ())
        self.root.bind ("<Up>", lambda event: self.__upLevel ())
        self.root.bind ("<Down>", lambda event: self.__downLevel ())
        self.root.bind ("<Right>", lambda event: self.__down ())
        self.root.bind ("<Left>", lambda event: self.__up ())
    # Give the user an option to reconfigure the calendar
    def config (self, **kw):
        """
Configure the calendar widget.
Key words that are not standard for a tkinter canvas are listed below:

levels=
    Allowed user accuracy of the calendar.
    1 = Month
    2 = Day
    3 = 10 minutes
    The default is 3.
    (levels/Levels)

close_action=
    What happens when user clicks the 'OK' button.
    1 = Remove from the window
    2 = Disable the calendar
    The default is 2.
    (close_action/Close_action/close_Action/Close_Action)
        """
        try:
            self.levels = kw ["levels"]
            del kw ["levels"]
        except:
            try:
                self.levels = kw ["Levels"]
                del kw ["Levels"]
            except: pass
        try:
            self.close = kw ["close_action"]
            del kw ["close_action"]
        except:
            try:
                self.close = kw ["Close_action"]
                del kw ["Close_action"]
            except:
                try:
                    self.close = kw ["close_Action"]
                    del kw ["close_Action"]
                except:
                    try:
                        self.close = kw ["Close_Action"]
                        del kw ["Close_Action"]
                    except: pass
        if 4 - self.levels > self.level: self.level = 4 - self.levels
        self.sup.config (**kw)
        self.__setup ()
    # Draw the calendar on the canvas
    def __setup (self):
        self.root.update ()
        width, height = self.winfo_width (), self.winfo_height ()
        if height < 80: height = 80
        if width < 120: width = 120
        self.delete (ALL)
        if self.level != 3:
            a = [self.create_polygon ((40, 0), (width - 40, 0), (width - 20, 20), (20, 20), fill = "red", outline = "black"),
                 self.create_line (int (width / 2) - 10, 15, int (width / 2), 5, width = 2),
                 self.create_line (int (width / 2) + 10, 15, int (width / 2), 5, width = 2)]
            for i in a: self.tag_bind (i, "<Button-1>", lambda event: self.__upLevel ())
        if self.level != 4 - self.levels:
            a = [self.create_polygon ((40, height), (width - 40, height), (width - 20, height - 20), (20, height - 20), fill = "red", outline = "black"),
                 self.create_line (int (width / 2) - 10, height - 15, int (width / 2), height - 5, width = 2),
                 self.create_line (int (width / 2) + 10, height - 15, int (width / 2), height - 5, width = 2)]
            for i in a: self.tag_bind (i, "<Button-1>", lambda event: self.__downLevel ())
        a = [self.create_polygon ((0, 40), (20, 20), (20, height - 20), (0, height - 40), fill = "red", outline = "black"),
             self.create_line (15, int (height / 2) - 10, 5, int (height / 2), width = 2),
             self.create_line (15, int (height / 2) + 10, 5, int (height / 2), width = 2)]
        for i in a: self.tag_bind (i, "<Button-1>", lambda event: self.__up ())
        a = [self.create_polygon ((width, 40), (width - 20, 20), (width - 20, height - 20), (width, height - 40), fill = "red", outline = "black"),
             self.create_line (width - 15, int (height / 2) - 10, width - 5, int (height / 2), width = 2),
             self.create_line (width - 15, int (height / 2) + 10, width - 5, int (height / 2), width = 2)]
        for i in a: self.tag_bind (i, "<Button-1>", lambda event: self.__down ())
        a = [self.create_polygon ((35, height - 20), (width - 35, height - 20), (width - 55, height - 40), (55, height - 40), fill = "red", outline = "black"),
             self.create_text (int (width / 2), height - 30, text = "OK")]
        for i in a: self.tag_bind (i, "<Button-1>", lambda event: self.__ok ())
        if self.level == 3:
            if width - 40 < height - 80: self.height, self.width = (width - 40) / 4, (width - 40) / 3
            else: self.width, self.height = (height - 80) / 3, (height - 80) / 4
            self.create_text (int (width / 2), 30, text = str (self.cur [3]))
            font = ("Courier New", int (self.height * 0.45 - 1))
            if font [1] < 1: font  = ("Courier New", 1)
            for y in range (4):
                for x in range (3):
                    b = [self.create_rectangle (x * self.width + 20, y * self.height + 40, x * self.width + self.width + 20, y * self.height + self.height + 40, fill = "white"),
                         self.create_text (x * self.width + (self.width / 2) + 20, y * self.height + (self.height / 2) + 40, text = calendar.month_abbr [y * 3 + x + 1], font = font)]
                    for i in b: self.tag_bind (i, "<Button-1>", lambda event, x = x, y = y: self.__click (y, x, None))
                    if y * 3 + x + 1 == self.cur [4]: self.__click (y, x, None)
        elif self.level == 2:
            self.rows = len (self.cal.monthdayscalendar (*self.cur [3 : ]))
            if width - 40 < height - 80: self.height, self.width = (width - 40) / self.rows, (width - 40) / 7
            else: self.width, self.height = (height - 80) / 7, (height - 80) / self.rows
            font = ("Courier New", int (self.height * 0.45))
            self.create_text (int (width / 2), 30, text = calendar.month_name [self.cur [4]] + " " + str (self.cur [3]))
            if font [1] < 1: font = ("Courier New", 1)
            for w, week in enumerate (self.cal.monthdayscalendar (*self.cur [3 : ])):
                for d, day in enumerate (week):
                    if day:
                        b = [self.create_rectangle (d * self.width + 20, w * self.height + 40, d * self.width + self.width + 20, w * self.height + self.height + 40, fill = "white"),
                             self.create_text (d * self.width + (self.width / 2) + 20, w * self.height + (self.height / 2) + 40, text = day, font = font)]
                        for i in b: self.tag_bind (i, "<Button-1>", lambda event, w = w, d = d, day = day: self.__click (w, d, day))
                    if day == self.cur [2]: self.__click (w, d, day)
        else:
            if width - 40 < height - 80: self.height, self.width = (width - 40) / 24, (width - 40) / 6
            else: self.width, self.height = (height - 80) / 6, (height - 80) / 24
            font = ("Courier New", int (self.height * 0.45 - 1))
            self.create_text (int (width / 2), 30, text = "%s %s %s" % (self.__dayToPosition (self.cur [2]), calendar.month_name [self.cur [4]], str (self.cur [3])))
            if font [1] < 1: font  = ("Courier New", 1)
            for h in range (24):
                for m in range (0, 6):
                    b = [self.create_rectangle (m * self.width + 20, h * self.height + 40, m * self.width + self.width + 20, h * self.height + self.height + 40, fill = "white"),
                         self.create_text (m * self.width + (self.width / 2) + 20, h * self.height + (self.height / 2) + 40, text = "%s:%s" % (h if h >= 10 else "0" + str (h), m * 10 if m > 0 else "00"), font = font)]
                    for i in b: self.tag_bind (i, "<Button-1>", lambda event, h = h, m = m: self.__click (h, m, None))
                    if h == self.cur [1] and m * 10 == self.cur [0]: self.__click (h, m , None)
        if self.end:
            self.tag_bind (ALL, "<Button-1>", lambda event: None)
            self.create_rectangle (0, 0, width, height, fill = "black", stipple = "gray50")
    # Format and return the selected date (and time)
    def get (self):
        """
Get the day selected by the user
        """
        cur = self.cur
        a = cur [4]
        cur [4] = cur [3]
        cur [3] = a
        cur.insert (3, calendar.month_abbr [a])
        cur.insert (2, calendar.day_abbr [datetime.datetime (cur [5], cur [4], cur [2]).weekday ()])
        cur [0] = "%s:%s" % (cur [1] if cur [1] >= 10 else "0" + str (cur [1]), cur [0] if cur [0] >= 10 else "0" + str (cur [0]))
        del cur [1]
        return cur [6 - self.levels * 2 : ]
    # Handle the mouse clicks
    def __click (self, w, d, day):
        self.delete (self.rect)
        self.rect = self.create_rectangle (d * self.width + 21, w * self.height + 41, d * self.width + self.width + 20, w * self.height + self.height + 40, fill = "red", stipple = "gray25", width = 0),
        if self.level == 3: self.cur = [self.cur [0], self.cur [1], self.cur [2], self.cur [3], w * 3 + d + 1]
        elif self.level == 2: self.cur = [self.cur [0], self.cur [1], day, self.cur [3], self.cur [4]]
        else: self.cur = [d * 10, w, self.cur [2], self.cur [3], self.cur [4]]
    # Move the calendar
    def __up (self):
        if self.level == 3: self.cur [3] -= 1
        elif self.level == 2:
            self.cur [4] -= 1
            if self.cur [4] < 1: self.cur = [self.cur [0], self.cur [1], self.cur [2], self.cur [3] - 1, 12]
        else:
            self.cur [2] -= 1
            if self.cur [2] < 1: self.cur = [self.cur [0], self.cur [1], calendar.monthrange (self.cur [3], self.cur [4] - 1 if self.cur [4] - 1 > 0 else 12) [1], self.cur [3], self.cur [4] - 1]
            if self.cur [4] < 1: self.cur = [self.cur [0], self.cur [1], self.cur [2], self.cur [3] - 1, 12]
        self.__setup ()
    def __down (self):
        if self.level == 3: self.cur [3] += 1
        elif self.level == 2:
            self.cur [4] += 1
            if self.cur [4] > 12: self.cur = [self.cur [0], self.cur [1], self.cur [2], self.cur [3] + 1, 1]
        else:
            self.cur [2] += 1
            if self.cur [2] > calendar.monthrange (self.cur [3], self.cur [4]) [1]: self.cur = [self.cur [0], self.cur [1], 1, self.cur [3], self.cur [4] + 1]
            if self.cur [4] > 12: self.cur = [self.cur [0], self.cur [1], self.cur [2], self.cur [3] + 1, 1]
        self.__setup ()
    # Move calendar level
    def __upLevel (self):
        if self.level < 3:
            self.level += 1
            self.__setup ()
    def __downLevel (self, release = False):
        if self.level > 4 - self.levels:
            self.level -= 1
            self.__setup ()
    # Format a number to named position (e.g. 1 -> 1st)
    def __dayToPosition (self, num):
        if num > 9 and str(num) [-2] == '1': return str (num) + 'th'
        lastDigit = num % 10
        if (lastDigit == 1): return str (num) + 'st'
        elif (lastDigit == 2): return str (num) + 'nd'
        elif (lastDigit == 3): return str (num) + 'rd'
        else: return str (num) + 'th'
    # Handle when the user clicks ok
    def __ok (self):
        if self.close == 1:
            if self.added == 1: self.pack_remove ()
            elif self.added == 2: self.grid_remove ()
            elif self.added == 3: self.place_remove ()
        elif self.added == 2:
            self.end = True
            self.__setup ()
    # The demonstration method
    def demo ():
        """
This method is a demostration of the widget. It creates it's own 'Tk' app to put it on.
        """
        root = Tk ()
        root.title ("Calendar Demo")
        c = Calendar (root)
        c.grid (sticky = "nsew")
        #help (Calendar)
        root.mainloop ()
        print (c.get ())
    # Configure the geometry managers
    def pack (self, *cnf, **kw):
        self.added = 1
        self.sup.pack (*cnf, **kw)
        self.__setup ()
    def pack_configure (self, *cnf, **kw):
        self.sup.pack_configure (*cnf, **kw)
        self.__setup ()
    def grid (self, *cnf, **kw):
        self.sup.grid (*cnf, **kw)
        coords, self.added = [(child.grid_info () ["column"], child.grid_info () ["row"]) for child in self.root.children.values () if child == self] [0], 2
        try: [Grid.columnconfigure (self.root, coords [0] + x, weight = 1) for x in range (kw ["columnspan"])]
        except KeyError: Grid.columnconfigure (self.root, coords [0], weight = 1)
        try: [Grid.rowconfigure (self.root, coords [1] + y, weight = 1) for y in range (kw ["rowspan"])]
        except KeyError: Grid.rowconfigure (self.root, coords [1], weight = 1)
        self.__setup ()
    def grid_configure (self, *cnf, **kw):
        self.sup.grid_configure (*cnf, **kw)
        self.__setup ()
    def place (self, *cnf, **kw):
        self.added = 3
        self.sup.place (*cnf, **kw)
        self.__setup ()
    def place_configure (self, *cnf, **kw):
        self.sup.place_configure (*cnf, **kw)
        self.__setup ()
if __name__ == "__main__": Calendar.demo ()
