from tkinter import * 
from tkinter import ttk,messagebox  
import csv #บันทึกลงcsv
from datetime import datetime 


GUI = Tk()
GUI.title('โปรแกรมบันทึกค่าใช้จ่าย')
GUI.geometry('700x600+50+60') #สร้างขนาดหน้าต่าง +50+60 คือระยะห่างจากขอบจอแนวแกนxและyตามลำดับ
#------------------menubar-------------
menubar = Menu(GUI)
GUI.config(menu=menubar)

#-----file menu-----------------------
filemenu = Menu(menubar)
filemenu = Menu(menubar,tearoff=0)#ปิด - ไม่ให้ถูกดึงมา
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='import CSV')
filemenu.add_command(label='Export to Googlesheet')

def About():
    messagebox.showinfo('About','ทดลองเขียนโปรแกรม')
helpmenu = Menu(menubar)
helpmenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help',menu=helpmenu)
helpmenu.add_command(label='About',command=About)



#-------------------------Tab----------
Tab = ttk.Notebook(GUI)#สร้างTab
T1 = Frame(Tab)
T2 = Frame(Tab)
Tab.pack(fill=BOTH,expand=1)

icon_t1 =PhotoImage(file='T1_expense.png')#ขนาดภาพ24px
icon_t2 =PhotoImage(file='T2_expense.png')

Tab.add(T1,text=f'{"ค่าใช้จ่าย":^{30}}',image=icon_t1,compound='top')
Tab.add(T2,text=f'{"ค่าใช้จ่ายทั้งหมด":^{30}}',image=icon_t2,compound='top')

#--------------------------------------
F1 = Frame(T1)#นำF1ใส่ในtab(T1)
#F1.place(x=100,y=50)
F1.pack()

days = {'Mon':'จันทร์',
'Tue':'อังคาร',
'Wed': 'พุธ',
'Thu':'พฤหัสบดี',
'Fri':'ศุกร์',
'Sat':'เสาร์',
'Sun':'อาทิตย์'}
def Save (event=None) :
    expense = v_expense.get() #.get()ดึงค่ามาจากv_expense = StringVar()
    price = v_price.get()
    quantity = v_quantity.get()
    
    if expense == '':
        print('No Data')
        messagebox.showwarning('ERROR','กรุณากรอกข้อมุลให้ครบ')
        return
    elif price== '':
        messagebox.showwarning('ERROR','กรุณากรอกข้อมุลให้ครบ')
        return
    elif quantity== '':
        quantity = 1

    total = float(price)*float(quantity)
    try:
        total = float(price)*float(quantity)#ใช้intจะได้เฉพาะจำนนเต็ม ใช้floatมีทศนิยม
        print('รายการ : {} ราคา : {} บาท '.format(expense,price))
        print('จำนวน : {} ชิ้น รวม : {} บาท'.format(quantity,total))
       
        text ='รายการ : {} ราคา : {} บาท '.format(expense,price)#แสดงผลในโปรแกรมมาจากv_resultด้านล่าง
        text = text + 'จำนวน : {} ชิ้น รวม : {} บาท'.format(quantity,total)#แสดงผลในโปรแกรม
        v_result.set(text)
       
        v_expense.set('') #clearข้อมูลเก่า
        v_price.set('') #clearข้อมูลเก่า
        v_quantity.set('')

        #บันทึกข้อมูลลงในcsvต้อง import csv ด้วย
        today = datetime.now().strftime('%a')#days['Mon']='จันทร์'
        print(today)
        stamp = datetime.now()
        dt = stamp.strftime('%Y-%m-%d-%H:%M:%S') #ดึงวันที่และเวลาจากคอม
        transactionid = stamp.strftime('%Y%m%d%H%M%f')
        dt = days[today]+'-'+dt
        with open('savedata2.csv','a',encoding='utf-8',newline='') as f:
            #with คือสั่งเปิดไฟล์แล้วปิดอัตโนมัติ
            # 'a' การบันทึกข้อมูลต่อไปจากข้อมูลเก่าเป็น'w'จะลบข้อมูลเก่า
            #newline=''ทำให้ข้อมูลไม่มีบรรทัดว่าง
            fw = csv.writer(f) #สร้างฟังก์ชั่นสำหรับเขียนข้อมูล
            data = [transactionid,expense,price,quantity,total,dt] #ข้อมูลที่จะบันทึก
            fw.writerow(data)
        #ทำให้curserกลับไปช่องกรอก
        E1.focus()
        update_table()#อัพเดทจากtab2
    except Exception as e:
        print('ERROR',e)
        # messagebox.showerror('ERROR','กรุณากรอกข้อมุลใหม่')
        # messagebox.showwarning('ERROR','กรุณากรอกข้อมุลใหม่')
        messagebox.showinfo('ERROR','กรุณากรอกข้อมุลใหม่')
        v_expense.set('') #clearข้อมูลเก่า
        v_price.set('') #clearข้อมูลเก่า
        v_quantity.set('')

GUI.bind('<Return>',Save)#ทำให้สามารถกดenterได้ ต้องเพิ่มใน def Save (event=None)
FONT1 = (None,18) # Noneเปลี่ยนเป็นชื่อfontได้
FONT2 = (None,12)
FONT3 = (None,15)

#---------image-----------
main_icon = PhotoImage(file='icon.png')
Mainicon = Label(F1,image=main_icon)
Mainicon.pack()

#-------------text1-----------------
L = ttk.Label(F1,text='รายการค่าใช้จ่าย',font = FONT1).pack()
v_expense = StringVar() #StringVar()ตัวแปลพิเศษสำหรับเก็บข้อมูลในGUI
E1 = ttk.Entry(F1,textvariable=v_expense,font=FONT2)
E1.pack()

#-------------text2-----------------
L = ttk.Label(F1,text='ราคา (บาท)',font = FONT1).pack()
v_price = StringVar()
E2 = ttk.Entry(F1,textvariable=v_price,font=FONT2)
E2.pack()

#---------------text3--------------------------
L = ttk.Label(F1,text='จำนวน  (ชิ้น)',font = FONT1).pack()
v_quantity = StringVar()
E3 = ttk.Entry(F1,textvariable=v_quantity,font=FONT2)
E3.pack()

#-------------------button--------------------------------

icon_b1 = PhotoImage(file='b_save.png')
B2 = ttk.Button(F1,text=f'{"SAVE":>{10}}',image=icon_b1,compound='left',command=Save)#commandเรียกใช้ฟังก์ชัน 
B2.pack(ipadx=30,ipady=5,pady=20)  

#-------------แสดงผลในหน้าต่าง--------------
v_result = StringVar()
v_result.set('--- รายการ ---')
result = ttk.Label(F1,textvariable=v_result,font=FONT3,foreground='red')
result.pack(pady=20)

#--------------------Tab2-----------------
def read_csv():
    with open('savedata2.csv',newline='',encoding='utf-8') as f: #ตั้งชื่อf
        fr = csv.reader(f)
        data = list(fr)
    return data
       
#----------------table-------------------
L = ttk.Label(T2,text='ตารางแสดงรายการ',font=FONT1).pack(pady=20)

header = ['รหัสรายการ','รายการ','ราคา (บาท)','จำนวน (ชิ้น) ','รวมทั้งหมด (บาท)','วันที่-เวลา']
resulttable = ttk.Treeview(T2,columns=header,show='headings',height=20)
resulttable.pack()

#for i in range(len(header)):
 #   resulttable.heading(header[i],text=header[i])

for h in header:
    resulttable.heading(h,text=h)

headerwidth = [130,170,70,70,100,180]
for h,w in zip(header,headerwidth):
    resulttable.column(h,width=w)

#--------ปุ่มลบ------------------------
alltransaction = {}


def UpdateCSV():
     with open('savedata2.csv','w',newline='',encoding='utf-8') as f: 
        fw = csv.writer(f)
        #เตรียมข้อมูลให้กลายเป็นlist
        data = list(alltransaction.values())
        fw.writerows(data)
        print('Table was update')
        #update_table()

def DeleteRecord(event=None):
    check = messagebox.askyesno('Confirm','ลบข้อมูล?')
    print('Yes/No',check)

    if check == True:
        print('delete')
        #print('delete')
        select = resulttable.selection()
        #print(select)
        data = resulttable.item(select)
        data = data['values']
        transactionid = data[0]
        #print(transactionid)
        del alltransaction[str(transactionid)] #ลบข้อมูล
        #print(alltransaction)
        UpdateCSV()
        update_table()
    else:
        print('cancel')

BDelete = ttk.Button(T2,text ='Delete',command=DeleteRecord)
BDelete.place(x=20,y=510)

resulttable.bind('<Delete>',DeleteRecord)

#---------------------------------------
def update_table():
    resulttable.delete(*resulttable.get_children())
    #for c in resulttable.insert():
     #   resulttable.delete(c)
    try: #ป้องกันการerrorกรณีไม่มีcsv
        data = read_csv()
        for d in data:
            #สร้างtransaction data
            alltransaction[d[0]] = d #d[0]=transactionid
            resulttable.insert('',0,value=d)
        print(alltransaction)
    except Exception as e :#ป้องกันการerrorกรณีไม่มีcsv
        print('No File')
        print('ERROR',e)


update_table()
print('GET CHILD :',resulttable.get_children())
#------------------------------------------
GUI.bind('<Tab>',lambda x: E2.focus())
GUI.mainloop()
