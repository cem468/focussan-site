"""Use the AI-enhanced photo for background, floor and grade, but take every person
(faces, jackets, logos) from the original, aligned and colour-matched.

usage: people_band.py ORIGINAL ENHANCED OUT
"""
import sys
import cv2
import numpy as np

orig_path, enh_path, out_path = sys.argv[1:4]
orig, enh = cv2.imread(orig_path), cv2.imread(enh_path)
H, W = enh.shape[:2]
big = cv2.resize(orig, (W, H), interpolation=cv2.INTER_LANCZOS4)

sift = cv2.SIFT_create(10000)
k1, d1 = sift.detectAndCompute(cv2.cvtColor(big, cv2.COLOR_BGR2GRAY), None)
k2, d2 = sift.detectAndCompute(cv2.cvtColor(enh, cv2.COLOR_BGR2GRAY), None)
good = [m for m, n in cv2.FlannBasedMatcher(dict(algorithm=1, trees=5), dict(checks=64)).knnMatch(d1, d2, k=2) if m.distance < 0.7 * n.distance]
M, _ = cv2.estimateAffinePartial2D(np.float32([k1[m.queryIdx].pt for m in good]), np.float32([k2[m.trainIdx].pt for m in good]), method=cv2.RANSAC, ransacReprojThreshold=3.0)
warped = cv2.warpAffine(big, M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)

# People occupy x 30..1300, y 295..720 in the 1600x936 original (heads to below the hands)
sx, sy = W / orig.shape[1], H / orig.shape[0]
pts = cv2.transform(np.float32([[[30 * sx, 295 * sy], [1300 * sx, 720 * sy]]]), M)[0].astype(int)
mask = np.zeros((H, W), np.float32)
cv2.rectangle(mask, tuple(pts[0]), tuple(pts[1]), 1.0, -1)
mask = cv2.GaussianBlur(mask, (0, 0), W / 120)

# Colour-match the original people to the enhanced grade (LAB mean/std over the band)
lab_w = cv2.cvtColor(warped, cv2.COLOR_BGR2LAB).astype(np.float32)
lab_e = cv2.cvtColor(enh, cv2.COLOR_BGR2LAB).astype(np.float32)
sel = mask > 0.9
for c in range(3):
    sw, se = lab_w[..., c][sel], lab_e[..., c][sel]
    lab_w[..., c] = (lab_w[..., c] - sw.mean()) * (se.std() / (sw.std() + 1e-6)) + se.mean()
graded = cv2.cvtColor(np.clip(lab_w, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
# gentle sharpening so the original people do not look softer than the background
blur = cv2.GaussianBlur(graded, (0, 0), 1.2)
graded = cv2.addWeighted(graded, 1.35, blur, -0.35, 0)

m = mask[..., None]
cv2.imwrite(out_path, (graded * m + enh * (1 - m)).astype(np.uint8))
print('done', W, H)
