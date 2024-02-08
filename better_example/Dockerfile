FROM continuumio/miniconda3:latest

WORKDIR /app

# Make RUN commands use `bash --login` for conda activate to work
SHELL ["/bin/bash", "--login", "-c"]

COPY environment.yml .

RUN conda env create -f environment.yml
RUN conda activate ragline

COPY db db/
COPY logger logger/
COPY server server/
COPY utils utils/
COPY vector_store vector_store/

EXPOSE 9000

CMD ["/bin/bash", "--login", "-c", "conda activate ragline && uvicorn server.main:app --host 0.0.0.0 --port 9000 --reload"]