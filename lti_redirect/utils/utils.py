def check_email_parameter(launch_data):
    if "email" in launch_data:
        return launch_data["email"]
    return None