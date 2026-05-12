"""
================================================================================
        SAVITRIBAI PHULE PUNE UNIVERSITY
        Third Year Computer Engineering - Artificial Intelligence Lab
        Assignment No: 5
================================================================================

TITLE:
    Develop an Elementary Chatbot for a suitable Customer Interaction
    Application. Here we build a Restaurant Ordering Chatbot for MET Restaurant.

--------------------------------------------------------------------------------
PART 1 - THEORY
--------------------------------------------------------------------------------

1. WHAT IS A CHATBOT?
----------------------
A Chatbot is a computer program designed to simulate conversation with
human users, especially over the internet or through a terminal.

It interacts with users in natural language (text or voice) and responds
based on predefined rules, patterns, or AI models.

Types of Chatbots:
    - Rule-Based Chatbot  : Responds based on fixed rules and keywords.
                            Simple, fast, and easy to build.
                            Example: Menu-driven ordering system. (Used here)
    - AI-Based Chatbot    : Uses Machine Learning / NLP to understand
                            free-form text. Example: ChatGPT, Siri, Alexa.
    - Hybrid Chatbot      : Combination of Rule-Based and AI-Based.


2. WHAT IS AN ELEMENTARY CHATBOT?
-----------------------------------
An Elementary (Rule-Based) Chatbot:
    - Works on a set of PREDEFINED RULES.
    - Matches user input to known patterns or menu options.
    - Gives fixed responses based on the matched rule.
    - Does NOT learn from conversations.
    - Easy to implement using if-else or menu-driven logic.

Our chatbot follows a MENU-DRIVEN approach:
    - Greets the user by name.
    - Displays a food menu.
    - Takes order input from the user.
    - Validates the input.
    - Tracks quantity of each item ordered.
    - Calculates and displays the total bill.
    - Thanks the user at the end.


3. COMPONENTS OF OUR CHATBOT
------------------------------
    a) Greeting Module    : Welcomes user by name.
    b) Menu Display       : Shows available food items with options.
    c) Input Handler      : Reads and validates user's choice.
    d) Order Tracker      : Tracks how many of each item is ordered.
    e) Bill Calculator    : Computes total cost based on quantities.
    f) Order Summary      : Displays final order before billing.
    g) Exit Handler       : Ends conversation gracefully.


4. WORKING OF THE CHATBOT
---------------------------
Step 1 : Ask for the user's name -> Personalize the greeting.
Step 2 : Display the food menu with numbered options.
Step 3 : User selects an option (1 to 5).
Step 4 : Validate input -> if invalid, show error and repeat.
Step 5 : Confirm the selected item and update order count.
Step 6 : Ask if user wants to order more (yes/no).
Step 7 : If yes -> repeat from Step 2.
         If no  -> go to Step 8.
Step 8 : Display full order summary.
Step 9 : Calculate and display total bill.
Step 10: Thank the user and exit.


5. EXAMPLE INTERACTION
------------------------
    Bot  : Enter Your Name : Kamli
    Bot  : Hello Kamli Welcome to MET-Restaurant!
    Bot  : What would you like to order Kamli?
    Bot  : Option 1 : Rice-Plate    - Rs. 50
           Option 2 : Samosa        - Rs. 25
           Option 3 : Vada-Pava     - Rs. 25
           Option 4 : Chole-Bhature - Rs. 55
           Option 5 : Pohe          - Rs. 25
    User : 3
    Bot  : You Confirmed order: Vada-Pava
    Bot  : Do you want anything else? (yes/no): yes
    User : 5
    Bot  : You Confirmed order: Pohe
    Bot  : Do you want anything else? (yes/no): no
    Bot  : Your Order is:
             Vada-Pava x1
             Pohe      x1
    Bot  : Your total bill is Rs. 50
    Bot  : Thanks for your order!


6. MENU AND PRICING
---------------------
    Item No.    Item Name         Price (Rs.)
    --------    ---------------   -----------
    1           Rice-Plate        50
    2           Samosa            25
    3           Vada-Pava         25
    4           Chole-Bhature     55
    5           Pohe              25


7. APPLICATIONS OF CHATBOTS
------------------------------
    - Customer support (FAQs, complaints, tracking).
    - Restaurant and food ordering systems.
    - E-commerce product search and checkout.
    - Hospital appointment booking.
    - Bank balance inquiry and transactions.
    - Educational Q&A assistants.
    - Travel and ticket booking.


8. ADVANTAGES OF RULE-BASED CHATBOT
--------------------------------------
    - Simple to develop and maintain.
    - Fast response time (no AI processing).
    - Predictable and reliable behavior.
    - No training data required.
    - Suitable for structured interactions like ordering.

Disadvantages:
    - Cannot handle free-form or unexpected inputs.
    - Must be updated manually when rules change.
    - Limited to predefined responses only.


9. CONCLUSION
--------------
    - A Chatbot simulates human conversation to assist users automatically.
    - Our chatbot is Rule-Based and Menu-Driven for a restaurant use case.
    - It greets the user, takes food orders, validates input, tracks quantities,
      computes bill, and ends the session politely.
    - Rule-based chatbots are simple, fast, and reliable for structured tasks.
    - For complex interactions, AI/NLP-based chatbots are preferred.

================================================================================
PART 2 - PROGRAM
================================================================================
"""


# ============================================================
#  MENU ITEMS and PRICES
#  Parallel lists: menuOptions[i] has price prices[i]
# ============================================================
menu_options = ["Rice-Plate", "Samosa", "Vada-Pava", "Chole-Bhature", "Pohe"]
prices       = [50, 25, 25, 55, 25]


# ============================================================
#  display_menu() - Prints all food items with index and price
# ============================================================
def display_menu():
    for i in range(len(menu_options)):
        print(f"  Option {i+1} : {menu_options[i]:<20} - Rs. {prices[i]}")


# ============================================================
#  your_order() - Displays summary of items ordered
#  Parameter:
#    q_count - list of quantities for each menu item
# ============================================================
def your_order(q_count):
    print("\nYour Order is:")
    for i in range(len(menu_options)):
        if q_count[i] > 0:                              # Only show ordered items
            print(f"  {menu_options[i]:<20} x{q_count[i]}")


# ============================================================
#  total_bill() - Calculates total cost of the order
#  Parameter:
#    q_count - list of quantities for each menu item
#  Returns:
#    Total bill amount (int)
# ============================================================
def total_bill(q_count):
    total = 0
    for i in range(len(menu_options)):
        total += q_count[i] * prices[i]    # qty * price for each item
    return total


# ============================================================
#  chatbot_system() - Main chatbot function
#  Handles the full conversation: greeting -> ordering -> billing
# ============================================================
def chatbot_system():

    print("=" * 50)
    print("     Welcome to MET-Restaurant ChatBot")
    print("=" * 50)

    # Step 1: Ask for user's name to personalize the session
    name = input("\nEnter Your Name : ")
    print(f"\nHello {name}! Welcome to MET-Restaurant!")
    print(f"What would you like to order {name}?\n")

    # Track quantity of each item ordered (starts at 0 for all)
    q_count = [0] * len(menu_options)

    # Ordering loop - keeps running until user says no or max qty reached
    while True:

        # Display the full menu
        display_menu()

        # Read the user's choice
        opt = int(input("\nI would like to have option : "))

        # Input Validation: option must be between 1 and 5
        if opt < 1 or opt > len(menu_options):
            print("Invalid option! Please select a valid menu item.\n")
            continue    # Show menu again

        # Confirm the selected item (opt-1 for 0-based index)
        print(f"\nYou Confirmed order : {menu_options[opt-1]}")

        # Increment quantity count for the selected item
        q_count[opt-1] += 1

        # Safety check: stop if any item ordered 5 or more times
        if q_count[opt-1] >= 5:
            print("Maximum quantity reached for this item!")
            break

        # Ask if the user wants to order more
        order = input("Do you want anything else? (yes/no): ")
        print()

        # If YES continue loop, if NO exit loop
        if order.strip().lower() == "yes":
            continue
        else:
            break

    # Display the full order summary
    your_order(q_count)

    # Calculate and display the total bill
    print(f"\nYour total bill is Rs. {total_bill(q_count)}")
    print("\nThanks for your order!")
    print("=" * 50)


# ============================================================
#  MAIN - Entry point of the program
# ============================================================
if __name__ == "__main__":
    chatbot_system()    # Launch the restaurant chatbot