from flask import Blueprint, render_template, request

itinerary_bp = Blueprint('itinerary', __name__)


@itinerary_bp.route('/')
def index():
    return render_template('index.html')


@itinerary_bp.route('/generate', methods=['POST'])
def generate():
    data = {
        'destination': request.form.get('destination', ''),
        'interests': request.form.get('interests', ''),
        'duration': request.form.get('duration', ''),
        'group_size': request.form.get('group_size', ''),
    }
    return render_template('result.html', **data)
