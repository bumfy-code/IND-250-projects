import os
import sys
from pypdf import PdfWriter, PdfReader

def main():
    # 1 & 2. Validation: Ensure both output name and folder path are provided
    if len(sys.argv) < 3:
        print("Error: Required arguments missing.")
        print("Usage: python pdfmerger.py <output_filename> <target_directory>")
        sys.exit(1)

    output_name = sys.argv[1]
    if not output_name.endswith('.pdf'):
        output_name += '.pdf'
    
    target_dir = sys.argv[2]

    # Validate that the target path is actually a directory
    if not os.path.isdir(target_dir):
        print(f"Error: '{target_dir}' is not a valid directory.")
        sys.exit(1)

    # 3. Initialize: Create merger object
    merger = PdfWriter()

    # 4 & 5. Retrieve & Filter: Scan the specified folder for PDFs
    try:
        all_files = os.listdir(target_dir)
    except Exception as e:
        print(f"Error accessing directory: {e}")
        sys.exit(1)

    pdf_files = [f for f in all_files if f.lower().endswith('.pdf') and f != output_name]

    # 6. Sort: Alphabetical order
    pdf_files.sort()

    # 7. Report: Count and list found files
    print(f"PDF files found in '{target_dir}': {len(pdf_files)}")
    print("List:")
    for f in pdf_files:
        print(f" - {f}")

    if not pdf_files:
        print("No PDF files found to merge.")
        sys.exit(0)

    # 8. Prompt: Ask the user whether to continue
    choice = input("Continue (y/n): ").strip().lower()
    if choice != 'y':
        print("Operation cancelled.")
        sys.exit(0)

    # 9. Append: Add each PDF using its full path
    for pdf in pdf_files:
        full_path = os.path.join(target_dir, pdf)
        try:
            reader = PdfReader(full_path)
            merger.add_pages(reader.pages)
        except Exception as e:
            print(f"Could not read {pdf}: {e}")

    # 10. Export: Save final combined file
    try:
        merger.write(output_name)
        merger.close()
        print(f"\nSuccess! Merged file saved as: {output_name}")
    except Exception as e:
        print(f"Error saving file: {e}")

if __name__ == '__main__':
    main()
