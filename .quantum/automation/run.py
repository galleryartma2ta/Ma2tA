from auto_save import QuantumAutoSave
import os

def main():
    # Make sure we're in the right directory
    os.chdir("C:\\Users\\Ma2tA\\Documents\\GitHub\\Ma2tA")
    
    saver = QuantumAutoSave()
    
    print("💫 Quantum Auto-Save System")
    print("🌊 Waiting for input... (Enter 'END' on a new line to process)")
    
    message = []
    while True:
        try:
            line = input()
            if line.strip() == "END":
                break
            message.append(line)
        except KeyboardInterrupt:
            print("\n✨ Operation cancelled by user")
            return
    
    full_message = "\n".join(message)
    saver.process_message(full_message)
    print("✨ Processing complete!")

if __name__ == "__main__":
    main()