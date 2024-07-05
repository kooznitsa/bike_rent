def custom_preprocessing_hook(endpoints):
    filtered = []

    excluded_paths = (
        '/v1/user/change-password/',
        '/v1/user/login/',
        '/v1/user/logout/',
        '/v1/user/profile/',
        '/v1/user/reset-password/',
        '/v1/user/set-password/',
    )

    for (path, path_regex, method, callback) in endpoints:
        if not path.startswith(excluded_paths):
            filtered.append((path, path_regex, method, callback))

    return filtered
