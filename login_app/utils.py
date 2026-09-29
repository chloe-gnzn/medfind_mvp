from admin_app.models import ActivityLog


def log_activity(actor_type, actor_id, action, description=''):
    """Write one row to Activity_Log."""
    return ActivityLog.objects.create(
        actor_type=actor_type,
        actor_id=actor_id,
        action=action,
        description=description,
    )
