import datetime
from flask import Flask
from flask import request
from DripRequest import *
from flask import redirect
from random import randrange
from datetime import datetime
from datetime import timedelta
from flask import render_template

app = Flask(__name__)

# Problems:
# Handle Input Better
# Improve Captcha Security with SHA Hashing
# Improve IP Address Obfuscation

# Features:
# Autodeploy Using Github Hooks
# Revamp Coupon System

# Globals
DATABASE_FILE = 'trc.db'
DATABASE_TABLE = 'drip_request'
DEFAULT_SEND_VAL = 0.0001

# Helper Functions
def sub_cypher(num, offset):
	"""Number substitution offset cypher. Don't use offset values 0-9."""
	# Implement Better Cypher: rotate((ip % sum1bits(ip) ), sum0bits(ip))
	return [(abs(int(x) - offset)%10) if x.isdigit() else '.' for x in num]

def get_html(save_time, ip, trans_id):
	"""Transform database output into a table."""
	diff_time = datetime.now() - datetime.strptime(save_time, "%Y-%m-%d %H:%M:%S")
	diff_time = divmod(diff_time.seconds, 60)
	diff_time = "{0} mins, {1} secs ago".format(diff_time[0], diff_time[1])
	obfuscated_ip = ''.join(map(str, sub_cypher(list(ip), 655)))
	if trans_id == "UNSENT":
		html = "<tr><td>{0}</td><td>{1}</td><td>Processing...</td></tr>"
		html = html.format(diff_time, obfuscated_ip)
	else:
		short_trans_id = trans_id[:37] + "..."
		trans_id_url = "http://cryptocoinexplorer.com:3750/tx/{0}".format(trans_id)
		html = "<tr><td>{0}</td><td>{1}</td><td><a href='{2}'>{3}</a></td></tr>"
		html = html.format(diff_time, obfuscated_ip, trans_id_url, short_trans_id)
	
	return html

def get_index(form_submit_status = None):
	"""Displays the default index page, or a success/error page."""
	data = Database(DATABASE_FILE, DATABASE_TABLE)
	captcha = (randrange(1, 15), randrange(1, 15))
	captcha_awns = captcha[0] + captcha[1]
	recent_drips = data.get_recent()
	recent_drips_html = [get_html(x[1], x[2], x[5]) for x in recent_drips if True]
	recent = ''.join(map(str, recent_drips_html))
	stats = 3060 + data.get_count()[0][0]
	return render_template('index.html', recent=recent, form_submit=form_submit_status,
						   captcha=captcha, captcha_awns=captcha_awns, stats=stats)

def send_coins():
	"""Sends queued coins."""
	data = Database(DATABASE_FILE, DATABASE_TABLE)
	for i in data.get_unsent():
		DripRequest(i[3], i[4], i[2], i[0]).send(DEFAULT_SEND_VAL, data)
	return "Sent!"

# Routes
@app.route('/')
def index(): return get_index()

@app.route('/add', methods=['POST'])
def add(): 
	ip = str(request.remote_addr)
	try:
		if request.form['captcha'] != request.form['captcha_awns']: 
			raise ValueError
		print("Good drip request. Saving to database...")
		data = Database(DATABASE_FILE, DATABASE_TABLE)
		DripRequest(request.form['address'], request.form['coupon'],
				    ip).save(data)
		return redirect('/good')
	except ValueError:
		print("Bad drip request. Redirecting...")
		return redirect('/bad')
	except LookupError:
		print("Duplicate IP or Address. Redirecting...")
		return redirect('/duplicate')
	else:
		print("Unexplained failure.")
		return redirect('/bad')

@app.route('/send')
def send(): return send_coins()
@app.route('/good')
def good(): return get_index("good")
@app.route('/bad')
def bad(): return get_index("bad")
@app.route('/duplicate')
def duplicate(): return get_index("duplicate")

@app.route('/chat')
def chat(): return render_template('chat.html')
@app.route('/resources')
def resources(): return render_template('resources.html')

#@app.route('/gitdeploy-hj83k5')
#def deploy(): subprocess.call(["sh /root/deploy.sh"], cwd='/root/')

# Main
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True)