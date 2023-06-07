"""
Genres public controllers.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from flask import jsonify

from .model import Genre
from .schema_public import GenreSchema

def get_genres():
    """Performs a basic system health check/smoke test.

    :returns: JSON string; status code
    :rtype: (str, int)
    """
    
    query = Genre.query.all()
    
    # retrieve and return results
    results = list(query)
    if len(results) > 0:

        # prep initial output
        output = {
            'genres': GenreSchema(many=True).dump(results),
            'total': query.count()
        }

        return jsonify(output), 200

    return '', 204

