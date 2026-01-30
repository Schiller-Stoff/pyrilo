from pyrilo.exceptions import PyriloError


class ProjectError(PyriloError):
    """
    Base class for all gams project related errors
    """

class ProjectAlreadyExistsError(ProjectError):
    """
    Gams project already exist
    """

class ProjectNotFoundError(ProjectError):
    """
    Gams project not found
    """