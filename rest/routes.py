from . import views


def setup_routes(app):
    app.router.add_route(
            '*', '/',
            views.ItemListView,
            name='item-list')
    app.router.add_route(
            '*', '/{id}',
            views.ItemDetailView,
            name='item-detail')
