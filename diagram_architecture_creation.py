from diagrams import Diagram, Edge, Cluster
from diagrams.onprem.network import Nginx
from diagrams.onprem.client import Client
from diagrams.onprem.database import Postgresql, Mongodb
from diagrams.onprem.queue import Kafka
from diagrams.programming.framework import Django
from diagrams.custom import Custom


with Diagram(name="Project architecture"):
    client = Client("User")
    with Cluster("Docker"):
        postgres = Postgresql("Postgres")
        mongodb = Mongodb("Mongodb")
        kafka = Kafka("Kafka")
        django = Django("Django")
        svelte = Custom("Svelte", icon_path="diagram/Svelte_Logo.svg.png")
        nginx = Nginx("Nginx")
        ai_node = Custom("Image recognition", icon_path="diagram/AI.png")
        llm_node = Custom("LLM Node", icon_path="diagram/LLM.png")

        client >> Edge(color="green") << nginx
        nginx >> Edge(color="green") << svelte
        django >> Edge(color="blue") << svelte
        django >> Edge(color="darkblue", label="internal") << postgres
        django >> Edge(color="lightgreen", label="topics") << kafka
        kafka >> Edge(color="lightgreen", label="topic-1") << mongodb
        kafka >> Edge(color="darkgreen", label="topic-2") << ai_node
        llm_node >> Edge(color="pink", label="topic-3") << kafka

