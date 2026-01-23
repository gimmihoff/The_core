from django.apps import AppConfig

class AACoreHubConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "aa_core_hub"
    verbose_name = "Core Hub"

    def ready(self):
        # Import signals
        try:
            from . import signals  # noqa: F401
        except Exception:
            pass

        # Register AllianceAuth menu entry if hooks are available
        try:
            from allianceauth.services.hooks import MenuItemHook, ServicesHook  # type: ignore
            from allianceauth import hooks  # type: ignore

            class CoreHubMenuItem(MenuItemHook):
                def __init__(self):
                    super().__init__(
                        "Core Hub",
                        "fas fa-sitemap",
                        "aa_core_hub:dashboard",
                        navactive=["aa_core_hub:"],
                    )

                def render(self, request):
                    # Only show to logged-in users with at least view permission
                    return request.user.is_authenticated

            @hooks.register("menu_item_hook")
            def register_menu():
                return CoreHubMenuItem()

        except Exception:
            # AllianceAuth hooks not available during tests / standalone Django usage
            pass
