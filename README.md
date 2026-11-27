# rag-chunk-bench

Demonstração independente, sem vínculo com a PSM Company (cliente não diz).

Uma ferramenta pequena para responder a uma pergunta que aparece em todo projeto de RAG (busca em documentos para alimentar um modelo de linguagem): como cortar o texto em pedaços? Ela corta os mesmos documentos de cinco jeitos, busca com BM25 e conta em quantas perguntas o pedaço certo aparece entre os `k` primeiros resultados.

Não usa nenhuma biblioteca de terceiros. Roda offline.

## Como rodar

```bash
uv sync
uv run pytest -q
uv run rag-chunk-bench        # k=3
uv run rag-chunk-bench -k 1   # só o primeiro resultado conta
```

Para usar seus próprios dados: `--docs pasta_com_arquivos_txt --questions perguntas.json`. Cada pergunta tem `id`, `question` e `answer`. Uma resposta conta como encontrada quando as palavras de `answer` aparecem juntas e em ordem dentro de um pedaço recuperado.

## Estratégias comparadas

- `fixed-20`, `fixed-40`: janelas fixas de 20 e de 40 palavras.
- `fixed-40-overlap-10`: 40 palavras, com 10 repetidas entre pedaços vizinhos.
- `sentences-40`: frases inteiras, juntadas até chegar a cerca de 40 palavras.
- `paragraphs`: um pedaço por parágrafo.

## Resultado nos dados de exemplo

Os 4 documentos e as 16 perguntas em `data/` são **inventados** (políticas de uma empresa fictícia, em português). Com `k=3`:

| estratégia | pedaços | acertos |
|---|---|---|
| sentences-40 | 23 | 15/16 |
| fixed-40-overlap-10 | 23 | 13/16 |
| paragraphs | 22 | 13/16 |
| fixed-40 | 19 | 12/16 |
| fixed-20 | 35 | 8/16 |

A janela de 20 palavras corta a frase que contém a resposta em duas metades. Nenhuma metade contém a resposta inteira, e a pergunta fica sem resposta mesmo quando o documento certo foi encontrado.

## What was tested

- 16 testes automáticos, todos offline: cada estratégia de corte, o BM25, a regra de acerto, a contagem de erros, a saída da linha de comando e a verificação de que toda resposta de exemplo existe de fato em algum documento.
- O CI roda os testes e a comparação a cada push.

## What was not tested

- Dados reais. O exemplo tem 4 documentos curtos e 16 perguntas escritas por mim; a diferença entre as estratégias pode mudar bastante em outro corpus.
- Busca vetorial, busca híbrida, reranking ou qualquer serviço de nuvem. Só BM25.
- Textos em outros idiomas e documentos longos (PDF, tabelas, HTML).
- Desempenho com muitos documentos.
