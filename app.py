import streamlit as st
from streamlit_chat import message
import datetime

def get_text():
	input_text = st.text_input("You: ","Hello, how are you?", key="input")
	return input_text 

def query(params):
	if params["desc"] == "None":
		pass #analyze using NLP thingy
	else:
		return "We got da time"+str(params["date"])+" "+str(params["time"])+"-->"+str(params["desc"])
	return "Lmao"

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
			output = query({
					"date": d,
					"time": t,
					"desc": desc,
					"text": user_input,
				})
			st.session_state.past.append(user_input)
			st.session_state.generated.append(output)

	if st.session_state['generated']:
		for i in range(len(st.session_state['generated'])-1, -1, -1):
			message(st.session_state["generated"][i], key=str(i))
			message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

if __name__ == '__main__':
	main()