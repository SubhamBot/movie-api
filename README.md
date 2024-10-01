# Movie Data Upload and Retrieval API

This Flask application provides an API for uploading movie data from a CSV file into an SQL database, as well as an API for retrieving, filtering, and sorting that data.

## Features
- Upload a CSV file containing movie data to be stored in a database.
- Retrieve movie data sorted by **release date** and **ratings** (`vote_average`).
- Filter data by **year of release** and **language**.
- Supports pagination for efficient data retrieval.

## Requirements

Before running this project, ensure you have the following installed:

- Python 3.x
- Flask
- Flask-SQLAlchemy
- pandas
- SQLAlchemy

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/movie-api.git
   cd movie-api
2. ** Install dependencies: Install the required packages using pip**:
   ```bash
   pip install -r requirements.txt
3.**Run the application: Start the Flask development server**:
   ```bash
    python app.py
   ```
## API Endpoints

### 1. Upload Movie Data (CSV)
- **URL**: `http://127.0.0.1:5000/upload`
- **Method**: `POST`
- **Description**: Uploads a CSV file containing movie data to the database.

#### Request Example:
```bash
curl -F "file=@movies.csv" http://127.0.0.1:5000/upload
```
### 2. Retrieve Movie Data
- **URL**: `/data`
- **Method**: `GET`
- **Description**: Retrieves the movie data, sorted by release date and ratings. Supports filtering by year and language, and includes pagination.
- **Query Parameters**:
  - `page`: The page number for pagination (default: 1).
  - `per_page`: Number of records per page (default: 10).
  - `year`: Filter by release year (optional).
  - `language`: Filter by original language (optional).
- **Response**:
  - **Success**: Returns the movie data in JSON format, along with pagination details.
  - **Failure**: Returns an error message if any issues arise during data retrieval.
#### Request Example:
```bash
curl "http://127.0.0.1:5000/data?year=1995&language=en&page=1&per_page=10"
```


