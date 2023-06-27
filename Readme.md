# Flask Cafes API

A Flask API for managing cafes, their details, and performing various operations.
## Description

This Flask application provides an API for managing cafes. It allows users to retrieve random cafes, search for cafes by location, add new cafes, update coffee prices, and delete cafes. The API is built using Flask, Flask SQLAlchemy, and SQLite.
## Getting Started

### Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/your-username/your-repo.git
pip install -r requirements.txt
python app.py
## API Documentation

### Endpoints

- `GET /random`: Retrieve a random cafe from the database.
- `GET /all`: Retrieve all cafes.
- `GET /search?loc=<location>`: Search for cafes by location.
- `POST /add`: Add a new cafe to the database.
- `GET /update-price/<cafe_id>?new_price=<price>`: Update the coffee price for a cafe.
- `DELETE /cafe_closed/<cafe_id>?api_key=<key>`: Delete a cafe from the database.

Refer to the source code for additional details on request formats, responses, and parameters.
## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any inquiries or feedback, please contact me at your-email@example.com.
