import os
import sys
import argparse
import re
from pathlib import Path
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Carga las variables secretas de tu archivo .env
load_dotenv()

# 1. CONFIGURATION
VAULT_DIR = Path(r"C:\Users\ADMIN\Documents\segundo-cerebro")

# Ahora busca la llave de forma segura, sin mostrarla en el código
API_KEY = os.environ.get("GEMINI_API_KEY")

PROMPT_TEMPLATE = """
You are my personal AI assistant connected to my Obsidian vault.
Use the following context from my notes to answer the question.
If the answer is not in the notes, say so. Keep it concise and practical.

CONTEXT:
{context}

QUESTION:
{question}
"""

def extract_significant_words(text):
    """Basic keyword extractor: removes punctuation, ignores words <= 3 chars and basic stopwords."""
    if not text:
        return set()
    stopwords = {"this", "that", "with", "from", "your", "what", "when", "where", "have", "they", "como", "para", "este", "esta", "cual"}
    clean_text = re.sub(r'[^\w\s]', '', text.lower())
    return {w for w in clean_text.split() if len(w) > 3 and w not in stopwords}

def get_vault_context(args, current_question=None):
    """Loads and filters notes based on user arguments."""
    base_dir = VAULT_DIR
    files_to_read = []

    # Filter 1: Folder
    if args.folder:
        base_dir = VAULT_DIR / args.folder
        if not base_dir.exists() or not base_dir.is_dir():
            print(f"Error: Folder '{args.folder}' does not exist inside {VAULT_DIR}", file=sys.stderr)
            sys.exit(1)

    # File resolution
    if args.file:
        fpath = VAULT_DIR / args.file
        if fpath.exists() and fpath.is_file():
            files_to_read.append(fpath)
        else:
            print(f"Error: File '{args.file}' not found.", file=sys.stderr)
            sys.exit(1)
    else:
        files_to_read = list(base_dir.rglob("*.md"))

    # Relevance setup
    significant_words = set()
    if args.relevant and current_question:
        significant_words = extract_significant_words(current_question)

    loaded_notes = []
    total_chars = 0
    loaded_filenames = []

    for fpath in files_to_read:
        try:
            content = fpath.read_text(encoding="utf-8")
        except Exception:
            continue
            
        # Filter 2: Tag
        if args.tag and f"#{args.tag}" not in content:
            continue
            
        # Filter 3: Relevance (Applies after folder and tag)
        if args.relevant and significant_words:
            content_lower = content.lower()
            if not any(word in content_lower for word in significant_words):
                continue

        loaded_notes.append(f"--- NOTE: {fpath.name} ---\n{content}\n")
        loaded_filenames.append(fpath.name)
        total_chars += len(content)

    return loaded_notes, loaded_filenames, total_chars

def main():
    parser = argparse.ArgumentParser(description="Brain - Obsidian Vault AI Assistant")
    parser.add_argument("query", nargs="*", help="Question to ask (if empty, enters interactive mode)")
    parser.add_argument("-f", "--file", help="Single file mode: only load this specific file")
    parser.add_argument("--tag", help="Only load notes containing '#TAG' (exclude the # in the argument)")
    parser.add_argument("--folder", help="Only load notes inside VAULT_DIR/FOLDER")
    parser.add_argument("--relevant", action="store_true", help="Only include notes with significant words from the question")
    
    args = parser.parse_args()

    # Security check
    if not VAULT_DIR.exists():
        print(f"Error: Vault directory not found at {VAULT_DIR}", file=sys.stderr)
        sys.exit(1)
        
    if not API_KEY:
        print("Error: No se encontró GEMINI_API_KEY en el archivo .env", file=sys.stderr)
        sys.exit(1)

    client = genai.Client(api_key=API_KEY)
    
    # Determine mode
    interactive_mode = len(args.query) == 0
    question = " ".join(args.query) if not interactive_mode else ""

    # Check for full-vault warning
    if not args.file and not args.tag and not args.folder and not args.relevant:
        print("\n⚠️  WARNING: No filters applied. Loading the ENTIRE vault.")

    # --- SINGLE QUERY MODE ---
    if not interactive_mode:
        process_query(args, client, question)
        return

    # --- INTERACTIVE MODE ---
    print("\n🧠 Brain Interactive Mode Started. Type 'exit' or 'quit' to stop.")
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ['exit', 'quit']:
                break
            if not user_input:
                continue
            process_query(args, client, user_input)
        except (KeyboardInterrupt, EOFError):
            break
    print("\nGoodbye!")

def process_query(args, client, question):
    """Handles fetching context, printing stats, and calling Gemini."""
    notes, filenames, char_count = get_vault_context(args, question)
    
    # Print Load Stats BEFORE Gemini Call
    print("\n" + "="*40)
    print("📊 CONTEXT LOAD STATS")
    if filenames:
        print(f"Notes loaded: {len(filenames)} ({', '.join(filenames[:5])}{'...' if len(filenames)>5 else ''})")
    else:
        print("Notes loaded: 0")
    print(f"Estimated size: {char_count} characters (~{char_count // 4} tokens)")
    print("="*40 + "\n")

    if not notes:
        print("No context found matching your filters. Try asking differently or adjusting filters.")
        return

    full_context = "\n".join(notes)
    prompt = PROMPT_TEMPLATE.format(context=full_context, question=question)

    print("🤖 Pensando...\n")
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.3)
        )
        print(response.text)
    except Exception as e:
        print(f"Error connecting to Gemini: {e}")

if __name__ == "__main__":
    main()