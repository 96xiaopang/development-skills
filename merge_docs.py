import os

def merge_markdown_files(source_dir, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Walk through the directory
        all_files = []
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                if file.endswith('.md'):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, source_dir)
                    all_files.append((rel_path, full_path))
        
        # Sort files to ensure deterministic order (alphabetical)
        # You might want to adjust this sorting if there's a specific order needed (e.g. SUMMARY.md)
        all_files.sort()
        
        for rel_path, full_path in all_files:
            try:
                with open(full_path, 'r', encoding='utf-8') as infile:
                    content = infile.read()
                    
                    # Add a header for the file
                    outfile.write(f"\n\n# File: {rel_path}\n\n")
                    outfile.write(content)
                    outfile.write("\n") # Ensure separation
                    
                print(f"Merged: {rel_path}")
            except Exception as e:
                print(f"Error reading {rel_path}: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python merge_docs.py <source_dir> <output_file>")
        sys.exit(1)
        
    source_dir = sys.argv[1]
    output_file = sys.argv[2]
    
    print(f"Merging docs from {source_dir} to {output_file}...")
    merge_markdown_files(source_dir, output_file)
    print("Done.")
