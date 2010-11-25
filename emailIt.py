import sys
import os

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

import optparse
from optparse import OptionParser

#########################################################
#
# emailIt function
#
# A free, no authentication internet SMTP server: relay.free-online.co.uk
#
#########################################################

def emailIt():

	# Constants

	# Internal variables with initial values

	usage = "Usage: %prog [options]"
	parser = OptionParser(usage)

	parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=True, 
			help="verbose debug output to stdout")

	parser.add_option("-q", "--quiet", action="store_false", dest="verbose", 
			help="no verbose debug output to stdout")

	parser.add_option("-t", "--to", dest="send_to_list", default=None,
			help="address(es) to send the email to", action="append")

	parser.add_option("-f", "--from", dest="from_address", default=None,
			help="email from address", action="store")

	parser.add_option("-s", "--subject", dest="subject", default=None,
			help="email subject", action="store")

	parser.add_option("", "--server", dest="server", default=None,
			help="smtp email server address", action="store")

	parser.add_option("-b", "--body", dest="body", default=None,
			help="email message text body", action="store")

	parser.add_option("-a", "--attach", dest="attach_list", default=None,
			help="file(s) to attach to the email", action="append")

	(options, args) = parser.parse_args()

	if len(args) != 0:
		parser.error("Incorrect number of arguments (-h for help)")

	if options.verbose == True:
		print("")
		print("Verbose output")
		print("")

	if options.from_address == None:
		parser.error("Email from address not set (-h for help)")
		
	if options.send_to_list == None:
		parser.error("Email to address(es) not set (-h for help)")

	if options.subject == None:
		parser.error("Email subject not set (-h for help)")

	if options.server == None:
		parser.error("SMTP email server not set (-h for help)")

	if options.body == None:
		if options.attach_list == None:
			parser.error("Must specify email message text body or files to attach (-h for help)")
		
	if options.verbose == True:
		print("Email From: "+options.from_address)
		print("Email To: "+",".join(options.send_to_list))
		print("Email Subject: "+options.subject)
		if options.body != None:
			print("Email Body Test: "+options.body)
		if options.attach_list != None:
			print("Attach Files: "+",".join(options.attach_list))
			
	msg = MIMEMultipart()
	msg['From'] = options.from_address
	msg['To'] = COMMASPACE.join(options.send_to_list)
	msg['Date'] = formatdate(localtime=True)
	msg['Subject'] = options.subject

	msg.attach( MIMEText(options.body) )

	for f in options.attach_list:
		part = MIMEBase('application', "octet-stream")
		part.set_payload( open(f,"rb").read() )
		Encoders.encode_base64(part)
		part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
		msg.attach(part)

	smtp = smtplib.SMTP(options.server)
	smtp.sendmail(options.from_address, options.send_to_list, msg.as_string())
	smtp.close()
	
#########################################################
#
# Main function call if running from command line
#
#########################################################

if __name__ == "__main__":
    sys.exit(emailIt())

