// Qt includes
#include <QApplication>

// Project includes
#include "opendrive_parser.hpp"
#include "opendrive/opendrive_map.hpp"
#include <QDebug>

int main(int argc, char *argv[]) {
  QApplication a(argc, argv);
  OpenDriveMap map;
  QString pwd = QDir::currentPath();
  QDir currentDir(pwd);
  currentDir.cd("..");

  QString test_map = currentDir.absolutePath() + "/road_net/map.xml";
  qDebug() << test_map;
  OpenDriveParser odp(test_map);
  //odp.show();

  odp.set_map_file(test_map);
  odp.parse_map_file(&map);

  QString dst= currentDir.absolutePath() + "/road_net/pathInfo";
  odp.save_road_points(dst);

  //odp.save_road_points("/home/wendao/projects/data1");
  //  map.print_map();
  //return a.exec();
  return 0;
}


