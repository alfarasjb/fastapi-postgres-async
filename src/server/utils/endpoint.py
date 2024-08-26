from fastapi import APIRouter, Request, Response


api = APIRouter()


@api.get("/")
async def default_route(request: Request) -> Response:
    return Response(status_code=200, content="success")
