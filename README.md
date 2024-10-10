
# Travel-Itinerary-Generator

This is a Travel Itinerary Generator web application that generates personalized itineraries based on user input and enriched travel data using clustering techniques. It is built with Node.js for the backend, Python for AI/ML, and a simple HTML/CSS frontend. The clustering algorithm, powered by KMeans, groups travel itineraries based on expenses, travel vibes, and package amounts.

Table of Contents
Technologies
Features
System Architecture
Setup Instructions
Prerequisites
Local Installation
Running the Application
Testing the Solution
AWS Deployment (Optional)
Project Structure
Technologies
Backend: Node.js, Express
AI/ML: Python, KMeans clustering (with scikit-learn)
Frontend: HTML5, CSS, JavaScript (jQuery)
Database: Mock data in CSV format for travel info
Deployment: (Optional) AWS Beanstalk, RDS (mock setup included)
Others: Body-parser for parsing request bodies, child_process for executing Python scripts
Features
Enter a place to receive a personalized travel itinerary.
Clusters itineraries by expenses, travel vibe, and package amounts using KMeans.
Provides a multi-day itinerary, detailing places to visit, activities to do, and the total cost.
Simple and clean user interface for quick interaction.
System Architecture
Frontend: Simple HTML/CSS form for user input.
Backend: Node.js server handles requests and communicates with the Python script to generate itineraries.
AI Component: Python script loads and processes the travel data, applies clustering to generate itinerary suggestions based on the input place.
Setup Instructions
Prerequisites
Node.js (v14 or higher)
Python (v3.7 or higher)
npm (Node Package Manager)
Git (for cloning the repository)
(Optional) AWS account with credentials for Beanstalk, RDS setup


