import ezdxf
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import geojson
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def convert_dxf_to_geojson(dxf_path):
    doc = ezdxf.readfile(dxf_path)
    msp = doc.modelspace()

    features = []

    for entity in msp:
        if entity.dxftype() == 'LINE':
            feature = {
                'type': 'Feature',
                'geometry': {
                    'type': 'LineString',
                    'coordinates': [
                        [entity.dxf.start[0], entity.dxf.start[1]],
                        [entity.dxf.end[0], entity.dxf.end[1]]
                    ]
                },
                'properties': {}
            }
            features.append(feature)

    feature_collection = {
        'type': 'FeatureCollection',
        'features': features
    }

    return geojson.dumps(feature_collection)


def generate_geopdf(geojson_data, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=letter)

    # Draw the GeoJSON geometries
    for feature in geojson.loads(geojson_data)['features']:
        geometry = feature['geometry']
        if geometry['type'] == 'LineString':
            coordinates = geometry['coordinates']
            for i in range(len(coordinates) - 1):
                start = coordinates[i]
                end = coordinates[i + 1]
                c.line(start[0], start[1], end[0], end[1])

    c.save()


def dxf_to_geopdf(dxf_file_path, output_pdf_path):
    geojson_data = convert_dxf_to_geojson(dxf_file_path)
    generate_geopdf(geojson_data, output_pdf_path)


# Provide the path to your DXF file and the output file path for the GeoPDF
dxf_file_path = 'C:/Users/chanw/OneDrive/Exchange with company computer/Land type v3.dxf'
output_pdf_path = 'Geo_pdf_output.pdf'

# Convert DXF to GeoPDF
dxf_to_geopdf(dxf_file_path, output_pdf_path)
