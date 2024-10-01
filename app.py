from flask import Flask, render_template, request, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import pandas as pd
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy import extract

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    budget = db.Column(db.Integer)
    homepage = db.Column(db.String(255))
    original_language = db.Column(db.String(10))
    original_title = db.Column(db.String(255))
    overview = db.Column(db.Text)
    release_date = db.Column(db.String(100))
    revenue = db.Column(db.BigInteger)
    runtime = db.Column(db.Float)
    status = db.Column(db.String(50))
    title = db.Column(db.String(255))
    vote_average = db.Column(db.Float)
    vote_count = db.Column(db.Integer)
    production_company_id = db.Column(db.Integer)
    genre_id = db.Column(db.Integer)
    languages = db.Column(db.String(255))

    def __repr__(self):
        return f'<Data {self.id}>'


@app.route('/')
def index():
    return render_template('upload.html')


@app.route('/data', methods=['GET'])
def get_data():
    try:
        # Get filter parameters from the request
        year = request.args.get('year', type=int)
        language = request.args.get('language', type=str)

        # Get pagination parameters (default values for page and per_page)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        
        query = Data.query

    
        if year:
            query = query.filter(extract('year', Data.release_date) == year)

        
        if language:
            query = query.filter(Data.original_language == language)

        # Apply sorting by release_date and vote_average in descending order
        query = query.order_by(Data.release_date.desc(), Data.vote_average.desc())

        # Paginate the results
        paginated_data = query.paginate(page=page, per_page=per_page)

        
        data_list = []
        for entry in paginated_data.items:
            data_list.append({
                'id': entry.id,
                'budget': entry.budget,
                'homepage': entry.homepage,
                'original_language': entry.original_language,
                'original_title': entry.original_title,
                'overview': entry.overview,
                'release_date': entry.release_date,
                'revenue': entry.revenue,
                'runtime': entry.runtime,
                'status': entry.status,
                'title': entry.title,
                'vote_average': entry.vote_average,
                'vote_count': entry.vote_count,
                'production_company_id': entry.production_company_id,
                'genre_id': entry.genre_id,
                'languages': entry.languages
            })

        
        return jsonify({
            'data': data_list,
            'total': paginated_data.total,
            'pages': paginated_data.pages,
            'current_page': paginated_data.page,
            'per_page': paginated_data.per_page
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file') 

    if file and file.filename.endswith('.csv'):
        try:
           
            data = pd.read_csv(file)
            data.columns = data.columns.str.strip().str.lower() 
            
            
            for index, row in data.iterrows():
                new_entry = Data(
                    budget=row.get('budget', 0),
                    homepage=row.get('homepage', ''),
                    original_language=row.get('original_language', ''),
                    original_title=row.get('original_title', ''),
                    overview=row.get('overview', ''),
                    release_date=row.get('release_date', ''),
                    revenue=row.get('revenue', 0),
                    runtime=row.get('runtime', 0),
                    status=row.get('status', ''),
                    title=row.get('title', ''),
                    vote_average=row.get('vote_average', 0.0),
                    vote_count=row.get('vote_count', 0),
                    production_company_id=row.get('production_company_id', 0),
                    genre_id=row.get('genre_id', 0),
                    languages=row.get('languages', '')
                )
                db.session.add(new_entry)

            db.session.commit() 
            return "Data uploaded successfully!"
        
        except IntegrityError as e:
            db.session.rollback()
            return f"IntegrityError: {str(e)}"
        
        except DataError as e:
            db.session.rollback()
            return f"DataError: {str(e)}"
        
        except Exception as e:
            db.session.rollback()
            return f"An error occurred: {str(e)}"
    else:
        return "No valid file uploaded."


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()  
    app.run(debug=True)
