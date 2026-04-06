import sys
from pathlib import Path
from tkinter import Canvas, PhotoImage, Button, Tk
from typing import Callable

from config import (
    BACKGROUND_COLOR, CARD_W, CARD_H,
    LANG_FONT, WORD_FONT, FLIP_DELAY_MS,
)


class Display:
    """Owns the Tk root window and every widget. No app logic lives here."""

    def __init__(
        self,
        images_dir: Path,
        on_known: Callable[[], None],
        on_unknown: Callable[[], None],
        on_card_click: Callable[[], None],
    ) -> None:
        self._on_known = on_known
        self._on_unknown = on_unknown
        self._on_card_click = on_card_click
        self._flip_timer: str | None = None

        self._root = Tk()
        self._root.title("Flashy")
        self._root.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

        self._card_front_img = PhotoImage(file=str(images_dir / "card_front.png"))
        self._card_back_img = PhotoImage(file=str(images_dir / "card_back.png"))
        self._cross_img = PhotoImage(file=str(images_dir / "wrong.png"))
        self._check_img = PhotoImage(file=str(images_dir / "right.png"))

        self._canvas = Canvas(
            self._root,
            width=CARD_W, height=CARD_H,
            bg=BACKGROUND_COLOR, highlightthickness=0,
        )
        self._card_bg = self._canvas.create_image(
            CARD_W // 2, CARD_H // 2, image=self._card_front_img,
        )
        self._card_title = self._canvas.create_text(
            CARD_W // 2, 150, text="", font=LANG_FONT, fill="black",
        )
        self._card_word = self._canvas.create_text(
            CARD_W // 2, 263, text="", font=WORD_FONT, fill="black",
        )
        self._canvas.grid(row=0, column=0, columnspan=2)
        self._canvas.bind("<Button-1>", lambda _e: self._on_card_click())

        self._unknown_btn = Button(
            self._root,
            image=self._cross_img,
            highlightthickness=0, borderwidth=0,
            bg=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR,
            command=self._on_unknown,
        )
        self._unknown_btn.grid(row=1, column=0)

        self._known_btn = Button(
            self._root,
            image=self._check_img,
            highlightthickness=0, borderwidth=0,
            bg=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR,
            command=self._on_known,
        )
        self._known_btn.grid(row=1, column=1)

        self._root.focus_set()

    @property
    def root(self) -> Tk:
        return self._root

    def render_front(self, french: str) -> None:
        """Show the French side of the card."""
        self._canvas.itemconfig(self._card_bg, image=self._card_front_img)
        self._canvas.itemconfig(self._card_title, text="French", fill="black")
        self._canvas.itemconfig(self._card_word, text=french, fill="black")

    def render_back(self, english: str) -> None:
        """Show the English side of the card."""
        self._canvas.itemconfig(self._card_bg, image=self._card_back_img)
        self._canvas.itemconfig(self._card_title, text="English", fill="white")
        self._canvas.itemconfig(self._card_word, text=english, fill="white")

    def render_complete(self) -> None:
        """Show the deck-exhausted congratulation state and disable buttons."""
        self._canvas.itemconfig(self._card_bg, image=self._card_front_img)
        self._canvas.itemconfig(
            self._card_title, text="All done!", fill="black", font=LANG_FONT,
        )
        self._canvas.itemconfig(
            self._card_word, text="You learned every word.", fill="black", font=WORD_FONT,
        )
        self._canvas.unbind("<Button-1>")
        self._known_btn.config(state="disabled")
        self._unknown_btn.config(state="disabled")

    def schedule_flip(self, callback: Callable[[], None]) -> None:
        """Cancel any pending flip timer and schedule a new one."""
        self.cancel_flip()
        self._flip_timer = self._root.after(FLIP_DELAY_MS, callback)

    def cancel_flip(self) -> None:
        """Cancel the pending auto-flip timer if one exists."""
        if self._flip_timer:
            try:
                self._root.after_cancel(self._flip_timer)
            except Exception:
                pass
            self._flip_timer = None

    def close(self) -> None:
        sys.exit(0)
