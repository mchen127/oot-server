from flask import Flask, jsonify, send_file, request, render_template, redirect, url_for
# from PIL import Image
import cv2
import os
import subprocess

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        model_image_path = f'./OOTDiffusion/images/{uploaded_file.filename}'
        uploaded_file.save(model_image_path)
    else:
        print('upload image error')
    cloth_image_path = './OOTDiffusion/images/shirt.jpg'
    # oot diffusion process
    script_path = './oot-inference.sh'
    command = [
        script_path,
        '--model_path', model_image_path,
        '--cloth_path', cloth_image_path,
        '--scale', '2.0',
        '--sample', '4'
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    
    # Print the output
    print("Return code:", result.returncode)
    print("Output:", result.stdout)
    print("Error:", result.stderr)

    # fake diffusion process
    shirt = cv2.imread(cloth_image_path, 1)
    man = cv2.imread(model_image_path, 1)
    img = cv2.add(man, shirt)
    output_path = './OOTDiffusion/run/images_output/output_image.jpg'
    cv2.imwrite(output_path, img)
    print(f"Image saved to {output_path}")
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download(filename):
    IMAGE_DIRECTORY = "./OOTDiffusion/run/images_output"
    file_path = os.path.join(IMAGE_DIRECTORY, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "File not found", 404

@app.route("/api/hello", methods=['GET'])
def helloWorld():
    return jsonify({
        "message": "Hello WORLD!",
        "haha": "wfrwf"
    })

@app.route("/api/get-image", methods=['GET'])
def getImage():
    print(request)
    return send_file("OOTDiffusion/images/demo.png", mimetype='image/png')

@app.route("/api/post-image", methods=['GET', 'POST'])
def postImage():
    print(request)
    print(request.files)
    # img1 = Image.open(request.files['model'])
    # img2 = Image.open(request.files['cloth'])
    return 'Success!'


@app.route("/api/post-text", methods=['GET', 'POST'])
def returnText():
    print(request.method)
    if request.method == 'POST':
        # print(request.view_args())
        print(request.get_json())
        # return 'haha'
    return 'haha'



if __name__ == '__main__':
    app.run(debug=True, port=8080)