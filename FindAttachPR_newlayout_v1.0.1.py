# findpdf.py

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox, ttk
import os
from PyPDF2 import PdfFileReader
import requests
s

# Color
bg='#323333' #ตั้งค่า default สีพื้นหลังได้
fg='#f2f2f2' #ตั้งสีเพิ่มได้

# Font
f1 = ('Browalia New',30)
f2 = (None,12)
f3 = ('Angsana New', 14)


GUI = Tk()
GUI.geometry('800x500+400+100') #กว้างxยาว+ตำแหน่งแนวนอน+ตำแหน่งแนวตั้ง
# GUI.configure(background=bg) #นำ default สีพื้นหลังมาใช้
# GUI.state('zoomed')
GUI.title('โปรแกรมเสริม V1.0.1')

####### Tab setting ##############################################################
Tab = ttk.Notebook(GUI)
Tab.pack(fill=BOTH,expand=1)

T1 = Frame(Tab)
T2 = Frame(Tab)
T3 = Frame(Tab)

icon_tab1 = PhotoImage(file='tab1.png')
icon_tab2 = PhotoImage(file='tab2.png')

Tab.add(T1, text='ค้นหาไฟล์แนบ', image=icon_tab1, compound='left')
Tab.add(T2, text='จัดการผู้ใช้งาน', image=icon_tab2, compound='left')


##################################################################################

# WW = GUI.winfo_screenwidth() #กำหนดให้ GUI แสดงตามขนาดความกว้างหน้าจอที่รันจริง
# WH = GUI.winfo_screenwidth() ##กำหนดให้ GUI แสดงตามขนาดความสูงหน้าจอที่รันจริง

GUI.attributes('-fullscreen',False)
GUI.bind('<F10>', lambda event: GUI.attributes('-fullscreen', not GUI.attributes('-fullscreen')))

# print(GUI.winfo_screenwidth()) #ดูขนาดความกว้างหน้าจอของเครื่องที่ terminal
# print(GUI.winfo_screenheight()) #ดูขนาดความสูงหน้าจอของเครื่องที่ terminal
# canvas = Canvas(GUI,width=WW,height=WH,background=bg) #canvas คือ widget ตัวนึงมาแปะที่ GUI
# canvas.configure(bd=0,relief='ridge',highlightthickness=0) #เซ็ตให้ canvas ไม่มีขอบสีขาว
# canvas.place(x=0,y=0) #เราจะใช้ widget canvas เป็นหน้าโปรแกรมไม่เกี่ยวกับ GUI ที่เป็นพื้นจอ

def FrameRect(x,y,width=200,height=200,fill=False): #สร้างฟังก์ชันของเฟรมเพื่อใช้งานได้หลายครั้ง
	if fill: #ถ้า Fill เป็น true
		frame1 = canvas.create_rectangle(0,0,width,height,outline=fg,width=1,fill=fg)
	else:
		frame1 = canvas.create_rectangle(0,0,width,height,outline=fg,width=1) #สร้างสีเหลี่ยม ใส่สีได้โดยเพิ่ม fill='blue'
	canvas.move(frame1,x,y) #dot move คือ ต้องการวางสีเหลี่ยมจำแหน่งใด หรือถ้าระบุเป็นศูนย์ ต้องไประบุด้านบนแทน

# สร้างฟังก์ชัน Text เฉพาะตัว
def FixedText(x,y,text='fixed text',font=f2,Color=fg):
	L1 = Label(T1,text=text,font=f2)
	# L1.place(x=x,y=y)
	L1.pack(ipady=10, pady=5)

FixedText(220,10,'--- ค้นหาไฟล์แนบ PR ---') #ใส่ Info User

# Entry สร้างช่องค้นหาไฟล์แนบ
v_search = StringVar()
E1 = Entry(T1,textvariable=v_search,font=('Angsana New',22),width=50)
E1.configure(insertbackground=fg) #สร้างช่อง search
E1.configure(highlightthickness=2, highlightbackground=fg,highlightcolor=fg) #ตั้งค่าช่องเป็นสี
# E1.place(x=50,y=50)
E1.pack(ipadx=50,ipady=5,pady=30)

v_namefile = StringVar()
namefile = '--- Result ---'
v_namefile.set(namefile)
namefileinfo = Label(T1,textvariable=v_namefile,fg='blue',font=(None,14))
namefileinfo.pack()

def finding():

	showtxt = 'ค้นหาไฟล์    '

	# กำหนดพาทที่จะค้นหาไฟล์
	firstdir = "เช่น //192.168.0.1/ABC/attachfile"

	# ตัวแปร keyword รับค่าจากช่องค้นหา
	keyword = v_search.get()
	v_namefile.set(showtxt+keyword)
	print('Please wait searching file.....',keyword)

	# for loop ค้นหาไฟล์
	for root, dirs, files in os.walk(firstdir):
		# print(files)

		# นำตัวแปร keyword ไปค้นหาในตัวแปร files
		if keyword in files:
			# ถ้าพบไฟล์ที่ค้นหาแล้ว popup แจ้ง
			openfile = messagebox.askokcancel('Search File','พบไฟล์ที่คุณต้องการแล้ว คุณต้องการบันทึกไฟล์นี้หรือไม่ ?')
			# messagebox ถามความต้องการบันทึกไฟล์ที่พบ
			# ถ้าตอบ yes ให้ดาวน์โหลดไฟล์มาเก็บที่ไดร์ฟ D
			if openfile == True:
				# กำหนดพาทที่อยู่ไฟล์ attach และนำคีย์เวิร์ดชื่อไฟล์ที่จะค้นหามาใส่ต่อท้าย
				url = "เช่น //192.168.0.1/ABC/attachfile/"+keyword
				
				# กำหนดพาทไดร์ฟ D เพื่อเป็นที่ save ไฟล์ defualt เป็นเครื่องผู้ใช้งาน
				pathdir = 'D:/'
				# join path เพื่อให้ไฟล์สามารถเข้าถึงพาทปลายทางที่กำหนดได้
				destpath = os.path.join(pathdir,keyword)
				# กำหนดตัวแปร f อ่านไฟล์ และกำหนดตัวแปร w บันทึกไฟล์ไดร์ฟ D ของผู้ใช้งาน
				with open(url,'rb') as f, open(destpath,'wb') as w:
					# กำหนดตัวแปร block เช็คขนาดไฟล์
					while True:
						block = f.read(16*1024)
						if not block:
							break
						w.write(block)
				messagebox.showinfo('บันทึกไฟล์สำเร็จ','บันทึกไฟล์เรียบร้อย ตรวจสอบไฟล์ในคอมพิวเตอร์คุณที่ไดร์ฟ D: ')
				ResetFinding()
				print('Save file success!!!')
			else:
				ResetFinding()
				print('OK You cannot download file')
		else:
			openfile = messagebox.showerror('Search File Error','ไม่พบไฟล์ที่คุณต้องการ กรุณาตรวจสอบชื่อไฟล์อีกครั้ง')
			ResetFinding()
			print('file not found...')

# สร้างฟังก์ชัน reset ค่า result
def ResetFinding():
	v_namefile.set('--- Result ---')


B1 = Button(T1,text='ค้นหา',command=finding)
B1.pack(ipadx=30,ipady=10,pady=30)

######### แท็บโปรแกรมจัดการ user JDE ###########

L2 = Label(T2,text='จัดการผู้ใช้งานระบบ', font=('Angsana New',22))
L2.pack()




GUI.mainloop()