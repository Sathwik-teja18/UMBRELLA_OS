import os

print(">> INITIATING FOLDER STRUCTURE REPAIR...")

# The required folders
folders = ['core', 'apps', 'ui', 'assets']

for folder in folders:
    # 1. Create the folder if it doesn't exist
    os.makedirs(folder, exist_ok=True)
    print(f"Verified folder: {folder}/")
    
    # 2. Create the __init__.py file inside the module folders
    if folder != 'assets':
        init_path = os.path.join(folder, '__init__.py')
        with open(init_path, 'a') as f:
            pass # Just creates an empty file
        print(f"  -> Verified: {folder}/__init__.py")

print("\n>> REPAIR COMPLETE. YOU MAY NOW MOVE YOUR CODE INTO THESE FOLDERS.")