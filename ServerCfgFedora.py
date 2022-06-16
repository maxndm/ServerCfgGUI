import os
import glob
import subprocess
import string
import time
from tkinter import *
from tkinter import filedialog
from tkinter import ttk


class CreateToolTip(object):
    """
    creates a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()


class ServerConfig():

	def __init__(self,master):
		self.master = master
		master.geometry("700x350")
		master.title("Server Config")
		master.resizable(width=False,height=False)

		self.kvota1='"'

		self.server = 0
		self.internal = 0
		self.external = 0
		self.dhcpanddns = 0
		self.samba_value = 0

		self.servername = ""
		self.gateway = ""

		self.cardname2 = ""
		self.ip2 = ""
		self.netmask2 = ""
		self.prefix2 = ""
		self.subnetforinternalnet = ""

		self.cardname1 = ""
		self.subnetforexternalnet = ""
		self.ip1 = ""
		self.netmask1 = ""
		self.prefix1 = ""

		self.dnsname = ""
		self.subnetfordhcp = ""
		self.maskfordhcp = ""
		self.dhcprangefrom = ""
		self.dhcprangeto = ""

		self.dhcpi = 0
		self.dnsi = 0
		self.sambai = 0
		self.NAT = 0

		self.externalAsDhcpVar = 0


		self.sambaBASIC = 0
		self.sambaDC = 0


		self.filename = "/"
		self.shfoldername = ""

		self.readonly = "no"
		self.guestok = "no"
		self.browseable = "no"

		self.validusers = ""


		self.serverandgateway()

		#############################self.directorytoc1 = "/etc/sysconfig/network-scripts/ifcfg-{}".format(self.cardname1)
		#############################self.directorytoc2 = "/etc/sysconfig/network-scripts/ifcfg-{}".format(self.cardname2)
		self.ethports = []
		os.mkdir("/etc/sysconfig/network-scripts")
		os.chdir("/etc/sysconfig/network-scripts")
		cmd = subprocess.Popen(["nmcli -t -f DEVICE c show --active"],stdout=subprocess.PIPE, shell=True)
		(out,err) = cmd.communicate()
		self.ethports = (out.decode("utf-8")).split("\n")
		del self.ethports[-1]

		#print(self.ethports)

	def serverandgateway(self):
		try:
			self.sambaBASIC = self.sambaBASICIV.get()
			self.sambaDC = self.sambaDCIV.get()

			self.filename = self.filenameSV.get()
			self.shfoldername = self.shfoldernameSV.get()
			self.validusers = self.validusersSV.get()

			self.guestok = self.guestokIV.get()
			self.browseable = self.browseableIV.get()
			self.readonly = self.readonlyIV.get()
		except:
			pass

		try:
			self.ip2 = self.ip2SV.get()
			self.netmask2 = self.netmask2SV.get()
			self.prefix2 = self.prefix2SV.get()
			self.subnetforinternalnet = self.subnetforinternalnetSV.get()
			self.cardname2 = self.cardname2SV.get()

		except:
			pass
		try:
			self.cardname1 = self.cardname1SV.get()
			self.subnetforexternalnet = self.subnetforexternalnetSV.get()
			self.ip1 = self.ip1SV.get()
			self.netmask1 = self.netmask1SV.get()
			self.prefix1 = self.prefix1SV.get()
		except:
			pass

		try:

			self.dnsname = self.dnsnameSV.get()
			self.subnetfordhcp = self.subnetfordhcpSV.get()
			self.maskfordhcp = self.maskfordhcpSV.get()
			self.dhcprangefrom = self.dhcprangefromSV.get()
			self.dhcprangeto = self.dhcprangetoSV.get()

		except:
			pass

		self.server = 1
		#print("server = ",self.server)
		#print("internal = ",self.internal)
		#print("external = ",self.external)

		if self.internal == 1:
			self.internal = 0
			self.internalnetworkframe.destroy()

		if self.external == 1:
			self.external = 0
			self.externalnetworkframe.destroy()

		if self.dhcpanddns == 1:
			self.dhcpanddns = 0
			self.dhcpdanddnsframe.destroy()

		if self.samba_value == 1:
			self.samba_value = 0
			self.sambaframe.destroy()

		self.serverandgatewayframe = Frame(self.master,width=700,height=700,background="#2e302f",borderwidth=5,relief="ridge")
		self.serverandgatewayframe.pack()

		self.buttonserveragateway= Button(self.serverandgatewayframe,text="Server & Main gateway",fg="white",bg="#1c1c1b",command=self.serverandgateway)
		self.buttonserveragateway.place(x=10,y=10)
		self.buttonserveragateway.configure(state="disabled")

		self.buttoninternal= Button(self.serverandgatewayframe,text="Internal Network",fg="white",bg="#1c1c1b",command=self.internalnetwork)
		self.buttoninternal.place(x=190,y=10)
		self.buttoninternal.configure(state="normal")

		self.buttonexternal= Button(self.serverandgatewayframe,text="External Network",fg="white",bg="#1c1c1b",command=self.externalnetwork)
		self.buttonexternal.place(x=330,y=10)
		self.buttonexternal.configure(state="normal")

		self.buttondhcpdanddns= Button(self.serverandgatewayframe,text="DHCP & DNS",fg="white",bg="#1c1c1b",command=self.dhcpdanddns)
		self.buttondhcpdanddns.place(x=470,y=10)
		self.buttondhcpdanddns.configure(state="normal")

		self.samba= Button(self.serverandgatewayframe,text="Samba",fg="white",bg="#1c1c1b",command=self.sambaconf)
		self.samba.place(x=590,y=10)
		self.samba.configure(state="normal")
				########################################################################################################################################################################################################################################
		self.servernameSV = StringVar()
		self.servernamelabel = Label(self.serverandgatewayframe,width=15,text="Server name: ",fg="white",borderwidth=3,relief="raised",background="#272928",font="Arial 12").place(x=50,y=50)
		self.servernameentry = Entry(self.serverandgatewayframe,textvariable=self.servernameSV,width=20,background="#464a48",font="Arial 12").place(x=200,y=50)
		self.servernameSV.set(self.servername)

		self.gatewaySV = StringVar()
		self.gatewaylabel = Label(self.serverandgatewayframe,width=15,text="Default gateway: ",fg="white",borderwidth=3,relief="raised",background="#272928",font="Arial 12").place(x=50,y=100)
		self.gatewayentry = Entry(self.serverandgatewayframe,textvariable=self.gatewaySV,width=20,background="#464a48",font="Arial 12").place(x=200,y=100)
		self.gatewaySV.set(self.gateway)

		self.dhcpiIV = IntVar()
		self.dhcpinstall = Checkbutton(self.serverandgatewayframe, variable=self.dhcpiIV,fg="black",background="#272928",activebackground="#4a4a46").place(x=50,y=150)
		self.dhcplabel = Label(self.serverandgatewayframe, text="install DHCP service",fg="white",background="#272928").place(x=80,y=150)
		self.dhcpiIV.set(self.dhcpi)

		self.dnsiIV = IntVar()
		self.dnsinstall = Checkbutton(self.serverandgatewayframe, variable=self.dnsiIV,fg="black",background="#272928",activebackground="#4a4a46").place(x=50,y=180)
		self.dnslabel = Label(self.serverandgatewayframe, text="install DNS service",fg="white",background="#272928").place(x=80,y=180)
		self.dnsiIV.set(self.dnsi)

		self.sambaiIV = IntVar()
		self.sambainstall = Checkbutton(self.serverandgatewayframe, variable=self.sambaiIV,fg="black",background="#272928",activebackground="#4a4a46").place(x=50,y=210)
		self.sambalabel = Label(self.serverandgatewayframe, text="install SAMBA service",fg="white",background="#272928").place(x=80,y=210)
		self.sambaiIV.set(self.sambai)

		self.NATIV = IntVar()
		self.natconfig = Checkbutton(self.serverandgatewayframe, variable=self.NATIV,fg="black",background="#272928",activebackground="#4a4a46").place(x=50,y=240)
		self.NATlabel = Label(self.serverandgatewayframe, text="NAT service",fg="white",background="#272928").place(x=80,y=240)
		self.NATIV.set(self.NAT)

		self.buttonproceed= Button(self.serverandgatewayframe,text="Proceed configuration",fg="white",bg="#1c1c1b",command=self.installingandconfiguring)
		self.buttonproceed.place(x=470,y=250)

	def sambaconf(self):


		self.dhcpi = self.dhcpiIV.get()
		self.dnsi = self.dnsiIV.get()
		self.sambai = self.sambaiIV.get()
		self.NAT = 	self.NATIV.get()


		try:
			self.servername = self.servernameSV.get()
			self.gateway = self.gatewaySV.get()

		except:
			pass

		try:

			self.ip2 = self.ip2SV.get()
			self.netmask2 = self.netmask2SV.get()
			self.prefix2 = self.prefix2SV.get()
			self.subnetforinternalnet = self.subnetforinternalnetSV.get()
			self.cardname2 = self.cardname2SV.get()

		except:
			pass

		try:

			self.cardname1 = self.cardname1SV.get()
			self.subnetforexternalnet = self.subnetforexternalnetSV.get()
			self.ip1 = self.ip1SV.get()
			self.netmask1 = self.netmask1SV.get()
			self.prefix1 = self.prefix1SV.get()

			self.dnsname = self.dnsnameSV.get()
			self.subnetfordhcp = self.subnetfordhcpSV.get()
			self.maskfordhcp = self.maskfordhcpSV.get()
			self.dhcprangefrom = self.dhcprangefromSV.get()
			self.dhcprangeto = self.dhcprangetoSV.get()

		except:
			pass

		self.samba_value = 1

		if self.server == 1:
			self.server = 0
			self.serverandgatewayframe.destroy()

		if self.internal == 1:
			self.internal = 0
			self.internalnetworkframe.destroy()

		if self.external == 1:
			self.external = 0
			self.externalnetworkframe.destroy()

		if self.dhcpanddns == 1:
			self.dhcpanddns = 0
			self.dhcpdanddnsframe.destroy()




		self.sambaframe = Frame(self.master,width=700,height=700,background="#2e302f",borderwidth=5,relief="ridge")
		self.sambaframe.pack()

		self.buttonserveragateway= Button(self.sambaframe,text="Server & Main gateway",fg="white",bg="#1c1c1b",command=self.serverandgateway)
		self.buttonserveragateway.place(x=10,y=10)
		self.buttonserveragateway.configure(state="normal")

		self.buttoninternal= Button(self.sambaframe,text="Internal Network",fg="white",bg="#1c1c1b",command=self.internalnetwork)
		self.buttoninternal.place(x=190,y=10)
		self.buttoninternal.configure(state="normal")

		self.buttonexternal= Button(self.sambaframe,text="External Network",fg="white",bg="#1c1c1b",command=self.externalnetwork)
		self.buttonexternal.place(x=330,y=10)
		self.buttonexternal.configure(state="normal")

		self.buttondhcpdanddns= Button(self.sambaframe,text="DHCP & DNS",fg="white",bg="#1c1c1b",command=self.dhcpdanddns)
		self.buttondhcpdanddns.place(x=470,y=10)
		self.buttondhcpdanddns.configure(state="normal")

		self.samba= Button(self.sambaframe,text="Samba",fg="white",bg="#1c1c1b",command=self.sambaconf)
		self.samba.place(x=590,y=10)
		self.samba.configure(state="disabled")

		self.sambaBASICIV = IntVar()
		self.sambaBASICinstall = Checkbutton(self.sambaframe, variable=self.sambaBASICIV,fg="black",background="#272928",activebackground="#4a4a46",command=self.changevalueofsamba)
		self.sambaBASICinstall.place(x=50,y=50)
		self.sambaBASIClabel = Label(self.sambaframe, text="Configure Samba shares",fg="white",background="#272928").place(x=80,y=50)
		self.sambaBASICIV.set(self.sambaBASIC)

		self.sambaDCIV = IntVar()
		self.sambaDCinstall = Checkbutton(self.sambaframe, variable=self.sambaDCIV,fg="black",background="#272928",activebackground="#4a4a46",command=self.changevalueofsamba2)
		self.sambaDCinstall.place(x=50,y=80)
		self.sambaDCSlabel = Label(self.sambaframe, text="Configure Samba domain controller",fg="white",background="#272928").place(x=80,y=80)
		self.sambaDCIV.set(self.sambaDC)

		if self.sambaBASIC ==1:

			self.sambaDC = 0
			self.sambaDCIV.set(self.sambaDC)

			self.sambaBASICinstall.configure(state="disabled")
			self.sambaDCinstall.configure(state="normal")


		elif self.sambaDC == 1:

			self.sambaBASIC = 0
			self.sambaBASICIV.set(self.sambaBASIC)

			self.sambaBASICinstall.configure(state="normal")
			self.sambaDCinstall.configure(state="disabled")

	def changevalueofsamba(self):

		self.sambaDC = 0
		self.sambaDCIV.set(self.sambaDC)

		self.sambaBASICinstall.configure(state="disabled")
		self.sambaDCinstall.configure(state="normal")

		self.filenameSV = StringVar()
		self.filenamelabel = Label(self.sambaframe,width=15,text="Folder: ",fg="white",background="#272928",font="Arial 12",borderwidth=3,relief="raised")
		self.filenamelabel.place(x=50,y=120)
		self.filenameEntry = Entry(self.sambaframe,width=20,textvariable=self.filenameSV,background="#272928",font="Arial 12",fg="white")
		self.filenameEntry .place(x=205,y=120)
		self.filenameSV.set(self.filename)

		self.selectbutton = Button(self.sambaframe,text="|||",fg="white",bg="#1c1c1b",command=self.choosefolder)
		self.selectbutton.place(x=395,y=120)

		self.shfoldernameSV = StringVar()
		self.shfoldernamelabel = Label(self.sambaframe,width=15,text="Folder name: ",fg="white",background="#272928",font="Arial 12",borderwidth=3,relief="raised")
		self.shfoldernamelabel.place(x=50,y=160)
		self.shfoldernameEntry = Entry(self.sambaframe,width=20,textvariable=self.shfoldernameSV,background="#272928",font="Arial 12",fg="white")
		self.shfoldernameEntry .place(x=205,y=160)
		self.shfoldernameSV.set(self.shfoldername)

		self.validusersSV = StringVar()
		self.validuserslabel = Label(self.sambaframe,width=15,text="Valid users: ",fg="white",background="#272928",font="Arial 12",borderwidth=3,relief="raised")
		self.validuserslabel.place(x=50,y=200)
		self.validusersEntry = Entry(self.sambaframe,width=20,textvariable=self.validusersSV,background="#272928",font="Arial 12",fg="white")
		self.validusersEntry .place(x=205,y=200)
		self.validusersSV.set(self.validusers)
		self.tooltiplabel = Label(self.sambaframe,text=" ? ")
		self.tooltiplabel.place(x=400,y=204)
		self.tooltip = CreateToolTip(self.tooltiplabel, 'user1,user2,user3,@group1,@group2,@group3...')


		self.guestokIV = StringVar()
		self.guestokCB = Checkbutton(self.sambaframe, variable=self.guestokIV,fg="black",background="#272928",activebackground="#4a4a46",onvalue="yes",offvalue="no")
		self.guestokCB.place(x=50,y=240)
		self.guestoklabel = Label(self.sambaframe, text="Allow guests",fg="white",background="#272928")
		self.guestoklabel.place(x=80,y=240)
		self.guestokIV.set(self.guestok)

		self.browseableIV = StringVar()
		self.browseableCB = Checkbutton(self.sambaframe, variable=self.browseableIV,fg="black",background="#272928",activebackground="#4a4a46",onvalue="yes",offvalue="no")
		self.browseableCB.place(x=50,y=270)
		self.browseablelabel = Label(self.sambaframe, text="Browseable",fg="white",background="#272928")
		self.browseablelabel.place(x=80,y=270)
		self.browseableIV.set(self.browseable)

		self.readonlyIV = StringVar()
		self.readonlyCB = Checkbutton(self.sambaframe, variable=self.readonlyIV,fg="black",background="#272928",activebackground="#4a4a46",onvalue="yes",offvalue="no")
		self.readonlyCB.place(x=50,y=300)
		self.readonlylabel = Label(self.sambaframe, text="Read only",fg="white",background="#272928")
		self.readonlylabel.place(x=80,y=300)
		self.readonlyIV.set(self.readonly)

	def changevalueofsamba2(self):
		self.sambaBASIC = 0
		self.sambaBASICIV.set(self.sambaBASIC)

		self.sambaBASICinstall.configure(state="normal")
		self.sambaDCinstall.configure(state="disabled")

		self.filenamelabel.destroy()
		self.selectbutton.destroy()
		self.filenameEntry.destroy()
		self.shfoldernamelabel.destroy()
		self.shfoldernameEntry.destroy()
		self.validuserslabel.destroy()
		self.validusersEntry.destroy()
		self.guestokCB.destroy()
		self.guestoklabel.destroy()
		self.browseableCB.destroy()
		self.browseablelabel.destroy()
		self.readonlyCB.destroy()
		self.readonlylabel.destroy()

	def choosefolder(self):

		self.sambaframe.option_add('*foreground', 'black')  # set all tk widgets' foreground to red
		self.sambaframe.option_add('*activeForeground', 'black')  # set all tk widgets' foreground to red


		style = ttk.Style(self.sambaframe)
		style.configure('TLabel', foreground='black')
		style.configure('TEntry', foreground='black')
		style.configure('TMenubutton', foreground='black')
		style.configure('TButton', foreground='black')
		#self.filename = filedialog.askopenfilename(initialdir="/")
		self.filename = filedialog.askdirectory(initialdir="/")
		#print(self.filename)
		self.filenameSV.set(self.filename)

	def sambaconfigprocess(self):

		if self.sambaBASIC == 1:
			subprocess.call(["setsebool","-P", "samba_export_all_ro=1", "samba_export_all_rw=1"])
			subprocess.call(["firewall-cmd", "--permanent", "--add-service=samba"])
			subprocess.call(["firewall-cmd", "--reload"])
			subprocess.call(["cp","/etc/samba/smb.conf","/etc/samba/smb.conf.back"])

			self.contents = []

			with open("/etc/samba/smb.conf", "r", encoding="iso 8859-2") as file:
				for i in file:
					self.contents.append(i)
					print(i)


			with open("/etc/samba/smb.conf", "w", encoding="iso 8859-2") as file:
				for i in self.contents:
					file.write(str(i))


				file.write(("[{}]\n").format(self.shfoldername))
				file.write(("	browsable = {}\n").format(self.browseable))
				file.write(("	path = {}\n").format(self.filename))
				file.write(("	valid users = {}\n").format(self.validusers))
				file.write(("	allow guests = {}\n").format(self.guestok))
				file.write(("	read only = {}\n").format(self.readonly))


			subprocess.call(["chmod", "777", "{}".format(self.filename)])
			subprocess.call(["setsebool", "-P", "samba_export_all_ro=1", "samba_export_all_rw=1"])

			subprocess.call(["systemctl","enable", "smb"])
			subprocess.call(["systemctl","enable", "nmb"])



		elif self.sambaDC == 1:
			pass

	def internalnetwork(self):

		self.dhcpi = self.dhcpiIV.get()
		self.dnsi = self.dnsiIV.get()
		self.sambai = self.sambaiIV.get()
		self.NAT = 	self.NATIV.get()

		try:
			self.sambaBASIC = self.sambaBASICIV.get()
			self.sambaDC = self.sambaDCIV.get()

			self.filename = self.filenameSV.get()
			self.shfoldername = self.shfoldernameSV.get()
			self.validusers = self.validusersSV.get()

			self.guestok = self.guestokIV.get()
			self.browseable = self.browseableIV.get()
			self.readonly = self.readonlyIV.get()
		except:
			pass
		try:

			self.servername = self.servernameSV.get()
			self.gateway = self.gatewaySV.get()
		except:
			pass

		try:

			self.cardname1 = self.cardname1SV.get()
			self.subnetforexternalnet = self.subnetforexternalnetSV.get()
			self.ip1 = self.ip1SV.get()
			self.netmask1 = self.netmask1SV.get()
			self.prefix1 = self.prefix1SV.get()
		except:
			pass
		try:

			self.dnsname = self.dnsnameSV.get()
			self.subnetfordhcp = self.subnetfordhcpSV.get()
			self.maskfordhcp = self.maskfordhcpSV.get()
			self.dhcprangefrom = self.dhcprangefromSV.get()
			self.dhcprangeto = self.dhcprangetoSV.get()

		except:
			pass


		self.internal = 1
		#print("server = ",self.server)
		#print("internal = ",self.internal)
		#print("external = ",self.external)

		if self.server == 1:
			self.server = 0
			self.serverandgatewayframe.destroy()

		if self.external == 1:
			self.external = 0
			self.externalnetworkframe.destroy()

		if self.dhcpanddns == 1:
			self.dhcpanddns = 0
			self.dhcpdanddnsframe.destroy()

		if self.samba_value == 1:
			self.samba_value = 0
			self.sambaframe.destroy()

		self.internalnetworkframe = Frame(self.master,width=700,height=700,background="#2e302f",borderwidth=5,relief="ridge")
		self.internalnetworkframe.pack()

		self.buttonserveragateway= Button(self.internalnetworkframe,text="Server & Main gateway",fg="white",bg="#1c1c1b",command=self.serverandgateway)
		self.buttonserveragateway.place(x=10,y=10)
		self.buttonserveragateway.configure(state="normal")

		self.buttoninternal= Button(self.internalnetworkframe,text="Internal Network",fg="white",bg="#1c1c1b",command=self.internalnetwork)
		self.buttoninternal.place(x=190,y=10)
		self.buttoninternal.configure(state="disabled")

		self.buttonexternal= Button(self.internalnetworkframe,text="External Network",fg="white",bg="#1c1c1b",command=self.externalnetwork)
		self.buttonexternal.place(x=330,y=10)
		self.buttonexternal.configure(state="normal")

		self.buttondhcpdanddns= Button(self.internalnetworkframe,text="DHCP & DNS",fg="white",bg="#1c1c1b",command=self.dhcpdanddns)
		self.buttondhcpdanddns.place(x=470,y=10)
		self.buttondhcpdanddns.configure(state="normal")

		self.samba= Button(self.internalnetworkframe,text="Samba",fg="white",bg="#1c1c1b",command=self.sambaconf)
		self.samba.place(x=590,y=10)
		self.samba.configure(state="normal")


		self.cardname2SV = StringVar(self.internalnetworkframe)
		self.cardname2SV.set(self.ethports[0])
		self.cardname2label = Label(self.internalnetworkframe,width=15,text="Card name: ",fg="white",borderwidth=3,relief="raised",background="#272928",font="Arial 12").place(x=50,y=50)

		try:
			self.cardname2input = OptionMenu(self.internalnetworkframe, self.cardname2SV, self.ethports[0],self.ethports[1],self.ethports[2],self.ethports[3],self.ethports[4])

		except:
			try:
				self.cardname2input = OptionMenu(self.internalnetworkframe, self.cardname2SV, self.ethports[0],self.ethports[1],self.ethports[2],self.ethports[3])

			except:
				try:
					self.cardname2input = OptionMenu(self.internalnetworkframe, self.cardname2SV, self.ethports[0],self.ethports[1],self.ethports[2])
				except:
					try:
						self.cardname2input = OptionMenu(self.internalnetworkframe, self.cardname2SV, self.ethports[0],self.ethports[1])
					except:
						self.cardname2input = OptionMenu(self.internalnetworkframe, self.cardname2SV, self.ethports[0])

		self.cardname2input.place(x=200,y=50)
		self.cardname2input.configure(width=16,font="Arial 12",fg="white",bg="#1c1c1b",activebackground="#1c1c1b",activeforeground="white")
		self.cardname2SV.set(self.cardname2)

		self.subnetforinternalnetSV = StringVar()
		self.subnetforinternalnetlabel = Label(self.internalnetworkframe,fg="white",width=15,text="IP Subnet: ",borderwidth=3,relief="raised",background="#272928",font="Arial 12").place(x=50,y=100)
		self.subnetforinternalnetentry = Entry(self.internalnetworkframe,textvariable=self.subnetforinternalnetSV,width=20,background="#464a48",font="Arial 12").place(x=200,y=100)
		self.subnetforinternalnetSV.set(self.subnetforinternalnet)

		self.ip2SV = StringVar()
		self.ip2label = Label(self.internalnetworkframe,width=15,text="IP Address: ",fg="white",borderwidth=3,relief="raised",background="#272928",font="Arial 12").place(x=50,y=150)
		self.ip2entry = Entry(self.internalnetworkframe,textvariable=self.ip2SV,width=20,background="#464a48",font="Arial 12").place(x=200,y=150)
		self.ip2SV.set(self.ip2)

		self.netmask2SV = StringVar()
		self.netmask2label = Label(self.internalnetworkframe,width=15,text="Netmask: ",fg="white",borderwidth=3,relief="raised",background="#272928",font="Arial 12").place(x=50,y=200)
		self.netmask2entry  = Entry(self.internalnetworkframe,textvariable=self.netmask2SV,width=20,background="#464a48",font="Arial 12").place(x=200,y=200)
		self.netmask2SV.set(self.netmask2)

		self.prefix2SV = StringVar()
		self.prefix2label = Label(self.internalnetworkframe,width=15,text="Prefix: ",fg="white",borderwidth=3,relief="raised",background="#272928",font="Arial 12").place(x=50,y=250)
		self.prefix2entry = Entry(self.internalnetworkframe,textvariable=self.prefix2SV,width=20,background="#464a48",font="Arial 12").place(x=200,y=250)
		self.prefix2SV.set(self.prefix2)

	def externalnetwork(self):


		self.dhcpi = self.dhcpiIV.get()
		self.dnsi = self.dnsiIV.get()
		self.sambai = self.sambaiIV.get()
		self.NAT = 	self.NATIV.get()


		try:

			self.sambaBASIC = self.sambaBASICIV.get()
			self.sambaDC = self.sambaDCIV.get()

			self.filename = self.filenameSV.get()
			self.shfoldername = self.shfoldernameSV.get()
			self.validusers = self.validusersSV.get()

			self.guestok = self.guestokIV.get()
			self.browseable = self.browseableIV.get()
			self.readonly = self.readonlyIV.get()
		except:
			pass
		try:

			self.servername = self.servernameSV.get()
			self.gateway = self.gatewaySV.get()
		except:
			pass
		try:

			self.ip2 = self.ip2SV.get()
			self.netmask2 = self.netmask2SV.get()
			self.prefix2 = self.prefix2SV.get()
			self.subnetforinternalnet = self.subnetforinternalnetSV.get()
			self.cardname2 = self.cardname2SV.get()

		except:
			pass

		try:

			self.dnsname = self.dnsnameSV.get()
			self.subnetfordhcp = self.subnetfordhcpSV.get()
			self.maskfordhcp = self.maskfordhcpSV.get()
			self.dhcprangefrom = self.dhcprangefromSV.get()
			self.dhcprangeto = self.dhcprangetoSV.get()

		except:
			pass

		self.external = 1
		#print("server = ",self.server)
		#print("internal = ",self.internal)
		#print("external = ",self.external)

		if self.server == 1:
			self.server = 0
			self.serverandgatewayframe.destroy()

		if self.internal == 1:
			self.interval = 0
			self.internalnetworkframe.destroy()

		if self.dhcpanddns == 1:
			self.dhcpanddns = 0
			self.dhcpdanddnsframe.destroy()

		if self.samba_value == 1:
			self.samba_value = 0
			self.sambaframe.destroy()

		self.externalnetworkframe = Frame(self.master,width=700,height=700,background="#2e302f",borderwidth=5,relief="ridge")
		self.externalnetworkframe.pack()

		self.buttonserveragateway= Button(self.externalnetworkframe,text="Server & Main gateway",fg="white",bg="#1c1c1b",command=self.serverandgateway)
		self.buttonserveragateway.place(x=10,y=10)
		self.buttonserveragateway.configure(state="normal")

		self.buttoninternal= Button(self.externalnetworkframe,text="Internal Network",fg="white",bg="#1c1c1b",command=self.internalnetwork)
		self.buttoninternal.place(x=190,y=10)
		self.buttoninternal.configure(state="normal")

		self.buttonexternal= Button(self.externalnetworkframe,text="External Network",fg="white",bg="#1c1c1b",command=self.externalnetwork)
		self.buttonexternal.place(x=330,y=10)
		self.buttonexternal.configure(state="disabled")

		self.buttondhcpdanddns= Button(self.externalnetworkframe,text="DHCP & DNS",fg="white",bg="#1c1c1b",command=self.dhcpdanddns)
		self.buttondhcpdanddns.place(x=470,y=10)
		self.buttondhcpdanddns.configure(state="normal")

		self.samba= Button(self.externalnetworkframe,text="Samba",fg="white",bg="#1c1c1b",command=self.sambaconf)
		self.samba.place(x=590,y=10)
		self.samba.configure(state="normal")


		self.cardname1SV = StringVar(self.externalnetworkframe)
		self.cardname1SV.set("eth")
		self.cardname1label = Label(self.externalnetworkframe,width=15,text="Card name: ",fg="white",borderwidth=3,relief="raised",background="#272928",font="Arial 12").place(x=50,y=50)

		try:
			self.cardname1input = OptionMenu(self.externalnetworkframe, self.cardname1SV, self.ethports[0],self.ethports[1],self.ethports[2],self.ethports[3],self.ethports[4])

		except:
			try:
				self.cardname1input = OptionMenu(self.externalnetworkframe, self.cardname1SV, self.ethports[0],self.ethports[1],self.ethports[2],self.ethports[3])

			except:
				try:
					self.cardname1input = OptionMenu(self.externalnetworkframe, self.cardname1SV, self.ethports[0],self.ethports[1],self.ethports[2])
				except:
					try:
						self.cardname1input = OptionMenu(self.externalnetworkframe, self.cardname1SV, self.ethports[0],self.ethports[1])
					except:
						self.cardname1input = OptionMenu(self.externalnetworkframe, self.cardname1SV, self.ethports[0])

		self.cardname1input.place(x=200,y=50)
		self.cardname1input.configure(width=16,font="Arial 12",fg="white",bg="#1c1c1b",activebackground="#1c1c1b",activeforeground="white")
		self.cardname1SV.set(self.cardname1)

		self.subnetforexternalnetSV = StringVar()
		self.subnetforexternalnetlabel = Label(self.externalnetworkframe,width=15,text="IP Subnet: ",fg="white",borderwidth=3,relief="raised",background="#272928",font="Arial 12").place(x=50,y=100)
		self.subnetforexternalnetentry = Entry(self.externalnetworkframe,textvariable=self.subnetforexternalnetSV,width=20,background="#464a48",font="Arial 12")
		self.subnetforexternalnetentry.place(x=200,y=100)
		self.subnetforexternalnetSV.set(self.subnetforexternalnet)

		self.ip1SV = StringVar()
		self.ip1label = Label(self.externalnetworkframe,width=15,text="IP Address: ",fg="white",borderwidth=3,relief="raised",background="#272928",font="Arial 12").place(x=50,y=150)
		self.ip1entry = Entry(self.externalnetworkframe,textvariable=self.ip1SV, width=20,background="#464a48",font="Arial 12")
		self.ip1entry.place(x=200,y=150)
		self.ip1SV.set(self.ip1)

		self.netmask1SV = StringVar()
		self.netmask1label = Label(self.externalnetworkframe,width=15,text="Netmask: ",fg="white",borderwidth=3,relief="raised",background="#272928",font="Arial 12").place(x=50,y=200)
		self.netmask1entry  = Entry(self.externalnetworkframe,textvariable=self.netmask1SV,width=20,background="#464a48",font="Arial 12")
		self.netmask1entry.place(x=200,y=200)
		self.netmask1SV.set(self.netmask1)

		self.prefix1SV = StringVar()
		self.prefix1label = Label(self.externalnetworkframe,width=15,text="Prefix: ",fg="white",borderwidth=3,relief="raised",background="#272928",font="Arial 12").place(x=50,y=250)
		self.prefix1entry  = Entry(self.externalnetworkframe,textvariable=self.prefix1SV,width=20,background="#464a48",font="Arial 12")
		self.prefix1entry.place(x=200,y=250)
		self.prefix1SV.set(self.prefix1)

		self.externalAsDhcpIV = IntVar()
		self.externalAsDhcp = Checkbutton(self.externalnetworkframe, variable=self.externalAsDhcpIV,fg="black",background="#272928",activebackground="#4a4a46",command=self.disable_external_options)
		self.externalAsDhcp.place(x=50,y=300)
		self.externalAsDhcplabel = Label(self.externalnetworkframe, text="IP from DHCP",fg="white",background="#272928").place(x=80,y=300)
		self.externalAsDhcpIV.set(self.externalAsDhcpVar)

		if self.externalAsDhcpVar == 1:
			#print(self.externalAsDhcpVar)
			self.ip1entry.configure(state="disabled")
			self.subnetforexternalnetentry.configure(state="disabled")
			self.netmask1entry.configure(state="disabled")
			self.prefix1entry.configure(state="disabled")
		else:
			#print(self.externalAsDhcpVar)
			self.ip1entry.configure(state="normal")
			self.subnetforexternalnetentry.configure(state="normal")
			self.netmask1entry.configure(state="normal")
			self.prefix1entry.configure(state="normal")

	def disable_external_options(self):
		self.externalAsDhcpVar = self.externalAsDhcpIV.get()

		if self.externalAsDhcpVar == 1:
			#print(self.externalAsDhcpVar)
			self.ip1entry.configure(state="disabled")
			self.subnetforexternalnetentry.configure(state="disabled")
			self.netmask1entry.configure(state="disabled")
			self.prefix1entry.configure(state="disabled")
		else:
			#print(self.externalAsDhcpVar)
			self.ip1entry.configure(state="normal")
			self.subnetforexternalnetentry.configure(state="normal")
			self.netmask1entry.configure(state="normal")
			self.prefix1entry.configure(state="normal")

	def dhcpdanddns(self):

		self.dhcpi = self.dhcpiIV.get()
		self.dnsi = self.dnsiIV.get()
		self.sambai = self.sambaiIV.get()
		self.NAT = 	self.NATIV.get()


		try:

			self.sambaBASIC = self.sambaBASICIV.get()
			self.sambaDC = self.sambaDCIV.get()

			self.filename = self.filenameSV.get()
			self.shfoldername = self.shfoldernameSV.get()
			self.validusers = self.validusersSV.get()

			self.guestok = self.guestokIV.get()
			self.browseable = self.browseableIV.get()
			self.readonly = self.readonlyIV.get()

		except:
			pass

		try:

			self.servername = self.servernameSV.get()
			self.gateway = self.gatewaySV.get()
		except:
			pass
		try:

			self.ip2 = self.ip2SV.get()
			self.netmask2 = self.netmask2SV.get()
			self.prefix2 = self.prefix2SV.get()
			self.subnetforinternalnet = self.subnetforinternalnetSV.get()
			self.cardname2 = self.cardname2SV.get()

		except:
			pass

		try:

			self.cardname1 = self.cardname1SV.get()
			self.subnetforexternalnet = self.subnetforexternalnetSV.get()
			self.ip1 = self.ip1SV.get()
			self.netmask1 = self.netmask1SV.get()
			self.prefix1 = self.prefix1SV.get()

		except:
			pass

		self.dhcpanddns = 1

		if self.server == 1:
			self.server = 0
			self.serverandgatewayframe.destroy()

		if self.internal == 1:
			self.interval = 0
			self.internalnetworkframe.destroy()

		if self.external == 1:
			self.external = 0
			self.externalnetworkframe.destroy()

		if self.samba_value == 1:
			self.samba_value = 0
			self.sambaframe.destroy()

		self.dhcpdanddnsframe = Frame(self.master,width=700,height=700,background="#2e302f",borderwidth=5,relief="ridge")
		self.dhcpdanddnsframe.pack()

		self.buttonserveragateway= Button(self.dhcpdanddnsframe,text="Server & Main gateway",fg="white",bg="#1c1c1b",command=self.serverandgateway)
		self.buttonserveragateway.place(x=10,y=10)
		self.buttonserveragateway.configure(state="normal")

		self.buttoninternal= Button(self.dhcpdanddnsframe,text="Internal Network",fg="white",bg="#1c1c1b",command=self.internalnetwork)
		self.buttoninternal.place(x=190,y=10)
		self.buttoninternal.configure(state="normal")

		self.buttonexternal= Button(self.dhcpdanddnsframe,text="External Network",fg="white",bg="#1c1c1b",command=self.externalnetwork)
		self.buttonexternal.place(x=330,y=10)
		self.buttonexternal.configure(state="normal")

		self.buttondhcpdanddns= Button(self.dhcpdanddnsframe,text="DHCP & DNS",fg="white",bg="#1c1c1b",command=self.dhcpdanddns)
		self.buttondhcpdanddns.place(x=470,y=10)
		self.buttondhcpdanddns.configure(state="disabled")

		self.samba= Button(self.dhcpdanddnsframe,text="Samba",fg="white",bg="#1c1c1b",command=self.sambaconf)
		self.samba.place(x=590,y=10)
		self.samba.configure(state="normal")

		self.dnsnameSV = StringVar()
		self.dnsnamelabel = Label(self.dhcpdanddnsframe,text="Domain name: ",fg="white",width=15,borderwidth=3,relief="raised",background="#272928",font="Arial 12").place(x=50,y=50)
		self.dnsnameentry = Entry(self.dhcpdanddnsframe,textvariable=self.dnsnameSV,width=20,background="#464a48",font="Arial 12").place(x=200,y=50)
		self.dnsnameSV.set(self.dnsname)

		self.subnetfordhcpSV = StringVar()
		self.subnetfordhcplabel = Label(self.dhcpdanddnsframe,text="DHCP subnet: ",fg="white",width=15,borderwidth=3,relief="raised",background="#272928",font="Arial 12").place(x=50,y=100)
		self.subnetfordhcpentry = Entry(self.dhcpdanddnsframe,textvariable=self.subnetfordhcpSV,width=20,background="#464a48",font="Arial 12").place(x=200,y=100)
		self.subnetfordhcpSV.set(self.subnetfordhcp)

		self.maskfordhcpSV = StringVar()
		self.maskfordhcplabel = Label(self.dhcpdanddnsframe,text="DHCP Netmask: ",fg="white",width=15,borderwidth=3,relief="raised",background="#272928",font="Arial 12").place(x=50,y=150)
		self.maskfordhcpentry = Entry(self.dhcpdanddnsframe,textvariable=self.maskfordhcpSV,width=20,background="#464a48",font="Arial 12").place(x=200,y=150)
		self.maskfordhcpSV.set(self.maskfordhcp)

		self.dhcprangefromSV = StringVar()
		self.dhcprangefromlabel = Label(self.dhcpdanddnsframe,text="IP range from: ",fg="white",width=15,borderwidth=3,relief="raised",background="#272928",font="Arial 12").place(x=50,y=200)
		self.dhcprangefromentry = Entry(self.dhcpdanddnsframe,textvariable=self.dhcprangefromSV,width=20,background="#464a48",font="Arial 12").place(x=200,y=200)
		self.dhcprangefromSV.set(self.dhcprangefrom)

		self.dhcprangetoSV = StringVar()
		self.dhcprangetolabel = Label(self.dhcpdanddnsframe,text="IP range to: ",fg="white",width=15,borderwidth=3,relief="raised",background="#272928",font="Arial 12").place(x=50,y=250)
		self.dhcprangetoentry = Entry(self.dhcpdanddnsframe,textvariable=self.dhcprangetoSV,width=20,background="#464a48",font="Arial 12").place(x=200,y=250)
		self.dhcprangetoSV.set(self.dhcprangeto)

	def installingandconfiguring(self):


		self.dhcpi = self.dhcpiIV.get()
		self.dnsi = self.dnsiIV.get()
		self.sambai = self.sambaiIV.get()
		self.NAT = 	self.NATIV.get()

		try:

			self.sambaBASIC = self.sambaBASICIV.get()
			self.sambaDC = self.sambaDCIV.get()

			self.filename = self.filenameSV.get()
			self.shfoldername = self.shfoldernameSV.get()
			self.validusers = self.validusersSV.get()

			self.guestok = self.guestokIV.get()
			self.browseable = self.browseableIV.get()
			self.readonly = self.readonlyIV.get()

		except:
			pass

		try:
			self.servername = self.servernameSV.get()
			self.gateway = self.gatewaySV.get()
		except:
			pass

		try:
			self.ip2 = self.ip2SV.get()
			self.netmask2 = self.netmask2SV.get()
			self.prefix2 = self.prefix2SV.get()
			self.subnetforinternalnet = self.subnetforinternalnetSV.get()
			self.cardname2 = self.cardname2SV.get()
		except:
			pass
		try:
			self.cardname1 = self.cardname1SV.get()
			self.subnetforexternalnet = self.subnetforexternalnetSV.get()
			self.ip1 = self.ip1SV.get()
			self.netmask1 = self.netmask1SV.get()
			self.prefix1 = self.prefix1SV.get()
		except:
			pass
		try:
			self.dnsname = self.dnsnameSV.get()
			self.subnetfordhcp = self.subnetfordhcpSV.get()
			self.maskfordhcp = self.maskfordhcpSV.get()
			self.dhcprangefrom = self.dhcprangefromSV.get()
			self.dhcprangeto = self.dhcprangetoSV.get()

		except:
			pass

		if self.dhcpi == 1:
			subprocess.call(["yum","install","dhcp","-y"])

		if self.dnsi == 1:
			subprocess.call(["yum","install","bind*","bind-utils","-y"])

		if self.sambai == 1:
			subprocess.call(["yum","install","samba","-y"])
			subprocess.call(["yum","install","samba-client","-y"])
			subprocess.call(["yum","install","samba-common","-y"])

		if self.NAT == 	1:
			self.NATconfig()

		self.NICconfig()
		self.DNSconfig()
		self.DHCPconfig()
		self.sambaconfigprocess()
		self.reboot()

	def NICconfig(self): #########################################################################################################################################################################
		print("___________________________________SETTING UP NETWORK CARDS..._____________________________")
		self.directorytoc1 = "/etc/sysconfig/network-scripts/ifcfg-{}".format(self.cardname1)
		self.directorytoc2 = "/etc/sysconfig/network-scripts/ifcfg-{}".format(self.cardname2)

		try:
			with open(self.directorytoc2,"r",encoding="iso 8859-2") as netfile1:
				container = []
				for line in netfile1:

					if "dhcp" in line:
						container.append(line.replace("dhcp","static"))

					elif "IPADDR" not in line:
						if "DNS1" not in line:
							if "DNS2" not in line:
								if "DOMAIN" not in line:
									if "NETMASK" not in line:
										if "GATEWAY" not in line:
											container.append(line)



			with open(self.directorytoc2,"w",encoding="iso 8859-2") as netfile1:
				for i in container:
					netfile1.write(i)
				netfile1.write(("GATEWAY={}\n").format(self.gateway))
				netfile1.write(("IPADDR={}\n").format(self.ip2))
				netfile1.write(("NETMASK={}\n").format(self.netmask2))
				netfile1.write(("DOMAIN={}{}{}\n").format(self.kvota1,str(self.dnsname),self.kvota1))
				netfile1.write(("DNS1={}\n").format(self.ip2))
				netfile1.write(("DNS2=8.8.8.8\n"))
		except:
			print("no internal card configured(Missing folder or Physical card) ")

		if self.externalAsDhcpVar == 0:

			try:


				with open(self.directorytoc1,"r",encoding="iso 8859-2") as netfile1:
					container = []
					for line in netfile1:
						status=0
						if "dhcp" in line:
							container.append(line.replace("dhcp","static"))

						elif "IPADDR" not in line:
							if "DNS1" not in line:
								if "DNS2" not in line:
									if "DOMAIN" not in line:
										if "NETMASK" not in line:
											if "GATEWAY" not in line:
												container.append(line)


				with open(self.directorytoc1,"w",encoding="iso 8859-2") as netfile1:
					for i in container:
						netfile1.write(i)
					netfile1.write(("GATEWAY={}\n").format(self.gateway))
					netfile1.write(("IPADDR={}\n").format(self.ip1))
					netfile1.write(("NETMASK={}\n").format(self.netmask1))
					netfile1.write(("DOMAIN={}{}{}\n").format(self.kvota1,str(self.dnsname),self.kvota1))
					netfile1.write(("DNS1={}\n").format(self.ip2))
					netfile1.write(("DNS2=8.8.8.8\n"))

			except:
				print("no external card configured(Missing folder or Physical card) ")
		else:
			pass


		with open("/etc/sysconfig/network","w") as networkfile:
			networkfile.write("NETWORKING=yes\n")
			networkfile.write(("HOSTNAME={}\n").format(self.servername))

		with open("/etc/resolv.conf","w") as resolvfile:
			resolvfile.write(("search {}\n").format(self.dnsname))
			resolvfile.write(("nameserver {}\n").format(self.ip2))
			resolvfile.write("nameserver 8.8.8.8\n")

		print("Done..........")

	def DNSconfig(self):####################################################################################################################################################################x

		self.ip_rev = self.ip2.split(".")
		self.ip_rev = self.ip_rev[::-1]
		self.ip_rev = ".".join(self.ip_rev[1:])

		self.dnsname_short = self.dnsname.split(".")
		self.dnsname_short = self.dnsname_short[0]

		self.curly_bracket_left = "{"
		self.curly_bracket_right = "}"

		self.directory_for_zone = "/var/named/{}.zone".format(self.dnsname_short)
		self.directory_for_revzone = "/var/named/{}.rev".format(self.dnsname_short)

		with open("/etc/named.conf","w") as namedconf:

			namedconf.write("// named.conf\n")
			namedconf.write("//\n")
			namedconf.write("// Provided by Red Hat bind package to configure the ISC BIND named(8) DNS\n")
			namedconf.write("// server as a caching only nameserver (as a localhost DNS resolver only).\n")
			namedconf.write("//\n")
			namedconf.write("// See /usr/share/doc/bind*/sample/ for example named configuration files.\n")
			namedconf.write("// See the BIND Administrator's Reference Manual (ARM) for details about the\n")
			namedconf.write("// configuration located in /usr/share/doc/bind-{version}/Bv9ARM.html\n")

			namedconf.write("options {\n")
			namedconf.write(("        listen-on port 53 {} 127.0.0.1;{}; {};\n").format(self.curly_bracket_left,self.ip2,self.curly_bracket_right))
			namedconf.write("        listen-on-v6 port 53 { ::1; };\n")
			namedconf.write('	        directory       "/var/named";\n')
			namedconf.write('	        dump-file       "/var/named/data/cache_dump.db";\n')
			namedconf.write('	        statistics-file "/var/named/data/named_stats.txt";\n')
			namedconf.write('	        memstatistics-file "/var/named/data/named_mem_stats.txt";\n')
			namedconf.write('	        recursing-file  "/var/named/data/named.recursing";\n')
			namedconf.write('	        secroots-file   "/var/named/data/named.secroots";\n')
			namedconf.write(('	        allow-query     {} localhost;{}/{}; {};\n').format(self.curly_bracket_left,self.subnetforinternalnet,self.prefix2,self.curly_bracket_right))

			namedconf.write('	        /*\n')
			namedconf.write('	         - If you are building an AUTHORITATIVE DNS server, do NOT enable recursion.\n')
			namedconf.write('	         - If you are building a RECURSIVE (caching) DNS server, you need to enable\n')
			namedconf.write('	           recursion.\n')
			namedconf.write('	         - If your recursive DNS server has a public IP address, you MUST enable access\n')
			namedconf.write('	           control to limit queries to your legitimate users. Failing to do so will\n')
			namedconf.write('	           cause your server to become part of large scale DNS amplification\n')
			namedconf.write('	           attacks. Implementing BCP38 within your network would greatly\n')
			namedconf.write('	           reduce such attack surface\n')
			namedconf.write('	        */\n')
			namedconf.write('	        recursion yes;\n')

			namedconf.write('	        dnssec-enable yes;\n')
			namedconf.write('	        dnssec-validation yes;\n')

			namedconf.write('	        /* Path to ISC DLV key */\n')
			namedconf.write('	        bindkeys-file "/etc/named.iscdlv.key";\n')

			namedconf.write('	        managed-keys-directory "/var/named/dynamic";\n')

			namedconf.write('	        pid-file "/run/named/named.pid";\n')
			namedconf.write('	        session-keyfile "/run/named/session.key";\n')
			namedconf.write('};\n')

			namedconf.write('	logging {\n')
			namedconf.write('	        channel default_debug {\n')
			namedconf.write('	                file "data/named.run";\n')
			namedconf.write('	                severity dynamic;\n')
			namedconf.write('	        };\n')
			namedconf.write('};\n')

			namedconf.write('	zone "." IN {\n')
			namedconf.write('	        type hint;\n')
			namedconf.write('	        file "named.ca";\n')
			namedconf.write('	};\n')

			namedconf.write(('	zone "{}" IN {}\n').format(self.dnsname,self.curly_bracket_left))
			namedconf.write('		type master;\n')
			namedconf.write(('		file "{}.zone";\n').format(self.dnsname_short))
			namedconf.write('		allow-update { none; };\n')
			namedconf.write('	};\n')

			namedconf.write(('	zone "{}.in-addr.arpa" IN {}\n').format(self.ip_rev,self.curly_bracket_left))
			namedconf.write('		type master;\n')
			namedconf.write(('		file "{}.rev";\n').format(self.dnsname_short))
			namedconf.write('		allow-update { none; };\n')
			namedconf.write('	};\n')

			namedconf.write('	include "/etc/named.rfc1912.zones";\n')
			namedconf.write('	include "/etc/named.root.key";\n')

		with open(self.directory_for_zone,"w",encoding="iso 8859-2") as zone:
			zone.write(("$ORIGIN {}.\n").format(self.dnsname))
			zone.write("$TTL 86400\n")
			zone.write(("@	IN	SOA	dns1.{}. hostmaster.{}. (\n").format(self.dnsname,self.dnsname))
			zone.write("	2001062501	; serial\n")
			zone.write("	21600	;refresh after 6 hours\n")
			zone.write("	3600	;retry after 1 hour\n")
			zone.write("	604800	;expire after week\n")
			zone.write("	86400 )	;minimum TTL 1 day\n")
			zone.write(("	IN	NS	dns1.{}.\n").format(self.dnsname))
			zone.write(("	IN	MX	10	mail.{}.\n").format(self.dnsname))
			zone.write(("	IN	A	{}\n").format(self.ip2))
			zone.write(("dns1	IN	A	{}\n").format(self.ip2))
			zone.write(("server	IN	A	{}\n").format(self.ip2))
			zone.write(("ftp	IN	A	{}\n").format(self.ip2))
			zone.write(("mail	IN	CNAME	{}\n").format(self.servername))
			zone.write(("www	IN	CNAME	{}\n").format(self.servername))

		with open(self.directory_for_revzone,"w",encoding="iso 8859-2") as rev:
			rev.write(("$ORIGIN {}.in-addr.arpa.\n").format(self.ip_rev))
			rev.write("$TTL 86400\n")
			rev.write(("@	IN	SOA	dns1.{}. hostmaster.{}. (\n").format(self.dnsname,self.dnsname))
			rev.write("		2001062501	; serial\n")
			rev.write("		21600	;refresh after 6 hours\n")
			rev.write("		3600	;retry after 1 hour\n")
			rev.write("		604800	;expire after week\n")
			rev.write("		86400 )	;minimum TTL 1 day\n")
			rev.write(("@	IN	NS	{}.{}.\n").format(self.servername,self.dnsname))
			rev.write(("1	IN	PTR	{}.{}.\n").format(self.servername,self.dnsname))
			rev.write(("2	IN	PTR	{}.{}.\n").format(self.servername,self.dnsname))
			rev.write(("3	IN	PTR	{}.{}.\n").format(self.servername,self.dnsname))
			rev.write(("4	IN	PTR	{}.{}.\n").format(self.servername,self.dnsname))

		print("DNS-DONE...")

	def DHCPconfig(self):

		with open("/etc/dhcp/dhcpd.conf","w") as dhcp:

			dhcp.write(('option domain-name "{}";\n').format(self.dnsname))
			dhcp.write(("option domain-name-servers {},8.8.8.8;\n").format(self.ip2))
			dhcp.write("default-lease-time 600;\n")
			dhcp.write("authoritative;\n")
			dhcp.write("log-facility local7;\n")
			dhcp.write(("subnet {} netmask {} {}\n").format(self.subnetfordhcp,self.maskfordhcp,self.curly_bracket_left))
			dhcp.write("}\n")
			dhcp.write(("subnet {} netmask {} {}\n").format(self.subnetfordhcp,self.maskfordhcp,self.curly_bracket_left))
			dhcp.write(("	range	{}	{};\n").format(self.dhcprangefrom,self.dhcprangeto))
			dhcp.write(("	option routers		{};\n").format(self.ip2))
			dhcp.write(("	option domain-search            {}{}{};\n").format(self.kvota1,self.dnsname,self.kvota1))
			dhcp.write(("	option domain-name-servers      {} ;\n").format(self.ip2))
			dhcp.write("}\n")


		print("DHCP-DONE...")
		subprocess.call(["systemctl","enable","dhcpd"])
		subprocess.call(["systemctl","start","dhcpd"])
		subprocess.call(["systemctl","enable","named"])
		subprocess.call(["systemctl","start","named"])

	def NATconfig(self):

		subprocess.call(["systemctl","restart","systemd-sysctl"])
		subprocess.call(["sysctl","-w","net.ipv4.ip_forward=1"])

		subprocess.call(["firewall-cmd","--complete-reload"])
		subprocess.call(["firewall-cmd","--list-all-zones"])

		subprocess.call(["firewall-cmd","--zone=external","--add-masquerade","--permanent"])
		subprocess.call(["firewall-cmd","--permanent","--direct","--passthrough","ipv4","-t","nat","-I","POSTROUTING","-o",self.cardname1,"-j","MASQUERADE","-s","{}/{}".format(self.ip1,self.prefix1)])

		subprocess.call(["firewall-cmd","--change-interface={}".format(self.cardname1),"--zone=external","--permanent"])
		subprocess.call(["firewall-cmd","--set-default-zone=internal"])

		subprocess.call(["firewall-cmd","--permanent","--zone=internal","--add-service=dhcp"])
		subprocess.call(["firewall-cmd","--permanent","--zone=internal","--add-service=tftp"])
		subprocess.call(["firewall-cmd","--permanent","--zone=internal","--add-service=dns"])
		subprocess.call(["firewall-cmd","--permanent","--zone=internal","--add-service=http"])
		subprocess.call(["firewall-cmd","--permanent","--zone=internal","--add-service=nfs"])
		subprocess.call(["firewall-cmd","--permanent","--zone=internal","--add-service=ssh"])
		subprocess.call(["firewall-cmd","--permanent","--zone=internal","--add-service=samba"])

		subprocess.call(["firewall-cmd","--complete-reload"])
		subprocess.call(["firewall-cmd","--list-all-zones"])
	def reboot(self):
		print("system will reboot in 10s")
		t = 10
		while t:
			print(t)
			time.sleep(1)
			t -= 1
		print('Rebooting!!')
		subprocess.call("reboot")

root = Tk()
start = ServerConfig(root)
root.mainloop()
