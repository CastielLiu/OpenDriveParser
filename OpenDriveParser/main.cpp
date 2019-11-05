// Qt includes
#include <QApplication>

// Project includes
#include "opendrive_parser.hpp"
#include "opendrive/opendrive_map.hpp"

int main(int argc, char *argv[]) {
  QApplication a(argc, argv);
  OpenDriveMap map;

  QString test_map = "/home/wendao/Desktop/road_net/map.xml";

  OpenDriveParser odp(test_map);
  //odp.show();

  odp.set_map_file(test_map);
  odp.parse_map_file(&map);
  odp.save_road_points("/home/wendao/Desktop/road_net");
  //  map.print_map();

  //return a.exec();
  return 0;
}


