from src.app import App
import traceback

if __name__ == "__main__":
    try:
        app = App()
        app.run()
    except Exception as e:
        # This will catch any error and print it to the terminal
        print("--- AN UNEXPECTED ERROR OCCURRED ---")
        traceback.print_exc()
        input("\nPress Enter to exit...") # This keeps the terminal open