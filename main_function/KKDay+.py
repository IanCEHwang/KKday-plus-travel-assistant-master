import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import os
from tkinter import scrolledtext
import tkinter.font as tkFont
from date_selection import Calendar  # import class
from datetime import datetime
from tkinter import messagebox
from Web_scraping_currency import Currency, currency_function  # import function(country)
# return nowout, past6out, lowest_day(list), lowest
from Web_scraping_temperature import temperature  # import function(city_input, date1_input, date2_input)
# return highest_out, lowest_out
from Web_scraping_pollution import Get_pollution  # run_pollution(city) => return [list] of pulluction notices
from Web_scraping_safety import safety  # import function
# return answer(not provided) or answerlist(a list)
from Web_scraping_schedule import schedule # import function(kwlist, nolist, SelectCity)
# return answer(not found) or resultList(a list)


class Window(tk.Frame):

	def __init__(self):
		tk.Frame.__init__(self)
		self.grid()
		self.create_widgets()
	
	def input_time_wrong_message_box(self):
			messagebox.showinfo( "錯誤!", "結束日期早於開始日期")

	def combine_func(self):
		self.end_date_str_gain()
		if self.end_date_str.get() == "" or self.date_str.get() == "":
			return
		elif self.check_time(self.date_str.get(),self.end_date_str.get()) == 0:
			self.input_time_wrong_message_box()
			self.combine_func()
		else:
			return 
		
	
	def create_widgets(self):
		f = tkFont.Font(size = 20, family = "Courier New")

		self.dict = {'泰國': ['芭達雅', '普吉島', '曼谷'],
                     '日本': ['東京', '沖繩', '大阪', '京都'],
                     '韓國': ['釜山', '首爾'],
					 '香港': ['香港'],
					 '新加坡': ['新加坡']}
		self.variable1 = tk.StringVar()
		self.variable2 = tk.StringVar()
		self.variable1.set('選擇國家')
		self.variable2.set('選擇城市')
		self.variable1.trace('w', self.updateoptions)
		self.droplist1 = tk.OptionMenu(self, self.variable1, *self.dict.keys(), command=self.getValue())
		self.droplist2 = tk.OptionMenu(self, self.variable2, '', command=self.getValue())

		default1 = "要的行程"
		self.txt1 = tk.Entry(self, bd=1)
		self.txt1.insert(0, default1)
		self.txt1.bind('<FocusIn>', lambda event:self.on_entry_click(self.txt1, default1))
		self.txt1.bind('<FocusOut>', lambda event:self.on_focusout(self.txt1, default1))
		self.txt1.config(fg='grey')
		default2 = "不要的行程"
		self.txt2 = tk.Entry(self, bd=1)
		self.txt2.insert(0, default2)
		self.txt2.bind('<FocusIn>', lambda event:self.on_entry_click(self.txt2, default2))
		self.txt2.bind('<FocusOut>', lambda event:self.on_focusout(self.txt2, default2))
		self.txt2.config(fg='grey')
		

		#開始日期
		self.date_str = tk.StringVar()
		self.date = ttk.Entry(self, textvariable = self.date_str)
		self.date.grid(row = 3, column = 0, columnspan = 5,sticky = 'ew')
		self.date_str_gain = lambda: [
			self.date_str.set(self.date)
			for self.date in [Calendar((500,500),'ur').selection()]
			if self.date]
		tk.Button(self, text = '開始日期', command = self.date_str_gain).grid(row = 3,column = 5, columnspan = 10, sticky = tk.W)
		

		#結束日期
		self.end_date_str = tk.StringVar()
		self.end_date = ttk.Entry(self, textvariable = self.end_date_str)
		self.end_date.grid(row = 3, column = 8, columnspan = 5,sticky = 'ew')
		self.end_date_str_gain = lambda: [
			self.end_date_str.set(self.end_date)
			for self.end_date in [Calendar((500,500),'ur').selection()]
			if self.end_date]
		tk.Button(self, text = '結束日期', command = self.combine_func).grid(row = 3,column = 13, columnspan = 10, sticky = 'W')
		
		

		self.btn1 = tk.Button(self, height=2, width=8, text="Search", command=self.clickBtn, font=f)
		self.cvsMain = tk.Canvas(self, width = 800, height = 600, bg = "white")
	
		
		# self.lbl = tk.Label(self.cvsMain, text=self.List)
		
		self.text = tk.Text(self.cvsMain,width=40,font=("Symbol", 14))
		self.text.insert(tk.INSERT,"天氣")

		
		
		self.droplist1.grid(row=0, column=0, columnspan=8,sticky=tk.E+tk.W)
		self.droplist2.grid(row=0, column=8, columnspan=8,sticky=tk.E+tk.W)
		self.txt1.grid(row=1, column=0, columnspan=16,sticky=tk.E+tk.W)
		self.txt2.grid(row=2, column=0, columnspan=16,sticky=tk.E+tk.W)
		self.btn1.grid(row=2, column=17, rowspan=2, columnspan=6, sticky=tk.E+tk.W)
		self.cvsMain.grid(row=5, column=0, columnspan=18, sticky= tk.NE + tk.SW)
		# self.lbl.grid(row=6, column=0, columnspan=4, sticky=tk.E)
		

		#self.Logo = os.path.join(os.path.dirname())
		self.pic_raw = Image.open('coollogo_com-276451783 3.png')
		zoom =0.4
		pixels_x, pixels_y = tuple([int(zoom * x)  for x in self.pic_raw.size])
		self.pic = ImageTk.PhotoImage(image=self.pic_raw.resize((pixels_x, pixels_y)))
		self.pic_lb = tk.Label(self, image=self.pic)
		self.pic_lb.grid(row=0,column=17,rowspan=2,columnspan=6)
	

	def check_time(self,start,end):  #比較結束時間是否小於開始時間
		start_time = datetime.strptime(start,'%Y-%m-%d')
		end_time = datetime.strptime(end,'%Y-%m-%d')
		if start_time > end_time:
			return 0
		else:
			return 1


	def clickBtn(self): 
		country_to_use = self.variable1.get()
		city_to_use = self.variable2.get()
		start_time = self.date_str.get()
		end_time = self.end_date_str.get()
		kw_list = self.txt1.get()
		no_list = self.txt2.get()
		self.List = [0,0,0,0,0,0]
		self.List[0] = country_to_use       #國家
		self.List[1] = city_to_use          #城市
		self.List[2] = start_time           #開始時間
		self.List[3] = end_time             #結束時間
		if kw_list == '要的行程':
			self.List[4] = ''
		else:
			self.List[4] = kw_list
		if no_list == '不要的行程':
			self.List[5] = ''
		else:
			self.List[5] = no_list

		print(self.List)       #test print
		P_state = self.pollution(self.List[1])
		
		self.cvsMain.create_rectangle(20,30,390,120, outline='darkcyan',fill='darkcyan')
		self.cvsMain.create_text(205,20,fill="darkcyan",font="Times 15 bold", text="當前空氣品質")
		self.cvsMain.create_text(30,45,fill="white",font="Times 10 bold", text=P_state[0], anchor=W)
		self.cvsMain.create_text(30,65,fill="white",font="Times 10 bold", text=P_state[1], anchor=W)
		self.cvsMain.create_text(30,85,fill="white",font="Times 10 bold", text=P_state[2], anchor=W)
		self.cvsMain.create_text(30,105,fill="white",font="Times 10 bold", text=P_state[3], anchor=W)

		#self.lbl_p = tk.Label(self.cvsMain, text='當前空氣品質', borderwidth=1, relief="flat", fg = "coral").grid(row=6, column=0, columnspan=11, sticky=tk.W)
		#self.lbl_p1 = tk.Label(self.cvsMain, text=P_state[1], borderwidth=1, relief="flat", fg = "coral").grid(row=8, column=0, columnspan=11, sticky=tk.W)
		#self.lbl_p2 = tk.Label(self.cvsMain, text=P_state[0], borderwidth=1, relief="flat", fg = "coral").grid(row=7, column=0, columnspan=11, sticky=tk.W)
		#self.lbl_p3 = tk.Label(self.cvsMain, text=P_state[2], borderwidth=1, relief="flat", fg = "coral").grid(row=9, column=0, columnspan=11, sticky=tk.W)
		#self.lbl_p4 = tk.Label(self.cvsMain, text=P_state[3], borderwidth=1, relief="flat", fg = "coral").grid(row=10, column=0, columnspan=11, sticky=tk.W)
		
		now , past6, lowestday, lowest = currency_function(self.List[0])
		self.cvsMain.create_rectangle(415,30,780,120, outline='darkslateblue',fill='darkslateblue')
		self.cvsMain.create_text(600,20,fill="darkslateblue",font="Times 15 bold", text="台幣匯率")
		self.cvsMain.create_text(425,45,fill="white",font="Times 10 bold", text=self.List[0] + '現在的匯率為： ' + str(now), anchor=W)
		self.cvsMain.create_text(425,65,fill="white",font="Times 10 bold", text=self.List[0] + '六個月前的匯率為： ' + str(past6), anchor=W)
		self.cvsMain.create_text(425,85,fill="white",font="Times 10 bold", text=self.List[0] + '六個月以來最低匯率為： ' + str(lowest), anchor=W)
		#self.lbl_c = tk.Label(self.cvsMain, text='台幣匯率', borderwidth=1, relief="flat").grid(row=6, column=12, columnspan=11, sticky=tk.W)
		#self.lbl_c1 = tk.Label(self.cvsMain, text=self.List[0] + '現在的匯率為： ' + str(now), borderwidth=1, relief="flat").grid(row=7, column=12, columnspan=11, sticky=tk.W)
		#self.lbl_c2 = tk.Label(self.cvsMain, text=self.List[0] + '六個月前的匯率為： ' + str(past6), borderwidth=1, relief="flat").grid(row=8, column=12, columnspan=11, sticky=tk.W)
		#self.lbl_c3 = tk.Label(self.cvsMain, text=self.List[0] + '六個月以來最低匯率為： ' + str(lowest), borderwidth=1, relief="flat").grid(row=9, column=12, columnspan=11, sticky=tk.W)

		highest, lowest = temperature(self.List[1], self.List[2], self.List[3])
		self.cvsMain.create_rectangle(20,180,390,270, outline='skyblue',fill='skyblue')
		self.cvsMain.create_text(205,170,fill="skyblue",font="Times 15 bold", text="去年同期氣溫")
		self.cvsMain.create_text(30,195,fill="white",font="Times 10 bold", text=self.List[1] + '所選日期區間最高氣溫： ' + highest, anchor=W)
		self.cvsMain.create_text(30,215,fill="white",font="Times 10 bold", text=self.List[1] + '所選日期區間最低氣溫： ' + lowest, anchor=W)
		#self.lbl_t = tk.Label(self.cvsMain, text='去年同期氣溫', borderwidth=1, relief="flat").grid(row=6, column=24, columnspan=10, sticky=tk.W)
		#self.lbl_t1 = tk.Label(self.cvsMain, text=self.List[1] + '所選日期區間最高氣溫： ' + highest, borderwidth=1, relief="flat").grid(row=7, column=24, columnspan=10, sticky=tk.W)
		#self.lbl_t2 = tk.Label(self.cvsMain, text=self.List[1] + '所選日期區間最低氣溫： ' + lowest, borderwidth=1, relief="flat").grid(row=8, column=24, columnspan=10, sticky=tk.W)

		safety_list = safety(self.List[0])
		self.cvsMain.create_rectangle(415,180,780,270, outline='steelblue',fill='steelblue')
		self.cvsMain.create_text(600,170,fill="steelblue",font="Times 15 bold", text="當前國家安全警示狀況")
		#self.lbl_s = tk.Label(self.cvsMain, text='當前國家安全警示狀況', borderwidth=1, relief="flat").grid(row=6, column=35, columnspan=11, sticky=tk.W)
		#self.lbl_s1 = tk.Label(self.cvsMain, text=safety_list[0], borderwidth=1, relief="flat").grid(row=7, column=35, columnspan=15, sticky=tk.W)
		
		
		for i in range(len(safety_list)):
			try:
				value = safety_list[i]
				if len(value) > 20 :
					self.cvsMain.create_text(425,195,fill="white",font="Times 10 bold", text=value[:20], anchor=W)
					self.cvsMain.create_text(425,215,fill="white",font="Times 10 bold", text=value[21:], anchor=W)
				else:
					self.cvsMain.create_text(425,195+20*i,fill="white",font="Times 10 bold", text=value, anchor=W)
				#self.lbl_s2 = tk.Label(self.cvsMain, text=value, borderwidth=1, relief="flat").grid(row=7 + i, column=35, columnspan=15, sticky=tk.W)
			except ValueError:
				pass
		# try:
		# 	value2 = safety_list[2]
		# 	self.lbl_s3 = tk.Label(self.cvsMain, text=P_state[2], borderwidth=1, relief="flat").grid(row=9, column=35, columnspan=15, sticky=tk.W)
		# self.lbl_p4 = tk.Label(self.cvsMain, text=P_state[3], borderwidth=1, relief="flat").grid(row=10, column=35, columnspan=15, sticky=tk.W)
		
		

		schedule_list = schedule(self.List[4], self.List[5], self.List[1])
		print(schedule_list)
		self.cvsMain.create_rectangle(20,320,780,360, outline='darkslategrey',fill='darkslategrey')
		self.cvsMain.create_rectangle(20,360,780,600, outline='white', fill='white')
		self.cvsMain.create_text(400,340,fill="white",font="Times 22 bold", text="推薦行程")

		

		#self.lbl_sch = tk.Label(self.cvsMain, text='推薦行程', borderwidth=1, relief="flat").grid(row=11, column=0, columnspan=50, sticky=tk.W)
		if not isinstance(schedule_list, str):
			for i in range(len(schedule_list)):
				self.cvsMain.create_text(30,370+(80*i),fill="darkslategrey",font="Times 10 bold", text=schedule_list[i][0], anchor=W)
				self.cvsMain.create_text(30,390+(80*i),fill="darkslategrey",font="Times 10 bold", text=schedule_list[i][1], anchor=W)
				self.cvsMain.create_text(30,410+(80*i),fill="darkslategrey",font="Times 10 bold", text=schedule_list[i][3], anchor=W)
				self.cvsMain.create_text(30,430+(80*i),fill="darkslategrey",font="Times 10 bold", text='', anchor=W)
				#self.lbl_sch1 = tk.Label(self.cvsMain, text=schedule_list[i][0], borderwidth=1, relief="flat").grid(row=12 + (3*i), column=0, columnspan=50, sticky=tk.W)
				#self.lbl_sch2 = tk.Label(self.cvsMain, text=schedule_list[i][1], borderwidth=1, relief="flat").grid(row=13 + (3*i), column=0, columnspan=50, sticky=tk.W)
				#self.lbl_sch3 = tk.Label(self.cvsMain, text=schedule_list[i][3], borderwidth=1, relief="flat").grid(row=14 + (3*i), column=0, columnspan=50, sticky=tk.W)
				#self.lbl_sch4 = tk.Label(self.cvsMain, text='', borderwidth=1, relief="flat").grid(row=15 + (3*i), column=0, columnspan=50, sticky=tk.W)
		else:
			self.cvsMain.create_text(30,370,fill="darkslategrey",font="Times 10 bold", text=schedule_list, anchor=W)
			#self.lbl_sch5 = tk.Label(self.cvsMain, text=schedule_list, borderwidth=1, relief="flat").grid(row=12, column=0, columnspan=50, sticky=tk.W)
		return self.List

		

	def getValue(self):
		pass		


	def on_entry_click(self, entry, text):  # function that gets called whenever entry is clicked
		if entry.cget('fg') == 'grey':
			entry.delete(0, "end") # delete all the text in the entry
			entry.insert(0, '') #Insert blank for user input
			entry.config(fg = 'black')

	def on_focusout(self, entry, text):
		if entry.get() == '':
			entry.insert(0, text)
			entry.config(fg = 'grey')	

	def updateoptions(self, *args):
		countries = self.dict[self.variable1.get()]
		self.variable2.set(countries[0])
		menu = self.droplist2['menu']
		menu.delete(0, 'end')
		for country in countries:
			menu.add_command(label=country, command=lambda country=country: self.variable2.set(country))
	
	#  below combine the web scraping with the GUI
	def pollution(self, city):
		city = self.List[1]
		Pollu = Get_pollution()
		P_state = Pollu.run_pollution(city)
		# print(P_state)
		return P_state
	
	
		

	
		
	
mywindow = Window()
mywindow.master.title("KKDay+")
#print(Window.pollution())



mywindow.mainloop()