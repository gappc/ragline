import os
import shutil
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DOCS_PATH = os.getenv("DOCS_PATH", ".cache/docs")
TMP_PATH = os.getenv("TMP_PATH", ".cache/tmp")


def compute_docs_path(username, filename):
    return _compute_path(DOCS_PATH, username, filename)


def compute_tmp_path(username, filename):
    return _compute_path(TMP_PATH, username, filename)


def compute_user_path(username):
    return _compute_user_path(DOCS_PATH, username)


def create_user_paths(username):
    Path(TMP_PATH + "/" + username).mkdir(parents=True, exist_ok=True)
    Path(DOCS_PATH + "/" + username).mkdir(parents=True, exist_ok=True)


def delete_user_paths(username):
    shutil.rmtree(TMP_PATH + "/" + username, ignore_errors=True)
    shutil.rmtree(DOCS_PATH + "/" + username, ignore_errors=True)


def _compute_user_path(base, username):
    return base + "/" + username


def _compute_path(base, username, filename):
    return _compute_user_path(base, username) + "/" + filename
