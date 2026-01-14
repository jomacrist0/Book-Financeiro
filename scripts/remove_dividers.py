import os
import re

def remove_dividers_from_file(file_path):
    """Remove st.markdown('---') and st.markdown('<hr>') lines from a Python file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove st.markdown("---") lines
        content = re.sub(r'\s*st\.markdown\("---"\)\s*\n', '\n', content)
        
        # Remove st.markdown('<hr>') lines  
        content = re.sub(r'\s*st\.markdown\("<hr>", unsafe_allow_html=True\)\s*\n', '\n', content)
        
        # Remove st.markdown('<hr class="section-divider">') lines
        content = re.sub(r'\s*st\.markdown\(\'<hr class="section-divider">\', unsafe_allow_html=True\)\s*\n', '\n', content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Processed: {file_path}")
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Process all Python files in pages directory
pages_dir = r"c:\Users\iagos\OneDrive\Github 2\Book - Streamlit e BI\Book Financeiro - Streamlit\pages"
main_file = r"c:\Users\iagos\OneDrive\Github 2\Book - Streamlit e BI\Book Financeiro - Streamlit\Pagina_inicial.py"

# Process main file
remove_dividers_from_file(main_file)

# Process all Python files in pages directory
for filename in os.listdir(pages_dir):
    if filename.endswith('.py'):
        file_path = os.path.join(pages_dir, filename)
        remove_dividers_from_file(file_path)

print("All divider lines removed!")
