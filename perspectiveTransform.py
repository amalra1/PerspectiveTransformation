import cv2
import numpy as np

# Lista para armazenar os pontos clicados
points = []

# Função de callback para capturar os cliques
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN and len(points) < 4:
        points.append((x, y))
        print(f'Ponto {len(points)}: ({x}, {y})')
        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow("Clique nos 4 cantos da tela", img)

# Carrega a imagem
img = cv2.imread("images/Doom/Doom1.jpeg")
img = cv2.resize(img, (700, int(img.shape[0] * 700 / img.shape[1])))  # redimensiona para facilitar clique

cv2.imshow("Clique nos 4 cantos da tela", img)
cv2.setMouseCallback("Clique nos 4 cantos da tela", click_event)

# Espera até o usuário clicar os 4 pontos e pressionar uma tecla
cv2.waitKey(0)
cv2.destroyAllWindows()

# Converte os pontos para o formato adequado
if len(points) == 4:
    pts_src = np.array(points, dtype='float32')

    # Define a dimensão da saída (você pode ajustar conforme sua imagem)
    width, height = 640, 480
    pts_dst = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1] 
    ], dtype='float32')

    # Calcula a transformação e aplica
    M = cv2.getPerspectiveTransform(pts_src, pts_dst)
    warped = cv2.warpPerspective(img, M, (width, height))

    # Mostra o resultado
    cv2.imshow("Tela retificada", warped)
    cv2.imwrite("tela_retificada.jpg", warped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Você precisa clicar exatamente em 4 pontos.")
