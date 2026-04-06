import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from flashcard import FlashCard
from display import Display

HERE = Path(__file__).parent
DATA_DIR = HERE.parent / "data"
IMAGES_DIR = HERE.parent / "images"


def main() -> None:
    deck = FlashCard(DATA_DIR)

    # Mutable closure cell: True = showing front, False = showing back.
    is_front: list[bool] = [True]
    current_word: list[dict] = [{}]

    def show_next() -> None:
        display.cancel_flip()
        word = deck.next_word()
        if word is None:
            display.render_complete()
            return
        current_word[0] = word
        is_front[0] = True
        display.render_front(word["French"])
        display.schedule_flip(auto_flip)

    def auto_flip() -> None:
        display.cancel_flip()
        if is_front[0]:
            display.render_back(current_word[0]["English"])
            is_front[0] = False

    def on_card_click() -> None:
        if is_front[0]:
            # Manual flip before auto-timer fires.
            display.cancel_flip()
            display.render_back(current_word[0]["English"])
            is_front[0] = False
        else:
            display.render_front(current_word[0]["French"])
            is_front[0] = True

    def on_known() -> None:
        display.cancel_flip()
        deck.mark_known()
        show_next()

    def on_unknown() -> None:
        show_next()

    display = Display(
        images_dir=IMAGES_DIR,
        on_known=on_known,
        on_unknown=on_unknown,
        on_card_click=on_card_click,
    )

    show_next()
    display.root.mainloop()


if __name__ == "__main__":
    main()
