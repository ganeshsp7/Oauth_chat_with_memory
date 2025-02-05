# OAuthChat with Memory

OAuthChat with Memory is a chat assistant application built using Streamlit, LangChain, Google OAuth for authentication (via `streamlit_oauth`), and PostgreSQL for chat storage. The app allows users to log in with their Google account, have a conversation with an AI assistant, and stores chat history persistently in PostgreSQL.

## Features

- **Google OAuth Authentication**: Secure login with Google account using OAuth 2.0 via `streamlit_oauth` component.
- **Chat History Storage**: Stores chat history in PostgreSQL database to persist conversations across sessions.
- **AI Chat Assistant**: Uses LangChain and OpenAI to generate conversational responses based on chat history.


## Requirements

- Python 3.10
- Streamlit
- LangChain
- psycopg2
- streamlit_oauth
- OpenAI API
- PostgreSQL
- dotenv (for environment variable management)

## Setup

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/OAuthChatWithMemory.git
    cd OAuthChatWithMemory
    ```

2. **Create and activate a virtual environment**:

    For Windows:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

    For Mac/Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the required dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:

    Create a `.env` file in the root of the project and add the following credentials:

    ```
    CLIENT_ID=your_google_oauth_client_id
    CLIENT_SECRET=your_google_oauth_client_secret
    AUTHORIZE_ENDPOINT=https://accounts.google.com/o/oauth2/auth
    TOKEN_ENDPOINT=https://oauth2.googleapis.com/token
    REVOKE_ENDPOINT=https://oauth2.googleapis.com/revoke
    REDIRECT_URI=http://localhost:8501
    DATABASE_URL=your_postgresql_connection_url
    ```

    Replace the placeholder values with your actual credentials. You can get the Google OAuth client ID and secret from the [Google Cloud Console](https://console.cloud.google.com/).

5. **Set up PostgreSQL**:

    - Ensure you have PostgreSQL running locally or on a server.
    - The database URL should be in the following format:
    
      ```
      postgresql://<username>:<password>@<host>/<database_name>
      ```
      
    - Make sure you have created the database (`chat_history`), or modify the `DATABASE_URL` accordingly.

6. **Run the application**:

    After completing the setup, run the Streamlit app with the following command:

    ```bash
    streamlit run app.py
    ```

    This will start the application at `http://localhost:8501`, and you can log in with your Google account to start using the chat assistant.

## Usage

1. **Authentication**:
   - Upon visiting the app, users are prompted to log in using their Google account. This is handled securely via OAuth 2.0 with the help of the `OAuth2Component` from `streamlit_oauth`.

2. **Chat with the Assistant**:
   - After logging in, users can interact with the AI assistant.
   - The assistant uses LangChain's integration with OpenAI to process and respond to queries.
   - The chat history is stored in PostgreSQL and persists across sessions.


## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -am 'Add feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Create a new Pull Request.



## Acknowledgments

- [Streamlit](https://streamlit.io/) - Framework for building interactive web apps.
- [LangChain](https://www.langchain.com/) - For connecting language models with applications.
- [Google OAuth](https://developers.google.com/identity/protocols/oauth2) - For handling user authentication.
- [PostgreSQL](https://www.postgresql.org/) - For chat message storage.
- [OpenAI](https://openai.com/) - For the AI assistant model.
- [streamlit_oauth](https://github.com/dnplus/streamlit-oauth) - For handling Google OAuth authentication in Streamlit.

