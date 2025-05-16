import cv2
import numpy as np
import sys
import os

# Lista global para armazenar os pontos clicados
points = []

def click_event(event, x, y, flags, param):
    global points, img
    if event == cv2.EVENT_LBUTTONDOWN and len(points) < 4:
        points.append((x, y))
        print(f'Ponto {len(points)}: ({x}, {y})')
        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow("Clique nos 4 cantos da tela", img)

def apply_perspective_transform(img, pts_src, output_size=(640, 480)):
    width, height = output_size
    pts_dst = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1]
    ], dtype='float32')

    M = cv2.getPerspectiveTransform(pts_src, pts_dst)
    warped = cv2.warpPerspective(img, M, (width, height))
    return warped

def montar_comparacao_lado_a_lado(original, transformada):
    # Redimensiona as imagens para a mesma altura (se necessário)
    h = 500
    original = cv2.resize(original, (int(original.shape[1] * h / original.shape[0]), h))
    transformada = cv2.resize(transformada, (int(transformada.shape[1] * h / transformada.shape[0]), h))

    # Adiciona título nas imagens
    def adicionar_titulo(img, titulo):
        fonte = cv2.FONT_HERSHEY_SIMPLEX
        tamanho_fonte = 1
        espessura = 2
        altura_texto = 40

        largura = img.shape[1]
        canvas = np.ones((altura_texto, largura, 3), dtype=np.uint8) * 255
        texto_tamanho = cv2.getTextSize(titulo, fonte, tamanho_fonte, espessura)[0]
        x = (largura - texto_tamanho[0]) // 2
        y = (altura_texto + texto_tamanho[1]) // 2
        cv2.putText(canvas, titulo, (x, y), fonte, tamanho_fonte, (0, 0, 0), espessura)
        return np.vstack((canvas, img))

    original_titulada = adicionar_titulo(original, "Original")
    transformada_titulada = adicionar_titulo(transformada, "Transformada")

    # Junta lado a lado
    comparacao = np.hstack((original_titulada, transformada_titulada))
    return comparacao

def main(image_path):
    global img, points

    if not os.path.exists(image_path):
        print(f"Erro: arquivo '{image_path}' não encontrado.")
        return

    # Carrega e redimensiona a imagem original
    original_img = cv2.imread(image_path)
    original_img = cv2.resize(original_img, (700, int(original_img.shape[0] * 700 / original_img.shape[1])))

    # Copia apenas para visualização com clique
    img = original_img.copy()

    # Exibe e coleta pontos
    cv2.imshow("Clique nos 4 cantos da tela", img)
    cv2.setMouseCallback("Clique nos 4 cantos da tela", click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if len(points) == 4:
        pts_src = np.array(points, dtype='float32')
        resultado = apply_perspective_transform(original_img, pts_src)

        comparacao = montar_comparacao_lado_a_lado(original_img, resultado)
        output_name = "comparacao.jpg"
        cv2.imwrite(output_name, comparacao)
        print(f"Imagem de comparação salva como: {output_name}")
    else:
        print("Você precisa clicar exatamente em 4 pontos.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 perspective_transform.py <caminho_da_imagem>")
    else:
        main(sys.argv[1])
