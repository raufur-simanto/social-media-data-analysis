# Trending Topics API
## A Flask based REST API for Trending Topics data with time-based filtering

## Features
- Get latest trending topics data for a given time period(30m, 1h, 5h, 12h, 1d, 7d)
- Filter topic by keywords
- Basic logging system

## API Endpoints
- GET /trending_topics

## Parameters
- time_range: Time period for which trending topics data is required. Allowed values are 30m, 1h, 5h, 12h, 1d, 7d.
- filter: topic, min_mentions (optional)

## Example Request
```
# Get topics from last 30 minutes
curl "http://localhost:5000/api/v1/trending-topics?time_range=30m"

# Get topics from last 3 hours with filter
curl "http://localhost:5000/api/v1/trending-topics?time_range=5h&filter=AI&min_mentions=1000"

# Get topics from last 24 hours
curl "http://localhost:5000/api/v1/trending-topics?time_range=1d"
```
## Response Format
```
{
    "trending_topics": [
        {
            "likes": 67000,
            "mentions": 45000,
            "shares": 15800,
            "timestamp": "2025-01-03 21:30:00",
            "topic": "#Politics"
        }
    ]
}
```

## Setup and Installation
1. Create a virtual environment and activate it
 ```
 python3 -m venv venv   
 source venv/bin/activate
 ```
 . Install the required packages
 ```
 pip install -r requirements.txt
 ```
 3. Run the application
 ``` python trending_topics.py ```
