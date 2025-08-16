# backend/app/main.py
import logging
from typing import Optional, List, Dict, Any
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.tool_adapter import ToolAdapter
from app.xagent_controller import XAgentController

# ---------------------------
# Logging Configuration
# ---------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ---------------------------
# FastAPI App Initialization
# ---------------------------
app = FastAPI(
    title="L3AGI → XAgent Demo",
    version="0.1.0",
    description="Backend for XAgent with tool integration"
)

# ---------------------------
# CORS Configuration (Dev Mode: Allow All)
# ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Initialize Tools and Controller
# ---------------------------
try:
    tool_adapter = ToolAdapter()
    controller = XAgentController(tool_adapter)
    logger.info("ToolAdapter and XAgentController initialized successfully.")
except Exception as e:
    logger.exception("Error initializing tools or controller: %s", e)
    raise RuntimeError("Failed to initialize backend components.") from e

# ---------------------------
# Static Frontend
# ---------------------------
static_dir = Path(__file__).resolve().parent.parent / "static"
if not static_dir.exists():
    logger.warning("Static directory not found at %s", static_dir)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

# ---------------------------
# Request Models
# ---------------------------
class RunRequest(BaseModel):
    prompt: Optional[str] = None
    messages: Optional[List[Dict[str, Any]]] = None


# ---------------------------
# Routes
# ---------------------------
@app.get("/", include_in_schema=False)
async def index():
    """Serve the professional UI from /static/index.html."""
    index_file = static_dir / "index.html"
    if not index_file.exists():
        logger.error("index.html not found in static directory.")
        raise HTTPException(status_code=404, detail="Frontend not found.")
    return FileResponse(index_file)


@app.get("/health")
async def health():
    """Health check endpoint."""
    logger.debug("Health check requested.")
    return {"status": "ok", "engine": "xagent"}


@app.post("/run")
async def run(req: RunRequest, debug: bool = Query(False, description="Return full debug output if true")):
    """
    Run an agent request.
    - Returns clean result by default.
    - Use ?debug=true to get full debug output.
    """
    try:
        if req.prompt:
            query = req.prompt.strip()
        elif req.messages:
            query = " ".join(str(m.get("content", "")).strip() for m in req.messages)
        else:
            logger.warning("No prompt or messages provided in /run request.")
            raise HTTPException(status_code=400, detail="Provide 'prompt' or 'messages'.")

        logger.info("Running agent with query: %s", query)

        full_response = controller.run_agent(query)

        if debug:
            logger.debug("Returning full debug response.")
            return full_response

        return {
            "engine": full_response.get("engine", "xagent"),
            "result": full_response["assistant"]["content"]
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error processing /run request: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
