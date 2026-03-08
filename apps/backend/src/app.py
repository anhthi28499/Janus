from flask import Flask
from flask_cors import CORS

from core.config import Config
from core.database import init_db


def create_app():
    app = Flask(__name__)
    CORS(app)

    # Load configuration
    app.config.from_object(Config)

    # Initialize Database
    init_db(app)

    # Middleware registration
    from middlewares.logging import setup_logging
    setup_logging(app)

    # Blueprint registration
    from controllers.chat import chat_bp
    from controllers.evaluation import eval_bp
    from controllers.knowledgebase import kb_bp

    app.register_blueprint(kb_bp, url_prefix='/api/v1/knowledgebase')
    app.register_blueprint(eval_bp, url_prefix='/api/v1/evaluation')
    app.register_blueprint(chat_bp, url_prefix='/api/v1/chat')

    @app.route('/health', methods=['GET'])
    def health_check():
        return {'status': 'healthy', 'message': 'Janus API is running'}, 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)
