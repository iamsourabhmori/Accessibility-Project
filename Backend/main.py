# #main.py

# from speech import take_command
# from assistant import handle_command
# from speech import take_command, talk
# # from assistant import handle_command


# def main():
#     talk("Voice assistant started. Say a command.")
#     while True:
#         command = take_command()
#         if command:
#             print("👉 You said:", command)
#             handle_command(command)

# if __name__ == "__main__":
#     main()

#--------------------------------------------------------------------------------------------------------------


# main.py

from speech import take_command, talk
from assistant import handle_command


def main():
    """Main loop for the voice assistant"""
    talk("Voice assistant started. Say a command.")
    print("🎙️ Voice assistant is running...")

    while True:
        command = take_command()
        if command:
            print("👉 You said:", command)
            handle_command(command)
        else:
            # If no command was captured, keep listening
            continue


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Voice assistant stopped by user.")
        talk("Goodbye! Voice assistant stopped.")
