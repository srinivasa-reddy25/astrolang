from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from google.cloud import firestore
from langchain_google_firestore import FirestoreChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
import combine as combine
import uuid

unique_id = uuid.uuid4()

SESSION_ID = str(unique_id)


print("Start chatting with the AI. Type 'exit' to quit.")

ID=input("Enter your chat ID (if not you want to start fresh type 'new'): ")
if ID!="new":
    SESSION_ID=ID
    
 

load_dotenv()


PROJECT_ID = "first-langchain"

COLLECTION_NAME = "chat_history"

print("Initializing Firestore Client...")


client = firestore.Client(project=PROJECT_ID)



print("Initializing Firestore Chat Message History...")


chat_history1 = FirestoreChatMessageHistory(
    session_id=SESSION_ID,
    collection=COLLECTION_NAME,
    client=client,
)


print("Chat History Initialized.")

print("Current Chat History:", chat_history1.messages)





# llm = ChatOpenAI(
#     model="gpt-4o-mini",
#     temperature=0.7,
#     max_tokens=300,
#     top_p=0.9,
#     frequency_penalty=0.5,
#     presence_penalty=0.6,
#     stop=["END"]
# )


messages = [
    ("system","You are CosmoGuru, a fun, engaging, and insightful Telugu-English AI assistant, blending astrology with the festive spirit of Ugadi. "
    "You interact like a familiar companion, responding naturally and playfully, just like Alexa or Siri, but with a Telugu twist! "
    "50% of your focus is on Ugadi—its traditions, Panchanga Sravanam, festival predictions, significance, and cultural insights. "
    "You explain the meaning of Ugadi Pachadi, its symbolism, and how the festival sets the tone for the new year. "
    "The other 50% is on astrology, where you provide daily horoscopes, Vedic astrology insights, and fun, motivational predictions. "
    "Your tone is warm, humorous, and massy, like a cool 'Mama'. "
    "Use Telugu dialogues in English alphabets to make conversations feel relatable. "
    "Keep responses interactive, adding fun expressions and casual banter. "
    "Avoid absolute predictions, medical/financial/legal advice, and fear-based responses. "
    "Be a spiritual guide while keeping it lighthearted, festive, and engaging!"),
    ("human"," {query} "),
]

prompt_template = ChatPromptTemplate.from_messages(messages)
# prompt=prompt_template.invoke({
#     "query":query
# })


llm = ChatOpenAI(model="gpt-4o-mini" )

 
while True:
    
    # query=input("You: ")
    query=combine.get_voice_input()
    print("You:",query)

    if query.lower()=="exit":
        print("Here is your Session ID use this ID for future reference:", SESSION_ID)
        break

    chat_history1.add_user_message(query)
    # print("Chat History:", chat_history1.messages)
    formated_prompt=prompt_template.invoke({"query":query})
    # ai_response=llm.invoke(chat_history1.messages)
    ai_response2=llm.invoke(formated_prompt)
    
    chat_history1.add_ai_message(ai_response2.content)
    airesult=ai_response2.content
    processed_result = combine.process_ai_result(airesult)
    # print(f"AI: {ai_response.content}")
    print(f"AI: {ai_response2.content}")



