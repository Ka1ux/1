"""Testes de integração: roda o pipeline e valida os dados gerados."""
import subprocess
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable
SCRIPTS = ["src/01_gerar_dados.py", "src/02_analise_eda.py", "src/03_modelagem.py"]


def _run(script):
    r = subprocess.run([PY, script], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, f"{script} falhou:\n{r.stderr}"


def test_pipeline_roda_sem_erro():
    for s in SCRIPTS:
        _run(s)


def test_dados_gerados_sao_validos():
    _run("src/01_gerar_dados.py")
    df = pd.read_csv(ROOT / "dados" / "clientes_telecom.csv")
    assert len(df) > 1000
    assert set(df["churn"].unique()) <= {0, 1}
    assert (df["mensalidade"] > 0).all()
    assert df["tempo_casa_meses"].between(0, 72).all()
