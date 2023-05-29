from nodes import nodes,label_templates
import random
import datetime
import os
import time
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

SLACK_TOKEN = "xoxb-5327126797557-5333211755859-Njy523p9yEtsRhcWpfOn4cV9"
CHANNEL_ID = "C059TAEDP9Q"
BOT_USER_ID = "U12345678"  # Replace with your bot's user ID

client = WebClient(token=SLACK_TOKEN)

last_user_message = ""



def get_possible_questions(nodes):
    unique_sources = set()
    possible_questions = []

    while len(unique_sources) < random.randint(3, 4) and len(unique_sources) < len(nodes):
        node = random.choice(nodes)
        if isinstance(node['source'], list):
            for source in node['source']:
                if source not in unique_sources:
                    unique_sources.add(source)
                    possible_questions.append(source)
                    break
        else:
            if node['source'] not in unique_sources:
                unique_sources.add(node['source'])
                possible_questions.append(node['source'])

    return possible_questions


def retrieve_last_message():
    try:
        response = client.conversations_history(channel=CHANNEL_ID)
        messages = response["messages"]
        if messages:
            user_question = messages[0]
            if "text" in user_question and user_question.get("user") != BOT_USER_ID:
                return user_question["text"]
    except SlackApiError as e:
        print(f"Error fetching messages: {e.response['error']}")


def send_message(message):
    if message:  # Check if the message is non-empty
        try:
            response = client.chat_postMessage(channel=CHANNEL_ID, text=message)
            print("Message sent successfully!")
        except SlackApiError as e:
            print(f"Error sending message: {e.response['error']}")


def query_knowledge_graph(nodes, question):
    question = question.lower()

    who_are_you_keywords = ["who are you", "who designed you"]
    if any(keyword in question for keyword in ['all', 'every', 'every single', 'each', 'every news']):
        all_news = []
        for node in nodes:
            if 'label' in node and node['label'] != '':
                all_news.append(f"{node['source']} {node['label']} {node['target']}" if node[
                    'target'] else f"{node['source']} {node['label']}")
            else:
                all_news.append(f"{node['source']} {node['target']}" if node['target'] else node['source'])
        return "\n".join(all_news)
    if "date" in question or "time" in question:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"The current date and time is: {current_time}"
    if any(keyword in question for keyword in who_are_you_keywords):
        return "I'm NewsBot, designed by Anoop Shrestha"
    question = question.lower()
    for node in nodes:
        if 'label' in node and node['label'] != '':
            if any(keyword in question for keyword in ['news', 'information', 'updates']) or not any(keyword in question for keyword in ['news', 'information', 'updates']):
                if node['source'].lower() in question:
                    return construct_response(node['source'], node['label'], node['target'])
                elif node['target'] and node['target'].lower() in question:
                    return construct_response(node['source'], node['label'], node['target'])
                elif node['label'].lower() in question:
                    return construct_response(node['source'], node['label'], node['target'])
        else:
            if any(keyword in question for keyword in ['news', 'information', 'updates']) or not any(keyword in question for keyword in ['news', 'information', 'updates']):
                if node['source'].lower() in question:
                    return construct_response(node['source'], '', node['target'])
                elif node['target'] and node['target'].lower() in question:
                    return construct_response(node['source'], '', node['target'])
                elif node['source'].lower() == question or node['source'].lower() in question.split() or (node['target'] and node['target'].lower() in question.split()):
                    return construct_response(node['source'], '', node['target'])
    return None

def construct_response(source, label, target):
    if label == "":
        return source if target == "" else target
    if source == "":
        return f"{label} {target}" if target != "" else label
    if target == "":
        return f"{source} {label}"
    return f"{source} {label} {target}"


possible_questions = get_possible_questions(nodes)

# Print possible questions
print("You can ask me about:")
send_message("You can ask me about:")
for question in possible_questions:
    print(question)
    send_message(question)
send_message("")

# Continuously check for new messages in Slack
while True:
    user_message = retrieve_last_message()

    if user_message != last_user_message:
        last_user_message = user_message
        answer = query_knowledge_graph(nodes, user_message)

        if answer:
            send_message(answer)
            while True:
                user_message = retrieve_last_message()
                if user_message != last_user_message:
                    last_user_message = user_message
                    break
                time.sleep(1)
        else:
            send_message("Sorry, I couldn't find an answer to that question.")

    time.sleep(1)  # Wait for 1 second before checking for new messages
