
## Installation

To run this application, you need to have Python and Streamlit installed. Follow these steps to set up your environment:

1. Clone the repository:
   ```bash
   git clone git@github.com:sbneo2022/Hyperliquid.git
   cd Hyperliquid
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the Streamlit application, use the following command:

```bash
make run
```

This will start the application, and you can view it in your web browser at `http://localhost:8501`.

## Makefile Commands

- `make run`: Run the Streamlit application.
- `make help`: Show help information for available commands.

