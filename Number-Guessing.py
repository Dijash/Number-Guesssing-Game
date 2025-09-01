from browser import document
import random

number = random.randint(1, 100)
attempts = 0
max_attempts = 10

def update_attempts():
    document["attempts-left"].text = "Attempts left: " + str(max_attempts - attempts)

def set_message(text, cls="info"):
    msg = document["message"]
    msg.text = text
    msg.className = cls

def disable_game():
    document["guess-btn"].unbind("click", check_guess)
    document["guess"].disabled = True
    document["restart-btn"].style.display = "inline-block"

def check_guess(evt):
    global attempts, number
    raw = document["guess"].value.strip()

    if raw == "":
        set_message("Please enter a number between 1 and 100.", "error")
        return

    try:
        guess = int(raw)
    except:
        set_message("That's not a valid number.", "error")
        return

    if guess < 1 or guess > 100:
        set_message("Number must be between 1 and 100.", "error")
        return

    attempts += 1

    if guess < number:
        set_message("Too low.", "info")
    elif guess > number:
        set_message("Too high.", "info")
    else:
        set_message("🎉 You got it! The answer was " + str(number) + 
                    ". You guessed it in " + str(attempts) + " attempts.", "success")
        disable_game()
        return

    if attempts >= max_attempts:
        set_message("😢 Game over! The number was " + str(number) + ".", "error")
        disable_game()
        return

    update_attempts()

def restart(evt):
    global number, attempts
    number = random.randint(1, 100)
    attempts = 0
    document["guess"].value = ""
    document["guess"].disabled = False
    set_message("New game started. Good luck!", "info")
    update_attempts()
    document["restart-btn"].style.display = "none"
    document["guess-btn"].bind("click", check_guess)

# Bind events
document["guess-btn"].bind("click", check_guess)
document["restart-btn"].bind("click", restart)

# Allow pressing Enter in the input to trigger a guess
def _enter_key(evt):
    # evt.key is preferred; fallback to keyCode for older compatibility
    k = getattr(evt, 'key', None)
    code = getattr(evt, 'keyCode', None)
    if k == 'Enter' or code == 13:
        # Prevent the default form behavior (if any)
        try:
            evt.preventDefault()
        except Exception:
            pass
        check_guess(evt)

document["guess"].bind("keydown", _enter_key)

# Initialize attempts
update_attempts()
