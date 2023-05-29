import random
from nodes import nodes
import datetime

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
                    return f"{node['source']} {node['label']} {node['target']}" if node['target'] else f"{node['source']} {node['label']}"
                elif node['target'] and node['target'].lower() in question:
                    return f"{node['source']} {node['label']} {node['target']}" if node['target'] else f"{node['source']} {node['label']}"
                elif node['label'].lower() in question:
                    return f"{node['source']} {node['label']} {node['target']}" if node['target'] else f"{node['source']} {node['label']}"
        else:
            if any(keyword in question for keyword in ['news', 'information', 'updates']) or not any(keyword in question for keyword in ['news', 'information', 'updates']):
                if node['source'].lower() in question:
                    return f"{node['source']} {node['target']}" if node['target'] else node['source']
                elif node['target'] and node['target'].lower() in question:
                    return f"{node['source']} {node['target']}" if node['target'] else node['source']
                elif node['source'].lower() == question or node['source'].lower() in question.split() or (node['target'] and node['target'].lower() in question.split()):
                    return f"{node['source']} {node['target']}" if node['target'] else node['source']
    return None


# Get possible questions
possible_questions = get_possible_questions(nodes)

# Print possible questions
print("You can ask me about:")
for question in possible_questions:
    print(question)

# Ask questions and get answers
while True:
    user_question = input("\nEnter your question (or 'exit' to quit): ")
    if user_question.lower() == 'exit':
        break
    answer = query_knowledge_graph(nodes, user_question)
    print(answer if answer else "Sorry, I couldn't find an answer to that question.")
