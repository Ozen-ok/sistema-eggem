from datetime import datetime
from pathlib import Path

from docxtpl import DocxTemplate


def teste():
    """Gera um DOCX de teste usando dados fictícios, sem acessar banco ou SMTP."""
    raiz_projeto = Path(__file__).resolve().parents[1]
    caminho_modelo = raiz_projeto / "backend" / "formulario_modelo.docx"

    if not caminho_modelo.is_file():
        raise FileNotFoundError(f"Modelo não encontrado: {caminho_modelo}")

    # Os nomes das chaves correspondem aos campos do modelo DOCX do backend.
    dados = {
        "responsavel": "João da Silva",
        "cargo": "Servidor público",
        "secretaria": "SEMED",
        "telefone": "(98) 00000-0000",
        "email": "teste@example.com",
        "acao": "Ação de capacitação de teste",
        "tipo_acao": "Webinário",
        "publico_alvo": "Servidores municipais",
        "num_vagas": "30",
        "carga_horaria": "40",
        "data_inicio": "26/04/2024",
        "data_fim": "30/04/2024",
        "turno": "Matutino",
        "modalidade": "Semipresencial",
        "justificativa": "Texto fictício para testar a geração do documento.",
        "obj": "Verificar se o modelo é preenchido corretamente.",
        "sugestao_conteudo": "Tópico 1; tópico 2; tópico 3.",
    }

    documento = DocxTemplate(str(caminho_modelo))
    documento.render(dados)

    pasta_saida = Path(__file__).resolve().parent / "saidas"
    pasta_saida.mkdir(parents=True, exist_ok=True)

    identificador = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    caminho_saida = pasta_saida / f"documento_teste_{identificador}.docx"
    documento.save(str(caminho_saida))

    print(f"Documento de teste gerado: {caminho_saida}")
    return caminho_saida


if __name__ == "__main__":
    teste()
