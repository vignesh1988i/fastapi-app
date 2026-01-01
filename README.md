# FastAPI MQ Monitor Application

A FastAPI-based REST API application for monitoring and managing IBM MQ (Message Queue) services. This application provides endpoints for managing MQ channels, queue managers, and queues with authentication support.

## Project Overview

This project is a modern API service built with FastAPI that enables:
- Queue Manager (QMGR) management and monitoring
- Channel configuration and status tracking
- Queue operations and message handling
- Secure authentication and authorization
- RESTful API endpoints with automatic documentation

## Features

- **FastAPI Framework**: Modern, fast, and easy-to-use web framework
- **MQ Integration**: Seamless integration with IBM MQ
- **Authentication**: Built-in JWT-based authentication
- **Modular Architecture**: Organized routers and services
- **Auto Documentation**: Automatic interactive API documentation (Swagger UI)
- **Configuration Management**: Environment-based configuration

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- IBM MQ Client libraries (optional, for MQ connectivity)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/fastapi-app.git
   cd fastapi-app
   ```

2. **Create a virtual environment**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the root directory:
   ```
   DATABASE_URL=your_database_url
   SECRET_KEY=your_secret_key
   MQ_HOST=localhost
   MQ_PORT=1414
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```
   
   The API will be available at: `http://localhost:8000`

## API Documentation

Once the application is running, you can access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
fastapi-app/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── auth.py                 # Authentication and authorization
│   ├── config.py               # Configuration settings
│   ├── models.py               # Data models and schemas
│   ├── routers/
│   │   ├── channels.py         # Channel management endpoints
│   │   ├── qmgr.py             # Queue Manager endpoints
│   │   └── queues.py           # Queue operations endpoints
│   └── services/
│       ├── mq_client.py        # MQ client integration
│       └── __init__.py
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── .gitignore                  # Git ignore rules
```

## API Endpoints

### Channels (`/channels`)
- `GET /channels` - List all channels
- `POST /channels` - Create a new channel
- `GET /channels/{channel_id}` - Get channel details
- `PUT /channels/{channel_id}` - Update channel
- `DELETE /channels/{channel_id}` - Delete channel

### Queue Manager (`/qmgr`)
- `GET /qmgr` - Get queue manager status
- `GET /qmgr/details` - Get detailed information
- `POST /qmgr/start` - Start queue manager
- `POST /qmgr/stop` - Stop queue manager

### Queues (`/queues`)
- `GET /queues` - List all queues
- `POST /queues` - Create a new queue
- `GET /queues/{queue_id}` - Get queue details
- `PUT /queues/{queue_id}` - Update queue
- `DELETE /queues/{queue_id}` - Delete queue

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. To authenticate:

1. Obtain a token from the authentication endpoint
2. Include the token in the `Authorization` header:
   ```
   Authorization: Bearer <your_jwt_token>
   ```

## Running Tests

```bash
pytest
```

## Configuration

Configuration is managed through the `app/config.py` file. You can override settings using environment variables.

## Dependencies

See `requirements.txt` for all dependencies. Key packages:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation
- `sqlalchemy` - ORM (if database is used)
- `python-jose` - JWT authentication

## Development

### Install development dependencies
```bash
pip install -r requirements-dev.txt
```

### Run with auto-reload
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Code formatting
```bash
black .
```

### Linting
```bash
pylint app/
```

## Troubleshooting

### MQ Connection Issues
- Ensure IBM MQ is installed and running
- Check MQ host and port in `.env` file
- Verify network connectivity to MQ server

### Port Already in Use
```bash
# Use a different port
uvicorn app.main:app --port 8001
```

### Import Errors
Ensure you're in the virtual environment and all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Contributing

Contributions are welcome! Please follow these guidelines:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

**Vignesh SR**

For questions or support, please open an issue on GitHub or contact the author.

## Changelog

### Version 1.0.0 (Initial Release)
- Basic FastAPI setup
- Channel management endpoints
- Queue Manager endpoints
- Queue operations endpoints
- JWT authentication
- API documentation

---

**Last Updated**: January 1, 2026
