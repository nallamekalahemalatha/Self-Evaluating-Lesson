"""
Comprehensive Educational Curriculum & Assessment Model
Defines the complete multi-chapter RAG lesson, interactive quiz questions,
Mermaid diagrams, Python code walkthroughs, and comparison tables.
"""

from typing import List, Dict, Any


# Rich multi-chapter textbook-quality educational lesson
COMPREHENSIVE_RAG_LESSON = """# Introduction to RAG (Retrieval-Augmented Generation)
### *A Practical Step-by-Step Guide for Future AI Builders*

---

## 1. Lesson Overview & Prerequisites

- **Audience**: 12th-grade graduates from India.
- **English Level**: Non-English medium friendly. Simple everyday words.
- **Prerequisites**: No coding required. Basic smartphone familiarity.
- **Learning Time**: 25 minutes.
- **Career Value**: High. Used by Google, Microsoft, Indian banks, and startups.

---

## 2. The Core Problem: Why Does AI Make Things Up?

Imagine a student sitting for a **closed-book board exam**.
- They can only answer questions using facts stored in memory.
- What if the exam asks about a new scholarship announced yesterday morning?
- The student cannot know it from memory.
- If they refuse to leave it blank, they might make up a confident guess!

In Artificial Intelligence, this guessing problem is called **Hallucination**.
*In simple words: Hallucination happens when an AI model speaks with high confidence, but makes up false facts.*

Standard AI models (like ChatGPT) are like that student in a closed-book exam.
- They were trained on books up to a cutoff date.
- They do not know today's train updates or your college notices.
- If you ask about fresh facts, they cannot check a book. They might guess!

---

## 3. The Breakthrough: What is RAG?

Instead of a closed-book exam, what if the school allows an **Open-Book Exam**?
In an open-book exam:
1. You read the question.
2. You open a verified textbook on your desk.
3. You find the exact page with the right information.
4. You read that page and write down a 100% correct answer.

This is the exact secret of **RAG (Retrieval-Augmented Generation)**!

### Everyday Indian Examples:
1. **The Kirana Store**:
   When you ask a local shopkeeper for spices, they do not guess from memory. They check their store shelf, pick up the packet, and hand it to you.
2. **IRCTC Railway Inquiry**:
   When you check train seat availability on your phone, the app does not guess. It fetches live data from the railway database and prints your berth.

### Breaking Down R-A-G:
- **R = Retrieval (Searching)**:
  *In simple words: Fetching the right page from a digital library.*
- **A = Augmented (Added or Attached)**:
  *In simple words: Pasting that fresh page next to your question.*
- **G = Generation (Writing the Final Answer)**:
  *In simple words: The AI reads the page and writes a clear answer.*

> **Golden Architectural Rule**:  
> RAG does **NOT** retrain the AI or change its internal brain weights (*in simple words: the AI permanent memory wires*). Instead, it gives the AI a fresh reference note to look at while answering!

---

## 4. How RAG Works: Step-by-Step Architecture

Suppose you ask a college helpline:
> *"What is the last date to submit the 2026 hostel fee at Delhi University?"*

```mermaid
flowchart TD
    User["Student Question:<br/>Hostel Fee Deadline"] --> SearchEngine["Step 1: RETRIEVAL<br/>Searches Official Circular PDFs"]
    PDFStore[("University Circulars Database")] --> SearchEngine
    SearchEngine --> ExtractedDoc["Found Document:<br/>Hostel fee due 15th July 2026"]
    ExtractedDoc --> AugmentPrompt["Step 2: AUGMENTATION<br/>Pastes Fact into Prompt Note"]
    User --> AugmentPrompt
    AugmentPrompt --> LLMGen["Step 3: GENERATION<br/>AI Reads Note and Answers"]
    LLMGen --> FinalAnswer["Truthful Answer:<br/>Deadline is 15th July 2026!"]
```

### The 3 Steps in Action:
1. **Step 1: Retrieval (The Search)**: The system searches university circulars. It finds the PDF stating: *Hostel fee deadline is 15th July 2026.*
2. **Step 2: Augmentation (Attaching the Fact)**: The system pastes this fact next to your question.
3. **Step 3: Generation (Writing the Answer)**: The AI reads the fact and gives a polite, truthful reply.

---

## 5. Architectural Comparison: Standard AI vs RAG

| Comparison Dimension | Standard AI (Closed-Book) | RAG System (Open-Book) |
|---|---|---|
| **Exam Style** | Closed-Book Exam. Memory only. | Open-Book Exam. Consults notes. |
| **Knowledge** | Old training data. | Fresh live documents. |
| **Risk of Lies** | High risk of guessing. | Near zero risk. |
| **Cost to Update** | Millions of rupees. | Free. Add a new PDF. |
| **Data Privacy** | High risk of leaks. | Safe on private company server. |

---

## 6. Key Technical Terms Made Super Simple

1. **LLM (Large Language Model)**: *In simple words: Think of this as a smart student who read many books.*
2. **Prompt**: *In simple words: The question or instruction you type into the chat box.*
3. **Vector / Embedding**: *In simple words: Think of this as a digital GPS pin. AI uses numbers to find similar sentences, just like Google Maps finds your street.*
4. **Context Window**: *In simple words: Think of this as the digital desk space where the AI reads documents.*

---

## 7. Practical Code Walkthrough: Building a Simple RAG Engine

```python
# Step 1: Verified Knowledge Base (Our Digital Bookshelf)
KNOWLEDGE_BASE = {
    'hostel_fee': 'The last date to submit Delhi University hostel fees is 15th July 2026.',
    'library_rules': 'Students can borrow up to 4 books for 14 days with their student ID.'
}

def retrieve_fact(user_question: str) -> str:
    '''Step 1: RETRIEVAL - Search our knowledge base for relevant facts.'''
    for topic, fact in KNOWLEDGE_BASE.items():
        if any(word in user_question.lower() for word in topic.split('_')):
            return fact
    return 'No matching official document found.'

def augment_prompt(user_question: str, retrieved_fact: str) -> str:
    '''Step 2: AUGMENTATION - Attach verified fact to the question.'''
    return f'Fact: {retrieved_fact}\\nQuestion: {user_question}\\nAnswer:'

def generate_answer(user_question: str) -> str:
    '''Step 3: GENERATION - Write truthful answer.'''
    fact = retrieve_fact(user_question)
    return f'Official Answer: {fact}'

# Test the engine
response = generate_answer('When is hostel fee due?')
print(response)
```

---

## 8. Summary & Key Revision Notes

### 5 Golden Points to Remember:
1. **The Core Problem**: Standard AI hallucinates because it is like a closed-book exam.
2. **The RAG Solution**: RAG gives the AI an open book with fresh facts.
3. **The 3 Steps**: **R**etrieve facts -> **A**ugment prompt -> **G**enerate answer.
4. **Zero Weight Changes**: RAG never retrains the AI model.
5. **Career Value**: Companies pay top salaries to AI engineers who build reliable RAG systems.

---

## 9. Check Your Understanding! 🎯

### Question 1:
**In our exam analogy, what is the difference between standard AI and RAG?**
- **A)** Standard AI is open-book, RAG is closed-book.
- **B)** Standard AI is closed-book (memory only), RAG is open-book (looks at fresh notes).
- **C)** Standard AI writes in Hindi, RAG writes in English.

*Answer*: **B**! Standard AI relies only on past memorization. RAG gives the AI an open textbook to check facts.

### Question 2:
**Does RAG permanently change or retrain the AI model's internal brain weights?**
- **A)** Yes, every single time you ask a question.
- **B)** No, it just gives the model fresh facts inside the question prompt.

*Answer*: **B**! RAG never alters model weights. It acts like handing a reference paper to the student.

### Question 3:
**What does the 'A' in RAG stand for?**
- **A)** Artificial
- **B)** Augmented (meaning added or attached)
- **C)** Automatic

*Answer*: **B**! Augmented means adding external verified facts into the prompt.
"""


# Comprehensive Assessment Dataset for Part 5
INTERACTIVE_ASSESSMENT_DATA = [
    # 5 Multiple Choice Questions
    {
        "id": "q1",
        "type": "mcq",
        "category": "Core Concept",
        "question": "In our exam analogy, why is standard AI compared to a student in a 'closed-book exam'?",
        "options": [
            "Because standard AI uses textbooks to answer questions.",
            "Because standard AI can only answer from past memorized data and cannot check fresh documents.",
            "Because standard AI cannot write English properly.",
            "Because standard AI only works in school classrooms."
        ],
        "correct_index": 1,
        "explanation": "Standard AI was trained on static past data up to a cutoff date. When asked about new facts, it cannot open a book to check; it must answer from past memorization, which often leads to guessing (hallucination).",
        "misconception": "Some learners believe AI searches the live web automatically. In reality, core LLMs only know what was in their training set unless augmented with RAG."
    },
    {
        "id": "q2",
        "type": "mcq",
        "category": "Terminology",
        "question": "What does the letter 'A' stand for in the acronym RAG?",
        "options": [
            "Artificial",
            "Automatic",
            "Augmented (meaning added or attached to the prompt)",
            "Advanced"
        ],
        "correct_index": 2,
        "explanation": "Augmented means to add or attach. In RAG, external verified facts are added to the prompt right next to your question.",
        "misconception": "Learners often guess 'Artificial' because of Artificial Intelligence."
    },
    {
        "id": "q3",
        "type": "mcq",
        "category": "Architecture Mechanics",
        "question": "Does a RAG system permanently retrain or update the internal neural network weights of an AI model?",
        "options": [
            "Yes, every single time a question is asked.",
            "No, RAG never changes model weights; it only gives the AI a reference note to read.",
            "Yes, but only for programming questions.",
            "Yes, using backpropagation on every user query."
        ],
        "correct_index": 1,
        "explanation": "RAG is an in-context inference technique. The AI model's internal weights remain untouched. It simply reads the retrieved document inside its context window.",
        "misconception": "Many beginners confuse RAG with fine-tuning. Fine-tuning alters neural weights; RAG supplies fresh reference notes in the prompt."
    },
    {
        "id": "q4",
        "type": "mcq",
        "category": "Intuitive Analogies",
        "question": "What is the best everyday analogy for a 'Vector Embedding'?",
        "options": [
            "A fast train engine.",
            "A digital GPS coordinate or library shelf number that locates meaning in space.",
            "A battery charger for your computer.",
            "A computer screen display."
        ],
        "correct_index": 1,
        "explanation": "Just as Google Maps uses numbers (latitude and longitude) to find a house, AI uses numbers called vector embeddings to find sentences with similar meaning.",
        "misconception": "Beginners often think vectors are complex math matrices, when conceptually they are simply location pins for concepts."
    },
    {
        "id": "q5",
        "type": "mcq",
        "category": "Industry Application",
        "question": "Why do companies in Bengaluru, Hyderabad, and around the world hire GenAI engineers who know RAG?",
        "options": [
            "Because RAG is only used for playing online games.",
            "Because companies need accurate, truthful AI that cites verified business documents without costly retraining.",
            "Because RAG makes the computer screen brighter.",
            "Because RAG deletes all company databases."
        ],
        "correct_index": 1,
        "explanation": "Businesses cannot afford AI that hallucinates bank balances or college dates. RAG connects AI to verified internal documents with zero retraining cost.",
        "misconception": "Some think fine-tuning is always superior. In enterprise settings, RAG is faster, cheaper, and guarantees factual source citations."
    },

    # 3 True / False Questions
    {
        "id": "tf1",
        "type": "tf",
        "category": "True or False",
        "question": "True or False: An AI 'hallucination' means the computer screen is flickering.",
        "options": ["True", "False"],
        "correct_index": 1,
        "explanation": "False! In AI, 'hallucination' means the model speaks with high confidence but makes up false or invented facts.",
        "misconception": "Hallucination is an algorithmic terminology, not a computer hardware malfunction."
    },
    {
        "id": "tf2",
        "type": "tf",
        "category": "True or False",
        "question": "True or False: In a RAG pipeline, the Retrieval step happens BEFORE the Generation step.",
        "options": ["True", "False"],
        "correct_index": 0,
        "explanation": "True! The system must first search and retrieve relevant facts before the AI can read them and generate an answer.",
        "misconception": "The acronym R-A-G represents the exact sequential execution order: Retrieve -> Augment -> Generate."
    },
    {
        "id": "tf3",
        "type": "tf",
        "category": "True or False",
        "question": "True or False: If a university changes its fee circular tomorrow, you can simply add the new PDF to the RAG database without spending millions on retraining the AI.",
        "options": ["True", "False"],
        "correct_index": 0,
        "explanation": "True! That is one of the greatest superpowers of RAG. New documents are instantly searchable without retraining.",
        "misconception": "Updating knowledge in RAG takes seconds, unlike retraining which takes weeks."
    },

    # 2 Short Answer Questions
    {
        "id": "sa1",
        "type": "sa",
        "category": "Short Answer",
        "question": "Explain the 3 steps of RAG (Retrieve, Augment, Generate) in one simple sentence.",
        "sample_answer": "Retrieve searches for verified facts, Augment pastes those facts into the prompt note, and Generate writes the final clear answer.",
        "keywords": ["retrieve", "search", "augment", "attach", "paste", "generate", "write", "answer"],
        "explanation": "A complete answer mentions searching for facts, attaching them to the question, and having the AI generate the response."
    },
    {
        "id": "sa2",
        "type": "sa",
        "category": "Short Answer",
        "question": "Why is RAG much cheaper for a hospital or bank than retraining an entire AI model?",
        "sample_answer": "RAG does not require expensive supercomputer training; it simply searches local document folders and feeds the facts to an existing AI.",
        "keywords": ["cheaper", "retrain", "supercomputer", "training", "search", "documents", "weights", "cost"],
        "explanation": "Retraining requires massive GPU clusters and millions of dollars, while RAG simply searches existing documents during inference."
    },

    # 1 Practical Application Scenario
    {
        "id": "app1",
        "type": "application",
        "category": "Practical Scenario",
        "question": "Scenario: You are an AI Engineer at an Indian Railways ticket booking app. A passenger asks: 'What is the refund policy for a Tatkal ticket cancelled 2 hours before departure?' How does your RAG system handle this query?",
        "sample_answer": "The system retrieves the latest official IRCTC refund policy PDF, pastes the exact cancellation rules into the AI prompt note, and generates a verified response citing the official circular.",
        "rubric_points": [
            "Mentions searching/retrieving the official railway circular or IRCTC policy.",
            "Mentions attaching/augmenting the fact into the AI prompt.",
            "Mentions generating an accurate, grounded answer without hallucinating refund amounts."
        ],
        "explanation": "This real-world scenario demonstrates the three stages: Search the IRCTC rulebook (Retrieve), attach the rule to the passenger's question (Augment), and output the truthful refund calculation (Generate)."
    }
]
