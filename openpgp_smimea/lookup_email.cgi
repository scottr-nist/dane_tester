#!/usr/bin/env python3
# -*- mode: python; -*-
#
# Perform an email lookup
#
import cgitb;cgitb.enable()
from mako.template import Template
from tester import Tester
import dbmaint
import tester
import cgi
import sys

# Force output to be encoded in UTF8
# http://stackoverflow.com/questions/14860034/python-cgi-utf-8-doesnt-work
import codecs; sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

from subprocess import call,Popen,PIPE
import smimea
import openpgpkey

ANONYMOUS_USER="anonymous"
ANONYMOUS_HASH="Oijb1q03QNM="

def testid_html(testid,hash):
   return "<a href='lookup_test.cgi?testid={}&hash={}' target='_blank'>{}</a>".format(testid,hash,testid)

if __name__=="__main__":

   form = cgi.FieldStorage()
   try:
      email = form['email'].value
   except KeyError as e:
      email = ""

   from tester import Tester
   T = Tester()
   T.login(ANONYMOUS_USER,ANONYMOUS_HASH)
   T.newtest(testname="dig")

   print("Content-Type: text/html")    # HTML is following
   print()
   print("""<html><body>""")
   print("<p><i>Test {}</i></p>".format(testid_html(T.testid,ANONYMOUS_HASH)))
   print("<h3>SMIMEA Lookup for <tt>{}</tt></h3>".format(email))

   data = smimea.smimea_to_txt(T,email)
   if data:
      print("<pre>{}</pre>".format(data))
   else:
      print("<p>No SMIMEA record for {}</p>".format(email))

   print("<h3>OPENPGPA Lookup for <tt>{}</tt></h3>".format(email))
   data = openpgpkey.openpgpkey_to_txt(T,email)
   if data:
      print("<pre>{}</pre>".format(data))
   else:
      print("<p>No OPENPGPA record for {}</p>".format(email))

   
   print("<h3>Tester Status</h3>")
   if dbmaint.user_hash(T.conn,email=email):
      print("<p><tt>{}</tt> is a registered user of this system.</p>".format(email))
   else:
      print("<p><tt>{}</tt> is not a registered user of this system.</p>".format(email))

   print("</body></html>")
   T.commit()
