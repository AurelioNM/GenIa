import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
import httpx
from clients.customer_client import CustomerClient
from clients.product_client import ProductClient
from configs.db_conn import get_database_connection
from routes.order_router import create_order
from services.order_service import OrderService
from storage.order_storage import OrderStorage
from tools.order_tool import OrderTool
from models.order_request import OrderRequest, OrderResponse
from mcp.server.fastmcp import Context


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    global order_tool
    db_connection = get_database_connection()

    # product
    product_client = ProductClient(httpx)

    # customer
    customer_client = CustomerClient(httpx)

    # order
    order_storage = OrderStorage(db_connection)
    order_service = OrderService(
        order_storage=order_storage,
        customer_client=customer_client,
        product_client=product_client,
    )
    order_tool = OrderTool(order_service=order_service)

    yield
    logger.info("Shutdown order-service")


mcp = FastMCP(
    name="order-mcp-service",
    instructions="Use this tool when the user needs to make a purchase.",
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=False,
    ),
    lifespan=lifespan,
)
logger = logging.getLogger(__name__)


@mcp.tool(
    name="create_purchase_order",
    title="Purchase order",
    description="Executes a purchase order.",
    structured_output=True,
)
def create_purchase_order(
    order_request: OrderRequest,
) -> OrderResponse:
    logger.info(f"Started request createOrderV1: body={order_request.model_dump()}")

    if order_tool is None:
        logger.error(f"No order_tool initiated")
        raise RuntimeError("OrderTool not initialized")

    return order_tool.create_order(order_request)


app = mcp.streamable_http_app()
