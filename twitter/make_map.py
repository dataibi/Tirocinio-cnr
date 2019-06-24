from argparse import ArgumentParser
import folium


def get_parser():
    parser = ArgumentParser()
    parser.add_argument('--geojson')
    parser.add_argument('--map')
    return parser


def make_map(geojson_file, map_file):
    tweet_map = folium.Map(location=[45,11],
                           zoom_start=5)
    geojson_layer = folium.GeoJson(geojson_file,
                                   name='geojson')
    geojson_layer.add_to(tweet_map)
    tweet_map.save(map_file)


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    make_map(args.geojson, args.map)