
trackDetailsValidator = {
    '$jsonSchema': {
        'bsonType': 'object',
        'required': [
            'song_id', 'track_id', 'album_id', 'track_name', 'artist_name', 'track_link',
            'added_on', 'release_date', 'duration_ms', 'explicit',
            'danceability', 'energy', 'genres'
        ],
        'properties': {
            'song_id': {
                'bsonType': 'string'
            },
            'track_id': {
                'bsonType': 'string',
                'description': 'must be a string and is required'
            },
            'album_id': {
                'bsonType': 'string',
                'description': 'must be a string and is required'
            },
            'track_name': {
                'bsonType': 'string',
                'description': 'must be a string and is required'
            },
            'artist_name': {
                'bsonType': 'string',
                'description': 'must be a string and is required'
            },
            'track_link': {
                'bsonType': 'object',
                'required': ['spotify'],
                'properties': {
                    'spotify': {
                        'bsonType': 'string',
                        'description': 'must be a string and is required'
                    }
                }
            },
            'added_on': {
                'bsonType': 'string',
                'description': 'must be a string in a date-time format and is required'
            },
            'release_date': {
                'bsonType': 'string',
                'description': 'must be a string in a date format and is required'
            },
            'duration_ms': {
                'bsonType': 'int',
                'description': 'must be an integer and is required'
            },
            'explicit': {
                'bsonType': 'bool',
                'description': 'must be a boolean and is required'
            },
            'danceability': {
                'bsonType': 'double',
                'description': 'must be a double and is required'
            },
            'energy': {
                'bsonType': 'double',
                'description': 'must be a double and is required'
            },
            'genres': {
                'bsonType': 'array',
                'description': 'must be an array of strings and is required',
                'items': {
                    'bsonType': 'string'
                }
            }
        }
    }
}

updateTracksValidator = {
    '$jsonSchema': {
        'bsonType': 'object',
        'required': [
            'added_on', 'album_id', 'album_cover', 'album_name', 'artist_name',
            'release_date', 'track_id', 'track_name', 'track_link', 'duration_ms',
            'explicit', 'danceability', 'energy', 'genres', 'lyrics'
        ],
        'properties': {
            'added_on': {
                'bsonType': 'string',
                'description': 'must be a string in a date-time format and is required'
            },
            'album_id': {
                'bsonType': 'string',
                'description': 'must be a string and is required'
            },
            'album_cover': {
                'bsonType': 'array',
                'description': 'must be an array of objects and is required',
                'items': {
                    'bsonType': 'object',
                    'required': ['height', 'url', 'width'],
                    'properties': {
                        'height': {
                            'bsonType': 'int',
                            'description': 'must be an integer and is required'
                        },
                        'url': {
                            'bsonType': 'string',
                            'description': 'must be a string and is required'
                        },
                        'width': {
                            'bsonType': 'int',
                            'description': 'must be an integer and is required'
                        }
                    }
                }
            },
            'album_name': {
                'bsonType': 'string',
                'description': 'must be a string and is required'
            },
            'artist_name': {
                'bsonType': 'string',
                'description': 'must be a string and is required'
            },
            'release_date': {
                'bsonType': 'string',
                'description': 'must be a string in a date format and is required'
            },
            'track_id': {
                'bsonType': 'string',
                'description': 'must be a string and is required'
            },
            'track_name': {
                'bsonType': 'string',
                'description': 'must be a string and is required'
            },
            'track_link': {
                'bsonType': 'object',
                'required': ['spotify'],
                'properties': {
                    'spotify': {
                        'bsonType': 'string',
                        'description': 'must be a string and is required'
                    }
                }
            },
            'duration_ms': {
                'bsonType': 'int',
                'description': 'must be an integer and is required'
            },
            'explicit': {
                'bsonType': 'bool',
                'description': 'must be a boolean and is required'
            },
            'danceability': {
                'bsonType': 'double',
                'description': 'must be a double and is required'
            },
            'energy': {
                'bsonType': 'double',
                'description': 'must be a double and is required'
            },
            'genres': {
                'bsonType': 'array',
                'description': 'must be an array of strings and is required',
                'items': {
                    'bsonType': 'string'
                }
            },
            'lyrics': {
                'bsonType': 'string',
                'description': 'must be a string and is required'
            }
        }
    }
}

album_validator = {
    '$jsonSchema': {
        'bsonType': 'object',
        'required': ['album_id', 'album_cover', 'album_name'],
        'properties': {
            'album_id': {
                'bsonType': 'string'
            },
            'album_cover': {
                'bsonType': 'array',
                'items': {
                    'bsonType': 'object',
                    'required': ['height', 'url', 'width'],
                    'properties': {
                        'height': {'bsonType': 'int'},
                        'url': {'bsonType': 'string'},
                        'width': {'bsonType': 'int'}
                    }
                }
            },
            'album_name': {
                'bsonType': 'string'
            }
        }
    }
}

TrackLyricsValidator = {
    '$jsonSchema': {
        'bsonType': 'object',
        'required': ['track_id', 'lyrics'],
        'properties': {
            'track_id': {
                'bsonType': 'string',
                'description': 'must be a string and is required'
            },
            'lyrics': {
                'bsonType': 'string',
                'description': 'must be a string and is required'
            }
        }
    }
}

tokenIndex = {
    '$jsonSchema': {
        'bsonType': 'object',
        'required': ['token', 'doc_pos'],
        'properties': {
            'token': {
                'bsonType': 'string',
                'description': 'must be a string and is required'
            },
            'doc_pos': {
                'bsonType': 'string',
                'description': 'must be a string and is required'
            }
        }
    }
}


lyric_indexer_validator = {
    '$jsonSchema': {
        'bsonType': 'object',
        'required': ['token', 'songs'],
        'properties': {
            'lyric': {
                'bsonType': 'string',
                'description': 'must be a string and is required'
            },
            'tracks': {
                'bsonType': 'string',
                'description': 'must be an array of objects with trackId and positions and is required',
                'items': {
                    'bsonType': 'object',
                    'required': ['songId', 'positions'],
                    'properties': {
                        'songId': {
                            'bsonType': 'string',
                            'description': 'must be a string and is required'
                        },
                        'positions': {
                            'bsonType': 'array',
                            'description': 'must be an array of integers and is required',
                            'items': {
                                'bsonType': 'int'
                            }
                        }
                    }
                }
            }
        }
    }
}



token_doc_stats = {
  "$jsonSchema": {
    "bsonType": "object",
    "required": ["token", "doc_frequency", "total_frequency", "documents"],
    "properties": {
      "token": {
        "bsonType": "string",
        "description": "must be a string and is required"
      },
      "doc_frequency": {
        "bsonType": "int",
        "minimum": 0,
        "description": "must be an integer greater than or equal to 0 and is required"
      },
      "total_frequency": {
        "bsonType": "int",
        "minimum": 0,
        "description": "must be an integer greater than or equal to 0 and is required"
      },
      "documents": {
        "bsonType": "array",
        "description": "must be an array of document details and is required",
        "items": {
          "bsonType": "object",
          "required": ["doc_id", "positions", "frequency"],
          "properties": {
            "doc_id": {
              "bsonType": "string",
              "description": "must be a string and is required"
            },
            "positions": {
              "bsonType": "array",
              "description": "must be an array of integers and is required",
              "items": {
                "bsonType": "int",
                "minimum": 0,
                "description": "must be an integer greater than or equal to 0"
              }
            },
            "frequency": {
              "bsonType": "int",
              "minimum": 1,
              "description": "must be an integer greater than or equal to 1 and is required"
            }
          }
        }
      }
    }
  }
}



