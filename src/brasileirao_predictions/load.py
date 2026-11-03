import pandas as pd

PARTIDAS_PATH = "data/raw/campeonato-brasileiro-full.csv"
ESTATISTICAS_PATH = "data/raw/campeonato-brasileiro-estatisticas-full.csv"


def cobertura_por_temporada(df: pd.DataFrame) -> pd.DataFrame:
	"""% de jogos com chutes e posse válidos por temporada (ano da data do jogo).

	Recebe o DataFrame já mesclado (uma linha por partida). Jogo válido: mandante e visitante com chutes > 0 (0 = dado ausente) e posse preenchida.
	"""
	temporada = pd.to_datetime(df["data"], dayfirst=True, format="mixed").dt.year.rename("temporada")
	tabela = pd.DataFrame({
		"chutes": (df[["chutes_mandante", "chutes_visitante"]] > 0).all(axis=1),
		"posse": df[["posse_de_bola_mandante", "posse_de_bola_visitante"]].notna().all(axis=1),
	}).groupby(temporada).agg(jogos=("chutes", "size"), chutes=("chutes", "mean"), posse=("posse", "mean"))
	tabela[["chutes", "posse"]] = (tabela[["chutes", "posse"]] * 100).round(1)
	return tabela


def validar_merge(merged: pd.DataFrame) -> None:
	"""Levanta ValueError se o merge perdeu, duplicou ou deixou partidas sem estatística."""
	ids = pd.read_csv(PARTIDAS_PATH, usecols=["ID"])["ID"]
	est = pd.read_csv(ESTATISTICAS_PATH, usecols=["partida_id", "clube"])
	problemas = {
		"linhas diferentes do original": len(merged) != len(ids),
		"IDs duplicados no merge": not merged["ID"].is_unique,
		"IDs diferentes do original": set(merged["ID"]) != set(ids),
		"(partida_id, clube) duplicado em estatisticas": est.duplicated().any(),
		"partida sem estatística de mandante ou visitante": merged[["partida_id_mandante", "partida_id_visitante"]].isna().any().any(),
	}
	falhas = [k for k, v in problemas.items() if v]
	if falhas:
		raise ValueError("Merge inconsistente: " + "; ".join(falhas))


def carregar_dados() -> pd.DataFrame:
    partidas = pd.read_csv(PARTIDAS_PATH, usecols=["ID", "rodata", "data", "mandante", "visitante", "vencedor", "mandante_Placar", "visitante_Placar"])

    estatisticas = pd.read_csv(ESTATISTICAS_PATH, usecols=["partida_id", "clube", "chutes", "chutes_no_alvo", "posse_de_bola"])

    partidas = pd.merge(
        partidas,
        estatisticas,
        left_on=["ID", "mandante"],
        right_on=["partida_id", "clube"],
        how="left",
    )
    partidas = pd.merge(
        partidas,
        estatisticas,
        left_on=["ID", "visitante"],
        right_on=["partida_id", "clube"],
        how="left",
        suffixes=("_mandante", "_visitante"),
    )

    validar_merge(partidas)
    
    return partidas


partidas = carregar_dados()
print(cobertura_por_temporada(partidas))