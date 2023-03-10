import streamlit as st
from streamlit_chat import message
from courier_gateway import ThreadedMessenger
from NLU import time_final, process_content
import datetime
import re
import parsedatetime

def get_text():
	input_text = st.text_input("You: ","Hello, how are you?", key="input")
	return input_text 

def query(courier_auth_token, slack_auth_token, params):
	prestring = ""
	if params["desc"] == "None":
		user_input = params['text']
		tmp_input = re.sub(r'[^\w\s]', '', user_input)
		time = time_final(tmp_input)
		default_time=time_final('')
		if time == default_time:
			return "Please enter your appointment details!", "NLU"
		else:
			details = process_content(user_input)
		app_time = time
		date_time_str = app_time
		date_time_obj = datetime.datetime.strptime(date_time_str, '%m-%d-%Y %H:%M:%S')
		date_time_obj_now = datetime.datetime.now()
		diff = date_time_obj - date_time_obj_now
		diff_seconds = diff.total_seconds()
		if diff_seconds<0:
			return "You can't schedule an appointment in the past!", "NLU"
		else:
			if "slack" in params["text"].lower():
				mode_type = "slack"
				email = 'Sending to Slack'
			else:
				mode_type = "email"
				match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', user_input)
				try:
					email = match.group(0)
				except:
					details += " (Default Email: amanpriyanshusms2001@gmail.com)"
					email = "amanpriyanshusms2001@gmail.com"
			toDetails = {'timeDetails': str(date_time_obj.time()), 'eventDetails': str(details), 'email': email}
			if diff_seconds>1800:
				ThreadedMessenger(courier_auth_token, slack_auth_token, toDetails, diff_seconds-1800, mode_type)
				ThreadedMessenger(courier_auth_token, slack_auth_token, toDetails, diff_seconds, mode_type)
				return "Scheduled an appointment for "+str(date_time_obj)+" with the specific details! With a reminder 30 minutes before your meeting.", "NLU"
			else:
				ThreadedMessenger(courier_auth_token, slack_auth_token, toDetails, diff_seconds, mode_type)
				return "Scheduled an appointment for "+str(date_time_obj)+" with the specific details!", "NLU"
	else:
		app_time = str(params["time"])
		if '.' in app_time:
			app_time = app_time[:app_time.index('.')]
		date_time_str = str(params["date"])+" "+app_time
		date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
		l_desc = params['desc'].lower()
		date_time_obj_now = datetime.datetime.now()
		diff = date_time_obj - date_time_obj_now
		diff_seconds = diff.total_seconds()
		if diff_seconds<0:
			return "You can't schedule an appointment in the past!", "Manual"
		else:
			mode_type = "email"
			toDetails = {'timeDetails': str(date_time_obj.time()), 'eventDetails': str(params["desc"]), 'email': "amanpriyanshusms2001@gmail.com"}
			if diff_seconds>1800:
				ThreadedMessenger(courier_auth_token, slack_auth_token, toDetails, diff_seconds-1800, mode_type)
				ThreadedMessenger(courier_auth_token, slack_auth_token, toDetails, diff_seconds, mode_type)
				return "Scheduled an appointment for "+str(params["date"])+" "+str(params["time"])+" to the user's amanpriyanshusms2001@gmail.com! With a reminder 30 minutes before your meeting.", "Manual"
			else:
				ThreadedMessenger(courier_auth_token, slack_auth_token, toDetails, diff_seconds, mode_type)
				return "Scheduled an appointment for "+str(params["date"])+" "+str(params["time"])+" to the user's amanpriyanshusms2001@gmail.com!", "Manual"

def clear_desc():
	st.session_state['description'] = 'None' 
	return 'None'


def main():
	st.title("Chat with our Bespoke Pigeon")
	st.markdown("##### We use Courier to deliver your messages, whereas our in-house chatbot helps organize your schedules amonst individuals or your slack team.")
	with st.sidebar:
		st.image('logo.png')
		courier_auth_token = st.text_input("Enter Courier Auth-Token", type="password")
		slack_auth_token = st.text_input("Enter Slack Auth-Token", type="password")

	if 'generated' not in st.session_state:
		st.session_state['generated'] = []
	if 'past' not in st.session_state:
		st.session_state['past'] = []

	with st.expander("Schedule your appointment (manually)"):
		_, col_j = st.columns([4, 1])
		with col_j:
			if st.button("Reset"):
				st.session_state['description'] = 'None'
		col_a, col_b, col_c = st.columns([1, 1, 4])
		with col_a:
			d = st.date_input("Enter Date", datetime.datetime.now().date())
		with col_b:
			t = st.time_input('Enter Time', datetime.datetime.now().time())
		with col_c:
			placeholder = st.empty()
			desc = placeholder.text_input("Enter Details", "None", key="description")

	col1, col2 = st.columns([7, 1])
	with col1:
		user_input = get_text()
	with col2:
		st.text("")
		st.text("")
		if st.button("Send"):
			output, response = query(courier_auth_token, slack_auth_token, {
					"date": d,
					"time": t,
					"desc": desc,
					"text": user_input,
				})
			if response=='Manual':
				st.session_state.past.append("Manually entered: "+str(d)+" "+str(t)+". With Details: "+desc)
			else:
				st.session_state.past.append(user_input)
			st.session_state.generated.append(output)

	if st.session_state['generated']:
		for i in range(len(st.session_state['generated'])-1, -1, -1):
			message(st.session_state["generated"][i], key=str(i))
			message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

if __name__ == '__main__':
	main()