from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import time
from functools import wraps
import logging


## logger setup
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

rate_limit_cache = {}

app = Flask(__name__)

### some moc data
trending_data = [
    {"topic": "#Politics", "platform": "Twitter", "mentions": 45000, "shares": 15800, "likes": 67000, "timestamp": "2025-01-03 21:30:00"},
    {"topic": "#WorldCup2026", "platform": "Facebook", "mentions": 38000, "shares": 12400, "likes": 52000, "timestamp": "2025-01-03 10:15:00"},
    {"topic": "SpaceX", "platform": "Twitter", "mentions": 32000, "shares": 9800, "likes": 41000, "timestamp": "2025-01-02 09:00:00"},
    {"topic": "#TaylorSwift", "platform": "Twitter", "mentions": 28000, "shares": 8900, "likes": 95000, "timestamp": "2025-01-03 08:45:00"},
    {"topic": "#AI", "platform": "Instagram", "mentions": 15000, "shares": 6200, "likes": 18000, "timestamp": "2025-01-03 06:30:00"},
    {"topic": "#CyberSecurity", "platform": "LinkedIn", "mentions": 22000, "shares": 7500, "likes": 25000, "timestamp": "2025-01-02 22:15:00"},
    {"topic": "#War", "platform": "Twitter", "mentions": 19000, "shares": 5900, "likes": 28000, "timestamp": "2025-01-02 18:00:00"},
    {"topic": "#Gaming", "platform": "Twitter", "mentions": 25000, "shares": 8200, "likes": 45000, "timestamp": "2025-01-02 18:00:00"},
    {"topic": "#Semantic Web", "platform": "LinkedIn", "mentions": 17000, "shares": 6800, "likes": 22000, "timestamp": "2025-01-02 18:00:00"},
    {"topic": "#NFTs", "platform": "Instagram", "mentions": 12000, "shares": 4500, "likes": 15000, "timestamp": "2025-01-02 18:00:00"}
]

time_map = {
    '30m': timedelta(minutes=30),
    '1h': timedelta(hours=1),
    '5h': timedelta(hours=5),
    '12h': timedelta(hours=12),
    '1d': timedelta(days=1),
    '7d': timedelta(days=7)
}


def rate_limit(limit, time_window):
    """ check if the request is within the rate limit """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.remote_addr
            logger.info(f"------------------------Client IP: {client_ip}")
            current_time = time.time()
            logger.info(f"------------------------Current time: {current_time}")
            if client_ip not in rate_limit_cache:
                rate_limit_cache[client_ip] = []

            # Remove timestamps older than the time window
            rate_limit_cache[client_ip] = [
                t for t in rate_limit_cache[client_ip] if current_time - t < time_window
            ]
            logging.info(f"Rate limit cache before cleanup: {rate_limit_cache}")
            if len(rate_limit_cache[client_ip]) >= limit:
                return jsonify({"error": "Rate limit exceeded"}), 429
            rate_limit_cache[client_ip].append(current_time)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
                        

@app.route('/api/v1/trending-topics', methods=['GET'])
@rate_limit(limit=10, time_window=60)  # 10 requests per minute
def get_trending_topics():
    """
    Get latest trending topics based on time range, topic filter, and minimum mentions.
    :return: JSON response containing trending topics.
    """
    try:
        # Input parameters
        time_range = request.args.get('time_range')
        topic_filter = request.args.get('topic')
        min_mentions = request.args.get('min_mentions')
        logger.info(f"Request received for time range: {time_range}")
        logger.info(f"Request received for topic filter: {topic_filter}")
        logger.info(f"Request received for minimum mentions: {min_mentions}")

        # Validate required parameters
        if not time_range or time_range not in time_map:
            return jsonify({"error": "Invalid time range or missing time range data"}), 400

        # Filter by time range using timestamp
        current_time = datetime.now()
        logger.info(f"------------Current time: {current_time}")
        outdated_boundary = current_time - time_map[time_range]
        logger.info(f"------------Outdated_boundary: {outdated_boundary}")

        filtered_data = []
        for post in trending_data:
            timestamp = datetime.strptime(post['timestamp'], '%Y-%m-%d %H:%M:%S')
            logger.info(f"------------Post time: {timestamp}")
            # logger.info(f"------------Time threshold: {outdated_boundary}")
            if timestamp >= outdated_boundary:
                logger.info(f"------------Post: {post}")
                filtered_data.append(post)
        logger.info(f"------------total posts: {len(filtered_data)}")
        
        if topic_filter:
            filtered_data = [post for post in filtered_data if topic_filter.lower() in post['topic'].lower()]
        
        if min_mentions:
            filtered_data = [post for post in filtered_data if post['mentions'] >= int(min_mentions)]
        
        logger.info(f"Request processed for time range: {time_range}")
        return jsonify({"trending_topics": filtered_data}), 200
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
