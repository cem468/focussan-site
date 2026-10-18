"""Keep real faces: align an AI-enhanced group photo to the original, measure how much
each face changed, and paste every original face back with a feathered mask.

usage: faces.py ORIGINAL ENHANCED OUT REPORT_IMAGE
"""
import sys
import cv2
import numpy as np

orig_path, enh_path, out_path, report_path = sys.argv[1:5]
orig = cv2.imread(orig_path)
enh = cv2.imread(enh_path)
H, W = enh.shape[:2]
big = cv2.resize(orig, (W, H), interpolation=cv2.INTER_LANCZOS4)

# 1) align original (upscaled) onto the enhanced image
sift = cv2.SIFT_create(10000)
g1, g2 = cv2.cvtColor(big, cv2.COLOR_BGR2GRAY), cv2.cvtColor(enh, cv2.COLOR_BGR2GRAY)
k1, d1 = sift.detectAndCompute(g1, None)
k2, d2 = sift.detectAndCompute(g2, None)
matches = cv2.FlannBasedMatcher(dict(algorithm=1, trees=5), dict(checks=64)).knnMatch(d1, d2, k=2)
good = [m for m, n in matches if m.distance < 0.7 * n.distance]
M, inl = cv2.estimateAffinePartial2D(np.float32([k1[m.queryIdx].pt for m in good]),
                                     np.float32([k2[m.trainIdx].pt for m in good]),
                                     method=cv2.RANSAC, ransacReprojThreshold=3.0)
print(f'align: matches={len(good)} inliers={int(inl.sum())} scale={np.hypot(M[0,0],M[1,0]):.4f} shift=({M[0,2]:.1f},{M[1,2]:.1f})')
warped = cv2.warpAffine(big, M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)

# 2) face boxes marked by hand on the original (x0, y0, x1, y1 in original pixels)
FACES = [(90,337,133,397),(215,355,258,415),(290,357,325,407),(327,350,365,407),(410,312,453,380),
         (432,367,470,422),(505,330,545,385),(533,378,598,436),(600,322,640,380),(647,345,692,405),
         (690,322,732,380),(740,348,787,412),(783,330,830,410),(855,300,900,360),(927,332,965,380),
         (967,307,1010,367),(1040,327,1078,377),(1112,325,1155,385),(1155,322,1192,380),(1237,330,1278,387)]
sx, sy = W / orig.shape[1], H / orig.shape[0]
merged = []
for x0, y0, x1, y1 in FACES:
    pts = cv2.transform(np.float32([[[x0 * sx, y0 * sy], [x1 * sx, y1 * sy]]]), M)[0]
    merged.append([pts[0][0], pts[0][1], pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]])
print('faces:', len(merged))

# 3) compare and paste back (head-sized region incl. hair/headscarf)
mask = np.zeros((H, W), np.float32)
diffs = []
for x, y, w, h in merged:
    x0, y0 = max(0, int(x - w * 0.25)), max(0, int(y - h * 0.3))
    x1, y1 = min(W, int(x + w * 1.25)), min(H, int(y + h * 1.15))
    a = cv2.cvtColor(warped[y0:y1, x0:x1], cv2.COLOR_BGR2GRAY).astype(np.float32)
    b = cv2.cvtColor(enh[y0:y1, x0:x1], cv2.COLOR_BGR2GRAY).astype(np.float32)
    a = (a - a.mean()) / (a.std() + 1e-6)
    b = (b - b.mean()) / (b.std() + 1e-6)
    diffs.append(float(np.mean(np.abs(cv2.GaussianBlur(a, (0, 0), 2) - cv2.GaussianBlur(b, (0, 0), 2)))))
    cv2.ellipse(mask, ((x0 + x1) // 2, (y0 + y1) // 2), ((x1 - x0) // 2, (y1 - y0) // 2), 0, 0, 360, 1.0, -1)
print('face difference (0 = identical):', ' '.join(f'{d:.2f}' for d in diffs))

# match original faces' colour to the enhanced grade so the patches blend
lab_w = cv2.cvtColor(warped, cv2.COLOR_BGR2LAB).astype(np.float32)
lab_e = cv2.cvtColor(enh, cv2.COLOR_BGR2LAB).astype(np.float32)
sel = mask > 0.5
if sel.any():
    for c in range(3):
        sw, se = lab_w[..., c][sel], lab_e[..., c][sel]
        lab_w[..., c] = (lab_w[..., c] - sw.mean()) * (se.std() / (sw.std() + 1e-6)) + se.mean()
graded = cv2.cvtColor(np.clip(lab_w, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
soft = cv2.GaussianBlur(mask, (0, 0), max(4, W / 500))[..., None]
out = (graded * soft + enh * (1 - soft)).astype(np.uint8)
cv2.imwrite(out_path, out)

# report: original | enhanced | final, for every face
tiles = []
for x, y, w, h in merged:
    x0, y0 = max(0, int(x - w * 0.35)), max(0, int(y - h * 0.55))
    x1, y1 = min(W, int(x + w * 1.35)), min(H, int(y + h * 1.35))
    row = [cv2.resize(img[y0:y1, x0:x1], (110, 130)) for img in (warped, enh, out)]
    tiles.append(np.vstack(row))
if tiles:
    cv2.imwrite(report_path, np.hstack(tiles))
