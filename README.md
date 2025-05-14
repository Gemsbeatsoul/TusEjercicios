# Tus preguntas ('your questions')
#### Description:

The ELE Platform is an interactive application developed in Python using the Streamlit library. It is designed to facilitate the creation and resolution of multiple-choice questions, especially in the context of teaching Spanish as a Foreign Language (ELE). The application allows teachers to create customized question sessions and enables students to participate interactively.



PROJECT STRUCTURE

- project.py: Main file containing the application logic, including functions to load and save questions, generate session codes, add questions, get random questions, and check answers.
- test_project.py: Test file containing functions to verify the correct functioning of the main project functions using pytest.
- requirements.txt: List of dependencies required to run the application, including Streamlit.
- README.md: This file, which provides a detailed description of the project, its structure, and how to use it.



FEATURES:

===Teacher Mode (Modo profesor)===

- Generation of a unique session code for each set of questions.
- Interface to input questions and answer options.
- Selection of the correct answer for each question.
- Display of the questions created in the current session.​
- Completion of the session and generation of a new code for future sessions.


===Student Mode (Modo Estudiante)===

- Input of the session code provided by the teacher.​
- Presentation of the session questions sequentially.
- Selection of answers by the student.
- Display of results at the end of the session, showing correct and incorrect answers (and for incorrect ones, showing the correct answer as well).



CS50P REQUERIMENTS

- Python Implementation: The entire project is developed in Python, using standard libraries and Streamlit for the user interface.
- Functions: The project.py file contains a main function main() and several additional functions (cargar_preguntas, guardar_preguntas, generar_codigo_sesion, agregar_pregunta, obtener_pregunta_aleatoria, verificar_respuesta).
- Testing with pytest: Tests have been implemented for at least three custom functions in the test_project.py file, using the pytest framework.
- Project Structure: The main file project.py and the test file test_project.py are located in the project's root directory, fulfilling the course specifications.
- requirements.txt: Includes all necessary dependencies for running the application, facilitating installation and execution.



DESIGN AND TECHNICAL DECISIONS

=== 1. File Structure and Data Storage: ===

Question and answer data is stored simply in JSON files. This avoids the need to set up a full database, keeping the application lightweight and easy to manage. Files are named with the session code to directly associate them with each set of questions and are loaded or saved using the cargar_preguntas and guardar_preguntas functions.

=== 2. Generation of Unique Session Codes: ===

The uuid4() function is used to generate a unique 6-character session code. This allows students to enter a short, distinctive code to access the teacher's questions. The code generation function ensures each session is identifiable and not repeated, improving the user experience and avoiding potential conflicts.

=== 3. Workflow for the Teacher: ===

The application design allows the teacher to interactively add questions by selecting the correct answers using a selectbox. The process of saving and storing questions is simple: once the form is filled out, the questions are stored in the JSON file corresponding to the session code.

=== 4. Workflow for the Student: ===

The student enters a session code and answers questions sequentially. The progress state is saved using st.session_state, ensuring students continue where they left off. Additionally, answers are stored in real-time, making it easier to calculate results once the session is complete.

=== 5. Interaction and State Management with Streamlit: ===

st.session_state is used to manage the application's state between user interactions. This is key to:
- Maintaining progress of the questions (such as the current question index).
- Storing student responses while interacting with the application.
- Generating a new session code when the teacher finishes a session and wants to create a new one.

=== 6. Answer Validation: ===

An index dictionary (A, B, C) is used to map answer options and check the student's selected answer. The comparison between the student's answer and the correct one is done in the verificar_respuesta function.

=== 7. User Interface: ===

The user interface is fully interactive thanks to Streamlit, allowing both teachers and students to manage their tasks in a simple and efficient way:
- Teacher mode allows adding questions and viewing the generated session code.
- Student mode allows entering the session code and answering questions in a clear and organized format.

=== 8. Error Handling: ===

Although detailed exception handling is not specified, the platform ensures that JSON files are read and written securely, and a warning message is displayed if no questions are found for the entered session code.



USAGE INSTRUCTIONS

1. Clone the repository or download the project files.

2. Install the necessary dependencies by running:

pip install -r requirements.txt

3. Run the application with the following command:

streamlit run project.py

4. Select your role (Teacher or Student) in the sidebar and follow the instructions provided in the interface.



CONCLUSION

The ELE Platform provides a simple and effective tool for creating and resolving multiple-choice questions, facilitating the teaching and learning process in the context of ELE. It meets all the requirements established by the CS50P course and demonstrates the practical application of the knowledge acquired throughout the course.
