FROM agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim

RUN pip install -U pip & pip install pipenv

COPY [ "Pipfile", "Pipfile.lock", "./" ]

RUN pipenv install --system --deploy

COPY model/model.bin model/model.bin

COPY [ "deployment.py", "deployment.py" ]

ENTRYPOINT [ "python", "deployment.py" ]