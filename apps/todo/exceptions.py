from rest_framework.exceptions import APIException


class BaseTaskException(APIException):
    pass


class UserTasksNotFoundException(BaseTaskException):
    status_code = 404
    default_detail = "User tasks are not found"
    default_code = "service_not_found_tasks"
