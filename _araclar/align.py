"""Align an AI-upscaled image to its source frame and optionally paste source regions back.

usage: align.py SRC UPSCALED OUT [x0,y0,x1,y1 ...]   (regions in SRC pixel coords)
"""
import sys
import cv2
import numpy as np

src_path, up_path, out_path = sys.argv[1:4]
regions = [tuple(int(v) for v in r.split(',')) for r in sys.argv[4:]]

src = cv2.imread(src_path)
up = cv2.imread(up_path)
H, W = up.shape[:2]

sift = cv2.SIFT_create(8000)
g1 = cv2.cvtColor(cv2.resize(src, (W, H), interpolation=cv2.INTER_LANCZOS4), cv2.COLOR_BGR2GRAY)
g2 = cv2.cvtColor(up, cv2.COLOR_BGR2GRAY)
k1, d1 = sift.detectAndCompute(g1, None)
k2, d2 = sift.detectAndCompute(g2, None)
matches = cv2.FlannBasedMatcher(dict(algorithm=1, trees=5), dict(checks=64)).knnMatch(d1, d2, k=2)
good = [m for m, n in matches if m.distance < 0.7 * n.distance]
p1 = np.float32([k1[m.queryIdx].pt for m in good])
p2 = np.float32([k2[m.trainIdx].pt for m in good])
M, inliers = cv2.estimateAffinePartial2D(p1, p2, method=cv2.RANSAC, ransacReprojThreshold=3.0)
scale = float(np.hypot(M[0, 0], M[1, 0]))
print(f'matches={len(good)} inliers={int(inliers.sum())} scale={scale:.4f} shift=({M[0,2]:.1f},{M[1,2]:.1f}) px in {W}x{H}')

out = up.copy()
if regions:
    big = cv2.resize(src, (W, H), interpolation=cv2.INTER_LANCZOS4)
    warped = cv2.warpAffine(big, M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)
    sx, sy = W / src.shape[1], H / src.shape[0]
    mask = np.zeros((H, W), np.float32)
    for x0, y0, x1, y1 in regions:
        pts = np.float32([[x0 * sx, y0 * sy], [x1 * sx, y0 * sy], [x1 * sx, y1 * sy], [x0 * sx, y1 * sy]])
        pts = cv2.transform(pts[None], M)[0].astype(np.int32)
        cv2.fillConvexPoly(mask, pts, 1.0)
    mask = cv2.GaussianBlur(mask, (0, 0), 6)[..., None]
    out = (warped * mask + up * (1 - mask)).astype(np.uint8)

cv2.imwrite(out_path, out)
