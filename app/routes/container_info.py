from fastapi import APIRouter, HTTPException
import docker

router = APIRouter()

@router.get("/containers")
def get_container(container_name: str):
    try:
        client = docker.from_env()
        container = client.containers.get(container_name)
        container_details = {
            "container_name": container.name,
            "operating_system": container.attrs["Config"]["Image"],
            "external_volumes": [mount["Source"] for mount in container.attrs["Mounts"]],
            "ip_address": container.attrs["NetworkSettings"]["IPAddress"],
            "ports": container.attrs["NetworkSettings"]["Ports"]
        }
        return {"status": "success", "data": container_details}
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail=f"Container '{container_name}' not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))