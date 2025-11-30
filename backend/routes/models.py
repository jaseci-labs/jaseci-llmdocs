"""Model and variant route handlers"""
from flask import jsonify, request
from backend.services import LLMService
from database import DocumentationService


def register_routes(app, socketio=None, running_benchmarks=None):

    @app.route('/api/models', methods=['GET'])
    def get_models():
        llm_service = LLMService()
        models = llm_service.fetch_available_models()
        formatted = [
            {
                'id': m.get('id'),
                'name': m.get('name'),
                'context_length': m.get('context_length'),
                'pricing': m.get('pricing'),
                'architecture': m.get('architecture'),
                'top_provider': m.get('top_provider')
            }
            for m in models
        ]
        return jsonify({'models': formatted})

    @app.route('/api/variants', methods=['GET'])
    def get_variants():
        variants = DocumentationService.get_all_variants()
        return jsonify({'variants': variants})

    @app.route('/api/variants', methods=['POST'])
    def create_variant():
        data = request.get_json()
        variant_name = data.get('variant_name')
        url = data.get('url')
        version = data.get('version')
        description = data.get('description')

        if not variant_name or not url or not version:
            return jsonify({'error': 'variant_name, url, and version are required'}), 400

        try:
            DocumentationService.create_variant(variant_name, url, version, description)
            return jsonify({'success': True, 'message': 'Variant created successfully'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/variants/<variant_name>', methods=['DELETE'])
    def delete_variant(variant_name):
        try:
            DocumentationService.delete_variant(variant_name)
            return jsonify({'success': True, 'message': 'Variant deleted successfully'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
