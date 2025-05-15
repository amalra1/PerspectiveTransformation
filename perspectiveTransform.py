import cv2
import numpy as np
import sys
import os

# Lista global para armazenar os pontos clicados
points = []

def click_event(event, x, y, flags, param):
    """Callback para capturar os 4 cliques do mouse."""
    global points, img
    if event == cv2.EVENT_LBUTTONDOWN and len(points) < 4:
        points.append((x, y))
        print(f'Ponto {len(points)}: ({x}, {y})')
        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow("Clique nos 4 cantos da tela", img)

def apply_perspective_transform(img, pts_src, output_size=(640, 480)):
    """Aplica a transformação de perspectiva com base nos pontos dados."""
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

def main(image_path):
    global img, points

    if not os.path.exists(image_path):
        print(f"Erro: arquivo '{image_path}' não encontrado.")
        return

    # Carrega e redimensiona a imagem
    img = cv2.imread(image_path)
    img = cv2.resize(img, (700, int(img.shape[0] * 700 / img.shape[1])))

    # Abre janela para clique
    cv2.imshow("Clique nos 4 cantos da tela", img)
    cv2.setMouseCallback("Clique nos 4 cantos da tela", click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if len(points) == 4:
        pts_src = np.array(points, dtype='float32')
        result = apply_perspective_transform(img, pts_src)

        output_name = "tela_retificada.jpg"
        cv2.imwrite(output_name, result)
        print(f"[✔] Imagem salva como: {output_name}")
    else:
        print("[!] Você precisa clicar exatamente em 4 pontos.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 perspective_transform.py <caminho_da_imagem>")
    else:
        main(sys.argv[1])
