# Course Notes — Day 31: Flash Card App

## Exercise Description

Build a French-to-English flashcard application using Tkinter.

The app should:
- Load a list of French words and their English translations from a CSV file.
- Display one random French word at a time on a card graphic.
- Automatically flip the card to reveal the English translation after 3 seconds.
- Allow the user to click the card to flip it manually at any time.
- Let the user mark a word as **known** (green check button) — it is then removed from the deck and progress is saved to a separate CSV file.
- Let the user mark a word as **unknown** (red cross button) — it stays in the deck and a new word appears.
- On the next launch, load the saved progress file so already-known words are skipped.
- When all words have been marked as known, display a congratulations message and disable the buttons.

## Key Concepts Practised

- **Tkinter basics**: `Tk()`, `Canvas`, `Button`, `PhotoImage`, `grid` layout.
- **Canvas items**: `create_image`, `create_text`, `itemconfig` for dynamic updates.
- **`root.after(ms, callback)`**: scheduling a delayed action without blocking the event loop.
- **`root.after_cancel(id)`**: cancelling a scheduled callback.
- **Pandas**: `read_csv`, `to_dict(orient="records")`, `DataFrame.to_csv`.
- **Try/except for file existence**: falling back to the original dataset when no save file exists.
- **Global state management**: using `global` to share mutable variables across functions.
- **Path handling**: using `os.path.dirname(__file__)` for robust file resolution.
