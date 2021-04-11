import win32clipboard
from io import BytesIO
from pynput.keyboard import Key, Controller,Listener
from pynput import keyboard
import keyboard
import clipboard
import winclip32
from PIL import Image,ImageGrab , BmpImagePlugin
import time
import os


class Sclip:

	def __init__(self):
		self.placeholder = ""
		self.content = ""
		self.kb = Controller()

		with open("content.env" , "r") as j:
			if(len(j.readlines()) < 10):
				self.SendtoSecondaryRaw(j.read())
			j.close()

	def __SetClipData(self,data,arg):
	
		if(ImageGrab.grabclipboard() == None):
			try:
				win32clipboard.OpenClipboard()
				self.placeholder = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
			except:
				self.placeholder = ""
		else:
			self.placeholder = ImageGrab.grabclipboard()


		win32clipboard.OpenClipboard()
		win32clipboard.EmptyClipboard()
		win32clipboard.SetClipboardData(arg, data)
		win32clipboard.CloseClipboard()


	def SendtoMainClipboard(self, k , img=False):
		if(img):
			print(k)
			output = BytesIO()
			k.convert('RGB').save(output,'BMP')
	
			self.__SetClipData(output.getvalue()[14:] , win32clipboard.CF_DIB)
			output.close()
		else:
			self.__SetClipData(k , win32clipboard.CF_UNICODETEXT)


	def SendtoSecondaryClipboard(self):
		self.SendtoMainClipboard(" ")
		self.content = self.placeholder


		with open("content.env" , "w") as h:
			try:
				h.write(self.content)
			except:
				i = BytesIO()
				self.content.save(i , format = "BMP")
				h.write(str(i.getvalue()))


	def SendtoSecondaryRaw(self,k):
		self.content = k


	def SwapClipboards(self):
		if(win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT)):
			win32clipboard.OpenClipboard()
			curr_clip = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
			win32clipboard.CloseClipboard()

			pl = self.content

			self.content = curr_clip
			if(type(pl) == str):
				win32clipboard.OpenClipboard()
				win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT , pl)
				win32clipboard.CloseClipboard()
			elif(type(pl) == bytes):
				win32clipboard.OpenClipboard()
				win32clipboard.SetClipboardData(win32clipboard.CF_DIB , pl)
				win32clipboard.CloseClipboard()
			else:
				otpt = BytesIO()
				pl.convert('RGB').save(otpt , 'BMP')
				win32clipboard.OpenClipboard()
				win32clipboard.SetClipboardData(win32clipboard.CF_DIB , otpt.getvalue()[14:])
				win32clipboard.CloseClipboard()

		elif(win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_DIB)):
			win32clipboard.OpenClipboard()
			curr_clip = win32clipboard.GetClipboardData(win32clipboard.CF_DIB)
			win32clipboard.CloseClipboard()

			plc = self.content

			self.content = curr_clip
			if(type(plc) == str):
				win32clipboard.OpenClipboard()
				win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT , plc)
				win32clipboard.CloseClipboard()
			elif(type(plc) == bytes):
				win32clipboard.OpenClipboard()
				win32clipboard.SetClipboardData(win32clipboard.CF_DIB , plc)
				win32clipboard.CloseClipboard()
			else:
				otpt = BytesIO()
				plc.convert('RGB').save(otpt , 'BMP')
				win32clipboard.OpenClipboard()
				win32clipboard.SetClipboardData(win32clipboard.CF_DIB , otpt.getvalue()[14:])
				win32clipboard.CloseClipboard()


	def EmptySClip(self):
		self.content = None


	def EmptyClipboards(self):
		self.EmptySClip()

		win32clipboard.OpenClipboard()
		win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT , " ")
		win32clipboard.CloseClipboard()


	def PasteMainClip(self):
		self.kb.press(Key.ctrl)
		self.kb.press('v')
		self.kb.release(Key.ctrl)
		self.kb.release('v')

	def PasteFromSclip(self):
		self.SwapClipboards()
		time.sleep(0.1)
		self.PasteMainClip()
		time.sleep(0.1)		
		self.SwapClipboards()


