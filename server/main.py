from flask import Flask, request, jsonify
# import my_search_module  # Importa el módulo de búsqueda
import search_module_v2

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return jsonify({"status": "Error", "message": "No search query provided"}), 400
    results = search_module_v2.search(query)
    return jsonify(results)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
