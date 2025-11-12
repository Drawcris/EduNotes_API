# EduNotes

EduNotes is a collaborative note-taking platform designed to streamline educational content management for students and organizations. It offers customizable channels and topics, enabling users to organize and share notes efficiently.

## Tech Stack

- **Backend**: FastAPI with REST API, secured with JWT  
- **Frontend**: React, Next.js, Tailwind CSS, Shadcn UI, Material UI  
- **Database**: PostgreSQL with a custom DB DockerFile  

## Features

- **Collaborative Environment**: Users can create organizations and add subject-specific channels with topics, where notes are shared in a chat-like interface supporting text and images.  
- **Interactive Dashboard**: Provides an overview of recent notes, user statistics, rank, and a calendar for tracking events and deadlines.  
- **Organization Control**: Owners can invite, remove, or modify user roles and set avatars for their organizations.  
- **Ranking System**: Real-time like/dislike mechanism that influences user rankings and points, with a leaderboard highlighting top contributors.  
- **Event Scheduling**: Set deadlines for events like exams or tasks with specific dates and times.  
- **AI Capabilities**: Collect text notes and images, convert images to text via OCR, combine notes, and generate topic summaries using DeepSeek AI.  
- **Testing**: Comprehensive end-to-end tests implemented with Pytest for all endpoints.  
- **Containerization**: Fully Dockerized setup for the database, frontend, and backend.  

## Development Insights

This project was a collaborative effort by a team of two, with task management and planning handled through ClickUp.

## Getting Started

[Project Frontend Repository](https://github.com/AleeN1337/EduNotes-2.0)

1. Clone the repositories to your local machine.  
2. Ensure Docker is installed and run the containers for the database, frontend, and backend.  
3. Configure necessary environment variables for API keys and database settings.  
4. Launch the application and access it via the frontend URL.  

## Contributing

We welcome contributions! Fork the repository and submit pull requests with your improvements.

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
