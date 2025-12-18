import os
import re
from pathlib import Path

def parse_folder_structure(text_input):
    """
    Parse the pasted text into a proper folder structure 
    This version better handles the tree hierarchy
    """
    lines = text_input.strip().split('\n')
    root = {}
    
    for line in lines:
        line = line.rstrip()  # Remove trailing whitespace
        if not line:
            continue
        
        # Count indentation level
        indent_level = 0
        clean_line = line
        
        # Handle tree characters
        tree_chars = ['├', '└', '│', '─']
        for char in tree_chars:
            clean_line = clean_line.replace(char, ' ')
        
        # Count leading spaces for indentation
        leading_spaces = len(clean_line) - len(clean_line.lstrip())
        indent_level = leading_spaces // 2  # Approximate indent level
        
        clean_line = clean_line.strip()
        
        if not clean_line:
            continue
        
        # Determine if it's a file or folder
        is_file = '.' in clean_line.split('/')[-1] if '/' in clean_line else '.' in clean_line
        
        # Split path if it contains slashes
        if '/' in clean_line:
            parts = clean_line.split('/')
            current = root
            for i, part in enumerate(parts):
                if i == len(parts) - 1:  # Last part
                    if is_file:
                        current[part] = ""
                    else:
                        if part not in current:
                            current[part] = {}
                else:  # Intermediate directory
                    if part not in current:
                        current[part] = {}
                    current = current[part]
        else:
            # Simple entry - file or folder
            if is_file:
                root[clean_line] = ""
            else:
                if clean_line not in root:
                    root[clean_line] = {}
    
    return root

def create_structure(base_path, structure):
    """
    Recursively create the folder and file structure
    """
    for name, content in structure.items():
        full_path = os.path.join(base_path, name)
        
        if isinstance(content, dict):  # It's a folder
            os.makedirs(full_path, exist_ok=True)
            print(f"📁 Created folder: {full_path}")
            create_structure(full_path, content)
        else:  # It's a file
            # Ensure parent directory exists
            parent_dir = os.path.dirname(full_path)
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir, exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content or '')
            print(f"📄 Created file: {full_path}")

def display_welcome():
    """
    Display welcome message and instructions
    """
    print("=" * 60)
    print("🎯 FOLDER STRUCTURE GENERATOR")
    print("=" * 60)
    print("\n📋 INSTRUCTIONS:")
    print("1. Paste your folder structure below")
    print("2. You can use either format:")
    print("   - Tree format:")
    print("     project/")
    print("     ├── src/")
    print("     │   ├── main.py")
    print("     │   └── utils/")
    print("     └── README.md")
    print("   - Simple paths:")
    print("     project/src/main.py")
    print("     project/src/utils/")
    print("     project/README.md")
    print("3. Press Enter twice to finish pasting")
    print("=" * 60)

def get_user_input():
    """
    Get folder structure input from user with multi-line support
    """
    print("\n📝 Paste your folder structure (Press Enter twice when done):")
    print("─" * 50)
    
    lines = []
    while True:
        try:
            line = input()
            if line == '' and lines and lines[-1] == '':
                break
            lines.append(line)
        except EOFError:
            break
    
    # Remove the last empty line
    if lines and lines[-1] == '':
        lines.pop()
    
    return '\n'.join(lines)

def debug_structure(structure, indent=0):
    """
    Debug function to print the parsed structure
    """
    for name, content in structure.items():
        if isinstance(content, dict):
            print("  " * indent + f"📁 {name}/")
            debug_structure(content, indent + 1)
        else:
            print("  " * indent + f"📄 {name}")

def main():
    """
    Main function to run the folder structure generator
    """
    display_welcome()
    
    # Get the folder structure from user
    folder_structure_text = get_user_input()
    
    if not folder_structure_text.strip():
        print("❌ No folder structure provided. Exiting.")
        return
    
    # Get main folder name
    print("\n📁 Enter the main folder name (or press Enter for 'my_project'):")
    main_folder = input().strip()
    if not main_folder:
        main_folder = "my_project"
    
    # Parse the structure
    print("\n⏳ Parsing folder structure...")
    try:
        structure = parse_folder_structure(folder_structure_text)
        
        if not structure:
            print("❌ Could not parse any valid folder structure.")
            return
        
        # Debug: Show parsed structure
        print("\n🔍 Parsed structure:")
        debug_structure(structure)
        print("─" * 50)
        
        # Create the main folder
        if os.path.exists(main_folder):
            print(f"\n⚠️  Folder '{main_folder}' already exists.")
            overwrite = input("Do you want to overwrite it? (y/N): ").strip().lower()
            if overwrite != 'y':
                print("❌ Operation cancelled.")
                return
            # Remove existing folder
            import shutil
            shutil.rmtree(main_folder)
        
        # Create the structure
        print(f"\n🚀 Creating folder structure in '{main_folder}'...")
        print("─" * 50)
        
        create_structure(main_folder, structure)
        
        print("─" * 50)
        print(f"✅ Successfully created folder structure in '{main_folder}'!")
        print(f"📊 Summary:")
        print(f"   Location: {os.path.abspath(main_folder)}")
        
        # Count files and folders
        file_count = 0
        folder_count = 0
        for root, dirs, files in os.walk(main_folder):
            folder_count += len(dirs)
            file_count += len(files)
        
        print(f"   Folders created: {folder_count}")
        print(f"   Files created: {file_count}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        print("Please check your input format and try again.")

def create_example():
    """
    Optional: Create an example to demonstrate the program
    """
    example_structure = """project/
├── src/
│   ├── main.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py
│   └── config/
├── tests/
│   └── test_main.py
├── docs/
│   └── README.md
└── requirements.txt"""
    
    print("\n💡 EXAMPLE: Try pasting this structure to test:")
    print("─" * 40)
    print(example_structure)
    print("─" * 40)

# Alternative simpler parser that works better with tree structures
def parse_tree_structure(text_input):
    """
    Alternative parser specifically for tree-like structures
    """
    lines = text_input.strip().split('\n')
    stack = [{}]  # Stack to track current level
    path_stack = [""]  # Stack to track path names
    
    for line in lines:
        if not line.strip():
            continue
            
        # Clean the line
        clean_line = re.sub(r'[│├└──]\s*', '', line).strip()
        if not clean_line:
            continue
        
        # Count indentation by tree characters
        indent = 0
        for char in line:
            if char in [' ', '│']:
                indent += 1
            elif char in ['├', '└']:
                break
            else:
                break
        
        # Remove items from stack that are too deep
        while len(stack) > indent + 1:
            stack.pop()
            path_stack.pop()
        
        current_level = stack[-1]
        
        # Check if it's a directory (ends with / or no extension)
        if clean_line.endswith('/') or ('.' not in clean_line.split('/')[-1] and '/' not in clean_line):
            # It's a directory
            current_level[clean_line.rstrip('/')] = {}
            stack.append(current_level[clean_line.rstrip('/')])
            path_stack.append(clean_line.rstrip('/'))
        else:
            # It's a file
            current_level[clean_line] = ""
    
    return stack[0]

if __name__ == "__main__":
    # Show example first
    create_example()
    
    # Let user choose parser
    print("\n🔧 Choose input format:")
    print("1. Tree format (with ├, │, └ characters)")
    print("2. Simple paths (one path per line)")
    choice = input("Enter choice (1 or 2, default 1): ").strip()
    
    # Run the main program
    if choice == "2":
        # Use the original parser for simple paths
        main()
    else:
        # Use the tree parser
        display_welcome()
        folder_structure_text = get_user_input()
        
        if not folder_structure_text.strip():
            print("❌ No folder structure provided. Exiting.")
            exit()
        
        print("\n📁 Enter the main folder name (or press Enter for 'my_project'):")
        main_folder = input().strip() or "my_project"
        
        print("\n⏳ Parsing folder structure...")
        structure = parse_tree_structure(folder_structure_text)
        
        print("\n🔍 Parsed structure:")
        debug_structure(structure)
        
        if os.path.exists(main_folder):
            print(f"\n⚠️  Folder '{main_folder}' already exists.")
            overwrite = input("Do you want to overwrite it? (y/N): ").strip().lower()
            if overwrite != 'y':
                print("❌ Operation cancelled.")
                exit()
            import shutil
            shutil.rmtree(main_folder)
        
        print(f"\n🚀 Creating folder structure in '{main_folder}'...")
        create_structure(main_folder, structure)
        print(f"✅ Successfully created folder structure in '{main_folder}'!")
    
    # Keep console open
    input("\nPress Enter to exit...")

