
import calendar
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk

datetime = calendar.datetime.datetime
timedelta = calendar.datetime.timedelta

class Calendar():

    def __init__(self, point = None, position = None):
        # point    提供一個基點，來確定窗口位置
        # position 窗口在點的位置 'ur'-右上, 'ul'-左上, 'll'-左下, 'lr'-右下
        #self.master = tk.Tk()
        self.master = tk.Toplevel()
        self.master.withdraw()
        fwday = calendar.SUNDAY

        year = datetime.now().year
        month = datetime.now().month
        locale = None
        sel_bg = '#ecffc4'
        sel_fg = '#05640e'

        self._date = datetime(year, month, 1)
        self._selection = None # 設置為未選中日期

        self.G_Frame = ttk.Frame(self.master)

        self._cal = self.__get_calendar(locale, fwday)

        self.__setup_styles()       # 創建自定義函式
        self.__place_widgets()      # pack/grid 小部件
        self.__config_calendar()    # 調整日曆列和安裝標示
        # 配置畫布和正確綁定，以設定日期
        self.__setup_selection(sel_bg, sel_fg)

        # 儲存項ID，用於稍后插入。
        self._items = [self._calendar.insert('', 'end', values='') for _ in range(6)]

        #在當前空日曆插入日期
        self._update()

        self.G_Frame.pack(expand = 1, fill = 'both')
        self.master.overrideredirect(1)
        self.master.update_idletasks()
        width, height = self.master.winfo_reqwidth(), self.master.winfo_reqheight()
        if point and position:
            if   position == 'ur': x, y = point[0], point[1] - height
            elif position == 'lr': x, y = point[0], point[1]
            elif position == 'ul': x, y = point[0] - width, point[1] - height
            elif position == 'll': x, y = point[0] - width, point[1]
        else: x, y = (self.master.winfo_screenwidth() - width)/2, (self.master.winfo_screenheight() - height)/2
        self.master.geometry('%dx%d+%d+%d' % (width, height, x, y)) #窗口位置居中
        self.master.after(300, self._main_judge)
        self.master.deiconify()
        self.master.focus_set()
        self.master.wait_window() #這裡應該使用wait_window掛起窗口，如果使用mainloop,可能會導致主程序很多錯誤

    def __get_calendar(self, locale, fwday):
        # 實例化適當的日曆列
        if locale is None:
            return calendar.TextCalendar(fwday)
        else:
            return calendar.LocaleTextCalendar(fwday, locale)

    def __setitem__(self, item, value):
        if item in ('year', 'month'):
            raise AttributeError("attribute '%s' is not writeable" % item)
        elif item == 'selectbackground':
            self._canvas['background'] = value
        elif item == 'selectforeground':
            self._canvas.itemconfigure(self._canvas.text, item=value)
        else:
            self.G_Frame.__setitem__(self, item, value)

    def __getitem__(self, item):
        if item in ('year', 'month'):
            return getattr(self._date, item)
        elif item == 'selectbackground':
            return self._canvas['background']
        elif item == 'selectforeground':
            return self._canvas.itemcget(self._canvas.text, 'fill')
        else:
            r = ttk.tclobjs_to_py({item: ttk.Frame.__getitem__(self, item)})
            return r[item]

    def __setup_styles(self):
        # 自定義TTK風格
        style = ttk.Style(self.master)
        arrow_layout = lambda dir: (
            [('Button.focus', {'children': [('Button.%sarrow' % dir, None)]})]
        )
        style.layout('L.TButton', arrow_layout('left'))
        style.layout('R.TButton', arrow_layout('right'))

    def __place_widgets(self):
        # 標頭框架及其小部件
        Input_judgment_num = self.master.register(self.Input_judgment)  # 將函数包装一下
        hframe = ttk.Frame(self.G_Frame)
        gframe = ttk.Frame(self.G_Frame)
        bframe = ttk.Frame(self.G_Frame)
        hframe.pack(in_=self.G_Frame, side='top', pady=5, anchor='center')
        gframe.pack(in_=self.G_Frame, fill=tk.X, pady=5)
        bframe.pack(in_=self.G_Frame, side='bottom', pady=5)

        lbtn = ttk.Button(hframe, style='L.TButton', command=self._prev_month)
        lbtn.grid(in_=hframe, column=0, row=0, padx=12)
        rbtn = ttk.Button(hframe, style='R.TButton', command=self._next_month)
        rbtn.grid(in_=hframe, column=5, row=0, padx=12)
        
        self.CB_year = ttk.Combobox(hframe, width = 5, values = [str(year) for year in range(datetime.now().year, datetime.now().year-11,-1)], validate = 'key', validatecommand = (Input_judgment_num, '%P'))
        self.CB_year.current(0)
        self.CB_year.grid(in_=hframe, column=1, row=0)
        self.CB_year.bind('<KeyPress>', lambda event:self._update(event, True))
        self.CB_year.bind("<<ComboboxSelected>>", self._update)
        tk.Label(hframe, text = '年', justify = 'left').grid(in_=hframe, column=2, row=0, padx=(0,5))

        self.CB_month = ttk.Combobox(hframe, width = 3, values = ['%02d' % month for month in range(1,13)], state = 'readonly')
        self.CB_month.current(datetime.now().month - 1)
        self.CB_month.grid(in_=hframe, column=3, row=0)
        self.CB_month.bind("<<ComboboxSelected>>", self._update)
        tk.Label(hframe, text = '月', justify = 'left').grid(in_=hframe, column=4, row=0)

        # 日曆部件
        self._calendar = ttk.Treeview(gframe, show='', selectmode='none', height=7)
        self._calendar.pack(expand=1, fill='both', side='bottom', padx=5)

        ttk.Button(bframe, text = "確 定", width = 6, command = lambda: self._exit(True)).grid(row = 0, column = 0, sticky = 'ns', padx = 20)
        ttk.Button(bframe, text = "取 消", width = 6, command = self._exit).grid(row = 0, column = 1, sticky = 'ne', padx = 20)
        
        
        tk.Frame(self.G_Frame, bg = '#565656').place(x = 0, y = 0, relx = 0, rely = 0, relwidth = 1, relheigh = 2/200)
        tk.Frame(self.G_Frame, bg = '#565656').place(x = 0, y = 0, relx = 0, rely = 198/200, relwidth = 1, relheigh = 2/200)
        tk.Frame(self.G_Frame, bg = '#565656').place(x = 0, y = 0, relx = 0, rely = 0, relwidth = 2/200, relheigh = 1)
        tk.Frame(self.G_Frame, bg = '#565656').place(x = 0, y = 0, relx = 198/200, rely = 0, relwidth = 2/200, relheigh = 1)

    def __config_calendar(self):
        # cols = s._cal.formatweekheader(3).split()
        cols = ['日','一','二','三','四','五','六']
        self._calendar['columns'] = cols
        self._calendar.tag_configure('header', background='grey90')
        self._calendar.insert('', 'end', values=cols, tag='header')
        # 調整其列寬
        font = tkFont.Font()
        maxwidth = max(font.measure(col) for col in cols)
        for col in cols:
            self._calendar.column(col, width=maxwidth, minwidth=maxwidth,
                anchor='center')

    def __setup_selection(self, sel_bg, sel_fg):
        def __canvas_forget(evt):
            canvas.place_forget()
            self._selection = None

        self._font = tkFont.Font()
        self._canvas = canvas = tk.Canvas(self._calendar, background=sel_bg, borderwidth=0, highlightthickness=0)
        canvas.text = canvas.create_text(0, 0, fill=sel_fg, anchor='w')

        canvas.bind('<Button-1>', __canvas_forget)
        self._calendar.bind('<Configure>', __canvas_forget)
        self._calendar.bind('<Button-1>', self._pressed)

    def _build_calendar(self):
        year, month = self._date.year, self._date.month

        # update header text (Month, YEAR)
        self.header = self._cal.formatmonthname(year, month, 0)

        # 更新日曆顯示的日期
        cal = self._cal.monthdayscalendar(year, month)
        for indx, item in enumerate(self._items):
            week = cal[indx] if indx < len(cal) else []
            fmt_week = [('%02d' % day) if day else '' for day in week]
            self._calendar.item(item, values=fmt_week)

    def _show_select(self, text, bbox):
        #"""為新的選擇配置畫布。"""
        x, y, width, height = bbox

        textw = self._font.measure(text)

        canvas = self._canvas
        canvas.configure(width = width, height = height)
        canvas.coords(canvas.text, (width - textw)/2, height / 2 - 1)
        canvas.itemconfigure(canvas.text, text=text)
        canvas.place(in_=self._calendar, x=x, y=y)

    def _pressed(self, evt = None, item = None, column = None, widget = None):
        #"""在日曆的某個地方點擊。"""
        if not item:
            x, y, widget = evt.x, evt.y, evt.widget
            item = widget.identify_row(y)
            column = widget.identify_column(x)

        if not column or not item in self._items:
            # 在工作日行中單擊或僅在列外單擊。
            return

        item_values = widget.item(item)['values']
        if not len(item_values): # 這個月的行是空的。
            return

        text = item_values[int(column[1]) - 1]
        if not text: # 日期為空
            return

        bbox = widget.bbox(item, column)
        if not bbox: # 日曆尚不可見
            self.master.after(20, lambda : self._pressed(item = item, column = column, widget = widget))
            return

        # 更新，然後顯示選擇
        text = '%02d' % text
        self._selection = (text, item, column)
        self._show_select(text, bbox)

    def _prev_month(self):
        #"""更新日曆以顯示前一個月。"""
        self._canvas.place_forget()
        self._selection = None

        self._date = self._date - timedelta(days=1)
        self._date = datetime(self._date.year, self._date.month, 1)
        self.CB_year.set(self._date.year)
        self.CB_month.set(self._date.month)
        self._update()

    def _next_month(self):
        #"""更新日曆以顯示下一個月。"""
        self._canvas.place_forget()
        self._selection = None

        year, month = self._date.year, self._date.month
        self._date = self._date + timedelta(
            days=calendar.monthrange(year, month)[1] + 1)
        self._date = datetime(self._date.year, self._date.month, 1)
        self.CB_year.set(self._date.year)
        self.CB_month.set(self._date.month)
        self._update()

    def _update(self, event = None, key = None):
        #"""刷新界面"""
        if key and event.keysym != 'Return': return
        year = int(self.CB_year.get())
        month = int(self.CB_month.get())
        if year == 0 or year > 9999: return
        self._canvas.place_forget()
        self._date = datetime(year, month, 1)
        self._build_calendar() # 重建日曆

        if year == datetime.now().year and month == datetime.now().month:
            day = datetime.now().day
            for _item, day_list in enumerate(self._cal.monthdayscalendar(year, month)):
                if day in day_list:
                    item = 'I00' + str(_item + 2)
                    column = '#' + str(day_list.index(day)+1)
                    self.master.after(100, lambda :self._pressed(item = item, column = column, widget = self._calendar))

    def _exit(self, confirm = False):
        #"""退出窗口"""
        if not confirm: self._selection = None
        self.master.destroy()

    def _main_judge(self):
        #"""判斷窗口是否在最頂層"""
        #try:
            #s.master 為 TK 窗口
            #if not s.master.focus_displayof(): s._exit()
            #else: s.master.after(10, s._main_judge)

            #s.master 为 toplevel 窗口
        #    if s.master.focus_displayof() == None or 'toplevel' not in str(self.master.focus_displayof()): self._exit()
        #    else: s.master.after(10, self._main_judge)
        #except:
        self.master.after(10, self._main_judge)

        #s.master.tk_focusFollowsMouse() # 焦點跟随鼠標

    def selection(self):
        #"""返回表示當前選定日期的日期時間。"""
        if not self._selection: return None

        year, month = self._date.year, self._date.month
        #print(str(datetime(year, month, int(self._selection[0])))[:10])
        return str(datetime(year, month, int(self._selection[0])))[:10]

    def Input_judgment(self, content):
        #"""输入判斷"""
        if content.isdigit() or content == "":
            return True
        else:
            return False



def run_calendar(name):
    root = tk.Tk()
    given_name=name
    date_str = tk.StringVar()
    date = ttk.Entry(root, textvariable = date_str)
    date.grid(row = 0 , column = 10, columnspan = 10)
    #date.place(x = 0, y = 0, relx = 5/20, rely = 1/6, relwidth = 14/20, relheigh = 2/3)

    date_str_gain = lambda: [
        date_str.set(date)
        for date in [Calendar((), 'ur').selection()] #calendar(x,y)控制日曆位置
        if date]
    tk.Button(root, text = given_name, command = date_str_gain).grid(row = 0, column = 20, columnspan=10)
    root.mainloop()

#run_calendar('開始日期')


