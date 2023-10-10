import streamlit as st
import os
import sys
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.text_splitter import RecursiveCharacterTextSplitter, Language
from langchain.llms import VertexAI
import vertexai

# Initialize credentials and Vertex AI
credential_path = "C:\\Users\\bbaliram\\AppData\\Roaming\\gcloud\\application_default_credentials.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
vertexai.init(project="genai-loreal-sandbox", location="us-central1")

# Define parameters
parameters = {
    "candidate_count": 1,
    "max_output_tokens": 1000,
    "temperature": 0.2,
    "top_p": 0.8,
    "top_k": 40
}

# Define supported file extensions and corresponding programming languages
file_extensions_languages = {
    '.c': Language.CPP,
    '.cpp': Language.CPP,
    '.py': Language.PYTHON,
    '.go': Language.GO,
    '.java': Language.JAVA,
    '.js': Language.JS,
    '.php': Language.PHP,
    '.proto': Language.PROTO,
    '.rst': Language.RST,
    '.ruby': Language.RUBY,
    '.rust': Language.RUST,
    '.scala': Language.SCALA,
    '.swift': Language.SWIFT,
    '.markdown': Language.MARKDOWN,
    '.latex': Language.LATEX,
    '.html': Language.HTML,
    '.sol': Language.SOL
}

# Function to find the programming language from the file extension
def find_program_language_from_extension(fileExtension):
    return file_extensions_languages.get(fileExtension, Language.PYTHON)

# Function to generate unit test cases
def generate_unit_test_cases(code_content, fileExtension):
    if isinstance(code_content, bytes):
        code_content = code_content.decode('utf-8')
    program_language = find_program_language_from_extension(fileExtension)
    st.write(f"program_language: {program_language}")
    code_splitter = RecursiveCharacterTextSplitter.from_language(
        language=program_language, chunk_size=50, chunk_overlap=0)
    code_docs = code_splitter.create_documents([code_content])

    length_code_docs = len(code_docs)
    # print (f"splitter docs length = {len(code_docs)}")
    st.write(f"splitter docs length = {len(code_docs)}")

    # print (length_code_docs)
    st.write({length_code_docs})
    

    llm = VertexAI(model_name="code-bison", max_output_tokens=2048, temperature=0.3)

    if length_code_docs <= 150:
        qdocs = "".join([code_docs[i].page_content for i in range(length_code_docs)])
        response = llm(f"<<<{qdocs}>>> Question: write unit test cases for this code in {fileExtension} programming language. generate unit test cases that cover all the functions and methods in the code. The test cases should validate the expected output for a given input, handle edge cases, and check for potential exceptions.")
        return response
    else:
        i =1 
        j =1 
        k=100 
        file_no = 1
        remaining_length = length_code_docs
        while k <= length_code_docs:
            print ("outer loop====")
            i=j
            qdocs = "".join([code_docs[i].page_content for i in range(j, k)])

            response = llm(f"<<<{qdocs}>>> Question: write unit test cases for this code in {fileExtension} programming language. generate unit test cases that cover all the functions and methods in the code. The test cases should validate the expected output for a given input, handle edge cases, and check for potential exceptions.")

            output_filename = "unit_test_cases" + f"{file_no}" + fileExtension
            f = open(output_filename,'w+')
            sys.stdout = f

            # print(response)
            # st.write({response})
            if response:
                return response

            file_no = file_no + 1

            remaining_length = remaining_length - 100
            # print ("remaining length = ")
            # print (remaining_length)
            st.write(f"remaining length = {remaining_length}")

            j=k
            # print ("j=")
            # print (j)
            st.write(f"j = {j}")

            if remaining_length>= 150:
                k=k+100
            elif remaining_length > 0:
                k=k+remaining_length
            else:
                st.write("break remaining length 0")
                break 

def Launch():
    st.title("Code Generation and Unit Test Cases")

    # File uploader widget
    code_file = st.file_uploader("Upload your code file (.py, .cpp, .java, etc.)", type=["py", "c", "cpp", "java"])
    
    if code_file:
        st.write("File uploaded successfully.")
        st.write(f"Processing file: {code_file.name}")
        
        # Check if the file extension is supported
        file_extension = os.path.splitext(code_file.name)[-1]
        if file_extension in file_extensions_languages:
            with st.spinner("Generating unit test cases..."):
                code_content = code_file.read()
                unit_test_cases = generate_unit_test_cases(code_content, file_extension)
                st.subheader("Generated Unit Test Cases")
                st.code(unit_test_cases)
        else:
            st.error("Unsupported file extension. Please upload a supported code file.")

if __name__ == "__main__":
    Launch()
