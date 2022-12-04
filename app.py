from flask import Flask,request,redirect,jsonify,abort, flash, url_for
from model import Photos, setup_app
from flask_migrate import Migrate
from flask_cors import CORS


def get_formatted(photos):
    formatted = [photo.format() for photo in photos]
    return formatted

#

app = Flask(__name__)
setup_app(app)
    
CORS(app)

@app.after_request
def after_request(response):
        response.headers.add( "Access-Control-Allow-Headers", "Content-Type,Authorization,true")
        response.headers.add( "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE")
        response.headers.add(  "Access-Control-Allow-Origin", "*")
        return response


@app.route('/', methods=['GET'])
def photos():
        all_photos = Photos.query.order_by(Photos.id.desc()).all()
        # sorted_photos = sorted(all_photos, reverse=True)
       
        formatted_photos = get_formatted(all_photos)
        return jsonify({
            'status':True,
            'photos':formatted_photos
        })

# POSTING PHOTO 
@app.route('/photos', methods=['GET','POST'])
def add_photo():
        if request.method == 'POST':
            body = request.get_json()
            label = body.get('label', None)
            url = body.get('url', None)
            try:
                new_photo = Photos(
                label=label,
                url=url
            )
                new_photo.insert()
            
            except:
                return jsonify({
               'status': False,
               
            })

            photos = Photos.query.order_by(Photos.id).all()
            
            formatted_photos = get_formatted(photos)
            return jsonify({
            'status': True,
            'photos':  formatted_photos
        })


# DELETE A PHOTO
@app.route('/photos/<photo_id>', methods=['DELETE', 'GET'])
def delete_photo(photo_id):
        to_delete = Photos.query.filter(Photos.id == photo_id).one_or_none()

        if to_delete:
            to_delete.delete()

        formatted = Photos.query.order_by(Photos.id.desc()).all()
        format_photos = get_formatted(formatted)
        
        return jsonify({
            'status': True,
            'photos': format_photos
        })

@app.route('/search', methods=['GET', 'POST'])
def search_photo():
        body = request.get_json()
        search_term = body.get('search_term', None)
        try:
            the_photos = Photos.query.filter(Photos.label.ilike('%{}%'.format(search_term))).all()
            formatted_photo = get_formatted(the_photos)
            
            return jsonify({
            'status': True,
            'photos':  formatted_photo 
            })

        except Exception as e:
          abort(405)



# ERROR handling
@app.errorhandler(404)
def not_found():
            return jsonify({
                'status': False,
                'error': 404,
                'messsage': 'Resourcses Not Found'
            })
@app.errorhandler(422)
def Unprocessible():
            return jsonify({
                'status': False,
                'error': 422,
                'messsage': 'Unprocessible'
            })

@app.errorhandler(405)
def method_not_allowed():
            return jsonify({
                'status': False,
                'error': 405,
                'messsage': 'Method not allowed'
            })

