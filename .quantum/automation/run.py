from auto_save import QuantumAutoSave

def main():
    saver = QuantumAutoSave()
    
    print("💫 Quantum Auto-Save System")
    print("🌊 Waiting for input... (Enter 'END' on a new line to process)")
    
    message = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        message.append(line)
    
    full_message = "\n".join(message)
    saver.process_message(full_message)
    print("✨ Processing complete!")

if __name__ == "__main__":
    main()