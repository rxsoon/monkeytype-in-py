# Monkeytype – Python Edition

A **Python clone of Monkeytype** built with Pygame. Practice your typing speed and accuracy with different modes and track your top scores.

## Features

- **Typing Test**: Random text generated from 1000+ English words.
- **Word Count Options**: 30, 60, or 120 words per test.
- **Color Modes**:
  - Standard: Green = correct, Red = incorrect.
  - Gradient: Smooth green gradient for correct letters.
  - Rainbow: Each correct letter cycles through rainbow colors.
  - Neon: Glowing green effect.
- **Scrolling Text**: Only 5 lines visible at a time; text scrolls as you type.
- **Leaderboard**: Top 10 scores for each word count stored in `leaderboard.json`.
- **Menu**: Start test, choose word count, select color mode, view leaderboard.
- **Real-time WPM and Accuracy**: See your progress as you type.

## Controls

- `SPACE` → Start typing test
- `1`, `2`, `3` → Select word count (30/60/120)
- `C` → Change color mode
- `L` → View leaderboard
- `R` → Return to menu (from results or leaderboard)
- `BACKSPACE` → Delete character

## Installation

1. Install Python 3.x
2. Install Pygame:  
   ```bash
   pip install pygame
