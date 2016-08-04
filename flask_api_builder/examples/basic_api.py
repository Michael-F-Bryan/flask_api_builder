from flask import Blueprint, jsonify

api = Blueprint('api', __name__, url_prefix="/todo/api/v1")



@api.errorhandler(404)
def page_not_found(error):
    response = jsonify({'error': 'not found'})
    response.status_code = 404
    return response

@api.errorhandler(500)
def server_error(error):
    response = jsonify({'error': 'server error'})
    response.status_code = 500
    return response



@api.route('/tasks', methods=['GET'])
def get_tasks():
    """
    Retrieve list of tasks
    """
    # TODO: Complete me!
    raise NotImplemented


@api.route('/tasks/<int:task_id>', methods=['GET'])
def get_tasks_by_task_id(task_id):
    """
    Retrieve task number <task_id>
    """
    # TODO: Complete me!
    raise NotImplemented


@api.route('/tasks', methods=['POST'])
def post_tasks():
    """
    Create a new task
    """
    # TODO: Complete me!
    raise NotImplemented


@api.route('/tasks/<int:task_id>', methods=['PUT'])
def put_tasks_by_task_id(task_id):
    """
    Update an existing task
    """
    # TODO: Complete me!
    raise NotImplemented


@api.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_tasks_by_task_id(task_id):
    """
    Delete an existing task
    """
    # TODO: Complete me!
    raise NotImplemented
