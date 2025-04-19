import ansible_runner

def manage_ansible(action: str, params: dict) -> dict:
    """
    Manage Ansible operations (e.g., run playbook).
    """
    try:
        if action == "run_playbook":
            playbook_path = params.get("playbook_path")
            result = ansible_runner.run(
                private_data_dir='/tmp/ansible',
                playbook=playbook_path
            )
            if result.rc != 0:
                return {"error": f"Playbook execution failed: {result.stdout}"}
            return {"message": f"Playbook {playbook_path} executed successfully"}

        return {"error": f"Invalid action: {action}"}
    except Exception as e:
        return {"error": str(e)}