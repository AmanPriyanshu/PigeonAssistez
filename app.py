import streamlit as st
from streamlit_chat import message

def get_text():
	input_text = st.text_input("You: ","Hello, how are you?", key="input")
	return input_text 

def query(params):
	return "Lmao"

def main():
	with st.sidebar:
		st.image('logo.png')
		courier_auth_token = st.text_input("Enter Courier Auth-Token", type="password")
		slack_auth_token = st.text_input("Enter Slack Auth-Token", type="password")

	if 'generated' not in st.session_state:
		st.session_state['generated'] = []
	if 'past' not in st.session_state:
		st.session_state['past'] = []

	col1, col2 = st.columns([5, 1])
	with col1:
		user_input = get_text()
	with col2:
		st.text("")
		st.text("")
		if st.button("Send"):
			output = query({
					"past_user_inputs": st.session_state.past,
					"generated_responses": st.session_state.generated,
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