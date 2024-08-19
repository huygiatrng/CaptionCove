# CaptionCove

CaptionCove is a backend-focused project designed to convert video content into accurate subtitles and transcripts. This project was initiated in Spring 2024 and leverages advanced technologies to provide a reliable and efficient platform for generating and managing video transcripts.

## Features

- **Video Transcription**: Convert video content into precise subtitles and transcripts using OpenAI's Whisper. The platform supports multiple output formats, including SRT and VTT, and allows users to print the full script as a text file.
  
- **User Management**: Secure user login and authentication system built with Django, ensuring that user data is protected and accessible only to authorized users.

- **Scalable Backend**: Powered by PostgreSQL, the backend efficiently handles high volumes of transcript data and provides robust data management.

- **File Management**: Integrated with AWS S3 for secure and scalable file storage. All user data is encrypted to maintain privacy and security.

- **Optimized Performance**: Utilizes AWS Load Balancers and Celery, integrated with Redis for efficient task queue management. This ensures rapid processing rates and high service availability, even under heavy load.

- **Credit-Based System**: A credit-based system allows users to access transcription services based on video length. This system is designed to offer flexible service options and improve user experience.

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

6. Start the Django development server:

   ```bash
   python manage.py runserver
   ```

### Usage

- **API Integration**: Utilize the provided RESTful APIs to interact with the backend for uploading videos, managing user accounts, and generating transcripts.

- **Video Transcription**: Upload videos through the API to generate subtitles and transcripts, which can be retrieved in the desired format.

- **Transcript Management**: Access, download, or print transcripts via the API.
