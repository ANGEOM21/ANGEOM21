import os, sys, random
from PIL import Image, ImageOps, ImageEnhance
import numpy as np

def process_image(img_path, w=300, h=338):
    img = Image.open(img_path)
    gray = ImageOps.grayscale(img)
    
    # Aspect crop
    target_ratio = w / h
    curr_ratio = gray.width / gray.height
    if curr_ratio > target_ratio:
        new_w = int(gray.height * target_ratio)
        left = (gray.width - new_w) // 2
        gray = gray.crop((left, 0, left + new_w, gray.height))
    else:
        new_h = int(gray.width / target_ratio)
        top = (gray.height - new_h) // 2
        gray = gray.crop((0, top, gray.width, top + new_h))
        
    gray = gray.resize((w, h), Image.Resampling.LANCZOS)
    
    # Contrast and sharpness
    gray = ImageOps.autocontrast(gray, cutoff=2)
    enhancer = ImageEnhance.Contrast(gray)
    gray = enhancer.enhance(1.6)
    sharpener = ImageEnhance.Sharpness(gray)
    gray = sharpener.enhance(2.0)
    
    # Floyd-Steinberg dithering
    dithered = gray.convert('1', dither=Image.Dither.FLOYDSTEINBERG)
    return np.array(dithered)

def get_runs(arr, target_val=True, w=300, h=338):
    runs = []
    for y in range(h):
        in_run = False
        run_start = 0
        for x in range(w):
            val = (arr[y, x] == target_val)
            if val and not in_run:
                in_run = True
                run_start = x
            elif not val and in_run:
                in_run = False
                runs.append((run_start, y, x - run_start))
        if in_run:
            runs.append((run_start, y, w - run_start))
    return runs

def generate_svg_groups(runs, num_buckets=35, base_delay=0.20, max_delay=1.20):
    indexed_runs = []
    for r in runs:
        x, y, l = r
        score = y + random.uniform(-40, 40)
        indexed_runs.append((score, r))
    indexed_runs.sort(key=lambda item: item[0])
    
    buckets = [[] for _ in range(num_buckets)]
    for i, (_, r) in enumerate(indexed_runs):
        b_idx = int((i / len(indexed_runs)) * num_buckets)
        b_idx = min(max(b_idx, 0), num_buckets - 1)
        buckets[b_idx].append(r)
        
    lines = []
    delays = np.linspace(base_delay, max_delay, num_buckets)
    for b_idx, bucket in enumerate(buckets):
        if not bucket:
            continue
        t = delays[b_idx]
        d_chunks = []
        for x, y, l in bucket:
            d_chunks.append(f"M{x} {y}h{l}v1h-{l}z")
        path_d = "".join(d_chunks)
        group = (
            f'<g opacity="0">'
            f'<animate attributeName="opacity" values="0;1" dur="0.9s" begin="{t:.2f}s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".4 0 .2 1"/>'
            f'<path d="{path_d}"/>'
            f'</g>'
        )
        lines.append(group)
    return "\n".join(lines)

def generate_sparkles(runs, num_sparkles=40, theme="dark"):
    use_tag = "tvdark" if theme == "dark" else "tvlight"
    lines = []
    sample_points = random.sample(runs, min(len(runs), num_sparkles * 4))
    for i in range(num_sparkles):
        p1 = sample_points[i * 4]
        p2 = sample_points[i * 4 + 1]
        p3 = sample_points[i * 4 + 2]
        p4 = sample_points[i * 4 + 3]
        vals = f"{p1[0]} {p1[1]};{p1[0]} {p1[1]};{p2[0]} {p2[1]};{p2[0]} {p2[1]};{p3[0]} {p3[1]};{p3[0]} {p3[1]};{p4[0]} {p4[1]};{p4[0]} {p4[1]};{p1[0]} {p1[1]}"
        dur = round(12.0 + random.uniform(0, 3.0), 1)
        sp = (
            f'<use href="#{use_tag}" opacity="0">'
            f'<animate attributeName="opacity" values="0;0;1;1;1;1;1;1;0" keyTimes="0.000;0.194;0.288;0.432;0.525;0.669;0.763;0.906;1.000" dur="{dur}s" begin="3.2s" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="translate" values="{vals}" keyTimes="0.000;0.194;0.288;0.432;0.525;0.669;0.763;0.906;1.000" dur="{dur}s" begin="3.2s" repeatCount="indefinite"/>'
            f'</use>'
        )
        lines.append(sp)
    return "\n".join(lines)

def update_svg(svg_path, groups_str, sparkles_str):
    with open(svg_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    start_tag = '<set attributeName="opacity" to="0" begin="3.2s"/>'
    end_tag = '<path d="M 50 84 L 36 84 L 36 98"'
    
    start_idx = content.find(start_tag)
    end_idx = content.find(end_tag)
    
    if start_idx == -1 or end_idx == -1:
        print(f"Tags not found in {svg_path}!")
        return False
        
    start_pos = start_idx + len(start_tag)
    new_content = (
        content[:start_pos] + "\n" +
        groups_str + "\n" +
        sparkles_str + "\n" +
        content[end_idx:]
    )
    
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Updated {svg_path} successfully!")
    return True

if __name__ == "__main__":
    img_path = r"D:\berkas\profile.jpeg"
    arr = process_image(img_path)
    
    # Dark SVG
    dark_runs = get_runs(arr, target_val=True)
    dark_groups = generate_svg_groups(dark_runs)
    dark_sparkles = generate_sparkles(dark_runs, theme="dark")
    update_svg("dark.svg", dark_groups, dark_sparkles)
    
    # Light SVG
    light_runs = get_runs(arr, target_val=False)
    light_groups = generate_svg_groups(light_runs)
    light_sparkles = generate_sparkles(light_runs, theme="light")
    update_svg("light.svg", light_groups, light_sparkles)
