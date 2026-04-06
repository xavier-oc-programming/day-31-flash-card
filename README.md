# Day 31 — Flash Card App

A French-to-English flashcard app that auto-flips cards after 3 seconds and tracks which words you've already learned.

---

## Table of Contents

1. [Quick start](#1-quick-start)
2. [Builds comparison](#2-builds-comparison)
3. [Controls](#3-controls)
4. [App flow](#4-app-flow)
5. [Features](#5-features)
6. [Navigation flow](#6-navigation-flow)
7. [Architecture](#7-architecture)
8. [Module reference](#8-module-reference)
9. [Configuration reference](#9-configuration-reference)
10. [Display layout](#10-display-layout)
11. [Design decisions](#11-design-decisions)
12. [Course context](#12-course-context)
13. [Dependencies](#13-dependencies)

---

## 1. Quick start

```
python menu.py
```

Select **1** for the original build, **2** for the advanced build, or run either directly:

```
python original/main.py
python advanced/main.py
```

The original build requires pandas:

```
pip install pandas
```

The advanced build uses only the standard library — no install needed.

---

## 2. Builds comparison

| Feature | Original | Advanced |
|---|---|---|
| French flashcards from CSV | yes | yes |
| Auto-flip after 3 s | yes | yes |
| Manual flip on card click | yes | yes |
| Known / unknown buttons | yes | yes |
| Progress saved to CSV | yes | yes |
| Completion screen | yes | yes |
| Hardcoded paths via `os.path` | yes | — |
| `Path(__file__).parent` paths | — | yes |
| Global state | yes | — |
| OOP (`FlashCard`, `Display`) | — | yes |
| `config.py` — zero magic numbers | — | yes |
| Callbacks injected via `__init__` | — | yes |
| Logic / UI separation | — | yes |
| pandas dependency | yes | — |
| stdlib only (`csv` module) | — | yes |

---

## 3. Controls

### Main window

| Input | Action |
|---|---|
| Click card | Flip card (front ↔ back); cancels auto-flip timer if on front |
| Green check button | Mark current word as known, save progress, next card |
| Red cross button | Skip (keep word in deck), next card |

---

## 4. App flow

1. `menu.py` clears the console and prints the logo + menu.
2. User selects build 1 or 2; `subprocess.run` launches it.
3. On launch the app tries to load `data/words_to_learn.csv` (saved progress).  
   If not found, it falls back to `data/french_words.csv` (full deck).
4. A random French word appears on the card front.
5. After 3 seconds the card auto-flips to show the English translation.
6. The user can click the card at any time to flip it manually.
7. **Known** → word removed from deck, progress saved, new card shown.
8. **Unknown** → word stays in deck, new card shown immediately.
9. When all words are marked known the card displays "All done!" and buttons are disabled.
10. Closing the window exits the app; the menu reappears automatically.

---

## 5. Features

**Random card selection**  
Each new card is drawn at random from the remaining deck, so the same word won't always appear in the same order.

**Auto-flip timer**  
Three seconds after a French word appears, the card flips automatically to reveal the English translation. Any manual click before the timer fires cancels it first.

**Manual flip**  
Clicking anywhere on the card flips it between French (front) and English (back) at any time.

**Persistent progress**  
When the user marks a word as known it is removed from the in-memory list and the entire remaining list is written to `data/words_to_learn.csv`. On the next launch that file is loaded, so already-learned words are never shown again.

**Completion state** (advanced-only: rendered cleanly via `render_complete`)  
When all words have been marked known the card shows a congratulation message and both buttons are disabled.

**OOP architecture** (advanced only)  
`FlashCard` manages all word-list logic with no UI knowledge. `Display` owns all widgets with no business logic. `main.py` wires them together via callbacks.

**Zero magic numbers** (advanced only)  
Every size, colour, font, and delay lives in `config.py`. Nothing is hardcoded elsewhere.

---

## 6. Navigation flow

### Terminal menu tree

```
python menu.py
    │
    ├── 1 ──► python original/main.py  (blocks until window closed)
    │              └── returns to menu
    │
    ├── 2 ──► python advanced/main.py  (blocks until window closed)
    │              └── returns to menu
    │
    └── q ──► break  (menu exits)

Invalid input → "Invalid choice. Try again." → menu re-renders
```

### In-app flow

```
┌─────────────────────────┐
│  App launch             │
│  Load word list (CSV)   │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  FRONT of card shown    │◄──────────────────────────┐
│  French word displayed  │                           │
└───┬───────────┬─────────┘                           │
    │           │                                     │
    │ 3 s pass  │ user clicks card                    │
    ▼           ▼                                     │
┌──────────────────────────┐                          │
│  BACK of card shown      │                          │
│  English word displayed  │                          │
└───┬──────────────────────┘                          │
    │                                                 │
    ├── user clicks card ──► FRONT shown again        │
    │                                                 │
    ├── Known button ──► word removed, progress saved │
    │                    next card ───────────────────┘
    │
    └── Unknown button ──► next card ─────────────────┘
                                                      │
                (deck exhausted) ─────────────────────▼
                           ┌───────────────────────────┐
                           │  Completion state          │
                           │  "All done!" displayed     │
                           │  Buttons disabled          │
                           └───────────────────────────┘
```

---

## 7. Architecture

```
day-31-flash-card/
│
├── menu.py                  # Terminal menu: launch original or advanced build
├── art.py                   # LOGO constant, printed by menu.py
├── requirements.txt         # pandas required for original build only; advanced is stdlib-only
├── .gitignore
├── README.md
│
├── data/
│   └── french_words.csv     # Full deck — 200 French/English word pairs
│
├── images/
│   ├── card_front.png       # White card graphic
│   ├── card_back.png        # Green card graphic
│   ├── right.png            # Green check button image
│   └── wrong.png            # Red cross button image
│
├── docs/
│   └── COURSE_NOTES.md      # Original course exercise description
│
├── original/
│   ├── main.py              # Course solution verbatim (paths fixed for portability)
│   ├── data/
│   │   └── french_words.csv
│   └── images/
│       ├── card_back.png
│       ├── card_front.png
│       ├── right.png
│       └── wrong.png
│
└── advanced/
    ├── config.py            # All constants: colours, sizes, fonts, timing
    ├── flashcard.py         # FlashCard — pure word-list logic, no tkinter
    ├── display.py           # Display — owns every Tk widget, no app logic
    └── main.py              # Orchestrator: wires FlashCard ↔ Display via callbacks
```

---

## 8. Module reference

### `FlashCard` (`advanced/flashcard.py`)

| Method | Returns | Description |
|---|---|---|
| `__init__(data_dir)` | — | Loads word list from saved or original CSV |
| `next_word()` | `dict \| None` | Returns a random word dict; `None` if deck exhausted |
| `mark_known()` | `None` | Removes current word from deck and persists to CSV |
| `remaining` | `int` | Number of words left in the deck (property) |

### `Display` (`advanced/display.py`)

| Method | Returns | Description |
|---|---|---|
| `__init__(images_dir, on_known, on_unknown, on_card_click)` | — | Builds all widgets; stores callbacks |
| `render_front(french)` | `None` | Shows card front with French text |
| `render_back(english)` | `None` | Shows card back with English text |
| `render_complete()` | `None` | Shows completion message; disables buttons |
| `schedule_flip(callback)` | `None` | Cancels any pending timer; schedules new auto-flip |
| `cancel_flip()` | `None` | Cancels the pending auto-flip timer |
| `close()` | `None` | Calls `sys.exit(0)` |
| `root` | `Tk` | Exposes the root window for `mainloop()` |

---

## 9. Configuration reference

All constants are in [advanced/config.py](advanced/config.py).

| Constant | Default | Description |
|---|---|---|
| `BACKGROUND_COLOR` | `"#B1DDC6"` | Window and canvas background (mint green) |
| `CARD_W` | `800` | Canvas width in pixels |
| `CARD_H` | `526` | Canvas height in pixels |
| `LANG_FONT` | `("Arial", 40, "italic")` | Font for language label ("French" / "English") |
| `WORD_FONT` | `("Arial", 60, "bold")` | Font for the word displayed on the card |
| `FLIP_DELAY_MS` | `3000` | Milliseconds before the card auto-flips |

---

## 10. Display layout

```
┌──────────────────────────────────────────────────────────┐  window
│  [padx=50]                                  [padx=50]   │
│  ┌────────────────────────────────────────────────────┐  │
│  │              Canvas 800 × 526                      │  │
│  │                                                    │  │
│  │          card_title  (x=400, y=150)                │  │
│  │             "French" / "English"                   │  │
│  │                                                    │  │
│  │          card_word   (x=400, y=263)                │  │
│  │              <the word>                            │  │
│  │                                                    │  │
│  └────────────────────────────────────────────────────┘  │
│  [pady=50]                                               │
│  ┌───────────────────┐   ┌───────────────────┐          │
│  │  wrong.png        │   │  right.png        │          │
│  │  (col 0)          │   │  (col 1)          │          │
│  └───────────────────┘   └───────────────────┘          │
└──────────────────────────────────────────────────────────┘
```

---

## 11. Design decisions

**`display.py` owns all UI (testability, swappability)**  
All widget creation and state lives in `Display`. `FlashCard` has no knowledge of tkinter. This means the logic can be tested without a display, and the UI could be swapped for another toolkit without touching business logic.

**`config.py` — zero magic numbers**  
Every numeric or string constant is defined once in `config.py` with a descriptive name. Changing the flip delay, font size, or background colour requires editing exactly one line.

**Callbacks injected via `__init__`**  
`Display.__init__` accepts `on_known`, `on_unknown`, and `on_card_click` callables. It never imports `FlashCard` or `main`. This decouples the two layers: Display only fires events; `main.py` decides what to do with them.

**`current_word` and `is_front` as one-element lists**  
Both are mutable closure cells — callbacks defined in `main()` need to read and write them without `nonlocal`. A one-element list (`current_word: list[dict] = [{}]`) achieves this cleanly.

**`sys.path.insert` pattern**  
`advanced/main.py` inserts its own directory at the front of `sys.path` so `import config`, `import flashcard`, and `import display` work whether the file is launched directly or via `subprocess.run` from `menu.py`.

**`subprocess.run` + `cwd=`**  
`menu.py` uses `subprocess.run([sys.executable, str(path)], cwd=str(path.parent))` so each build's working directory is its own folder. This ensures relative imports and image/data paths resolve correctly regardless of where `menu.py` is run from.

**`while True` in `menu.py` vs recursion**  
The menu re-renders in a `while True` loop. Re-calling `main()` recursively would grow the call stack with every selection; a loop has constant stack depth.

**Console cleared before every menu render**  
`os.system("cls" if os.name == "nt" else "clear")` runs at the top of every loop iteration so the menu is always at the top of a clean terminal.

**`sys.exit(0)` vs `root.destroy()`**  
`Display.close()` calls `sys.exit(0)` rather than `root.destroy()`. Calling `destroy()` alone can trigger tkinter cleanup errors when the mainloop exits abruptly; `sys.exit(0)` exits the subprocess cleanly and returns control to `menu.py`.

**Auto-flip timer cancellation**  
`Display.schedule_flip` always calls `cancel_flip` before scheduling a new timer. This prevents double-fire: if `show_next` is called while a timer is still running (e.g. user clicks Known before the card flips), the stale callback is cancelled first.

---

## 12. Course context

Built as Day 31 of [100 Days of Code](https://www.udemy.com/course/100-days-of-code/) by Dr. Angela Yu.

**Concepts covered in the original build:**
- Tkinter `Canvas`, `PhotoImage`, `Button`, `grid` layout
- `canvas.create_image`, `create_text`, `itemconfig`
- `root.after(ms, callback)` and `root.after_cancel(id)`
- Pandas `read_csv`, `to_dict`, `DataFrame.to_csv`
- Try/except for file existence (progress fallback)
- Global state with `global` keyword
- `os.path.dirname(__file__)` for portable paths

**The advanced build extends into:**
- OOP: separating logic (`FlashCard`) from display (`Display`)
- Dependency injection via callbacks
- `pathlib.Path` for cross-platform path handling
- Mutable one-element lists as closure cells
- `sys.path.insert` for sibling-module imports
- `subprocess.run` orchestration from a terminal menu
- stdlib `csv` module instead of pandas for instant startup

See [docs/COURSE_NOTES.md](docs/COURSE_NOTES.md) for the full concept breakdown.

---

## 13. Dependencies

| Module | Used in | Purpose |
|---|---|---|
| Module | Used in | Purpose |
|---|---|---|
| `tkinter` | `original/main.py`, `advanced/display.py` | GUI widgets and event loop |
| `pandas` | `original/main.py` | Read/write CSV word lists (third-party) |
| `csv` | `advanced/flashcard.py` | Read/write CSV word lists (stdlib, no install) |
| `random` | `original/main.py`, `advanced/flashcard.py` | Random word selection |
| `pathlib` | `advanced/main.py`, `advanced/flashcard.py`, `advanced/display.py` | Cross-platform path handling |
| `sys` | `advanced/display.py`, `advanced/main.py`, `menu.py` | `sys.exit`, `sys.executable`, `sys.path` |
| `os` | `original/main.py`, `menu.py` | Path joining, console clear |
| `subprocess` | `menu.py` | Launch builds as child processes |
