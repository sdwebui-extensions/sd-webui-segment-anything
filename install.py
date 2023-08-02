import launch
import os
import shutil
try:
    from modules.paths_internal import models_path, shared_models_path
except:
    from modules.paths_internal import models_path 
    shared_models_path = None
from logger import logger

current_dir = os.path.dirname(os.path.realpath(__file__))
req_file = os.path.join(current_dir, "requirements.txt")

with open(req_file) as file:
    for lib in file:
        lib = lib.strip()
        if not launch.is_installed(lib):
            launch.run_pip(
                f"install {lib}",
                f"sd-webui-segment-anything requirement: {lib}")

sam_save_dir = os.path.join(models_path, 'sam')
dino_save_dir = os.path.join(models_path, 'grounding-dino')
os.makedirs(sam_save_dir, exist_ok=True)
os.makedirs(dino_save_dir, exist_ok=True)
shared_sam_models = os.path.join(shared_models_path, 'sam') if shared_models_path else None
shared_dino_models = os.path.join(shared_models_path, 'grounding-dino') if shared_models_path else None
if shared_sam_models and os.path.exists(shared_sam_models) and os.path.isdir(shared_sam_models):
    for pth_file in os.listdir(shared_sam_models):
        if pth_file.endswith('.pth'):
            pth_path = os.path.join(shared_sam_models, pth_file)
            if not os.path.exists(os.path.join(sam_save_dir, pth_path)):
                shutil.copyfile(pth_path, os.path.join(sam_save_dir, pth_path))
                logger.info(f'copy file from {pth_path} to {sam_save_dir}')
if shared_dino_models and os.path.exists(shared_dino_models) and os.path.isdir(shared_dino_models):
    for pth_file in os.listdir(shared_dino_models):
        if pth_file.endswith('.pth'):
            pth_path = os.path.join(shared_dino_models, pth_file)
            if not os.path.exists(os.path.join(dino_save_dir, pth_path)):
                shutil.copyfile(pth_path, os.path.join(dino_save_dir, pth_path))
                logger.info(f'copy file from {pth_path} to {dino_save_dir}')
