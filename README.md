# Perspective Transformation

Este projeto permite aplicar **transformações de perspectiva** em imagens, corrigindo planos inclinados (como quadros, folhas ou painéis fotografados em ângulo) para gerar uma visualização frontal retangular da área selecionada.  
  
Na pasta de imagens existem alguns exemplos de telas inclinadas e quadros de museus.

## O que o programa faz

A partir de uma imagem, o usuário seleciona **quatro pontos** que delimitam uma área (como um quadro em uma parede). O programa então:

- Ordena automaticamente os pontos no sentido correto (horário)
- Calcula uma **transformação de perspectiva**
- Exibe e salva uma imagem comparativa lado a lado: **original** vs **retificada**

O resultado é salvo como `comparison.jpg`.

---

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/amalra1/PerspectiveTransformation
cd PerspectiveTransformation
```

### 2. Instale as dependências  

```bash
pip install opencv-python numpy
```

---

## Execução

Execute o script fornecendo o caminho da imagem como argumento:

```bash
python3 perspective_transform.py caminho/para/imagem.jpg
```

### Exemplo  

```bash
python3 perspective_transform.py images/Paintings/museum2.jpg
```

---

## Uso

1. Ao abrir a janela em tela cheia, **clique com o botão esquerdo** nos **quatro cantos** da área desejada.
2. Os pontos podem ser clicados **em qualquer ordem**.
3. Após os quatro cliques, **pressione qualquer tecla** do teclado para confirmar.
4. A imagem será transformada e o resultado salvo como comparison.jpg, mostrando o antes e depois lado a lado.  
