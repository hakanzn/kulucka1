from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils
import time

class kulucka:
	def __init__(self):
		self.bekle = 1
		self.host = "212.154.74.164"
		self.port = 502
		self.timeout = 2000
		self.c = None
		self.sonuc = {}
		
		
	def baglan(self):
		self.c = ModbusClient(host=self.host, unit_id=1,timeout=self.timeout,auto_open=True, auto_close=True,port=self.port)
		
		
	def main(self):
		self.c.open()
		regs = self.c.read_holding_registers(12288,6)
		if regs:
			self.parse(regs)
		else:
			print("read error")
		self.c.close()
		
			
	def parse(self, regs):
			k = 1
			for i in range(0, len(regs), 2):
				sicaklik = regs[i] / 10
				nem = regs[i+1] / 10
				self.sonuc["kulucka"+str(k)]= {"sicaklik":sicaklik, "nem":nem}
				
				k += 1
			print()
			
		


