#Explanation of the Code
Configuration & Imports: It starts by importing streamlit, yaml, and pathlib for file system operations. The DATA_FOLDER constant makes it easy to change the subfolder name.

##Helper Functions:

get_yaml_files(): Uses pathlib to safely find all files ending with .yaml or .yml in the specified directory.

load_data(): Opens a file, parses it using pyyaml, and includes basic error handling to check for malformed YAML or missing title/questions keys.

save_data(): Takes a Python dictionary and writes it back to the specified YAML file in a human-readable format.

##Sidebar & File Selection:

A sidebar (st.sidebar) is used to display the list of available YAML files.

st.selectbox creates a dropdown menu for the user to choose a file. This is a clean way to handle selection.

Session State (st.session_state): This is the most critical part of the application for ensuring a smooth user experience.

When a user selects a file, its contents are loaded into st.session_state.data and the file path is stored in st.session_state.active_file.

The app only reloads the file from disk if the user selects a different file.

All edits, additions, and deletions first modify the data in st.session_state and then save it to the file. This prevents data loss and makes the UI feel fast and responsive.

##Editing Interface (st.form):

The main editing area is wrapped in an st.form. This is crucial because it groups all the text inputs and the main "Save All Changes" button.

This prevents the app from re-running every time you type a single character. The app only re-runs when you explicitly click the st.form_submit_button.

Each input widget (st.text_input, st.text_area) is given a unique key (e.g., f"question_{i}"). This is how Streamlit identifies and preserves the state of each individual widget across re-runs.

##Deletion Logic:

The delete button (🗑️) is placed inside the loop for each entry but outside the main form's logic.

When a delete button is clicked, it immediately removes the corresponding item from the list in st.session_state.data, saves the updated data to the file, and then calls st.rerun() to refresh the entire UI to reflect the change.

##Addition Logic:

The "Add a New Entry" section is kept separate at the bottom.

It uses its own input widgets with unique keys ("new_question", "new_answer").

When its button is clicked, it appends the new data to the list in st.session_state.data, saves to the file, and then calls st.rerun() to update the display. It also clears the input fields for the next addition.
