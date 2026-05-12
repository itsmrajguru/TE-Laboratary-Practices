"""
================================================================================
        SAVITRIBAI PHULE PUNE UNIVERSITY
        Third Year Computer Engineering - Artificial Intelligence Lab
        Assignment No: 6
================================================================================

TITLE:
    Implement an Expert System for Hospitals and Medical Facilities.
    Here we build a Medical Diagnosis Expert System that identifies
    possible diseases based on symptoms provided by the user.

--------------------------------------------------------------------------------
PART 1 - THEORY
--------------------------------------------------------------------------------

1. WHAT IS AN EXPERT SYSTEM?
------------------------------
An Expert System is an Artificial Intelligence program that simulates the
decision-making ability of a human expert in a specific domain.

It captures the knowledge of a human expert (doctor, engineer, lawyer)
in the form of IF-THEN rules and uses that knowledge to solve problems
or answer questions in that domain.

Key Idea:
    "Replace the human expert with a computer program that thinks
     and reasons the same way the expert would."

Real-world Examples:
    - MYCIN    : Diagnoses bacterial infections and recommends antibiotics.
    - DENDRAL  : Identifies chemical compounds from mass spectra.
    - CADUCEUS : Diagnoses internal medicine diseases.
    - Our System: Diagnoses common diseases from symptoms.


2. COMPONENTS OF AN EXPERT SYSTEM
------------------------------------
An Expert System has 3 main components:

    a) Knowledge Base:
       - Stores domain-specific knowledge as IF-THEN rules.
       - Contains facts about diseases and their symptoms.
       - Example: IF fever AND cough AND cold THEN disease = Flu

    b) Inference Engine:
       - The "brain" of the expert system.
       - Applies rules from the Knowledge Base to the user's input.
       - Uses reasoning to reach a conclusion (diagnosis).
       - Two types of reasoning:
             * Forward Chaining : Start from facts, derive conclusions.
                                  (Used in our system)
             * Backward Chaining: Start from conclusion, verify facts.

    c) User Interface:
       - The part that interacts with the user.
       - Asks questions, collects symptoms, displays diagnosis.


3. ARCHITECTURE OF EXPERT SYSTEM
-----------------------------------

    +----------------+       +-------------------+       +--------------+
    |   User         | <---> |  User Interface   | <---> |   Inference  |
    |  (Patient)     |       |  (Input/Output)   |       |   Engine     |
    +----------------+       +-------------------+       +------+-------+
                                                                |
                                                    +-----------+-----------+
                                                    |                       |
                                             +------+------+     +----------+------+
                                             | Knowledge   |     |   Working       |
                                             | Base        |     |   Memory        |
                                             | (IF-THEN    |     | (User symptoms) |
                                             |  Rules)     |     |                 |
                                             +-------------+     +-----------------+


4. HOW OUR MEDICAL EXPERT SYSTEM WORKS
----------------------------------------
Step 1 : Ask the user about symptoms one by one (yes/no questions).
Step 2 : Store the symptoms confirmed by the user.
Step 3 : Match the symptom set against the Knowledge Base rules.
Step 4 : If a rule fires (all symptoms of a disease match), diagnose it.
Step 5 : Display the diagnosis with precautions.
Step 6 : If no rule matches, advise the user to see a doctor.

This is FORWARD CHAINING:
    Facts (symptoms) --> Rules --> Conclusion (disease)


5. KNOWLEDGE BASE - RULES
---------------------------
Our system uses the following IF-THEN rules:

    Rule 1: IF fever AND cough AND cold AND headache
            THEN Disease = Flu (Influenza)

    Rule 2: IF fever AND rash AND joint_pain AND red_eyes
            THEN Disease = Dengue

    Rule 3: IF fever AND chills AND sweating AND vomiting
            THEN Disease = Malaria

    Rule 4: IF cough AND chest_pain AND shortness_of_breath AND fatigue
            THEN Disease = Pneumonia

    Rule 5: IF sore_throat AND fever AND swollen_glands AND fatigue
            THEN Disease = Typhoid

    Rule 6: IF nausea AND vomiting AND diarrhea AND stomach_pain
            THEN Disease = Food Poisoning

    Rule 7: IF sneezing AND runny_nose AND itchy_eyes AND no_fever
            THEN Disease = Allergy


6. EXAMPLE INTERACTION
------------------------
    System : Do you have fever? (yes/no): yes
    System : Do you have cough? (yes/no): yes
    System : Do you have cold? (yes/no): yes
    System : Do you have headache? (yes/no): yes
    ...
    System : Diagnosis  : Flu (Influenza)
    System : Precaution : Rest well, drink fluids, take paracetamol,
                          avoid cold exposure.


7. FORWARD CHAINING vs BACKWARD CHAINING
------------------------------------------

    Feature            Forward Chaining          Backward Chaining
    ---------------    ----------------------    ----------------------
    Start Point        Known Facts (symptoms)    Goal (disease)
    Direction          Facts -> Conclusion        Conclusion -> Facts
    Used When          All facts available        Specific goal to prove
    Example            Medical diagnosis          Fault diagnosis
    Our System         YES (used here)            No


8. ADVANTAGES OF EXPERT SYSTEMS
---------------------------------
    - Available 24/7 unlike human experts.
    - Consistent decisions (no fatigue or emotion).
    - Can store vast amounts of knowledge.
    - Useful in areas where human experts are scarce.
    - Can explain its reasoning (transparency).

Disadvantages:
    - Knowledge acquisition is difficult and time-consuming.
    - Cannot learn or update automatically.
    - Limited to the domain it is built for.
    - Cannot handle situations outside its knowledge base.


9. APPLICATIONS OF MEDICAL EXPERT SYSTEMS
-------------------------------------------
    - Disease diagnosis from symptoms.
    - Drug interaction checking.
    - Patient monitoring in ICUs.
    - Recommending treatment plans.
    - Medical image analysis support.


10. CONCLUSION
---------------
    - An Expert System mimics human expert reasoning using IF-THEN rules.
    - It has 3 components: Knowledge Base, Inference Engine, User Interface.
    - Our system uses Forward Chaining to diagnose diseases from symptoms.
    - It is simple, consistent, and available at all times.
    - Real medical expert systems like MYCIN have saved many lives.
    - Expert Systems are one of the earliest and most successful AI applications.

================================================================================
PART 2 - PROGRAM
================================================================================
"""


# ============================================================
#  KNOWLEDGE BASE
#  Dictionary of diseases with their symptoms and precautions.
#  Format:
#    'Disease Name': {
#        'symptoms'   : [list of symptoms that must be present],
#        'precaution' : "advice string"
#    }
# ============================================================
knowledge_base = {
    "Flu (Influenza)": {
        "symptoms"   : ["fever", "cough", "cold", "headache"],
        "precaution" : "Rest well, drink plenty of fluids, take paracetamol, avoid cold exposure."
    },
    "Dengue": {
        "symptoms"   : ["fever", "rash", "joint pain", "red eyes"],
        "precaution" : "Stay hydrated, take paracetamol (avoid aspirin), rest, consult a doctor immediately."
    },
    "Malaria": {
        "symptoms"   : ["fever", "chills", "sweating", "vomiting"],
        "precaution" : "Take prescribed antimalarial drugs, use mosquito nets, stay hydrated."
    },
    "Pneumonia": {
        "symptoms"   : ["cough", "chest pain", "shortness of breath", "fatigue"],
        "precaution" : "Take antibiotics as prescribed, rest, stay warm, drink warm fluids."
    },
    "Typhoid": {
        "symptoms"   : ["fever", "sore throat", "swollen glands", "fatigue"],
        "precaution" : "Take antibiotics, eat light food, drink boiled water, rest completely."
    },
    "Food Poisoning": {
        "symptoms"   : ["nausea", "vomiting", "diarrhea", "stomach pain"],
        "precaution" : "Stay hydrated with ORS, avoid solid food initially, rest, see doctor if severe."
    },
    "Allergy": {
        "symptoms"   : ["sneezing", "runny nose", "itchy eyes", "no fever"],
        "precaution" : "Take antihistamines, avoid allergens, wear a mask outdoors."
    }
}


# ============================================================
#  collect_symptoms() - Asks user about each possible symptom
#  Builds and returns a set of symptoms the user confirms.
# ============================================================
def collect_symptoms():

    # Collect all unique symptoms from the knowledge base
    all_symptoms = set()
    for disease_info in knowledge_base.values():
        for symptom in disease_info["symptoms"]:
            all_symptoms.add(symptom)

    print("\nPlease answer the following questions with yes or no:\n")
    print("-" * 50)

    # Set to store symptoms the user says YES to
    user_symptoms = set()

    for symptom in sorted(all_symptoms):    # Sort for consistent ordering

        # Ask yes/no for each symptom
        answer = input(f"  Do you have {symptom}? (yes/no): ").strip().lower()

        if answer == "yes":
            user_symptoms.add(symptom)      # Add confirmed symptom to set

    return user_symptoms


# ============================================================
#  diagnose() - Inference Engine (Forward Chaining)
#  Matches user symptoms against each rule in knowledge base.
#  Parameter:
#    user_symptoms - set of symptoms confirmed by the user
#  Returns:
#    List of (disease, precaution) tuples that match
# ============================================================
def diagnose(user_symptoms):

    results = []    # Store all matched diseases

    # Check each disease rule in the knowledge base
    for disease, info in knowledge_base.items():

        required_symptoms = set(info["symptoms"])   # Symptoms needed for this disease

        # FORWARD CHAINING: If ALL required symptoms are present -> rule fires
        if required_symptoms.issubset(user_symptoms):
            results.append((disease, info["precaution"]))   # Rule fired -> add diagnosis

    return results


# ============================================================
#  MAIN - Entry point of the program
# ============================================================
if __name__ == "__main__":

    print("=" * 50)
    print("   MEDICAL DIAGNOSIS EXPERT SYSTEM")
    print("   Hospitals and Medical Facilities")
    print("=" * 50)
    print("  This system diagnoses common diseases")
    print("  based on your symptoms using IF-THEN rules.")

    # Step 1: Collect symptoms from the user
    user_symptoms = collect_symptoms()

    print("\n" + "=" * 50)
    print("  Symptoms you reported:")
    if user_symptoms:
        for s in sorted(user_symptoms):
            print(f"    - {s}")
    else:
        print("    None reported.")

    print("\n" + "=" * 50)
    print("  DIAGNOSIS RESULT")
    print("=" * 50)

    # Step 2: Run the inference engine to get diagnosis
    results = diagnose(user_symptoms)

    # Step 3: Display results
    if results:
        for i, (disease, precaution) in enumerate(results, 1):
            print(f"\n  Diagnosis  {i} : {disease}")
            print(f"  Precaution   : {precaution}")
    else:
        # No rule matched -> advise to see a doctor
        print("\n  No specific disease matched your symptoms.")
        print("  Please consult a doctor for proper diagnosis.")

    print("\n" + "=" * 50)
    print("  NOTE: This is an AI-based advisory system only.")
    print("  Always consult a qualified doctor for treatment.")
    print("=" * 50)