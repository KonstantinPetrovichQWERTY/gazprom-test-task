from dynaconf import Dynaconf  # type: ignore

settings = Dynaconf(
    settings_files=["settings.toml"], load_dotenv=True, environments=True
)
