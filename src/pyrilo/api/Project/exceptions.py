from pyrilo.exceptions import PyriloError


class ProjectError(PyriloError):
    """
    Base class for all gams project related errors
    """

class ProjectAlreadyExistsError(ProjectError):
    """

    """