def get_current_time() -> str:
    """
    获取当前的时间并返回格式化字符串。

    Returns:
        str: 当前时间的字符串表示，格式为 'YYYY-MM-DD HH:MM:SS'
    """
    from datetime import datetime
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
