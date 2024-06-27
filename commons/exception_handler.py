from functools import wraps

from fastapi import HTTPException


def ensure_insert_one_inserted(obj_name: str = "Object"):
    """
    when trying to find a record, raise exception if it does not exist
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            insert_result = await func(*args, **kwargs)
            if insert_result.inserted_id is None:
                raise HTTPException(
                    status_code=404, detail=f"{obj_name} does not exist"
                )
            return insert_result

        return wrapper

    return decorator


def ensure_find_one_found(obj_name: str = "Object"):
    """
    when trying to find a record, raise exception if it does not exist
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            obj = await func(*args, **kwargs)
            if obj is None:
                raise HTTPException(
                    status_code=404, detail=f"{obj_name} does not exist"
                )
            return obj

        return wrapper

    return decorator


def ensure_find_one_found_plus_detail(detail: str):
    """
    when trying to find a record, raise exception with default message
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            obj = await func(*args, **kwargs)
            if obj is None:
                raise HTTPException(status_code=404, detail=detail)
            return obj

        return wrapper

    return decorator


def ensure_update_modified(obj_name: str = "Object"):
    """
    when trying to update a record, raise exception if it does not change the record
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            update_result = await func(*args, **kwargs)
            if update_result.modified_count < 1:
                raise HTTPException(
                    status_code=404,
                    detail=f"{obj_name} did not change, It probably does not exist",
                )
            return update_result

        return wrapper

    return decorator


def ensure_delete_one_found(obj_name: str = "Object"):
    """
    when trying to delete a record, raise exception if it does not exist
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            delete_result = await func(*args, **kwargs)
            if delete_result.deleted_count < 1:
                raise HTTPException(
                    status_code=404, detail=f"{obj_name} does not exist to delete"
                )
            return delete_result

        return wrapper

    return decorator
