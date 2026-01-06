from diagrams import Diagram, Edge
from diagrams.onprem.network import Nginx
from diagrams.onprem.client import Client
from diagrams.onprem.compute import Server
from diagrams.onprem.database import Postgresql, Mongodb
from diagrams.onprem.queue import Kafka
from diagrams.onprem.container import Docker
from diagrams.custom import Custom


with Diagram(name="Project architecture"):
    nginx = Nginx("Nginx")