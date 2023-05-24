from dependency_injector import containers, providers
from enowshop.endpoints.metrics.repository import OrdersRepository, OrdersItemsRepository, UsersRepository

from config import Config
from enowshop.domain.keycloak.keycloak import KeycloakService
from enowshop.endpoints.metrics.service import MetricsService
from enowshop.infrastructure.database.database_sql import PostgresDatabase


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    postgres_db = providers.Singleton(PostgresDatabase, database_url=Config.DATABASE_URL)

    # repository
    order_repository = providers.Factory(OrdersRepository, session_factory=postgres_db.provided.session)
    order_items_repository = providers.Factory(OrdersItemsRepository,
                                               session_factory=postgres_db.provided.session)
    users_repository = providers.Factory(UsersRepository, session_factory=postgres_db.provided.session)


    metrics_services = providers.Factory(MetricsService, order_repository=order_repository,
                                         order_items_repository=order_items_repository,
                                         users_repository=users_repository)
