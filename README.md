# King and Company

A digital adaptation of the dice and card game where players compete to build the most prosperous kingdom.

## 🎯 Game Objective

As a newly crowned king, your mission is to populate your kingdom by recruiting the most valuable inhabitants. You must achieve specific dice combinations to convince these characters to join your realm. The player with the most victory points at the end of the game wins.

## 🎲 Game Components

- 6 colored dice (2 red, 2 green, 2 blue)
- 65 cards:
  - 40 inhabitant cards
  - 15 location cards (5 locations × 3 values each)
  - 10 penalty cards

## 🛠 Game Setup

1. Location cards: Sorted by color into 5 piles for:

   - Ville (City)
   - Mine
   - Atelier (Workshop)
   - Village des orcs (Orc Village)
   - Forêt enchantée (Enchanted Forest)
     Each pile contains cards valued 2 (top), 3 (middle), and 4 (bottom).

2. Inhabitant cards: Shuffled face-down. The top 5 cards are placed face-up below the location piles.

3. Penalty cards: Shuffled and placed face-up to the right of the inhabitant cards.

4. Each player starts with an empty kingdom.

## 🔄 Turn Sequence

The game proceeds clockwise, starting with the oldest player. Each turn has three phases:

1. Rolling Dice:

   - Roll all 6 dice up to three times
   - After each roll, you can set aside any number of dice and reroll the others
   - Your goal is to achieve a combination matching one of the visible inhabitant cards

2. Recruiting or Taking a Penalty:

   - If you succeed in making a combination:
     - Take the matching inhabitant card and add it to your kingdom
     - If this card matches the color of a location, you may also take that location card
   - If you fail to make any combination:
     - Take the top penalty card and add it to your kingdom
     - Discard the rightmost inhabitant card

3. Replenishing Cards:
   - Shift remaining inhabitant cards to the right to fill empty spaces
   - Draw a new inhabitant card and place it on the far left

## 🏆 Scoring

- Inhabitant cards: +1 point each
- Location cards: +2 to +4 points (as shown on card)
- Penalty cards: -1 to -3 points (as shown on card)

The player with the highest total score wins!

## 🖥 Technical Requirements

- Python 3.8+
- Required packages (see requirements.txt)

## 🚀 Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Running the Game

```bash
python main.py
```

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 📜 License

[MIT](https://choosealicense.com/licenses/mit/)
