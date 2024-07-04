# Documentation Assistant


## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Ensure you have the following installed:
- Python 3.x
- pip

### Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/pmcode9992/DocumentationAssistant
   cd DocumentationAssistant
   ```

2. **Install the required packages:**

   ```sh
   pip install -r requirements.txt
   ```

3. **Set up the environment variables:**

   Create a `.env` file in the root directory of the project with the following content:

   ```env
   contextWindow=16000
   SingleSession_APIKEY=your_openai_api_key
   ```

### Running the Application

To run the application, use the following command:

```sh
streamlit run main.py
```

## Usage

create the file structure, when satisfied with the file structure generated (ensure you remove build folders like node_modules, virtual environments etc


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
