from flask import Flask, render_template, request, send_from_directory
from collections import deque
from PIL import Image
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'files'


if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def region_growing_with_intermediate_images(img, seed, thresh, boundary_value=255, connectivity=8):
    width, height = len(img[0]), len(img)

    neighbors = [(-1, 0), (0, -1), (0, 1), (1, 0)] if connectivity == 4 else [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    img_with_boundary = [row[:] for row in img]
    region = deque([seed])
    segmented = [[False] * width for _ in range(height)]
    segmented[seed[1]][seed[0]] = True

    total_pixels = width * height
    region_size = 1
    intermediate_saves = [0.1, 0.2]
    save_indices = [int(total_pixels * p) for p in intermediate_saves]
    current_save_index = 0
    intermediate_results = []

    while region:
        x, y = region.popleft()
        for dx, dy in neighbors:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and not segmented[ny][nx]:
                if abs(img[ny][nx] - img[seed[1]][seed[0]]) < thresh:
                    segmented[ny][nx] = True
                    region.append((nx, ny))
                    region_size += 1
                else:
                    img_with_boundary[ny][nx] = boundary_value

        if current_save_index < len(save_indices) and region_size >= save_indices[current_save_index]:
            intermediate_copy = [row[:] for row in img_with_boundary]
            intermediate_results.append(intermediate_copy)
            current_save_index += 1

    return intermediate_results + [img_with_boundary]

def read_pgm(pgm_path):
    with open(pgm_path, 'rb') as f:
        assert f.readline().strip() == b'P5'
        while True:
            line = f.readline()
            if line.startswith(b'#'):
                continue
            else:
                width, height = [int(i) for i in line.split()]
                break
        maxval = int(f.readline().strip())
        img = [list(f.read(width)) for _ in range(height)]
        return img, maxval

def write_pgm(pgm_path, img, maxval):
    height, width = len(img), len(img[0])
    with open(pgm_path, 'wb') as f:
        f.write(bytes('P5\n', 'ascii'))
        f.write(bytes(f'{width} {height}\n', 'ascii'))
        f.write(bytes(f'{maxval}\n', 'ascii'))
        for row in img:
            f.write(bytearray(row))

def convert_pgm_to_png(pgm_path, png_path):
    with open(pgm_path, 'rb') as f:
        f.readline()
        line = f.readline()
        while line.startswith(b'#'):
            line = f.readline()
        width, height = map(int, line.split())
        maxval = int(f.readline().strip())
        img_data = f.read()

    image = Image.frombytes('L', (width, height), img_data)
    image.save(png_path, 'PNG')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_file = request.files['input_image']
        input_image_path = os.path.join(app.config['UPLOAD_FOLDER'], input_file.filename)
        input_file.save(input_image_path)

        seed_x = int(request.form['seed_x'])
        seed_y = int(request.form['seed_y'])
        threshold_value = int(request.form['threshold'])
        connectivity_type = int(request.form['connectivity'])

        intermediate_path_1 = os.path.join(app.config['UPLOAD_FOLDER'], 'intermediate1.pgm').replace("\\", "/")
        intermediate_png_1 = os.path.join(app.config['UPLOAD_FOLDER'], 'intermediate1.png').replace("\\", "/")
        intermediate_path_2 = os.path.join(app.config['UPLOAD_FOLDER'], 'intermediate2.pgm').replace("\\", "/")
        intermediate_png_2 = os.path.join(app.config['UPLOAD_FOLDER'], 'intermediate2.png').replace("\\", "/")
        final_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'final_output.pgm').replace("\\", "/")
        final_png = os.path.join(app.config['UPLOAD_FOLDER'], 'final_output.png').replace("\\", "/")

        input_img, max_value = read_pgm(input_image_path)

        intermediate_results = region_growing_with_intermediate_images(input_img, (seed_x, seed_y), threshold_value, connectivity=connectivity_type)

        write_pgm(intermediate_path_1, intermediate_results[0], max_value)
        write_pgm(intermediate_path_2, intermediate_results[1], max_value)
        write_pgm(final_image_path, intermediate_results[2], max_value)

        convert_pgm_to_png(intermediate_path_1, intermediate_png_1)
        convert_pgm_to_png(intermediate_path_2, intermediate_png_2)
        convert_pgm_to_png(final_image_path, final_png)

    
        return render_template(
            'result.html',
            intermediate1=intermediate_png_1.split('/')[-1],
            intermediate2=intermediate_png_2.split('/')[-1],
            final=final_png.split('/')[-1],
            intermediate1_pgm=intermediate_path_1.split('/')[-1],
            intermediate2_pgm=intermediate_path_2.split('/')[-1],
            final_pgm=final_image_path.split('/')[-1]
        )
    return render_template('index.html')

@app.route('/files/<filename>')
def serve_files(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
