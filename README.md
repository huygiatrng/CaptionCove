# CaptionCove

CaptionCove is a dynamic web application designed to convert video content into accurate subtitles and transcripts. This project was initiated in Spring 2024 and leverages state-of-the-art technologies to provide users with a reliable and efficient platform for generating and managing video transcripts.

## Features

- **Video Transcription**: Convert video content into precise subtitles and transcripts using OpenAI's Whisper. The platform supports multiple output formats, including SRT and VTT, and allows users to print the full script as a text file.
  
- **User Management**: Secure user login and authentication system built with Django, ensuring that user data is protected and accessible only to authorized users.

- **Scalable Backend**: The backend is powered by PostgreSQL, providing robust data management and handling high volumes of transcript data efficiently.

- **File Management**: Integrated with AWS S3 for secure and scalable file storage. All user data is encrypted to maintain privacy and security.

- **Optimized Performance**: Utilizes AWS Load Balancers and Celery, integrated with Redis for efficient task queue management. This ensures rapid processing rates and high service availability, even under heavy load.

- **Credit-Based System**: A credit-based system allows users to access transcription services based on video length. This system is designed to enhance user experience and offer flexible service options.

- **RESTful APIs**: Developed robust and reliable RESTful APIs for seamless interaction with the backend, rigorously tested with Postman to ensure efficiency and reliability.

## Getting Started

### Prerequisites

- Python 3.x
- Django
- PostgreSQL
- AWS account with S3 and Load Balancers setup
- Redis
- Celery
- Postman (for API testing)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/huygiatrng/CaptionCove.git
   cd CaptionCove
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up the PostgreSQL database:

   ```sql
   CREATE DATABASE captioncove;
   ```

4. Configure your environment variables for Django, PostgreSQL, AWS S3, and Redis.

5. Run the Django migrations:

   ```bash
   python manage.py migrate
   ```

6. Start the development server:

   ```bash
   python manage.py runserver
   ```

### Usage

- **Login/Signup**: Create an account or log in to your existing account to access the transcription services.
  
- **Upload Video**: Upload your video file for transcription. The system will generate subtitles and transcripts in your chosen format (SRT or VTT).
  
- **Manage Transcripts**: Access, download, or print your transcripts directly from the dashboard.
