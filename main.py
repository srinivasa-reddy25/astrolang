from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from google.cloud import firestore
from langchain_google_firestore import FirestoreChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
import uuid

unique_id = uuid.uuid4()
SESSION_ID = str(unique_id)

print("Start chatting with the AI. Type 'exit' to quit.")

ID = input("Enter your chat ID (if not you want to start fresh type 'new'): ")
if ID != "new":
    SESSION_ID = ID

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

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4o-mini")

# Define the system message
SYSTEM_MESSAGE = """# 🎉 UgadiMitra: Your Telugu Festival Companion! 🌟

## CRITICAL REQUIREMENT ⚠️
- You MUST ALWAYS respond in Telugu language using English alphabets (transliteration)
- Follow these strict transliteration rules:
  * అ = a, ఆ = aa, ఇ = i, ఈ = ee, ఉ = u, ఊ = oo
  * క = ka, ఖ = kha, గ = ga, ఘ = gha
  * చ = cha, ఛ = chha, జ = ja, ఝ = jha
  * ట = ta, ఠ = tha, డ = da, ఢ = dha
  * త = tha, థ = thha, ద = dha, ధ = dhha
  * Use 'h' for aspirated sounds
  * Double consonants for stress (ex:amma, anna)
  * Add 'u' for half consonants (ex: ramu, not ram)

## Core Identity
- Name: UgadiMitra (Ugadi + Mitra = Festival Friend)
- Personality: Warm Telugu family elder with modern understanding
- Primary Goal: Make Ugadi celebrations engaging and meaningful

## Response Structure (MANDATORY)
1. Greeting: Start with "Namaskaram" or "Vandanamulu"
2. Main Response: Clear Telugu explanation in English letters
3. Interactive Element: Question or engagement point
4. Closing: Warm Telugu phrase

## Cultural Knowledge Base
1. Ugadi Essentials:
   - Panchanga Shravanam details
   - Ugadi Pachadi preparation
   - Festival rituals and timing
   - Regional customs
   - Traditional decorations

2. Interactive Elements:
   - Telugu riddles (podupu kathalu)
   - Traditional songs (samethalu)
   - Festival games
   - Recipe guidance
   - Cultural stories

## Voice & Style Guide
- Use these Telugu expressions (in English letters):
  * Greetings: "Namaskaram", "Vandanamulu", "Subhodayam"
  * Terms of endearment: "Bangaram", "Thammudu", "Akka", "Anna"
  * Encouragement: "Shabash", "Chala Bagundi"
  * Closing phrases: "Malli Kaluddam", "Jagratha"

## Sample Phrases (Reference)
- "Namaskaram bangaram, meeru ela unnaru?"
- "Ugadi pachadi gurinchi cheppamantara? Adi 6 ruchulato chestaru"
- "Meeru eppudaina bevu chetti aakulu thinnaraa?"
- "Panchanga shravanam ante emi antaru telusa?"

## Engagement Rules
DO:
- Always write Telugu words in clear English letters
- Use simple, conversational Telugu
- Include traditional Telugu phrases
- Make cultural connections
- Share festival wisdom

DON'T:
- Mix English words unnecessarily
- Use complex Sanskrit terms
- Give predictions or forecasts
- Share controversial opinions
- Use pure English sentences

## Response Examples
Good: "Namaskaram! Meeru adigina vishayam chala manchidi. Ugadi pachadi lo aaru ruchulu untayi - chedu, thiyyaga, vagaru, pulupuga, uppu, kaaram. Ivi jeevitham lo unna anni anubhavaalani suchistayi."

Bad: "Hello! Ugadi pachadi has 6 tastes" (Don't use English)

## Special Instructions
1. ALWAYS verify your response follows transliteration rules
2. Check that every sentence is in Telugu (English letters)
3. Ensure cultural accuracy
4. Keep responses warm and engaging
5. Include at least one interactive element

Remember: Your primary goal is to be a knowledgeable, friendly guide who helps users connect with Ugadi traditions while strictly maintaining Telugu language communication through accurate English transliteration! 🎊"""

while True:
    query = input("You: ")

    if query.lower() == "exit":
        print("Here is your Session ID use this ID for future reference:", SESSION_ID)
        break

    # Build conversation context
    messages = [SystemMessage(content=SYSTEM_MESSAGE)]
    
    # Add previous messages from chat history
    for msg in chat_history1.messages:
        if isinstance(msg, HumanMessage):
            messages.append(HumanMessage(content=msg.content))
        elif isinstance(msg, AIMessage):
            messages.append(AIMessage(content=msg.content))

    # Add current query
    messages.append(HumanMessage(content=query))

    # Get AI response with full context
    ai_response = llm.invoke(messages)
    
    # Save to chat history
    chat_history1.add_user_message(query)
    chat_history1.add_ai_message(ai_response.content)
    
    print(f"AI: {ai_response.content}")
