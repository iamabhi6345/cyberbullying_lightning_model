from pathlib import Path
from typing import TYPE_CHECKING
from omegaconf import OmegaConf
import mlflow

from omegaconf import DictConfig

from cybulde.utils.config_utils import get_config, save_config_as_yaml

from cybulde.utils.mlflow_utils import activate_mlflow

if TYPE_CHECKING:
    from cybulde.config_schemas.config_schema import Config



@get_config(config_path="../configs",config_name="config",to_object=False,return_dict_config=True)
def generate_final_config(config):
    # print(OmegaConf.to_yaml(config))
    # return

    run: mlflow.ActiveRun
    with activate_mlflow(
        config.infrastructure.mlflow.experiment_name,
        run_id=config.infrastructure.mlflow.run_id,
        run_name=config.infrastructure.mlflow.run_name,
    ) as run:
        run_id: str = run.info.run_id
        experiment_id: str = run.info.experiment_id
        artifact_uri: str = run.info.artifact_uri

        config.infrastructure.mlflow.artifact_uri = artifact_uri
        config.infrastructure.mlflow.run_id = run_id
        config.infrastructure.mlflow.experiment_id = experiment_id

        # print("\n\n\n")
        # print(OmegaConf.to_yaml(config))
        # print("\n\n")
#           saving in local disk and in mlflow
        config_save_dir = Path("./cybulde/configs/automatically_generated/")
        config_save_dir.mkdir(parents=True, exist_ok=True)
        (config_save_dir / "__init__.py").touch(exist_ok=True)

        yaml_config_save_path = config_save_dir / "config.yaml"
        save_config_as_yaml(config, str(yaml_config_save_path))
        mlflow.log_artifact(str(yaml_config_save_path))





if __name__ == "__main__":
    generate_final_config()