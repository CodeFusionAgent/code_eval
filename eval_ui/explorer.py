import streamlit as st
import yaml
from pathlib import Path

# --- Configuration ---
# The subfolder where your YAML evaluation files are stored.
DATA_FOLDER = "./temp_datasets"

# --- Helper Functions ---

def get_yaml_files(folder_path: Path) -> list[Path]:
    """Scans the given folder for .yaml or .yml files."""
    if not folder_path.is_dir():
        return []
    return sorted(list(folder_path.glob("*.yaml")) + list(folder_path.glob("*.yml")))

def load_data(file_path: Path) -> dict:
    """Loads and parses a YAML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            # Basic validation for the expected structure
            if 'title' not in data or 'questions' not in data:
                st.error(f"Error: The file `{file_path.name}` does not have the required 'title' and 'questions' keys.")
                return None
            return data
    except yaml.YAMLError as e:
        st.error(f"Error parsing YAML file `{file_path.name}`: {e}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred while reading `{file_path.name}`: {e}")
        return None

def save_data(file_path: Path, data: dict):
    """Saves data to a YAML file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        st.toast(f"Successfully saved changes to `{file_path.name}`", icon="✅")
    except Exception as e:
        st.error(f"Failed to save file: {e}")


# --- Main Application ---

def main():
    st.set_page_config(layout="wide", page_title="YAML Evaluation Editor")

    st.title("📝 YAML Evaluation Dataset Editor")
    st.markdown("Select a dataset from the sidebar to view, edit, add, or delete question-answer pairs.")

    data_path = Path(DATA_FOLDER)
    data_path.mkdir(exist_ok=True)

    with st.sidebar:
        st.header("Datasets")
        yaml_files = get_yaml_files(data_path)

        if not yaml_files:
            st.info(
                f"No YAML files found in the `{DATA_FOLDER}` directory. "
                "Please create a `.yaml` file to get started."
            )
            st.stop()
        
        file_options = [f.name for f in yaml_files]
        selected_filename = st.selectbox(
            "Choose an evaluation file:",
            options=file_options,
            index=0
        )
        
        selected_file_path = data_path / selected_filename

    if 'active_file' not in st.session_state or st.session_state.active_file != selected_file_path:
        st.session_state.active_file = selected_file_path
        st.session_state.data = load_data(selected_file_path)
        st.session_state.new_question = ""
        st.session_state.new_answer = ""

    if st.session_state.data:
        data = st.session_state.data
        
        st.header(f"Editing: `{selected_file_path.name}`")
        
        # --- Display and Edit Title ---
        st.text_input("Dataset Title", value=data.get("title", ""), key="dataset_title")
        st.divider()

        # --- Display and Edit Existing Entries ---
        # The delete buttons are now outside any form, so they are valid.
        for i, item in enumerate(data.get("questions", [])):
            st.subheader(f"Entry #{i + 1}")
            cols = st.columns([1, 10])
            with cols[0]:
                if st.button("🗑️", key=f"delete_{i}", help="Delete this entry"):
                    del st.session_state.data['questions'][i]
                    save_data(selected_file_path, st.session_state.data)
                    st.rerun()

            with cols[1]:
                st.text_input("Question", value=item.get("question", ""), key=f"q_{i}")
                st.text_area("Expected Answer", value=item.get("answer", ""), key=f"a_{i}", height=120)
            st.divider()

        # --- Save All Button (not a form submit) ---
        if st.button("💾 Save All Changes", use_container_width=True, type="primary"):
            # Manually construct the new data from session_state
            updated_data = {
                "title": st.session_state.dataset_title,
                "questions": []
            }
            # The number of questions might have changed if one was deleted in a previous run
            # So we iterate based on the current length of the data in session state
            for i in range(len(st.session_state.data["questions"])):
                 # Check if the key exists (it might not if an entry was just deleted)
                if f"q_{i}" in st.session_state:
                    updated_data["questions"].append({
                        "question": st.session_state[f"q_{i}"],
                        "answer": st.session_state[f"a_{i}"]
                    })
            
            st.session_state.data = updated_data
            save_data(selected_file_path, st.session_state.data)
            st.rerun()


        # --- Section for Adding New Entries ---
        st.header("➕ Add a New Entry")
        
        new_question = st.text_input("New Question", key="new_question")
        new_answer = st.text_area("New Expected Answer", key="new_answer", height=120)

        if st.button("Add and Save New Entry", use_container_width=True):
            if new_question and new_answer:
                new_entry = {"question": new_question, "answer": new_answer}
                st.session_state.data["questions"].append(new_entry)
                save_data(selected_file_path, st.session_state.data)
                
                st.session_state.new_question = ""
                st.session_state.new_answer = ""
                st.experimental_rerun()
            else:
                st.warning("Both a question and an answer are required to add a new entry.")


if __name__ == "__main__":
    main()
