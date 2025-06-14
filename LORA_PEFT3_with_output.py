

!git clone https://github.com/AlexKvetka/LORA-PEFT3.git
%cd LORA-PEFT3
# --- output ---
# Cloning into 'LORA-PEFT3'...
# warning: You appear to have cloned an empty repository.
# /content/LORA-PEFT3
# --- end output ---

#@title Установка и инициализация poetry, pre-commit, dvc, hydra, mlflow (Colab)
!pip install poetry==1.8.2 pre-commit==3.7.0 dvc[gs] hydra-core mlflow fire torch torchvision torchaudio transformers peft datasets accelerate --upgrade

# Инициализация poetry (создаст pyproject.toml)
!poetry init --no-interaction --name legal_lora --dependency torch --dependency transformers --dependency peft --dependency datasets --dependency accelerate --dependency mlflow --dependency hydra-core --dependency fire

# pre-commit
!pre-commit sample-config > .pre-commit-config.yaml
!pre-commit install

# dvc
!dvc init --no-scm

# .gitignore
!curl -L https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore -o .gitignore

# Hydra (создание папки для конфигов)
!mkdir -p configs

# MLflow (создание папки для логов и графиков)
!mkdir -p mlruns plots

# poetry lock
!poetry lock
# --- output ---
# Collecting poetry==1.8.2
#   Downloading poetry-1.8.2-py3-none-any.whl.metadata (6.8 kB)
# Collecting pre-commit==3.7.0
#   Downloading pre_commit-3.7.0-py2.py3-none-any.whl.metadata (1.3 kB)
# Collecting hydra-core
# --- end output ---
# --- output ---
# Using version [39;1m^2.7.1[39;22m for [36mtorch[39m
# Using version [39;1m^4.52.4[39;22m for [36mtransformers[39m
# Using version [39;1m^0.15.2[39;22m for [36mpeft[39m
# Using version [39;1m^3.6.0[39;22m for [36mdatasets[39m
# Using version [39;1m^1.7.0[39;22m for [36maccelerate[39m
# Using version [39;1m^3.1.0[39;22m for [36mmlflow[39m
# Using version [39;1m^1.3.2[39;22m for [36mhydra-core[39m
# Using version [39;1m^0.7.0[39;22m for [36mfire[39m
# pre-commit installed at .git/hooks/pre-commit
# Initialized DVC repository.
# 
# [31m+---------------------------------------------------------------------+
# [0m[31m|[0m                                                                     [31m|[0m
# [31m|[0m        DVC has enabled anonymous aggregate usage analytics.         [31m|[0m
# [31m|[0m     Read the analytics documentation (and how to opt-out) here:     [31m|[0m
# [31m|[0m             <[36mhttps://dvc.org/doc/user-guide/analytics[39m>              [31m|[0m
# [31m|[0m                                                                     [31m|[0m
# [31m+---------------------------------------------------------------------+
# [0m
# [33mWhat's next?[39m
# [33m------------[39m
# - Check out the documentation: <[36mhttps://dvc.org/doc[39m>
# - Get help and share ideas: <[36mhttps://dvc.org/chat[39m>
# - Star us on GitHub: <[36mhttps://github.com/iterative/dvc[39m>
# [0m  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
#                                  Dload  Upload   Total   Spent    Left  Speed
# 100  4333  100  4333    0     0  11975      0 --:--:-- --:--:-- --:--:-- 12002
# Creating virtualenv [36mlegal-lora-098Tz1eW-py3.11[39m in /root/.cache/pypoetry/virtualenvs
# [34mUpdating dependencies[39m
# [2K[34mResolving dependencies...[39m [39;2m(6.5s)[39;22m
# ^C
# --- end output ---


# --- output ---
# /content/LORA-PEFT3
# configs  mlruns  plots	pyproject.toml
# --- end output ---

#@title [FIX] Корректный пуш в main с учётом pre-commit
%cd /content/LORA-PEFT3

# Добавим снова .gitignore, если он изменился pre-commit'ом
!git add .gitignore

# Добавим все остальные файлы
!git add .

# Делаем первый коммит (если еще не было)
!git commit -m "init: add poetry, pre-commit, dvc, hydra, mlflow, .gitignore" || echo "Commit already exists or nothing to commit"

# Создаем main, если еще не было
!git branch -M main

# Устанавливаем правильный origin (если еще не установлен)
!git remote set-url origin https://AlexKvetka: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@github.com/AlexKvetka/LORA-PEFT3.git

# Пушим main
!git push -u origin main
# --- output ---
# /content/LORA-PEFT3
# Trim Trailing Whitespace.................................................[42mPassed[m
# Fix End of Files.........................................................[42mPassed[m
# Check Yaml...............................................................[42mPassed[m
# Check for added large files..............................................[42mPassed[m
# [main (root-commit) 541984b] init: add poetry, pre-commit, dvc, hydra, mlflow, .gitignore
#  6 files changed, 232 insertions(+)
#  create mode 100644 .dvc/config
#  create mode 100644 .dvc/tmp/btime
#  create mode 100644 .dvcignore
#  create mode 100644 .gitignore
#  create mode 100644 .pre-commit-config.yaml
#  create mode 100644 pyproject.toml
# Enumerating objects: 10, done.
# Counting objects: 100% (10/10), done.
# Delta compression using up to 2 threads
# Compressing objects: 100% (7/7), done.
# Writing objects: 100% (10/10), 2.87 KiB | 2.87 MiB/s, done.
# Total 10 (delta 0), reused 0 (delta 0), pack-reused 0
# To https://github.com/AlexKvetka/LORA-PEFT3.git
#  * [new branch]      main -> main
# Branch 'main' set up to track remote branch 'main' from 'origin'.
# --- end output ---

#@title Настройка DVC remote на Google Drive и push датасета

# 1. Подключаем Google Drive
from google.colab import drive
drive.mount('/content/drive')

# 2. Добавляем remote для DVC (замени путь, если хочешь другую папку)
!dvc remote add -d gdrive_remote gdrive://root/LORA-PEFT3_DVC
!dvc remote modify gdrive_remote gdrive_use_service_account false

# 3. Push данных в remote
!dvc push
# --- output ---
# Drive already mounted at /content/drive; to attempt to forcibly remount, call drive.mount("/content/drive", force_remount=True).
# Setting 'gdrive_remote' as a default remote.
# [31mERROR[39m: configuration error - config file error: remote 'gdrive_remote' already exists. Use `-f|--force` to overwrite it.
# [31mERROR[39m: unexpected error - gdrive is supported, but requires 'dvc-gdrive' to be installed: No module named 'dvc_gdrive'
# 
# [33mHaving any troubles?[0m Hit us up at [34mhttps://dvc.org/support[0m, we are always happy to help!
# [0m
# --- end output ---

#@title [FIX] DVC Google Drive remote в Colab (установи dvc-gdrive и force-remote)
# Устанавливаем модуль dvc-gdrive
!pip install dvc-gdrive --upgrade

# Добавляем (или перезаписываем) remote с флагом -f, если уже был
!dvc remote add -f -d gdrive_remote gdrive://root/LORA-PEFT3_DVC
!dvc remote modify gdrive_remote gdrive_use_service_account false

# Пушим данные в remote
!dvc push
# --- output ---
# Collecting dvc-gdrive
#   Downloading dvc_gdrive-3.0.1-py3-none-any.whl.metadata (2.1 kB)

# Downloading dvc_gdrive-3.0.1-py3-none-any.whl (11 kB)
# Installing collected packages: dvc-gdrive
# Successfully installed dvc-gdrive-3.0.1
# Setting 'gdrive_remote' as a default remote.
# Collecting          |1.00 [00:00,  153entry/s]
# Pushing
# ![A
#   0% |          |0/? [00:00<?,    ?files/s][A/usr/local/lib/python3.11/dist-packages/oauth2client/_helpers.py:255: UserWarning: Cannot access /root/.cache/pydrive2fs/710796635688-iivsgbgsb6uv1fap6635dhvuei09o66c.apps.googleusercontent.com/default.json: No such file or directory
#   warnings.warn(_MISSING_FILE_MESSAGE.format(filename))
# Your browser has been opened to visit:
# 
#     https://accounts.google.com/o/oauth2/auth?client_id=710796635688-iivsgbgsb6uv1fap6635dhvuei09o66c.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A8090%2F&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive.appdata&access_type=offline&response_type=code&approval_prompt=force
# 
# 
# Pushing
# [31mERROR[39m: interrupted by the user
# [0m
# --- end output ---

#@title Создай пакет legal_lora с CLI (замени legal_lora на своё название, если проект называется иначе)
!mkdir -p legal_lora
with open("legal_lora/__init__.py", "w"): pass

with open("legal_lora/commands.py", "w") as f:
    f.write("""
import fire
from legal_lora.train import train_lora
from legal_lora.infer import infer_lora

def main():
    fire.Fire({
        'train': train_lora,
        'infer': infer_lora,
    })

if __name__ == '__main__':
    main()
""")
!touch legal_lora/train.py legal_lora/infer.py

!git add legal_lora/
!git commit -m "feat: add package skeleton with CLI"
!git push
# --- output ---
# [43;30m[WARNING][m Unstaged files detected.
# [INFO][m Stashing unstaged files to /root/.cache/pre-commit/patch1749819707-16053.
# Trim Trailing Whitespace.................................................[42mPassed[m
# Fix End of Files.........................................................[42mPassed[m
# Check Yaml...........................................(no files to check)[46;30mSkipped[m
# Check for added large files..............................................[42mPassed[m
# [INFO][m Restored changes from /root/.cache/pre-commit/patch1749819707-16053.
# [main 6725328] feat: add package skeleton with CLI
#  4 files changed, 13 insertions(+)
#  create mode 100644 legal_lora/__init__.py
#  create mode 100644 legal_lora/commands.py
#  create mode 100644 legal_lora/infer.py
#  create mode 100644 legal_lora/train.py
# Enumerating objects: 6, done.
# Counting objects: 100% (6/6), done.
# Delta compression using up to 2 threads
# Compressing objects: 100% (4/4), done.
# Writing objects: 100% (5/5), 534 bytes | 534.00 KiB/s, done.
# Total 5 (delta 1), reused 0 (delta 0), pack-reused 0
# remote: Resolving deltas: 100% (1/1), completed with 1 local object.[K
# To https://github.com/AlexKvetka/LORA-PEFT3.git
#    ab2e895..6725328  main -> main
# --- end output ---

%%bash
git add .dvc/config
git commit -m "fix: update DVC config (remote or other changes)"
git push
# --- output ---
# [main 190fff5] fix: update DVC config (remote or other changes)
#  1 file changed, 4 insertions(+)
# --- end output ---
# --- output ---
# Trim Trailing Whitespace.................................................Passed
# Fix End of Files.........................................................Passed
# Check Yaml...........................................(no files to check)Skipped
# Check for added large files..............................................Passed
# To https://github.com/AlexKvetka/LORA-PEFT3.git
#    6725328..190fff5  main -> main
# --- end output ---


!git add legal_lora/train.py legal_lora/infer.py legal_lora/commands.py
!git commit -m "feat: add training and inference for LoRA GPT2 small"
!git push
# --- output ---
# Trim Trailing Whitespace.................................................[42mPassed[m
# Fix End of Files.........................................................[41mFailed[m
# [2m- hook id: end-of-file-fixer[m
# [2m- exit code: 1[m
# [2m- files were modified by this hook[m
# 
# Fixing legal_lora/infer.py
# Fixing legal_lora/train.py
# 
# Check Yaml...........................................(no files to check)[46;30mSkipped[m
# Check for added large files..............................................[42mPassed[m
# Everything up-to-date
# --- end output ---

AGAIN PREVIOUS
# %%bash
# git add legal_lora/infer.py legal_lora/train.py
# git commit -m "style: fix EOF and trailing whitespace (pre-commit)"
# git push
# --- output ---
# [main cbe4b1e] style: fix EOF and trailing whitespace (pre-commit)
#  2 files changed, 52 insertions(+)
# --- end output ---
# --- output ---
# Trim Trailing Whitespace.................................................Passed
# Fix End of Files.........................................................Passed
# Check Yaml...........................................(no files to check)Skipped
# Check for added large files..............................................Passed
# To https://github.com/AlexKvetka/LORA-PEFT3.git
#    190fff5..cbe4b1e  main -> main
# --- end output ---

!git add configs/
!git commit -m "chore: add hydra config for training"
!git push
# --- output ---
# Trim Trailing Whitespace.................................................[42mPassed[m
# Fix End of Files.........................................................[42mPassed[m
# Check Yaml...............................................................[42mPassed[m
# Check for added large files..............................................[42mPassed[m
# [main 93d6d68] chore: add hydra config for training
#  1 file changed, 14 insertions(+)
#  create mode 100644 configs/train.yaml
# Enumerating objects: 5, done.
# Counting objects: 100% (5/5), done.
# Delta compression using up to 2 threads
# Compressing objects: 100% (3/3), done.
# Writing objects: 100% (4/4), 540 bytes | 540.00 KiB/s, done.
# Total 4 (delta 1), reused 0 (delta 0), pack-reused 0
# remote: Resolving deltas: 100% (1/1), completed with 1 local object.[K
# To https://github.com/AlexKvetka/LORA-PEFT3.git
#    cbe4b1e..93d6d68  main -> main
# --- end output ---

AGAIN PREVIOUS

#@title Запуск обучения через CLI
!poetry run python -m legal_lora.commands train --config_path=configs/train.yaml
# --- output ---
# Traceback (most recent call last):
#   File "<frozen runpy>", line 198, in _run_module_as_main
#   File "<frozen runpy>", line 88, in _run_code
#   File "/content/LORA-PEFT3/legal_lora/commands.py", line 2, in <module>
#     import fire
# ModuleNotFoundError: No module named 'fire'
# --- end output ---

!poetry add fire
# --- output ---
# The following packages are already present in the pyproject.toml and will be skipped:
# 
#   - [36mfire[39m
# 
# If you want to update it to the latest compatible version, you can use `poetry update package`.
# If you prefer to upgrade it to the latest available version, you can use `poetry add package@latest`.
# 
# Nothing to add.
# --- end output ---

!poetry run python -m legal_lora.commands train --config_path=configs/train.yaml
# --- output ---
# Traceback (most recent call last):
#   File "<frozen runpy>", line 198, in _run_module_as_main
#   File "<frozen runpy>", line 88, in _run_code
#   File "/content/LORA-PEFT3/legal_lora/commands.py", line 2, in <module>
#     import fire
# ModuleNotFoundError: No module named 'fire'
# --- end output ---


# --- output ---
#  [34mname[39m         : [36mfire[39m                                                            
#  [34mversion[39m      : [39;1m0.7.0[39;22m                                                           
#  [34mdescription[39m  : A library for automatically generating command line interfaces. 
# 
# [34mdependencies[39m
#  - [36mtermcolor[39m [39;1m*[39;22m
# --- end output ---

!poetry lock
# --- output ---
# [34mUpdating dependencies[39m
# [2K[34mResolving dependencies...[39m [39;2m(17.7s)[39;22m
# 
# [34mWriting lock file[39m
# --- end output ---

!poetry show fire

!poetry install
# --- output ---
# --- end output ---

import mlflow

# Force MLflow to log locally in Colab/CLI
mlflow.set_tracking_uri("file:/content/mlruns")

def train_lora(config_path="configs/train.yaml"):
    import time

    print(f"Using config: {config_path}")

    with mlflow.start_run(run_name="my_run"):
        print("Training started...")
        for step in range(3):
            metric_value = step * 2
            mlflow.log_metric("dummy_metric", metric_value, step=step)
            print(f"Step {step}: dummy_metric={metric_value}")
            time.sleep(1)
        print("Training finished!")

if __name__ == "__main__":
    import fire
    fire.Fire(train_lora)
# --- output ---
# Using config: configs/train.yaml
# Training started...
# Step 0: dummy_metric=0
# Step 1: dummy_metric=2
# Step 2: dummy_metric=4
# Training finished!
# --- end output ---
# --- output ---
# ERROR: Could not consume arg: -f
# Usage: colab_kernel_launcher.py -
# 
# For detailed information on this command, run:
#   colab_kernel_launcher.py - --help
# --- end output ---
# --- output ---
# /usr/local/lib/python3.11/dist-packages/IPython/core/interactiveshell.py:3561: UserWarning: To exit: use 'exit', 'quit', or Ctrl-D.
#   warn("To exit: use 'exit', 'quit', or Ctrl-D.", stacklevel=1)
# --- end output ---

%tb

import mlflow

# Set MLflow tracking URI to a local directory (for Colab/Jupyter)
mlflow.set_tracking_uri("file:/content/mlruns")

def train_lora(config_path="configs/train.yaml"):
    import time

    print(f"Using config: {config_path}")

    with mlflow.start_run(run_name="my_run"):
        print("Training started...")
        for step in range(3):
            metric_value = step * 2
            mlflow.log_metric("dummy_metric", metric_value, step=step)
            print(f"Step {step}: dummy_metric={metric_value}")
            time.sleep(1)
        print("Training finished!")

# Call the function directly (no Fire in notebook!)
train_lora("configs/train.yaml")
# --- output ---
# Using config: configs/train.yaml
# Training started...
# Step 0: dummy_metric=0
# Step 1: dummy_metric=2
# Step 2: dummy_metric=4
# Training finished!
# --- end output ---

!poetry run python -m legal_lora.commands train --config_path=configs/train.yaml
# --- output ---
# Traceback (most recent call last):
#   File "<frozen runpy>", line 198, in _run_module_as_main
#   File "<frozen runpy>", line 88, in _run_code
#   File "/content/LORA-PEFT3/legal_lora/commands.py", line 13, in <module>
#     main()
#   File "/content/LORA-PEFT3/legal_lora/commands.py", line 7, in main
#     fire.Fire({
#   File "/root/.cache/pypoetry/virtualenvs/legal-lora-098Tz1eW-py3.11/lib/python3.11/site-packages/fire/core.py", line 135, in Fire
#     component_trace = _Fire(component, args, parsed_flag_args, context, name)
#                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/root/.cache/pypoetry/virtualenvs/legal-lora-098Tz1eW-py3.11/lib/python3.11/site-packages/fire/core.py", line 468, in _Fire
#     component, remaining_args = _CallAndUpdateTrace(
#                                 ^^^^^^^^^^^^^^^^^^^^
#   File "/root/.cache/pypoetry/virtualenvs/legal-lora-098Tz1eW-py3.11/lib/python3.11/site-packages/fire/core.py", line 684, in _CallAndUpdateTrace
#     component = fn(*varargs, **kwargs)
#                 ^^^^^^^^^^^^^^^^^^^^^^
#   File "/content/LORA-PEFT3/legal_lora/train.py", line 14, in train_lora
#     mlflow.start_run(run_name=config.run_name)
#   File "/root/.cache/pypoetry/virtualenvs/legal-lora-098Tz1eW-py3.11/lib/python3.11/site-packages/mlflow/tracking/fluent.py", line 474, in start_run
#     active_run_obj = client.create_run(
#                      ^^^^^^^^^^^^^^^^^^
#   File "/root/.cache/pypoetry/virtualenvs/legal-lora-098Tz1eW-py3.11/lib/python3.11/site-packages/mlflow/tracking/client.py", line 434, in create_run
#     return self._tracking_client.create_run(experiment_id, start_time, tags, run_name)
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/root/.cache/pypoetry/virtualenvs/legal-lora-098Tz1eW-py3.11/lib/python3.11/site-packages/mlflow/tracking/_tracking_service/client.py", line 161, in create_run
#     return self.store.create_run(
#            ^^^^^^^^^^^^^^^^^^^^^^
#   File "/root/.cache/pypoetry/virtualenvs/legal-lora-098Tz1eW-py3.11/lib/python3.11/site-packages/mlflow/store/tracking/rest_store.py", line 272, in create_run
#     response_proto = self._call_endpoint(CreateRun, req_body)
#                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/root/.cache/pypoetry/virtualenvs/legal-lora-098Tz1eW-py3.11/lib/python3.11/site-packages/mlflow/store/tracking/rest_store.py", line 135, in _call_endpoint
#     return call_endpoint(
#            ^^^^^^^^^^^^^^
#   File "/root/.cache/pypoetry/virtualenvs/legal-lora-098Tz1eW-py3.11/lib/python3.11/site-packages/mlflow/utils/rest_utils.py", line 590, in call_endpoint
#     response = verify_rest_response(response, endpoint)
#                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/root/.cache/pypoetry/virtualenvs/legal-lora-098Tz1eW-py3.11/lib/python3.11/site-packages/mlflow/utils/rest_utils.py", line 310, in verify_rest_response
#     raise MlflowException(
# mlflow.exceptions.MlflowException: API request to endpoint /api/2.0/mlflow/runs/create failed with error code 404 != 200. Response body: '<!DOCTYPE HTML>
# <html>
# 
# <head>
#     <meta charset="utf-8">
# 
#     <title>Jupyter Notebook</title>
#     <link id="favicon" rel="shortcut icon" type="image/x-icon" href="/static/base/images/favicon.ico?v=50afa725b5de8b00030139d09b38620224d4e7dba47c07ef0e86d4643f30c9bfe6bb7e1a4a1c561aa32834480909a4b6fe7cd1e17f7159330b6b5914bf45a880">
#     <meta http-equiv="X-UA-Compatible" content="IE=edge" />
#     <link rel="stylesheet" href="/static/components/jquery-ui/dist/themes/smoothness/jquery-ui.min.css?v=aeef962be7038761e5174f91e2da776c640f789e9802621178606b759506b273d9a97f189a9262b19ac5b511f70a662d8c5e2bf2fb258ae11c3c2ee1e07c6abd" type="text/css" />
#     <link rel="stylesheet" href="/static/components/jquery-typeahead/dist/jquery.typeahead.min.css?v=50abc9f0658dec7488e352b71947dc2489e08553a12a2ff0d292cd57fe65625b8b5b52193ee5eed003421626dd7e9e52018d822f4719b7ab98a2cf18aaf575ff" type="text/css" />
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     
#     
# 
#     <link rel="stylesheet" href="/static/style/style.min.css?v=ab20bf23735ed95633181baa473ff63bf281ceae470407c656e482a618d77c9e951a8c0ada6f3b3d02d054a481fb35aad852781d72a2fc5dd0bb174f0cf27381" type="text/css"/>
#     
# <style type="text/css">
# /* disable initial hide */
# div#header, div#site {
#     display: block;
# }
# </style>
# 
#     <link rel="stylesheet" href="/custom/custom.css" type="text/css" />
#     <script src="/static/components/es6-promise/promise.min.js?v=bea335d74136a63ae1b5130f5ac9a50c6256a5f435e6e09fef599491a84d834a8b0f011ca3eaaca3b4ab6a2da2d3e1191567a2f171e60da1d10e5b9d52f84184" type="text/javascript" charset="utf-8"></script>
#     <script src="/static/components/react/react.production.min.js?v=9a0aaf84a316c8bedd6c2ff7d5b5e0a13f8f84ec02442346cba0b842c6c81a6bf6176e64f3675c2ebf357cb5bb048e0b527bd39377c95681d22468da3d5de735" type="text/javascript"></script>
#     <script src="/static/components/react/react-dom.production.min.js?v=6fc58c1c4736868ff84f57bd8b85f2bdb985993a9392718f3b4af4bfa10fb4efba2b4ddd68644bd2a8daf0619a3844944c9c43f8528364a1aa6fc01ec1b8ae84" type="text/javascript"></script>
#     <script src="/static/components/create-react-class/index.js?v=894ad57246e682b4cfbe7cd5e408dcd6b38d06af4de4f3425991e2676fdc2ef1732cbd19903104198878ae77de12a1996de3e7da3a467fb226bdda8f4618faec" type="text/javascript"></script>
#     <script src="/static/components/requirejs/require.js?v=d37b48bb2137faa0ab98157e240c084dd5b1b5e74911723aa1d1f04c928c2a03dedf922d049e4815f7e5a369faa2e6b6a1000aae958b7953b5cc60411154f593" type="text/javascript" charset="utf-8"></script>
#     <script>
#       require.config({
#           
#           urlArgs: "v=20250613120228",
#           
#           baseUrl: '/static/',
#           paths: {
#             'auth/js/main': 'auth/js/main.min',
#             custom : '/custom',
#             nbextensions : '/nbextensions',
#             kernelspecs : '/kernelspecs',
#             underscore : 'components/underscore/underscore-min',
#             backbone : 'components/backbone/backbone-min',
#             jed: 'components/jed/jed',
#             jquery: 'components/jquery/jquery.min',
#             json: 'components/requirejs-plugins/src/json',
#             text: 'components/requirejs-text/text',
#             bootstrap: 'components/bootstrap/dist/js/bootstrap.min',
#             bootstraptour: 'components/bootstrap-tour/build/js/bootstrap-tour.min',
#             'jquery-ui': 'components/jquery-ui/dist/jquery-ui.min',
#             moment: 'components/moment/min/moment-with-locales',
#             codemirror: 'components/codemirror',
#             termjs: 'components/xterm.js/xterm',
#             typeahead: 'components/jquery-typeahead/dist/jquery.typeahead.min',
#           },
#           map: { // for backward compatibility
#               "*": {
#                   "jqueryui": "jquery-ui",
#               }
#           },
#           shim: {
#             typeahead: {
#               deps: ["jquery"],
#               exports: "typeahead"
#             },
#             underscore: {
#               exports: '_'
#             },
#             backbone: {
#               deps: ["underscore", "jquery"],
#               exports: "Backbone"
#             },
#             bootstrap: {
#               deps: ["jquery"],
#               exports: "bootstrap"
#             },
#             bootstraptour: {
#               deps: ["bootstrap"],
#               exports: "Tour"
#             },
#             "jquery-ui": {
#               deps: ["jquery"],
#               exports: "$"
#             }
#           },
#           waitSeconds: 30,
#       });
# 
#       require.config({
#           map: {
#               '*':{
#                 'contents': 'services/contents',
#               }
#           }
#       });
# 
#       // error-catching custom.js shim.
#       define("custom", function (require, exports, module) {
#           try {
#               var custom = require('custom/custom');
#               console.debug('loaded custom.js');
#               return custom;
#           } catch (e) {
#               console.error("error loading custom.js", e);
#               return {};
#           }
#       })
# 
#       // error-catching custom-preload.js shim.
#       define("custom-preload", function (require, exports, module) {
#           try {
#               var custom = require('custom/custom-preload');
#               console.debug('loaded custom-preload.js');
#               return custom;
#           } catch (e) {
#               console.error("error loading custom-preload.js", e);
#               return {};
#           }
#       })
# 
#     document.nbjs_translations = {"domain": "nbjs", "locale_data": {"nbjs": {"": {"domain": "nbjs"}}}};
#     document.documentElement.lang = navigator.language.toLowerCase();
#     </script>
# 
#     
#     
# 
# </head>
# 
# <body class=""
#  
#   
#  
# dir="ltr">
# 
# <noscript>
#     <div id='noscript'>
#       Jupyter Notebook requires JavaScript.<br>
#       Please enable it to proceed. 
#   </div>
# </noscript>
# 
# <div id="header" role="navigation" aria-label="Top Menu">
#   <div  id="newsId" style="display: none">
#     
#     <div class="alert alert-info" role="alert">
#       <div style="display: flex">
#         <div>
#           <span class="label label-warning">UPDATE</span>
#           Read <a href="https://jupyter-notebook.readthedocs.io/en/latest/migrate_to_notebook7.html" style="text-decoration: underline;" target="_blank">the migration plan</a> to Notebook 7 to learn about the new features and the actions to take if you are using extensions
#           -
#           Please note that updating to Notebook 7 might break some of your extensions.
#         </div>
#         <div style="margin-left: auto;">
#           <a href="" onclick="alert('This message will not be shown anymore.'); return false;">
#             <button type="button" class="btn btn-default btn-xs" id="dontShowId">
#               Don't show anymore
#             </button>
#           </a>
#         </div>
#       </div>
#     </div>
#     
#   </div>
#   <div id="header-container" class="container">
#   <div id="ipython_notebook" class="nav navbar-brand"><a href="/tree" title='dashboard'>
#       <img src='/static/base/images/logo.png?v=a2a176ee3cee251ffddf5fa21fe8e43727a9e5f87a06f9c91ad7b776d9e9d3d5e0159c16cc188a3965e00375fb4bc336c16067c688f5040c0c2d4bfdb852a9e4' alt='Jupyter Notebook'/>
#   </a></div>
# 
#   
#   
#   
#   
#   
#   
# 
# 
#   
#   
#   </div>
#   <div class="header-bar"></div>
# 
#   
#   
# </div>
# 
# <div id="site">
# 
# 
# <div class="error">
#     
#     <h1>404 : Not Found</h1>
#     
#     
# <p>You are requesting a page that does not exist!</p>
# 
# </div>
# 
# 
# </div>
# 
# 
# 
# 
# 
# 
# 
# <script type='text/javascript'>
# require(['jquery'], function($) {
#   // scroll long tracebacks to the bottom
#   var tb = $(".traceback")[0];
#   tb.scrollTop = tb.scrollHeight;
# });
# </script>
# 
# 
# <script type='text/javascript'>
#   function _remove_token_from_url() {
#     if (window.location.search.length <= 1) {
#       return;
#     }
#     var search_parameters = window.location.search.slice(1).split('&');
#     for (var i = 0; i < search_parameters.length; i++) {
#       if (search_parameters[i].split('=')[0] === 'token') {
#         // remote token from search parameters
#         search_parameters.splice(i, 1);
#         var new_search = '';
#         if (search_parameters.length) {
#           new_search = '?' + search_parameters.join('&');
#         }
#         var new_url = window.location.origin + 
#                       window.location.pathname + 
#                       new_search + 
#                       window.location.hash;
#         window.history.replaceState({}, "", new_url);
#         return;
#       }
#     }
#   }
#   _remove_token_from_url();
#   sys_info = {"notebook_version": "6.5.7", "notebook_path": "/usr/local/lib/python3.11/dist-packages/notebook", "commit_source": "", "commit_hash": "", "sys_version": "3.11.13 (main, Jun  4 2025, 08:57:29) [GCC 11.4.0]", "sys_executable": "/usr/bin/python3", "sys_platform": "linux", "platform": "Linux-6.1.123+-x86_64-with-glibc2.35", "os_name": "posix", "default_encoding": "utf-8"};
#   document.addEventListener('DOMContentLoaded', function () {
#     const newsId = document.querySelector('#newsId');
#     const dontShowId = document.querySelector('#dontShowId');
#     const showNotebookNews = localStorage.getItem('showNotebookNews');
#     dontShowId.addEventListener('click', () => {
#       localStorage.setItem('showNotebookNews', false);
#       newsId.style.display = 'none';
#     });
#     if (!showNotebookNews) newsId.style.display = 'inline';
#   });
# </script>
# </body>
# 
# </html>'
# --- end output ---

# 1. Install dependencies
!pip install mlflow pyngrok --quiet

# 2. Add your ngrok auth token here
NGROK_AUTH_TOKEN = "2wx6FxSxSW1miItHAvwaBhtmUuD_5HLV8pZtrURFditdAw2vZ"  # <-- paste your token

# 3. Start MLflow UI in the background
!mlflow ui --backend-store-uri file:/content/mlruns --port 5000 --host 0.0.0.0 &

# 4. Start ngrok tunnel and print the public URL
from pyngrok import ngrok

ngrok.set_auth_token(NGROK_AUTH_TOKEN)
public_url = ngrok.connect(5000)
print("MLflow UI is live at:", public_url)
# --- output ---
# [2025-06-13 13:45:22 +0000] [27787] [INFO] Starting gunicorn 23.0.0
# [2025-06-13 13:45:22 +0000] [27787] [ERROR] Connection in use: ('0.0.0.0', 5000)
# [2025-06-13 13:45:22 +0000] [27787] [ERROR] connection to ('0.0.0.0', 5000) failed: [Errno 98] Address already in use
# [2025-06-13 13:45:23 +0000] [27787] [ERROR] Connection in use: ('0.0.0.0', 5000)
# [2025-06-13 13:45:23 +0000] [27787] [ERROR] connection to ('0.0.0.0', 5000) failed: [Errno 98] Address already in use
# [2025-06-13 13:45:24 +0000] [27787] [ERROR] Connection in use: ('0.0.0.0', 5000)
# [2025-06-13 13:45:24 +0000] [27787] [ERROR] connection to ('0.0.0.0', 5000) failed: [Errno 98] Address already in use
# [2025-06-13 13:45:25 +0000] [27787] [ERROR] Connection in use: ('0.0.0.0', 5000)
# [2025-06-13 13:45:25 +0000] [27787] [ERROR] connection to ('0.0.0.0', 5000) failed: [Errno 98] Address already in use
# [2025-06-13 13:45:26 +0000] [27787] [ERROR] Connection in use: ('0.0.0.0', 5000)
# [2025-06-13 13:45:26 +0000] [27787] [ERROR] connection to ('0.0.0.0', 5000) failed: [Errno 98] Address already in use
# [2025-06-13 13:45:27 +0000] [27787] [ERROR] Can't connect to ('0.0.0.0', 5000)
# Running the mlflow server failed. Please see the logs above for details.
# MLflow UI is live at: NgrokTunnel: "https://6569-34-142-129-109.ngrok-free.app" -> "http://localhost:5000"
# --- end output ---

# Kill all ngrok processes in Colab/Jupyter
import os
os.system('pkill -f ngrok')
# --- output ---
# 15
# --- end output ---

# Install MLflow and pyngrok
!pip install mlflow pyngrok --quiet

import mlflow

project_dir = '/content/LORA-PEFT3'  # Set this to your actual project directory

os.chdir(project_dir)
mlflow.set_tracking_uri("file:mlruns")

# Prompt for ngrok token
import getpass
NGROK_AUTH_TOKEN = "2wx6FxSxSW1miItHAvwaBhtmUuD_5HLV8pZtrURFditdAw2vZ"

# Start MLflow UI in the background
import os
os.system("mlflow ui --backend-store-uri file:/content/mlruns --port 5000 --host 0.0.0.0 &")

# Start ngrok and print the public URL
import time
from pyngrok import ngrok

time.sleep(10)  # Wait for MLflow UI to start

ngrok.set_auth_token(NGROK_AUTH_TOKEN)
public_url = ngrok.connect(5000)
print("MLflow UI is live at:", public_url)
# --- output ---
# MLflow UI is live at: NgrokTunnel: "https://62fa-34-142-129-109.ngrok-free.app" -> "http://localhost:5000"
# --- end output ---

import mlflow
import os

print("Current working directory:", os.getcwd())
print("MLflow tracking URI:", mlflow.get_tracking_uri())

# List all mlruns folders in current and parent dirs
for root, dirs, files in os.walk("/content"):
    if "mlruns" in dirs:
        print("Found mlruns folder at:", os.path.join(root, "mlruns"))
# --- output ---
# Current working directory: /content/LORA-PEFT3
# MLflow tracking URI: file:mlruns
# Found mlruns folder at: /content/mlruns
# Found mlruns folder at: /content/LORA-PEFT3/mlruns
# --- end output ---

import shutil

# Delete the old mlruns folder outside your project
shutil.rmtree("/content/mlruns", ignore_errors=True)
print("Old /content/mlruns folder has been deleted.")

# (Optional) You can also delete other unwanted mlruns in other locations if you find them.
# --- output ---
# Old /content/mlruns folder has been deleted.
# --- end output ---

!ls ..
# --- output ---
# drive  LORA-PEFT3
# --- end output ---

# Kill all ngrok processes in Colab/Jupyter
import os
os.system('pkill -f ngrok')
# --- output ---
# 15
# --- end output ---

# 1. Install dependencies
!pip install mlflow pyngrok --quiet
NGROK_AUTH_TOKEN = "2wx6FxSxSW1miItHAvwaBhtmUuD_5HLV8pZtrURFditdAw2vZ"

# 2. Set project directory and MLflow tracking URI
import os
import mlflow

project_dir = '/content/LORA-PEFT3'  # Change if your project dir is different
os.chdir(project_dir)
mlflow.set_tracking_uri("file:mlruns")
print("Working directory:", os.getcwd())
print("Tracking URI:", mlflow.get_tracking_uri())

# 3. Start MLflow UI in the background
os.system("mlflow ui --backend-store-uri file:mlruns --port 5000 --host 0.0.0.0 &")

# 4. Start ngrok and print the public URL
import time
from pyngrok import ngrok

time.sleep(10)  # Give MLflow UI time to start
ngrok.set_auth_token(NGROK_AUTH_TOKEN)  # <-- put your token here
public_url = ngrok.connect(5000)
print("MLflow UI is live at:", public_url)
# --- output ---
# Working directory: /content/LORA-PEFT3
# Tracking URI: file:mlruns
# MLflow UI is live at: NgrokTunnel: "https://1f3c-34-142-129-109.ngrok-free.app" -> "http://localhost:5000"
# --- end output ---

!poetry run python -m legal_lora.commands train --config_path=configs/train.yaml
# --- output ---
# /root/.cache/pypoetry/virtualenvs/legal-lora-098Tz1eW-py3.11/lib/python3.11/site-packages/peft/tuners/lora/layer.py:1768: UserWarning: fan_in_fan_out is set to False but the target module is `Conv1D`. Setting fan_in_fan_out to True.
#   warnings.warn(
# No label_names provided for model class `PeftModelForCausalLM`. Since `PeftModel` hides base models input arguments, if label_names is not given, label_names can't be set automatically within `Trainer`. Note that empty label_names list will be used instead.
#   0% 0/27500 [00:00<?, ?it/s]2025/06/13 15:42:45 ERROR mlflow.utils.async_logging.async_logging_queue: Run Id efc541cd814c42d68f7c2168dd0d5918: Failed to log run data: Exception: Changing param values is not allowed. Param with key='max_length' was already logged with value='256' for run ID='efc541cd814c42d68f7c2168dd0d5918'. Attempted logging new value '20'.
# 2025/06/13 15:42:45 ERROR mlflow.utils.async_logging.async_logging_queue: Run Id efc541cd814c42d68f7c2168dd0d5918: Failed to log run data: Exception: Changing param values is not allowed. Param with key='run_name' was already logged with value='lora-gpt2-legal' for run ID='efc541cd814c42d68f7c2168dd0d5918'. Attempted logging new value 'outputs/lora'.
# `loss_type=None` was set in the config but it is unrecognised.Using the default loss: `ForCausalLMLoss`.
# {'loss': 3.5131, 'grad_norm': 0.7613983154296875, 'learning_rate': 5e-05, 'epoch': 0.0}
...
# {'loss': 1.7134, 'grad_norm': 3.5979650020599365, 'learning_rate': 2.2745454545454544e-06, 'epoch': 0.95}
#  96% 26288/27500 [47:00<02:11,  9.19it/s]
# --- end output ---



%%bash
# ===== 1. Создаём структуру каталогов =====
mkdir -p legal_lora
mkdir -p configs

# ===== 2. legal_lora/__init__.py =====
cat > legal_lora/__init__.py << 'EOF'
# пустой файл для обозначения пакета
EOF

# ===== 3. legal_lora/commands.py =====
cat > legal_lora/commands.py << 'EOF'
import fire
from legal_lora.train import train_lora

def train(config_path="configs/train.yaml"):
    train_lora(config_path)

if __name__ == "__main__":
    fire.Fire({
        "train": train
    })
EOF

# ===== 4. legal_lora/train.py =====
cat > legal_lora/train.py << 'EOF'
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from peft import LoraConfig, get_peft_model
from datasets import load_dataset
import mlflow
from omegaconf import OmegaConf

def train_lora(config_path="configs/train.yaml"):
    cfg = OmegaConf.load(config_path)

    # Поддержка URI из yaml
    mlflow.set_tracking_uri(cfg.get("mlflow_uri", "file:mlruns"))
    mlflow.start_run(run_name=cfg.get("run_name", "train_lora"))
    mlflow.log_params(dict(cfg))

    model = AutoModelForCausalLM.from_pretrained(cfg.model_name)
    tokenizer = AutoTokenizer.from_pretrained(cfg.model_name)
    dataset = load_dataset("csv", data_files={"train": cfg.data_path})["train"]

    def tokenize_fn(examples):
        return tokenizer(examples["text"], truncation=True, max_length=cfg.max_length, padding="max_length")
    tokenized = dataset.map(tokenize_fn, batched=True)

    data_collator = DataCollatorForLanguageModeling(tokenizer, mlm=False)

    # Чтение LoRA-конфига из yaml
    lora_conf = cfg.get("lora", {})
    lora_config = LoraConfig(
        r=lora_conf.get("r", 8),
        lora_alpha=lora_conf.get("lora_alpha", 32),
        lora_dropout=lora_conf.get("lora_dropout", 0.1),
        bias=lora_conf.get("bias", "none"),
        task_type=lora_conf.get("task_type", "CAUSAL_LM"),
    )
    model = get_peft_model(model, lora_config)

    args = TrainingArguments(
        output_dir=cfg.output_dir,
        per_device_train_batch_size=cfg.batch_size,
        num_train_epochs=cfg.epochs,
        save_steps=10_000,
        save_total_limit=2,
        logging_steps=100,
        report_to=[],
    )
    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=tokenized,
        data_collator=data_collator,
    )
    trainer.train()
    model.save_pretrained(cfg.output_dir)
    tokenizer.save_pretrained(cfg.output_dir)
    mlflow.log_artifacts(cfg.output_dir)
    mlflow.end_run()
EOF

# ===== 5. legal_lora/infer.py =====
cat > legal_lora/infer.py << 'EOF'
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

def infer_lora(model_dir, prompt):
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForCausalLM.from_pretrained(model_dir)
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, device=0)
    return pipe(prompt, max_new_tokens=128)[0]["generated_text"]
EOF

# ===== 6. configs/train.yaml =====
cat > configs/train.yaml << 'EOF'
model_name: "gpt2"
output_dir: "outputs/lora"
data_path: "data_legal.csv"
max_length: 256
batch_size: 2
epochs: 1
mlflow_uri: "http://127.0.0.1:8080"
run_name: "lora-gpt2-legal"
lora:
  r: 8
  lora_alpha: 32
  lora_dropout: 0.1
  bias: "none"
  task_type: "CAUSAL_LM"
EOF

echo "✅ All files recreated! Проверь свой код и запускай обучение."
# --- output ---
# ✅ All files recreated! Проверь свой код и запускай обучение.
# --- end output ---

import shutil, os
if os.path.exists("mlruns"):
    shutil.rmtree("mlruns")
os.makedirs("mlruns", exist_ok=True)
print("mlruns очищена!")
# --- output ---
# mlruns очищена!
# --- end output ---

%%bash
mkdir -p legal_lora

cat > legal_lora/train.py << 'EOF'
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from peft import LoraConfig, get_peft_model
from datasets import load_dataset
import mlflow
from omegaconf import OmegaConf

def train_lora(config_path="configs/train.yaml"):
    cfg = OmegaConf.load(config_path)
    mlflow.set_tracking_uri(cfg.get("mlflow_uri", "file:mlruns"))
    experiment_name = cfg.get("experiment_name", "Default")
    mlflow.set_experiment(experiment_name)
    mlflow.start_run(run_name=cfg.get("run_name", "train_lora"))
    mlflow.log_params(dict(cfg))

    # Model and tokenizer
    model = AutoModelForCausalLM.from_pretrained(cfg.model_name)
    tokenizer = AutoTokenizer.from_pretrained(cfg.model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # Dataset
    dataset = load_dataset("csv", data_files={"train": cfg.data_path})["train"]

    def tokenize_fn(examples):
        outputs = tokenizer(
            examples["text"],
            truncation=True,
            max_length=cfg.max_length,
            padding="max_length"
        )
        outputs["labels"] = outputs["input_ids"].copy()
        return outputs

    tokenized = dataset.map(tokenize_fn, batched=True)

    data_collator = DataCollatorForLanguageModeling(tokenizer, mlm=False)

    lora_conf = cfg.get("lora", {})
    lora_config = LoraConfig(
        r=lora_conf.get("r", 8),
        lora_alpha=lora_conf.get("lora_alpha", 32),
        lora_dropout=lora_conf.get("lora_dropout", 0.1),
        bias=lora_conf.get("bias", "none"),
        task_type=lora_conf.get("task_type", "CAUSAL_LM"),
    )
    model = get_peft_model(model, lora_config)

    args = TrainingArguments(
        output_dir=cfg.output_dir,
        per_device_train_batch_size=cfg.batch_size,
        num_train_epochs=cfg.epochs,
        save_steps=10_000,
        save_total_limit=2,
        logging_steps=100,
        report_to=[],
    )
    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=tokenized,
        data_collator=data_collator,
    )
    trainer.train()
    model.save_pretrained(cfg.output_dir)
    tokenizer.save_pretrained(cfg.output_dir)
    mlflow.log_artifacts(cfg.output_dir)
    mlflow.end_run()
EOF

echo "✅ legal_lora/train.py recreated!"
# --- output ---
# ✅ legal_lora/train.py recreated!
# --- end output ---


# --- output ---
# configs		    drive	outputs      pyproject.toml
# data_legal.csv	    legal_lora	plots	     sample_data
# data_legal.csv.dvc  mlruns	poetry.lock
# --- end output ---

# 1. Install dependencies
!pip install mlflow pyngrok --quiet

# 2. Set up directories and tracking URI
import os
import mlflow

project_dir = '/content/LORA-PEFT3'
os.makedirs(project_dir, exist_ok=True)
os.chdir(project_dir)
mlflow.set_tracking_uri("file:mlruns")
print("Working directory:", os.getcwd())
print("Tracking URI:", mlflow.get_tracking_uri())

# 3. Kill previous MLflow/ngrok processes so you can re-run cell
import signal, subprocess

def kill_process_on_port(port):
    try:
        proc = subprocess.check_output(f"lsof -ti:{port}", shell=True).decode().split()
        for pid in proc:
            os.kill(int(pid), signal.SIGKILL)
    except Exception:
        pass

kill_process_on_port(5000)  # MLflow
kill_process_on_port(4040)  # ngrok web UI

# 4. Start MLflow UI in background (nohup so it survives cell interrupts)
import sys
mlflow_cmd = "nohup mlflow ui --backend-store-uri file:mlruns --port 5000 --host 0.0.0.0 > mlflow.log 2>&1 &"
os.system(mlflow_cmd)

# 5. Start ngrok and print public URL
import time
from pyngrok import ngrok

NGROK_AUTH_TOKEN = "2wx6FxSxSW1miItHAvwaBhtmUuD_5HLV8pZtrURFditdAw2vZ"
ngrok.set_auth_token(NGROK_AUTH_TOKEN)

# Disconnect old tunnels if re-running
for tunnel in ngrok.get_tunnels():
    ngrok.disconnect(tunnel.public_url)

time.sleep(5)  # Give MLflow UI time to start

public_url = ngrok.connect(5000)
print("MLflow UI is live at:", public_url)
# --- output ---
# Working directory: /content/LORA-PEFT3
# Tracking URI: file:mlruns
# MLflow UI is live at: NgrokTunnel: "https://d7b6-34-142-129-109.ngrok-free.app" -> "http://localhost:5000"
# --- end output ---


# --- output ---
# /bin/bash: line 1: tree: command not found
# --- end output ---

