from mcp.server.fastmcp import FastMCP

from app.mcp.tools.baggage_tools import register_baggage_tools
from app.mcp.tools.booking_tools import register_booking_tools
from app.mcp.tools.document_tools import register_document_tools
from app.mcp.tools.flight_tools import register_flight_tools
from app.mcp.tools.incident_tools import register_incident_tools

mcp = FastMCP(
    "AeroMind",
    instructions="Intelligent airport management tools for AI agents"
)

register_flight_tools(mcp)
register_booking_tools(mcp)
register_baggage_tools(mcp)
register_incident_tools(mcp)
register_document_tools(mcp)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
