"""Replace AI-drawn apron logos with the real Focus logo (white-on-navy version),
keeping hands/tools that overlap the print in front of it.

usage: fix_logos.py IMAGE LOGO_PNG OUT PREVIEW
"""
import sys
import cv2
import numpy as np

img_path, logo_path, out_path, prev_path = sys.argv[1:5]
img = cv2.imread(img_path)
H, W = img.shape[:2]
k = W / 1000  # windows below are in 1000-px-wide coordinates

logo = cv2.imread(logo_path)
alpha = np.clip((255 - logo[..., 2].astype(np.float32)) / 200, 0, 1)
ys, xs = np.where(alpha > 0.3)
alpha = alpha[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

# (window, print angle in degrees, require blobs inside window)
WINDOWS = [((135, 437, 200, 474), 0, True), ((345, 437, 410, 458), 0, False), ((570, 413, 636, 451), 9.5, True), ((820, 405, 886, 449), 0, True)]
out = img.copy()
previews = []
for (x0, y0, x1, y1), fixed_angle, inside in WINDOWS:
    X0, Y0, X1, Y1 = int(x0 * k), int(y0 * k), int(x1 * k), int(y1 * k)
    roi = out[Y0:Y1, X0:X1]
    h, w = roi.shape[:2]
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    Hh, S, V = hsv[..., 0].astype(int), hsv[..., 1].astype(int), hsv[..., 2].astype(int)
    bright = ((V > 150) & (S < 70)).astype(np.uint8)
    fabric = ((Hh >= 95) & (Hh <= 135) & (S > 35) & (V < 150)).astype(np.uint8)

    # old print = bright blobs that do not touch the window border (tools/hands do)
    n, labels, stats, _ = cv2.connectedComponentsWithStats(bright)
    keep = np.zeros_like(bright)
    for i in range(1, n):
        x, y, bw_, bh_, area = stats[i]
        if area > 12 and (not inside or (x > 0 and y > 0 and x + bw_ < w and y + bh_ < h)):
            keep[labels == i] = 1
    yy, xx = np.where(keep)
    bx0, by0, bx1 = xx.min(), yy.min(), xx.max() + 1

    # orientation of the old print (letters lie along its long axis)
    (_, _), (rw, rh), ang = cv2.minAreaRect(np.column_stack([xx, yy]).astype(np.float32))
    if rw < rh:
        ang -= 90
    ang = fixed_angle

    # erase old print from the fabric
    erase = cv2.dilate(keep * 255, np.ones((3, 3), np.uint8), iterations=2)
    roi[:] = cv2.inpaint(roi, erase, 5, cv2.INPAINT_TELEA)

    # scale by width (the "Focus®" line spans the full logo width), rotate to match
    scale = (bx1 - bx0) / alpha.shape[1] * 1.03
    lw, lh = int(alpha.shape[1] * scale), int(alpha.shape[0] * scale)
    a = cv2.resize(alpha, (lw, lh), interpolation=cv2.INTER_AREA)
    pad = int(max(lw, lh) * 0.3)
    a = cv2.copyMakeBorder(a, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)
    R = cv2.getRotationMatrix2D((a.shape[1] / 2, a.shape[0] / 2), -ang, 1)
    a = cv2.warpAffine(a, R, (a.shape[1], a.shape[0]), flags=cv2.INTER_LINEAR)
    a = cv2.GaussianBlur(a, (0, 0), 0.4) * 0.94
    ox, oy = bx0 - pad - int(lw * 0.015), by0 - pad - int(lh * 0.02)
    canvas = np.zeros((h, w), np.float32)
    sx0, sy0 = max(0, -ox), max(0, -oy)
    dx0, dy0 = max(0, ox), max(0, oy)
    cw, ch = min(a.shape[1] - sx0, w - dx0), min(a.shape[0] - sy0, h - dy0)
    canvas[dy0:dy0 + ch, dx0:dx0 + cw] = a[sy0:sy0 + ch, sx0:sx0 + cw]

    # only print on fabric or where the old print was -> occluders stay in front
    allowed = cv2.GaussianBlur(np.clip(fabric + erase / 255.0, 0, 1).astype(np.float32), (0, 0), 0.8)
    canvas *= allowed
    ink = np.array([234, 237, 240], np.float32)
    roi[:] = (roi.astype(np.float32) * (1 - canvas[..., None]) + ink * canvas[..., None]).astype(np.uint8)
    print(f'logo at ({x0},{y0}) angle={ang:.1f} scale={scale:.3f}')
    previews.append(cv2.resize(np.vstack([img[Y0:Y1, X0:X1], roi]), (260, 300)))

cv2.imwrite(out_path, out)
cv2.imwrite(prev_path, np.hstack(previews))
