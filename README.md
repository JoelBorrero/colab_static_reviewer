# 📝 Colab File Reviewer

This project, named **Colab File Reviewer**, is designed to validate Google Colab files against predefined criteria. It ensures your colab files follow:

1. 📝 Correct **prompt block** format.
2. 🐍 **Snake case** function names.
3. ✅ Proper **test cases** structure.

**🌟 Future Enhancements (Coming Soon)**
4. 📘 Validate the existence of `# Solution\nText...` block.
5. 🔍 Validate typing in function parameters (e.g., `def func(x: list[int]) -> int:`) for proper typing and import statements.
6. 🚫 Ensure there are no `print` statements within the Colab file.

## 📦 Project Structure
```
.
├── app/
│   ├── routers/
│   ├── utils/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── services.py
│   └── ...
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── README.md
└── requirements.txt
```

## 🚀 Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Make](https://www.gnu.org/software/make/)

### 🐳 Running with Docker

1. **Clone the Repository**:

    ```sh
    git clone <repository-url>
    cd colab-file-reviewer
    ```

2. **Build Docker Image**:

    ```sh
    make build
    ```

3. **Start Containers**:

    ```sh
    make up
    ```

4. **Stop Containers**:

    ```sh
    make down
    ```

5. **Restart Containers**:

    ```sh
    make restart
    ```

6. **View Logs**:

    ```sh
    make logs
    ```

7. **Access Bash**:

    ```sh
    make bash
    ```

### 🌐 API Endpoints

The main API endpoint for this project is:

- **POST** `/conversations/review`

### 📋 How to Use the API

The easiest way to use the API is through the Swagger UI.
To access the Swagger UI, navigate to [port 3000](http://0.0.0.0:3000/docs#/default/review_conversation_conversations_review_post) in your browser.

## 🤝 Contributing

Feel free to fork this repository and make changes. Pull requests are welcome! For significant changes, please open an issue first to discuss what you would like to change.

### 🔧 Development

1. **Fork the Repository**:

    ```sh
    git clone <your-fork-repository-url>
    cd colab_static_reviewer
    ```

2. **Create a New Branch**:

    ```sh
    git checkout -b feature/my-feature-branch
    ```

3. **Make Your Changes**.

4. **Commit and Push**:

    ```sh
    git add .
    git commit -m "add my awesome feature"
    git push origin feature/my-feature-branch
    ```

5. **Create a Pull Request** from your forked repository into the main one.

## 🛠️ Built With

- ⚡️ [FastAPI](https://fastapi.tiangolo.com/)
- 🐍 [Python](https://www.python.org/)
- 🐳 [Docker](https://www.docker.com/)

## 📞 Contact

For any questions or inquiries, feel free to reach out to me at [joel.b@turing.com](mailto:joel.b@turing.com).

Enjoy coding! 🚀👩‍💻👨‍💻
