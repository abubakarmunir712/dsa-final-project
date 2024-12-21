# DSA Final Project - Indian Rummy

# Introduction

Indian Rummy is a strategic multiplayer card game that involves each player being dealt 13 cards. The objective of the game is to form valid sequences and sets to win. This project implements a custom version of the game using various data structures and algorithms, such as Doubly Linked Lists, Queues, Stacks, Hashmaps, and Graphs. The game also features an AI player that intelligently evaluates hands and makes decisions based on the game state.

# Key Features

Indian Rummy implemented has following features:

## Multi-Player Support Using Server:

A server has been setup to support multiplayer game featuring both human and AI players. Players can join the game, and multiple AI players can be added to simulate a complete game.

## Card Handling:

Players can draw cards from the stockpile or the wastepile. Cards can also be discarded into the wastepile.

## Card Grouping & Sequences:

Players can group cards into sequences (runs of the same suit) or sets (cards with the same rank). Sequences and sets contribute to the player's score.

## AI Player Logic:

AI players has been added to the game for gameplaye. AI players evaluate their hands and make strategic decisions, including choosing whether to draw from the stockpile or wastepile, and which card to discard.

## Game State Management:

The game keeps track of the current player, game ID, and other essential game states. It automatically progresses through turns and manages the game flow. It automatically checks win condition after each set to ensure player's win.

## Input and Error handling:

Validations and try-except has been added to ensure the valid input and error handling in the game.

# Data Structures and Algorithms Used

The data structures and algorithms used in this project are:

## Doubly LinkedList:

We built a Doubly Linked List for implementing both the stack and queue of the game, allowing for constant time complexity (O(1)) for operations such as inserting and removing cards from the head or tail. This structure supports efficient manipulation of the cards.

- Time Complexity: O(1) for insertion and deletion at both ends.
- Space Complexity: O(n) where n is the number of elements in the list.

## Queue:

The Queue is implemented using the Doubly Linked List. The queue stores the stockpile of the game, from which players can draw cards.

## Stack:

The Stack is implemented using the Doubly Linked List and is used for the wastepile of the game, where discarded cards are placed.

- As the queue and stack is built over doubly linkedlist, both have same space and time complexity.

## Hashmap:

A custom HashMap is used to ensure that there are no duplicate cards within a sequence (same suit, different rank) in constant time (O(1)). The HashMap resizes dynamically to accommodate more elements as needed.

### Time Complexity:

- Insert: O(1) average case, O(n) worst case (during resizing).
- Get: O(1) for accessing values.
- Remove: O(n) for rehashing after removal.

### Space Complexity:

O(n) where n is the number of key-value pairs stored.

## Graphs:

The Graph structure is used to optimize the AI player's decision-making. Each card is represented as a node, and edges are created between cards that form valid sequences (runs) or sets (cards of the same rank but different suits). While 13 cards can generate over 6.2 billion possible combinations, making a brute-force approach inefficient in terms of memory and time complexity, the graph allows the AI to quickly evaluate valid hands. By analyzing the graph, the AI can identify valid sequences and sets without needing to check all possible combinations, improving both the efficiency and speed of its decision-making process.

- Time Complexity: O(n^2) for building the graph, where n is the number of cards in hand.
- Space Complexity: O(n) for storing the graph’s nodes and edges.

## DFS and BFS:

Using DFS and BFS for the AI player improves efficiency by reducing both time and space complexity. Instead of checking all possible card combinations, the AI traverses a graph of relevant sequences and sets, making the process linear in time (O(V + E)) rather than exponential. The graph structure also reduces memory usage by only storing necessary card connections, making the AI faster and more memory-efficient, especially as the number of cards increases.

## Bubble Sort:

A custom-built Bubble Sort is used to sort the cards, making it easier to traverse and identify sequences efficiently. This sorting ensures that cards are in order, simplifying the process of checking for valid sequences.

# Technologies Used

The technologies used in the implementation are:

- Game logic and classes: Python
- Server: Flask(Python)
- UI: Cli based (Python)

# Code Structure

## card.py

Contains the Card class, defining properties and behaviors of a playing card, including rank, suit, visibility, and points calculation.

## deck.py

Defines the Deck class, which creates, shuffles, and allows cards to be drawn or manipulated, including handling jokers.

## stockpile.py

Manages the stockpile, which stores and provides cards to players when drawn.

## wastepile.py

Handles the wastepile, where discarded cards are placed and can be accessed for future moves.

## player.py

The Player class manages a player's hand, points, and actions like drawing, discarding, or moving cards between sequences.

## sequence.py

Represents a collection of cards forming a sequence, handling validation, sorting, and calculations, including managing jokers and Ace adjustments.

## game_logic.py

Manages the main game logic, including player actions, deck handling, stockpile, wastepile, and determining the winner. Supports both AI and human players.

## utilities.py

Contains utility functions like bubble sort, and functions to find min and max values, aiding sequence and set traversal.

## backend/main.py

The entry point for the server, connecting the backend to the game logic via Flask.

## frontend/main.py

Contains the frontend code for the user interface, acting as the entry point for the game.

## Enums Folder

Contains enumeration files used throughout the game to define various statuses and game states

# Folder Structuring

Here is the folder structuring for the project:

      Backend
      ├── bot
      │   └── bot.py
      ├── classes
      │   ├── card.py
      │   ├── deck.py
      │   ├── player.py
      │   ├── sequence.py
      │   ├── stockpile.py
      │   └── wastepile.py
      ├── data_structures
      │   ├── hashmap.py
      │   ├── linkedlist.py
      │   ├── queue.py
      │   └── stack.py
      ├── enums
      │   ├── rank_enum.py
      │   ├── status_enum.py
      │   └── suit_enum.py
      ├── game_logic
      │   └── game.py
      ├── utility
      │   └── utilities.py
      └── main.py

      Frontend
      └── console
          └── main.py

# How to Run the Project

1. Clone the repository.

   ` bash` git clone https://github.com/abubakarmunir712/dsa-final-project

2. Install the necessary dependencies:
   - python 3.x or higher
   - flask
3. Start the backend server:
4. Open the frontend and play.

# Challenges and Solutions

Here are some challenges we faced while working on this project:

## Challenge: Managing sequences with jokers and Ace rank adjustments.

- Solution: Implemented logic in sequence.py to handle different sequence types and dynamically adjust Ace values.

## Challenge: Supporting both human and AI players.

- Solution: Designed the AIPlayer class and called its play method in game_logic.py to simulate player actions while handling all the rules

# Contributions:

Here are the contributors for this project:

- [aabr2612](https://github.com/aabr2612)
- [abubakarmunir712](https://github.com/abubakarmunir712)
- [ABUTAYYAB](https://github.com/ABUTAYYAB)

# Conclusion:

This project development helped us a lot in understanding the DSA concepts in details and it's implementation in real world applications.
