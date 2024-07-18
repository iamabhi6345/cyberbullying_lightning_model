from lightning.pytorch import seed_everything
import torch
from omegaconf import OmegaConf
from hydra.utils import instantiate
from cybulde.config_schemas.config_schema import Config
from cybulde.utils.config_utils import get_config
from cybulde.utils.torch_utils import get_local_rank
from cybulde.utils.utils import get_logger

@get_config(config_path="../configs/automatically_generated", config_name="config",to_object=False,return_dict_config=True)
def run_tasks(config: Config) -> None:
    
    # print("\n\n\n")
    # print(OmegaConf.to_yaml(config,resolve =True))
    # print("\n\n")
    # exit(0)
    
    
    logger = get_logger(__file__)  
    assert config.infrastructure.mlflow.run_id is not None, "Run id has to be set for running tasks"
    
    backend = "gloo"  
    if torch.cuda.is_available():
        torch.cuda.set_device(f"cuda:{get_local_rank()}")
        backend = "nccl"  
        
    torch.distributed.init_process_group(backend=backend)  # "distributed" is not a known member of module "torch"
    
    seed_everything(seed=config.seed, workers=True)
    
    for task_name, task_config in config.tasks.items():  # Cannot access member "tasks" for type "Config"
        logger.info(f"Running task: {task_name}")
        task = instantiate(task_config)  # Any
        task.run(config=config, task_config=task_config)
        
if __name__ == "__main__":
    run_tasks()  # type: ignore

    
    













# from lightning.pytorch import seed_everything
# import torch
# from omegaconf import OmegaConf
# from hydra.utils import instantiate
# from cybulde.config_schemas.config_schema import Config
# from cybulde.utils.config_utils import get_config
# from cybulde.utils.torch_utils import get_local_rank
# from cybulde.utils.utils import get_logger

# @get_config(config_path="../configs/automatically_generated", config_name="config", to_object=False, return_dict_config=True)
# def run_tasks(config: Config) -> None:
#     # Debug: Print the loaded configuration
#     # print("Loaded configuration:")
#     # print(OmegaConf.to_yaml(config, resolve=True))

#     logger = get_logger(__file__)
#     assert config.infrastructure.mlflow.run_id is not None, "Run id has to be set for running tasks"

#     # Debug: Verify the task import
#     try:
#         from cybulde.training.tasks.tar_model_exporting_training_task import TarModelExportingTrainingTask
#         print("TarModelExportingTrainingTask successfully imported")
#     except ImportError as e:
#         print(f"Failed to import TarModelExportingTrainingTask: {e}")
#         raise

#     backend = "gloo"
#     if torch.cuda.is_available():
#         torch.cuda.set_device(f"cuda:{get_local_rank()}")
#         backend = "nccl"

#     torch.distributed.init_process_group(backend=backend)

#     seed_everything(seed=config.seed, workers=True)

#     for task_name, task_config in config.tasks.items():
#         logger.info(f"Running task: {task_name}")
#         task = instantiate(task_config)
#         task.run(config=config, task_config=task_config)

# if __name__ == "__main__":
#     import os
#     os.environ["HYDRA_FULL_ERROR"] = "1"
#     run_tasks()
