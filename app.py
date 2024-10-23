from flask import Flask, jsonify
from flask_cors import CORS  # For handling CORS if needed
import json
import os
import random
from typing import Dict, List, Union

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
JSON_DIRECTORY = "json"  # Directory where your JSON files are stored

class JSONFileManager:
    def __init__(self, directory: str):
        self.directory = directory
        self._ensure_directory_exists()
        
    def _ensure_directory_exists(self) -> None:
        """Create the JSON directory if it doesn't exist."""
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
    
    def get_all_json_files(self) -> List[str]:
        """Get a list of all JSON files in the directory."""
        return [f for f in os.listdir(self.directory) 
                if f.endswith('.json')]
    
    def read_json_file(self, filename: str) -> Dict:
        """Read and parse a JSON file."""
        try:
            with open(os.path.join(self.directory, filename), 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            return {"error": f"Error reading file {filename}: {str(e)}"}
    
    def get_random_json(self) -> Union[Dict, None]:
        """Get a random JSON file's content."""
        files = self.get_all_json_files()
        if not files:
            return None
        random_file = random.choice(files)
        return self.read_json_file(random_file)
    
    def get_file_by_name(self, filename: str) -> Union[Dict, None]:
        """Get a specific JSON file's content by name."""
        if not filename.endswith('.json'):
            filename += '.json'
        if filename in self.get_all_json_files():
            return self.read_json_file(filename)
        return None

# Initialize the JSON file manager
json_manager = JSONFileManager(JSON_DIRECTORY)

@app.route('/api/random', methods=['GET'])
def get_random_json():
    """Endpoint to get a random JSON file."""
    json_data = json_manager.get_random_json()
    if json_data is None:
        return jsonify({"error": "No JSON files found"}), 404
    return jsonify(json_data)

@app.route('/api/files', methods=['GET'])
def get_all_files():
    """Endpoint to get a list of all available JSON files."""
    files = json_manager.get_all_json_files()
    return jsonify({"files": files})

@app.route('/api/file/<filename>', methods=['GET'])
def get_specific_file(filename):
    """Endpoint to get a specific JSON file by name."""
    json_data = json_manager.get_file_by_name(filename)
    if json_data is None:
        return jsonify({"error": "File not found"}), 404
    return jsonify(json_data)

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Configuration for running the app
    config = {
        'host': '0.0.0.0',  # Makes the server publicly available
        'port': 5000,       # Port to run the server on
        'debug': True       # Enable debug mode for development
    }
    
    # Print available endpoints when starting the server
    print("\nAvailable endpoints:")
    print("  * /api/random - Get a random JSON file")
    print("  * /api/files - List all available JSON files")
    print("  * /api/file/<filename> - Get a specific JSON file")
    print(f"\nServer running on http://{config['host']}:{config['port']}\n")
    
    app.run(**config)