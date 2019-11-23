from PIL import Image, ExifTags
import gmplot
import os



def get_filenames(dir):
    filenames = []
    for directory in os.listdir(dir):
        for filename in os.listdir(dir + '\\' + directory):
            print('start', filename)
            filenames.append(filename)
    return filenames


def convert_gps_to_degrees(list_of_gps):
    list_of_degrees = []
    for l in list_of_gps:
        latitude = l[0]
        longitude = l[1]
        filename = l[2]
        lat_degree = list(latitude[0])
        lat_degree = lat_degree[0] / lat_degree[1]
        lat_minute = list(latitude[1])
        lat_minute = lat_minute[0] / lat_minute[1]
        lat_minute = lat_minute / 60
        lat_second = list(latitude[2])
        lat_second = lat_second[0] / lat_second[1]
        lat_second = lat_second / 3600

        long_degree = list(longitude[0])
        long_degree = long_degree[0] / long_degree[1]
        long_minute = list(longitude[1])
        long_minute = long_minute[0] / long_minute[1]
        long_minute = long_minute / 60
        long_second = list(longitude[2])
        long_second = long_second[0] / long_second[1]
        long_second = long_second / 3600

        conv_lat = lat_degree + lat_minute + lat_second
        conv_lng = long_degree + long_minute + long_second
        conv_list = [conv_lat, conv_lng, filename]
        list_of_degrees.append(conv_list)
    return list_of_degrees


def get_GPS(dir):
    list_of = []
    for directory in os.listdir(dir):
        sub_dir = dir + '\\' + directory
        for filename in os.listdir(dir + '\\' + directory):
            path = sub_dir + '\\' + filename
            # print(path)
            try:
                img = Image.open(path)
                exif = {ExifTags.TAGS[k]: v for k,
                        v in img._getexif().items() if k in ExifTags.TAGS}
                gpsinfo = {}
                for key in exif['GPSInfo'].keys():
                    decode = ExifTags.GPSTAGS.get(key, key)
                    gpsinfo[decode] = exif['GPSInfo'][key]
                latitude = gpsinfo['GPSLatitude']
                longitude = gpsinfo['GPSLongitude']
                sub_list = [latitude, longitude, filename]
                list_of.append(sub_list)
            except:
                pass

    return list_of


def get_map(list_of_converted_gps, dest_dir):

    gmap = gmplot.GoogleMapPlotter(
        list_of_converted_gps[0][0], list_of_converted_gps[0][1], 10)
    #gmplot doesn't have functioning markers on windows, this is the solution to it'
    gmap.coloricon = gmap.coloricon.replace('/', '\\').replace('\\', '\\\\')

    
    for elems in list_of_converted_gps:
        gmap.marker(elems[0], elems[1],
                    'cornflowerblue', title=elems[2])
    # Pass the absolute path
    gmap.draw(dest_dir + '\\gpsmap.html')
    print('Google map drawn.')
