from flask import Blueprint, render_template
from flask import current_app as app
from application.model.architecture import model, transformer
from flask import request, render_template
from flask_pymongo import PyMongo
from PIL import Image
from datetime import  datetime

# Blueprint
model_bp = Blueprint(
    'model_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

mongo = PyMongo(app)

allowed_extension = ['jpg', 'jpeg']


@model_bp.route('/', methods=['GET'])
def upload():
    return render_template('image_upload.html')


@model_bp.route('/predict', methods=['POST'])
def get_labels():
    # chk if image is upload
    if 'image' in request.files:
        # get image
        image = request.files['image']
        # chk if extension is supported
        if image.filename.split('.')[-1] in allowed_extension:
            # get prredictions
            predictions = predict(image)
            # Upload image on mongoDB
            try:
                mongo.save_file(image.filename, image)
                mongo.db.testimages.insert({
                    "time": datetime.utcnow(),
                    "img_name": image.filename,
                    "predictions": predictions
                })

            except TimeoutError as e:
                print("Mongo Error")
                print(e)
                return "Server Timeout Error"

            if predictions['human']:
                if predictions['Swiggy']:
                    # human and swiggy detected
                    return render_template('predictions.html', predictions=['Human detected',"Swiggy"], support_types=None)
                # Human and other detected
                return render_template('predictions.html', predictions=['Human detected',"Others"], support_types=None)
            # no human detected
            return render_template('predictions.html', predictions=['No Human detected'], support_types=None)
        # extension not supported
        return render_template('predictions.html', predictions=None, support_types=allowed_extension)
    # no file uploaded
    return render_template('predictions.html', predictions=None, support_types=None)


def predict(img):
    """
    Predict labels for the given image
    :param img:
    :return: json file with label predictions
    """
    img = read_process(img)
    output = model(img)[0].tolist()
    print(output)
    prediction = {"human": output[0] > 0.8,
                  'Swiggy': output[1] > 0.8}
    return prediction


def read_process(img):
    """
    Read and transform image.
    :param img: Image file
    :return: Tranformed Image
    """
    try:
        img = Image.open(img).convert('RGB')
        img_tranformed = transformer(img).unsqueeze(0)
    except RuntimeError as e:
        return "Image Channels not supported<br> Upload RGB images"
    return img_tranformed
