import xml.etree.ElementTree as ET
import requests
import time
import pynotify

URL = "http://synd.cricbuzz.com/j2me/1.0/livematches.xml"

def Main():
	print "Starting Cricbuzz Scrapper...\n"
	try: 
		handle = requests.get(URL).content
	except:
		print 'Something wrong with your Internet connection'
		exit(1)
	# handle = open('livematches.xml').read()
	root = ET.fromstring(handle)
	livematches = []
	for i in root:
		if i.tag == "match":
			state = i.find('state')
			if state.attrib['mchState'] == "inprogress":
				livematches.append(i.attrib['mchDesc'])
			else:
				print i.attrib['mchDesc'] +'\n'+ state.attrib['status']+'\n\n'

	print "Live matches:"+str(len(livematches))
	for x,i in enumerate(livematches):
		print "\t"+str(x+1)+"."+i
	print
	pynotify.init("Start")
	if len(livematches)>0:
		myteam = int(raw_input("Select match:"))
		while 1:
			# handle = open('livematches.xml').read()
			try: 
				handle = requests.get(URL).content
			except :
				print 'Something wrong with your Internet connection,trying again..'
				pass
			root = ET.fromstring(handle)
			for i in root.iter('match'):
				state = i.find('state')
				if livematches[myteam-1] == i.attrib['mchDesc']:
					if state.attrib['mchState']=="inprogress":
						try:
							ee = i.find('mscr')
							inningsDetail = ee.find('inngsdetail')
							overs = inningsDetail.attrib['noofovers']
							crr = inningsDetail.attrib['crr']
							cprtshp = inningsDetail.attrib['cprtshp']
							print '\033[91m'+ str(i.attrib['mchDesc']) + '\033[0m'
							ing = ee.find('btTm')
							team = ing.attrib['sName']
							inngs = ing.find('Inngs')
							score = inngs.attrib['r']
							overs = inngs.attrib['ovrs']
							wkts = inngs.attrib['wkts']
							note = str(team)+'\t'+str(score) +"-"+ str(wkts) + "\t\n\nOvers: " + str(overs) +"\n\nCRR: "+str(crr) +"\n\nPartnership: "+str(cprtshp)+'\n'
							pynotify.Notification(summary=note).show()
							print str(team)+'\t'+str(score) +"-"+ str(wkts) + "\t" + str(overs)
						except:
							pass

						try:
							ing = ee.find('blgTm')
							team = ing.attrib['sName']
							inngs = ing.find('Inngs')
							score = inngs.attrib['r']
							overs = inngs.attrib['ovrs']
							wkts = inngs.attrib['wkts']
							note = str(team)+'\t'+str(score) +"-"+ str(wkts) + "\t" + str(overs) +"\nCRR: "+str(crr) +"\tPartnership: "+str(cprtshp)+state.attrib['status'] +'\n'
							notification = pynotify.Notification(summary=note)
							notification.show()
							print str(team)+'\t'+str(score) +"-"+ str(wkts) + "\t" + str(overs)
							print "\nCRR: "+str(crr) +"\tPartnership: "+str(cprtshp)
							print state.attrib['status'] +'\n'
						except:pass
					else:
						print '\033[91m'+ str(i.attrib['mchDesc']) + '\033[0m'
						print '\033[94m'+ state.attrib['status'] + '\033[0m'
						exit()
				else:
					# print "asdf"
					pass
			print
			time.sleep(20)
	else:
		print "No live matches.."


if __name__ == "__main__":
	Main()
