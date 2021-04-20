python3 setup.py py2app \
--includes='uvicorn.lifespan.off,uvicorn.lifespan.on,uvicorn.lifespan,uvicorn.protocols.websockets.auto,uvicorn.protocols.websockets.wsproto_impl,
uvicorn.protocols.websockets_impl,uvicorn.protocols.http.auto,
uvicorn.protocols.http.h11_impl,uvicorn.protocols.http.httptools_impl,
uvicorn.protocols.websockets,uvicorn.protocols.http,uvicorn.protocols,
uvicorn.loops.auto,uvicorn.loops.asyncio,uvicorn.loops.uvloop,uvicorn.loops,
uvicorn.logging' \
--packages uvicorn \
--dist-dir='/Users/swavan/Desktop/SwaVanOneUI'
